import logging
import multiprocessing as mp
import queue
import threading
import time
from itertools import count

from src.server.dto import ModelConfig, PoolConfig
from src.server.pool.base import BaseWorkerPool
from src.server.worker.model_worker import ModelWorker

logger = logging.getLogger(__name__)

_STOP = "__STOP__"
_GET_MEMORY = "__GET_MEMORY__"
_GET_METRICS = "__GET_METRICS__"


class _InferenceWorkItem:
    def __init__(self, tokenized_batch, request_id):
        self.tokenized_batch = tokenized_batch
        self.req_id = request_id


def _worker_main(
    worker_id: int,
    config_dict: dict,
    input_queue,
    output_queue,
    ready_event,
    memory_queue,
    metrics_queue=None,
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

            if hasattr(item, "tokenized_batch") and hasattr(item, "req_id"):
                from src.server.dto import WorkItem

                work_item = WorkItem(req_id=item.req_id, tokenized_batch=item.tokenized_batch)
                try:
                    result = worker.process(work_item)
                    output_queue.put((item.req_id, result, None))
                except Exception as e:
                    logger.error(f"Worker {worker_id} inference error: {e}")
                    output_queue.put((item.req_id, None, e))
            else:
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


class ModelPool(BaseWorkerPool):
    def __init__(self, config: PoolConfig):
        super().__init__(len(config.instances))
        self.config = config
        self._processes: list[mp.Process] = []
        self._input_queues: list[mp.Queue] = []
        self._output_queue = mp.Queue()
        self._memory_queue = mp.Queue()
        self._metrics_queue = mp.Queue()
        self._ready_events: list[mp.Event] = []
        self._result_thread: threading.Thread | None = None

        self._request_counts: dict[int, int] = {}
        # _worker_metrics and locks are in BaseWorkerPool

        # self._shutdown_event is in BaseWorkerPool
        self._inference_queue: queue.Queue | None = None
        self._pipeline_consumer_thread: threading.Thread | None = None
        self._round_robin_counter = count()  # Lock-free atomic counter
        self._total_inference_batches = 0
        self._total_inference_queries = 0
        self._pipeline_start_time: float | None = None
        self._stats_lock = threading.Lock()

    def start(self, timeout_s: float = 120.0) -> None:
        if self._is_started:
            return

        self._shutdown_event.clear()

        for i, inst in enumerate(self.config.instances):
            ready = mp.Event()
            self._ready_events.append(ready)
            input_queue = mp.Queue()
            self._input_queues.append(input_queue)

            p = mp.Process(
                target=_worker_main,
                args=(
                    i,
                    inst.model_dump(),
                    input_queue,
                    self._output_queue,
                    ready,
                    self._memory_queue,
                    self._metrics_queue,
                ),
                daemon=True,
            )
            p.start()
            self._processes.append(p)

        per_worker_timeout = 60.0
        for i, ev in enumerate(self._ready_events):
            logger.info(f"Waiting for worker {i} to initialize (timeout: {per_worker_timeout}s)...")
            if not ev.wait(per_worker_timeout):
                logger.warning(f"Worker {i} failed to start within {per_worker_timeout}s timeout")
                raise RuntimeError(f"Worker {i} failed to start within {per_worker_timeout}s")

        self._result_thread = threading.Thread(target=self._result_loop, daemon=True)
        self._result_thread.start()

        self.start_metrics_thread()

        self._is_started = True
        logger.info(f"Pool ready with {self.num_workers} workers")

    def submit(self, work_item) -> None:
        if not self._is_started:
            raise RuntimeError("Model pool not started")

        # Lock-free round-robin using atomic counter
        worker_idx = next(self._round_robin_counter) % self.num_workers

        try:
            self._input_queues[worker_idx].put_nowait(work_item)
        except queue.Full:
            raise RuntimeError("Model pool queue full") from None

    def set_inference_queue(self, inference_queue: queue.Queue) -> None:
        if not self._is_started:
            raise RuntimeError("Pool must be started before setting inference queue")

        super().set_inference_queue(inference_queue)
        self._pipeline_start_time = time.time()
        self._total_inference_batches = 0
        self._total_inference_queries = 0
        self._pipeline_consumer_thread = threading.Thread(
            target=self._pipeline_consumer_loop, daemon=True
        )
        self._pipeline_consumer_thread.start()

        logger.info("Model pool inference queue set, pipeline mode active")

    def stop(self, timeout_s: float = 30.0) -> None:
        if not self._is_started:
            return

        self._shutdown_event.set()

        for input_queue in self._input_queues:
            try:
                input_queue.put(_STOP, block=False)
            except Exception as e:
                logger.debug(f"Error sending STOP to worker: {e}")

        deadline = time.time() + timeout_s

        for p in self._processes:
            remaining = max(0, deadline - time.time())
            p.join(timeout=remaining)
            if p.is_alive():
                logger.warning("Worker process did not exit; terminating")
                p.terminate()
                p.join(timeout=1.0)

        if self._result_thread:
            remaining = max(0, deadline - time.time())
            self._result_thread.join(timeout=remaining)
            if self._result_thread.is_alive():
                logger.warning("Result thread did not exit cleanly")

        self.stop_metrics_thread(max(0, deadline - time.time()))

        if self._pipeline_consumer_thread:
            remaining = max(0, deadline - time.time())
            self._pipeline_consumer_thread.join(timeout=remaining)
            if self._pipeline_consumer_thread.is_alive():
                logger.warning("Pipeline consumer thread did not exit cleanly")

        if self._pipeline_start_time:
            elapsed = time.time() - self._pipeline_start_time
            with self._stats_lock:
                batches = self._total_inference_batches
                queries = self._total_inference_queries
            if elapsed > 0 and batches > 0:
                throughput = queries / elapsed
                logger.info(
                    f"Model Pool Statistics: {batches} batches, {queries} queries "
                    f"sent to workers in {elapsed:.1f}s ({throughput:.1f} q/s)"
                )

        for input_queue in self._input_queues:
            try:
                input_queue.close()
                input_queue.join_thread()
            except Exception as e:
                logger.debug(f"Error closing input queue: {e}")

        try:
            self._output_queue.close()
            self._output_queue.join_thread()
        except Exception as e:
            logger.debug(f"Error closing output queue: {e}")

        try:
            self._memory_queue.close()
            self._memory_queue.join_thread()
        except Exception as e:
            logger.debug(f"Error closing memory queue: {e}")

        try:
            self._metrics_queue.close()
            self._metrics_queue.join_thread()
        except Exception as e:
            logger.debug(f"Error closing metrics queue: {e}")

        self._processes.clear()
        self._input_queues.clear()
        self._is_started = False
        logger.info("Pool stopped")

    def _result_loop(self) -> None:
        while not self._shutdown_event.is_set():
            try:
                if self._inference_queue is not None:
                    time.sleep(0.5)
                    continue

                result = self._output_queue.get(timeout=0.5)
                if result is not None:
                    logger.debug("Drained stale result from output queue")
            except (queue.Empty, EOFError):
                continue
            except Exception as e:
                logger.error(f"Result loop error: {e}", exc_info=True)
                continue

    def _pipeline_consumer_loop(self) -> None:
        if not self._inference_queue:
            logger.error("Pipeline consumer loop started without inference queue")
            return

        pending_results = {}

        while not self._shutdown_event.is_set():
            try:
                try:
                    worker_result = self._output_queue.get_nowait()
                    if isinstance(worker_result, tuple) and len(worker_result) == 3:
                        request_id, result, error = worker_result
                        if request_id in pending_results:
                            request, enqueue_time = pending_results.pop(request_id)
                            if error:
                                request.error = error
                            else:
                                from src.server.dto import InferenceResult

                                if result:
                                    t_tokenize_ms = 0.0
                                    if request.tokenized_batch:
                                        t_tokenize_ms = request.tokenized_batch.tokenize_time_ms

                                    request.inference_result = InferenceResult(
                                        scores=result.scores,
                                        t_tokenize_ms=t_tokenize_ms,
                                        t_model_inference_ms=result.t_model_inference_ms,
                                        t_queue_wait_ms=result.t_queue_wait_ms
                                        + getattr(request, "t_queue_tokenization_wait_ms", 0.0)
                                        + getattr(request, "t_queue_inference_wait_ms", 0.0),
                                        t_tokenizer_queue_wait_ms=getattr(
                                            request, "t_queue_tokenization_wait_ms", 0.0
                                        ),
                                        t_model_queue_wait_ms=getattr(
                                            request, "t_queue_inference_wait_ms", 0.0
                                        ),
                                        t_overhead_ms=getattr(result, "t_overhead_ms", 0.0),
                                        t_mp_queue_send_ms=getattr(
                                            result, "t_mp_queue_send_ms", 0.0
                                        ),
                                        t_mp_queue_receive_ms=getattr(
                                            result, "t_mp_queue_receive_ms", 0.0
                                        ),
                                        total_ms=result.total_ms,
                                        total_tokens=result.total_tokens,
                                        real_tokens=result.real_tokens,
                                        padded_tokens=result.padded_tokens,
                                        padding_ratio=result.padding_ratio,
                                        max_seq_length=result.max_seq_length,
                                        avg_seq_length=result.avg_seq_length,
                                        batch_size=result.batch_size,
                                        worker_id=result.worker_id,
                                        tokenizer_worker_id=request.tokenizer_worker_id,
                                    )
                            request.result_event.set()
                except queue.Empty:
                    pass

                try:
                    inference_item = self._inference_queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                from src.server.dto.pipeline import InferenceQueueItem

                if not isinstance(inference_item, InferenceQueueItem):
                    continue

                request = inference_item.request
                tokenized_batch = inference_item.tokenized_batch
                enqueue_time = inference_item.enqueue_time

                queue_wait_ms = (time.perf_counter() - enqueue_time) * 1000
                request.t_queue_inference_wait_ms = queue_wait_ms

                try:
                    # Lock-free round-robin using atomic counter
                    worker_idx = next(self._round_robin_counter) % self.num_workers
                    selected_queue = self._input_queues[worker_idx]
                    work_item = _InferenceWorkItem(tokenized_batch, request.request_id)
                    selected_queue.put_nowait(work_item)
                    pending_results[request.request_id] = (request, enqueue_time)

                    with self._stats_lock:
                        self._total_inference_batches += 1
                        self._total_inference_queries += tokenized_batch.batch_size

                except queue.Full:
                    logger.error("Worker queue full, dropping inference request")
                    request.error = RuntimeError("Inference queue full")
                    request.result_event.set()
                except Exception as e:
                    logger.error(f"Pipeline routing error: {e}", exc_info=True)
                    request.error = e
                    request.result_event.set()

            except Exception as e:
                logger.error(f"Pipeline consumer loop error: {e}", exc_info=True)
                continue

    def get_gpu_memory_mb(self) -> float:
        if not self._is_started:
            return 0.0

        for input_queue in self._input_queues:
            try:
                input_queue.put(_GET_MEMORY, block=False)
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
        queue_size = 0
        worker_queue_size = 0
        if self._is_started:
            try:
                if self._inference_queue:
                    queue_size = self._inference_queue.qsize()

                # Also count items waiting in worker queues
                for q in self._input_queues:
                    worker_queue_size += q.qsize()
            except Exception as e:
                logger.debug(f"Error getting model queue size: {e}")

        return {
            "num_instances": self.num_workers,
            "is_loaded": self._is_started,
            "request_counts": dict(self._request_counts),
            "queue_size": queue_size + worker_queue_size,
            "inference_queue_size": queue_size,
            "worker_queue_size": worker_queue_size,
        }

    def get_worker_metrics(self) -> list[dict]:
        if not self._is_started:
            return []

        for input_queue in self._input_queues:
            try:
                input_queue.put(_GET_METRICS, block=False)
            except Exception:
                pass

        time.sleep(0.1)

        # Use base class method to return cached metrics
        return super().get_worker_metrics()

    def get_worker_metrics_by_id(self, worker_id: int) -> dict:
        if not self._is_started or worker_id >= self.num_workers:
            return {}

        try:
            self._input_queues[worker_id].put(_GET_METRICS, block=False)
        except Exception:
            pass

        time.sleep(0.1)

        return super().get_worker_metrics_by_id(worker_id)
