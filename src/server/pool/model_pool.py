"""Model pool for managing model inference workers in pipeline mode."""

import logging
import multiprocessing as mp
import queue
import threading
import time

from src.server.dto import ModelConfig, PoolConfig
from src.server.worker.model_worker import ModelWorker

logger = logging.getLogger(__name__)

_STOP = "__STOP__"
_GET_MEMORY = "__GET_MEMORY__"
_GET_METRICS = "__GET_METRICS__"


class _InferenceWorkItem:
    """Work item for pipeline mode inference routing."""
    def __init__(self, tokenized_batch, request_id):
        self.tokenized_batch = tokenized_batch
        self.request_id = request_id


def _worker_main(
    worker_id: int,
    config_dict: dict,
    input_queue,  # mp.Queue[WorkItem] - per-worker queue
    output_queue,  # mp.Queue[WorkResult]
    ready_event,  # mp.Event
    memory_queue,  # mp.Queue
    metrics_queue=None,  # Optional mp.Queue
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

            # Check if this is a pipeline inference work item
            if hasattr(item, 'tokenized_batch') and hasattr(item, 'request_id'):
                # Pipeline mode: process tokenized batch and put result in output queue
                try:
                    result = worker.process(item.tokenized_batch)
                    # Put result with request_id so main process can route it back
                    output_queue.put((item.request_id, result, None))
                except Exception as e:
                    logger.error(f"Worker {worker_id} inference error: {e}")
                    # Put error with request_id
                    output_queue.put((item.request_id, None, e))
            else:
                # Legacy mode: process and put to output queue
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
    """Model pool operating in pipeline mode only.
    
    In pipeline mode, inference requests are submitted asynchronously via a queue,
    and results are delivered back to the request object via an event.
    """
    
    def __init__(self, config: PoolConfig):
        self.config = config
        self.num_workers = len(config.instances)
        self._processes: list[mp.Process] = []
        self._input_queues: list[mp.Queue] = []  # Per-worker input queues
        self._output_queue = mp.Queue()
        self._memory_queue = mp.Queue()
        self._metrics_queue = mp.Queue()
        self._ready_events: list[mp.Event] = []
        self._is_started = False
        self._result_thread: threading.Thread | None = None
        self._metrics_thread: threading.Thread | None = None
        self._request_counts: dict[int, int] = {}
        self._worker_metrics: dict[int, dict] = {}
        self._metrics_lock = threading.Lock()
        self._shutdown_event = threading.Event()  # Signal for background threads to stop
        
        # Pipeline mode (always enabled)
        self._inference_queue: queue.Queue | None = None
        self._pipeline_consumer_thread: threading.Thread | None = None

    def start(self, timeout_s: float = 120.0) -> None:
        if self._is_started:
            return

        for i, inst in enumerate(self.config.instances):
            ready = mp.Event()
            self._ready_events.append(ready)
            
            # Create per-worker input queue
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

        for i, ev in enumerate(self._ready_events):
            if not ev.wait(timeout_s):
                raise RuntimeError(f"Worker {i} failed to start")

        self._result_thread = threading.Thread(target=self._result_loop, daemon=True)
        self._result_thread.start()
        self._metrics_thread = threading.Thread(target=self._metrics_loop, daemon=True)
        self._metrics_thread.start()
        self._is_started = True
        logger.info(f"Pool ready with {self.num_workers} workers")
    
    def set_inference_queue(self, inference_queue: queue.Queue) -> None:
        """
        Set the inference queue for pipeline mode processing.
        
        Args:
            inference_queue: Queue to consume tokenized batches from
        """
        if not self._is_started:
            raise RuntimeError("Pool must be started before setting inference queue")
        
        self._inference_queue = inference_queue
        self._pipeline_consumer_thread = threading.Thread(
            target=self._pipeline_consumer_loop, daemon=True
        )
        self._pipeline_consumer_thread.start()
        
        logger.info("Model pool inference queue set, pipeline mode active")

    def stop(self, timeout_s: float = 30.0) -> None:
        if not self._is_started:
            return

        # Signal result and metrics threads to stop
        self._shutdown_event.set()

        # Stop worker processes - send _STOP to each worker's per-worker queue
        for input_queue in self._input_queues:
            try:
                input_queue.put(_STOP, block=False)
            except Exception as e:
                logger.debug(f"Error sending STOP to worker: {e}")

        deadline = time.time() + timeout_s

        # Wait for worker processes to exit
        for p in self._processes:
            remaining = max(0, deadline - time.time())
            p.join(timeout=remaining)
            if p.is_alive():
                logger.warning("Worker process did not exit; terminating")
                p.terminate()
                p.join(timeout=1.0)

        # Wait for background threads to exit
        if self._result_thread:
            remaining = max(0, deadline - time.time())
            self._result_thread.join(timeout=remaining)
            if self._result_thread.is_alive():
                logger.warning("Result thread did not exit cleanly")

        if self._metrics_thread:
            remaining = max(0, deadline - time.time())
            self._metrics_thread.join(timeout=remaining)
            if self._metrics_thread.is_alive():
                logger.warning("Metrics thread did not exit cleanly")
        
        if self._pipeline_consumer_thread:
            remaining = max(0, deadline - time.time())
            self._pipeline_consumer_thread.join(timeout=remaining)
            if self._pipeline_consumer_thread.is_alive():
                logger.warning("Pipeline consumer thread did not exit cleanly")

        # Clean up multiprocessing queues to prevent resource leaks
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
        """Drain results from worker processes (not used in pipeline mode).
        
        In pipeline mode, results are handled directly in _pipeline_consumer_loop.
        This thread ensures the output queue doesn't back up.
        """
        while not self._shutdown_event.is_set():
            try:
                # Use timeout so we can check shutdown_event periodically
                result = self._output_queue.get(timeout=0.5)
                # In pipeline mode, results should be empty as they're consumed by pipeline loop
                if result is not None:
                    logger.debug(f"Drained stale result from output queue")
            except (queue.Empty, EOFError):
                # Normal conditions
                continue
            except Exception as e:
                logger.error(f"Result loop error: {e}", exc_info=True)
                continue

    def _metrics_loop(self) -> None:
        """Collect worker metrics until shutdown is signaled."""
        while not self._shutdown_event.is_set():
            try:
                worker_id, metrics_stats = self._metrics_queue.get(timeout=0.5)
                with self._metrics_lock:
                    self._worker_metrics[worker_id] = metrics_stats
            except (queue.Empty, OSError, EOFError):
                # Normal conditions when queue is empty or closed
                continue
            except Exception as e:
                logger.error(f"Metrics loop error: {e}", exc_info=True)
                continue

    def _pipeline_consumer_loop(self) -> None:
        """
        Consume items from the inference queue, send to workers, and deliver results.
        
        This loop runs in the main process and:
        1. Takes tokenized batches from the inference queue
        2. Sends them to worker processes for inference
        3. Waits for results from worker processes
        4. Delivers results directly to requests
        """
        if not self._inference_queue:
            logger.error("Pipeline consumer loop started without inference queue")
            return
        
        pending_results = {}  # Maps request_id -> (request, enqueue_time)
        
        while not self._shutdown_event.is_set():
            try:
                # Check for results from workers with small timeout
                try:
                    worker_result = self._output_queue.get_nowait()
                    if isinstance(worker_result, tuple) and len(worker_result) == 3:
                        request_id, result, error = worker_result
                        if request_id in pending_results:
                            request, enqueue_time = pending_results.pop(request_id)
                            if error:
                                request.error = error
                            else:
                                request.inference_result = result
                            request.result_event.set()
                except queue.Empty:
                    pass
                
                # Get new inference items with timeout
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
                
                # Record queue wait time
                queue_wait_ms = (time.perf_counter() - enqueue_time) * 1000
                request.t_queue_inference_wait_ms = queue_wait_ms
                
                try:
                    # Route to a worker (round-robin)
                    worker_idx = len(self._input_queues) % self.num_workers if self.num_workers > 0 else 0
                    if worker_idx >= len(self._input_queues):
                        worker_idx = 0
                    
                    selected_queue = self._input_queues[worker_idx]
                    
                    # Create work item with only picklable data
                    work_item = _InferenceWorkItem(tokenized_batch, request.request_id)
                    selected_queue.put_nowait(work_item)
                    
                    # Track this request so we can deliver results when they arrive
                    pending_results[request.request_id] = (request, enqueue_time)
                    
                except queue.Full:
                    logger.error(f"Worker queue full, dropping inference request")
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
        return {
            "num_instances": self.num_workers,
            "is_loaded": self._is_started,
            "request_counts": dict(self._request_counts),
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

        with self._metrics_lock:
            return [self._worker_metrics.get(i, {}) for i in range(self.num_workers)]

    def get_worker_metrics_by_id(self, worker_id: int) -> dict:
        if not self._is_started or worker_id >= self.num_workers:
            return {}

        try:
            self._input_queues[worker_id].put(_GET_METRICS, block=False)
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


__all__ = ["ModelPool"]
