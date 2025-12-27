"""Process-based model pool for parallel inference."""

import concurrent.futures
import logging
import multiprocessing as mp
import os
import threading
import time

from src.models import InferenceResult, PoolConfig, WorkItem, WorkResult

logger = logging.getLogger(__name__)

_STOP = "__STOP__"
_GET_MEMORY = "__GET_MEMORY__"


def _get_worker_gpu_memory() -> float:
    """Get GPU memory usage from worker process.

    Uses driver_allocated_memory() which aggregates memory across all processes
    using the Metal GPU. This should capture memory from all worker processes.
    """
    try:
        import torch

        if torch.backends.mps.is_available():
            # driver_allocated_memory() aggregates memory from ALL processes using Metal GPU
            # This includes all worker processes, so each worker will report the total
            driver_mem = torch.mps.driver_allocated_memory() / (1024 * 1024)
            if driver_mem > 0:
                return driver_mem

            # Fallback: current_allocated_memory (process-local only)
            # This only captures memory for this specific worker process
            current_mem = torch.mps.current_allocated_memory() / (1024 * 1024)
            if current_mem > 0:
                return current_mem
    except Exception as e:
        logger.error(f"Error getting GPU memory in worker: {e}")
    return 0.0


def _worker_main(
    worker_id: int,
    config_dict: dict,
    input_queue: mp.Queue,
    output_queue: mp.Queue,
    ready_event: mp.Event,
    memory_queue: mp.Queue,
):
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    # Import TokenizedBatch for deserialization of WorkItem with tokenized_batch
    from src.models import ModelConfig
    from src.server.backends import create_backend
    from src.server.services.tokenizer import TokenizedBatch  # noqa: F401

    cfg = ModelConfig(**config_dict)
    backend = create_backend(cfg)
    backend.load_model()
    backend.warmup(3)

    # Log initial GPU memory after model load
    try:
        initial_mem = _get_worker_gpu_memory()
        logger.info(f"Worker {worker_id} ready - GPU memory: {initial_mem:.2f} MB")
    except Exception:
        pass

    ready_event.set()

    while True:
        try:
            item = input_queue.get()
            if item == _STOP:
                break
            if item == _GET_MEMORY:
                # Respond immediately with GPU memory
                memory_mb = _get_worker_gpu_memory()
                try:
                    memory_queue.put((worker_id, memory_mb), block=False)
                except Exception:
                    # Queue full, skip
                    pass
                continue

            # Regular inference work - use pre-tokenized batch
            result = backend.infer_with_tokenized(item.tokenized_batch)
            output_queue.put(
                WorkResult(
                    req_id=item.req_id,
                    scores=result.scores,
                    worker_id=worker_id,
                    t_tokenize_ms=0.0,  # Tokenization already done
                    t_model_inference_ms=result.t_model_inference_ms,
                    t_queue_wait_ms=0.0,  # Worker doesn't know queue wait, set by scheduler
                    total_ms=result.t_model_inference_ms,
                    total_tokens=result.total_tokens,
                    real_tokens=result.real_tokens,
                    padded_tokens=result.padded_tokens,
                    padding_ratio=result.padding_ratio,
                    max_seq_length=result.max_seq_length,
                    avg_seq_length=result.avg_seq_length,
                    batch_size=result.batch_size,
                )
            )
        except Exception as e:
            logger.error(f"Worker {worker_id} error: {e}")


class ModelPool:
    def __init__(self, config: PoolConfig):
        self.config = config
        self.num_workers = len(config.instances)
        self._processes: list[mp.Process] = []
        self._input_queue = mp.Queue()
        self._output_queue = mp.Queue()
        self._memory_queue = mp.Queue()
        self._ready_events: list[mp.Event] = []
        self._is_started = False
        self._next_req_id = 0
        self._pending: dict[int, concurrent.futures.Future] = {}
        self._result_thread: threading.Thread | None = None
        self._request_counts: dict[int, int] = {}
        self._pending_tokenize_metrics: dict[int, dict] = {}  # Tokenization metrics per request ID

    def start(self, timeout_s: float = 120.0) -> None:
        if self._is_started:
            return

        for i, inst in enumerate(self.config.instances):
            ready = mp.Event()
            self._ready_events.append(ready)

            p = mp.Process(
                target=_worker_main,
                args=(
                    i,
                    inst.model_dump(),
                    self._input_queue,
                    self._output_queue,
                    ready,
                    self._memory_queue,
                ),
                daemon=True,
            )
            p.start()
            self._processes.append(p)

        for i, ev in enumerate(self._ready_events):
            if not ev.wait(timeout_s):
                raise RuntimeError(f"Worker {i} failed to start")

        self._result_thread = threading.Thread(target=self._result_loop, daemon=True)
        self._result_thread.start()
        self._is_started = True
        logger.info(f"Pool ready with {self.num_workers} workers")

    def stop(self, timeout_s: float = 30.0) -> None:
        if not self._is_started:
            return

        for _ in range(self.num_workers):
            self._input_queue.put(_STOP)

        deadline = time.time() + timeout_s
        for p in self._processes:
            remaining = max(0, deadline - time.time())
            p.join(timeout=remaining)
            if p.is_alive():
                p.terminate()

        self._processes.clear()
        self._is_started = False
        logger.info("Pool stopped")

    def _result_loop(self) -> None:
        while True:
            try:
                result = self._output_queue.get()
                if not isinstance(result, WorkResult):
                    continue

                self._request_counts[result.worker_id] = (
                    self._request_counts.get(result.worker_id, 0) + 1
                )

                future = self._pending.pop(result.req_id, None)
                if future and not future.cancelled():
                    future.set_result(result)
            except Exception as e:
                logger.error(f"Result loop error: {e}")
                time.sleep(0.1)

    def infer_with_tokenized(self, tokenized_batch) -> InferenceResult:
        """Run inference with pre-tokenized batch (no tokenization in workers).

        Args:
            tokenized_batch: TokenizedBatch with features already tokenized

        Returns:
            InferenceResult with scores and timing
        """
        if not self._is_started:
            raise RuntimeError("Pool not started")

        req_id = self._next_req_id
        self._next_req_id += 1

        future = concurrent.futures.Future()
        self._pending[req_id] = future

        # Store tokenization metrics from the tokenized batch
        overhead_ms = getattr(tokenized_batch, "overhead_ms", 0.0)
        worker_id = getattr(tokenized_batch, "worker_id", -1)
        self._pending_tokenize_metrics[req_id] = {
            "t_tokenize_ms": tokenized_batch.tokenize_time_ms,
            "overhead_ms": overhead_ms,
            "total_tokens": tokenized_batch.total_tokens,
            "real_tokens": tokenized_batch.real_tokens,
            "padded_tokens": tokenized_batch.padded_tokens,
            "padding_ratio": tokenized_batch.padding_ratio,
            "max_seq_length": tokenized_batch.max_seq_length,
            "avg_seq_length": tokenized_batch.avg_seq_length,
            "worker_id": worker_id,
        }

        # Track multiprocessing queue send time
        mp_send_start = time.perf_counter()
        self._input_queue.put(WorkItem(req_id=req_id, tokenized_batch=tokenized_batch))
        t_mp_queue_send_ms = (time.perf_counter() - mp_send_start) * 1000

        # Track multiprocessing queue receive/wait time
        mp_receive_start = time.perf_counter()
        try:
            result = future.result()
            t_mp_queue_receive_total_ms = (time.perf_counter() - mp_receive_start) * 1000

            # MP queue receive time includes model inference time, so we calculate overhead only
            t_mp_queue_receive_ms = max(
                0.0, t_mp_queue_receive_total_ms - result.t_model_inference_ms
            )

            # Use tokenization metrics from tokenized batch
            tokenize_metrics = self._pending_tokenize_metrics.pop(req_id, None)
            if tokenize_metrics:
                overhead_ms = tokenize_metrics.get("overhead_ms", 0.0)
                tokenizer_worker_id = tokenize_metrics.get("worker_id", -1)
                result_obj = InferenceResult(
                    scores=result.scores,
                    t_tokenize_ms=tokenize_metrics["t_tokenize_ms"],
                    t_model_inference_ms=result.t_model_inference_ms,
                    t_queue_wait_ms=result.t_queue_wait_ms,
                    t_overhead_ms=overhead_ms,
                    t_mp_queue_send_ms=t_mp_queue_send_ms,
                    t_mp_queue_receive_ms=t_mp_queue_receive_ms,
                    total_ms=tokenize_metrics["t_tokenize_ms"]
                    + result.t_model_inference_ms
                    + overhead_ms
                    + t_mp_queue_send_ms
                    + t_mp_queue_receive_ms,
                    total_tokens=tokenize_metrics["total_tokens"],
                    real_tokens=tokenize_metrics["real_tokens"],
                    padded_tokens=tokenize_metrics["padded_tokens"],
                    padding_ratio=tokenize_metrics["padding_ratio"],
                    max_seq_length=tokenize_metrics["max_seq_length"],
                    avg_seq_length=tokenize_metrics["avg_seq_length"],
                    batch_size=result.batch_size,
                    worker_id=result.worker_id,
                )
                result_obj.tokenizer_worker_id = tokenizer_worker_id
                return result_obj
            else:
                # Fallback (should not happen)
                t_mp_queue_receive_ms = max(
                    0.0, t_mp_queue_receive_total_ms - result.t_model_inference_ms
                )
                return InferenceResult(
                    scores=result.scores,
                    t_tokenize_ms=0.0,  # Tokenization already done
                    t_model_inference_ms=result.t_model_inference_ms,
                    t_queue_wait_ms=result.t_queue_wait_ms,
                    t_mp_queue_send_ms=t_mp_queue_send_ms,
                    t_mp_queue_receive_ms=t_mp_queue_receive_ms,
                    total_ms=result.t_model_inference_ms
                    + t_mp_queue_send_ms
                    + t_mp_queue_receive_ms,
                    total_tokens=result.total_tokens,
                    real_tokens=result.real_tokens,
                    padded_tokens=result.padded_tokens,
                    padding_ratio=result.padding_ratio,
                    max_seq_length=result.max_seq_length,
                    avg_seq_length=result.avg_seq_length,
                    batch_size=result.batch_size,
                    worker_id=result.worker_id,
                )
        except Exception:
            self._pending.pop(req_id, None)
            self._pending_tokenize_metrics.pop(req_id, None)
            raise

    def get_gpu_memory_mb(self) -> float:
        """Get total GPU memory usage from all worker processes.

        Queries workers directly since they have models loaded and GPU memory allocated.
        Workers use driver_allocated_memory() which aggregates across all processes.
        """
        if not self._is_started:
            return 0.0

        # Query workers directly - they have the models loaded
        # Request memory info from all workers
        for _ in range(self.num_workers):
            try:
                self._input_queue.put(_GET_MEMORY, block=True, timeout=1.0)
            except Exception as e:
                logger.debug(f"Error sending memory query to worker: {e}")
                continue

        # Collect responses (with timeout)
        memory_values = []
        deadline = time.time() + 2.0  # 2 second timeout

        while len(memory_values) < self.num_workers and time.time() < deadline:
            try:
                worker_id, memory_mb = self._memory_queue.get(timeout=0.2)
                memory_values.append(memory_mb)
                logger.debug(f"Worker {worker_id} reported GPU memory: {memory_mb:.2f} MB")
            except Exception:
                # Timeout or queue empty - continue waiting
                continue

        if memory_values:
            # driver_allocated_memory() aggregates across all processes,
            # so we should get the same value from each worker
            # Use the maximum to be safe (in case some workers report differently)
            max_memory = max(memory_values)
            logger.debug(
                f"GPU memory from {len(memory_values)}/{self.num_workers} workers: {max_memory:.2f} MB"
            )
            return max_memory

        # Fallback: try driver_allocated_memory from main process
        # (might work if main process has initialized MPS)
        try:
            import torch

            if torch.backends.mps.is_available():
                driver_mem = torch.mps.driver_allocated_memory() / (1024 * 1024)
                if driver_mem > 0:
                    logger.debug(f"Fallback: GPU memory from main process: {driver_mem:.2f} MB")
                    return driver_mem
        except Exception as e:
            logger.debug(f"Error getting GPU memory from main process: {e}")

        logger.warning("Could not get GPU memory from any worker or main process")
        return 0.0

    def get_info(self) -> dict:
        return {
            "num_instances": self.num_workers,
            "is_loaded": self._is_started,
            "request_counts": dict(self._request_counts),
        }

    @property
    def is_loaded(self) -> bool:
        return self._is_started

    def __len__(self) -> int:
        return self.num_workers
