import concurrent.futures
import logging
import multiprocessing as mp
import queue
import threading
import time
from collections.abc import Callable

from src.server.backends import create_backend
from src.server.models import (
    InferenceResult,
    ModelConfig,
    PoolConfig,
    TokenizedBatch,
    WorkItem,
    WorkResult,
)
from src.server.models.metrics.worker import WorkerMetrics
from src.server.services.base import BaseWorker, get_worker_gpu_memory, setup_worker_environment
from src.server.services.service_base import PoolBasedService

logger = logging.getLogger(__name__)

_STOP = "__STOP__"
_GET_MEMORY = "__GET_MEMORY__"
_GET_METRICS = "__GET_METRICS__"


class ModelWorker(BaseWorker[WorkItem, WorkResult]):
    def __init__(self, worker_id: int, config: ModelConfig, metrics=None):
        if metrics is None:
            metrics = WorkerMetrics(worker_id=worker_id)
        super().__init__(worker_id, metrics=metrics)
        self.config = config
        self._backend = None

    def initialize(self) -> None:
        setup_worker_environment()
        self._backend = create_backend(self.config)
        self._backend.load_model()
        self._backend.warmup(3)

        try:
            initial_mem = get_worker_gpu_memory()
            logger.info(f"Worker {self.worker_id} ready - GPU memory: {initial_mem:.2f} MB")
        except Exception:
            pass

        self.set_ready()

    def process(self, work_item: WorkItem) -> WorkResult:
        if not self._backend:
            raise RuntimeError(f"Model worker {self.worker_id} not initialized")

        time.perf_counter()
        result = self._backend.infer_with_tokenized(work_item.tokenized_batch)
        latency_ms = result.t_model_inference_ms

        self._record_metrics(
            latency_ms=latency_ms,
            num_queries=result.batch_size,
        )

        return WorkResult(
            req_id=work_item.req_id,
            scores=result.scores,
            worker_id=self.worker_id,
            t_tokenize_ms=0.0,
            t_model_inference_ms=result.t_model_inference_ms,
            t_queue_wait_ms=0.0,
            total_ms=result.t_model_inference_ms,
            total_tokens=result.total_tokens,
            real_tokens=result.real_tokens,
            padded_tokens=result.padded_tokens,
            padding_ratio=result.padding_ratio,
            max_seq_length=result.max_seq_length,
            avg_seq_length=result.avg_seq_length,
            batch_size=result.batch_size,
        )

    def get_memory_mb(self) -> float:
        return get_worker_gpu_memory()


def _worker_main(
    worker_id: int,
    config_dict: dict,
    input_queue: mp.Queue,
    output_queue: mp.Queue,
    ready_event: mp.Event,
    memory_queue: mp.Queue,
    metrics_queue: mp.Queue | None = None,
):
    cfg = ModelConfig(**config_dict)
    worker = ModelWorker(worker_id, cfg)
    worker.initialize()
    ready_event.set()

    while True:
        try:
            item = input_queue.get()
            if item == _STOP:
                break
            if item == _GET_MEMORY:
                memory_mb = worker.get_memory_mb()
                try:
                    memory_queue.put((worker_id, memory_mb), block=False)
                except Exception:
                    pass
                continue
            if item == _GET_METRICS:
                if metrics_queue is not None:
                    try:
                        metrics_stats = worker.get_metrics_stats()
                        metrics_queue.put((worker_id, metrics_stats), block=False)
                    except Exception:
                        pass
                continue

            result = worker.process(item)
            output_queue.put(result)

            if metrics_queue is not None:
                try:
                    metrics_stats = worker.get_metrics_stats()
                    metrics_queue.put((worker_id, metrics_stats), block=False)
                except Exception:
                    pass
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
        self._metrics_queue = mp.Queue()
        self._ready_events: list[mp.Event] = []
        self._is_started = False
        self._next_req_id = 0
        self._pending: dict[int, concurrent.futures.Future] = {}
        self._result_thread: threading.Thread | None = None
        self._metrics_thread: threading.Thread | None = None
        self._request_counts: dict[int, int] = {}
        self._pending_tokenize_metrics: dict[int, dict] = {}
        self._worker_metrics: dict[int, dict] = {}
        self._metrics_lock = threading.Lock()

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
                    self._metrics_queue,
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
        self._metrics_thread = threading.Thread(target=self._metrics_loop, daemon=True)
        self._metrics_thread.start()
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

    def _metrics_loop(self) -> None:
        while True:
            try:
                try:
                    worker_id, metrics_stats = self._metrics_queue.get(timeout=1.0)
                    with self._metrics_lock:
                        self._worker_metrics[worker_id] = metrics_stats
                except (queue.Empty, OSError):
                    continue
            except Exception as e:
                logger.error(f"Metrics loop error: {e}")
                time.sleep(0.1)

    def infer_with_tokenized(self, tokenized_batch) -> InferenceResult:
        if not self._is_started:
            raise RuntimeError("Pool not started")

        req_id = self._next_req_id
        self._next_req_id += 1

        future = concurrent.futures.Future()
        self._pending[req_id] = future

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

        mp_send_start = time.perf_counter()
        self._input_queue.put(WorkItem(req_id=req_id, tokenized_batch=tokenized_batch))
        t_mp_queue_send_ms = (time.perf_counter() - mp_send_start) * 1000

        mp_receive_start = time.perf_counter()
        try:
            result = future.result()
            t_mp_queue_receive_total_ms = (time.perf_counter() - mp_receive_start) * 1000

            t_mp_queue_receive_ms = max(
                0.0, t_mp_queue_receive_total_ms - result.t_model_inference_ms
            )

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
                t_mp_queue_receive_ms = max(
                    0.0, t_mp_queue_receive_total_ms - result.t_model_inference_ms
                )
                return InferenceResult(
                    scores=result.scores,
                    t_tokenize_ms=0.0,
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
        if not self._is_started:
            return 0.0

        for _ in range(self.num_workers):
            try:
                self._input_queue.put(_GET_MEMORY, block=True, timeout=1.0)
            except Exception as e:
                logger.debug(f"Error sending memory query to worker: {e}")
                continue

        memory_values = []
        deadline = time.time() + 2.0

        while len(memory_values) < self.num_workers and time.time() < deadline:
            try:
                worker_id, memory_mb = self._memory_queue.get(timeout=0.2)
                memory_values.append(memory_mb)
                logger.debug(f"Worker {worker_id} reported GPU memory: {memory_mb:.2f} MB")
            except Exception:
                continue

        if memory_values:
            max_memory = max(memory_values)
            logger.debug(
                f"GPU memory from {len(memory_values)}/{self.num_workers} workers: {max_memory:.2f} MB"
            )
            return max_memory

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

    def get_worker_metrics(self) -> list[dict]:
        if not self._is_started:
            return []

        for _ in range(self.num_workers):
            try:
                self._input_queue.put(_GET_METRICS, block=False)
            except Exception:
                pass

        time.sleep(0.1)

        with self._metrics_lock:
            return [self._worker_metrics.get(i, {}) for i in range(self.num_workers)]

    def get_worker_metrics_by_id(self, worker_id: int) -> dict:
        if not self._is_started or worker_id >= self.num_workers:
            return {}

        try:
            self._input_queue.put(_GET_METRICS, block=False)
        except Exception:
            pass

        time.sleep(0.1)

        with self._metrics_lock:
            return self._worker_metrics.get(worker_id, {})

    def reset_worker_metrics(self) -> None:
        with self._metrics_lock:
            self._worker_metrics.clear()

    @property
    def is_loaded(self) -> bool:
        return self._is_started

    def __len__(self) -> int:
        return self.num_workers


class InferenceService(PoolBasedService):
    def __init__(self, model_pool: ModelPool):
        super().__init__(model_pool)
        self._model_pool = model_pool

    def infer_async(
        self,
        tokenized_batch: TokenizedBatch,
        callback: Callable[[InferenceResult | None, Exception | None], None],
    ) -> None:
        if not self.is_started:
            callback(None, RuntimeError("Inference service not started"))
            return

        def _infer():
            try:
                result = self._model_pool.infer_with_tokenized(tokenized_batch)
                callback(result, None)
            except Exception as e:
                logger.error(f"Inference error: {e}")
                callback(None, e)

        thread = threading.Thread(target=_infer, daemon=True)
        thread.start()

    def infer_sync(self, tokenized_batch: TokenizedBatch) -> InferenceResult:
        if not self.is_started:
            raise RuntimeError("Inference service not started")
        return self._model_pool.infer_with_tokenized(tokenized_batch)

    def get_gpu_memory_mb(self) -> float:
        if not self.is_started:
            return 0.0
        return self._model_pool.get_gpu_memory_mb()

    def get_worker_metrics(self) -> list[dict]:
        if not self.is_started:
            return []
        return self._model_pool.get_worker_metrics()

    def reset_worker_metrics(self) -> None:
        if self.is_started:
            self._model_pool.reset_worker_metrics()


__all__ = [
    "InferenceService",
    "ModelPool",
    "ModelWorker",
]
