"""Tokenizer pool for managing tokenization workers in pipeline mode."""

import logging
import queue
import threading
import time

from src.server.dto.pipeline import InferenceQueueItem, TokenizationQueueItem
from src.server.pool.base import BaseWorkerPool
from src.server.worker.tokenizer_worker import TokenizerWorker

logger = logging.getLogger(__name__)

_STOP = object()


class TokenizerPool(BaseWorkerPool):
    """Tokenizer pool operating in pipeline mode only.
    
    In pipeline mode, tokenization requests are submitted asynchronously via a queue,
    and results are pushed to the inference queue for downstream processing.
    """
    
    def __init__(self, model_name: str, num_workers: int = 1, max_length: int = 512):
        super().__init__(num_workers)
        self.model_name = model_name
        self.max_length = max_length
        self._work_queues: list[queue.Queue] = []
        self._worker_threads: list[threading.Thread] = []
        self._worker_instances: list[TokenizerWorker] = []
        self._round_robin_idx = 0
        self._round_robin_lock = threading.Lock()
        
        # Inference queue to push tokenized results to
        self._inference_queue: queue.Queue | None = None

    def _worker_thread(self, worker: TokenizerWorker, work_queue: queue.Queue) -> None:
        try:
            worker.initialize()

            while True:
                try:
                    item = work_queue.get(timeout=1.0)

                    if item is _STOP:
                        break

                    # Pipeline mode only
                    if not isinstance(item, TokenizationQueueItem):
                        logger.warning("Received non-TokenizationQueueItem in pipeline mode, ignoring")
                        continue
                    
                    tokenization_item = item
                    request = tokenization_item.request
                    pairs = tokenization_item.pairs
                    enqueue_time = tokenization_item.enqueue_time
                    
                    try:
                        tokenized = worker.process(pairs)
                        
                        # Record queue wait time
                        queue_wait_ms = (time.perf_counter() - enqueue_time) * 1000
                        request.t_queue_tokenization_wait_ms = queue_wait_ms
                        request.tokenized_batch = tokenized
                        request.tokenizer_worker_id = worker.worker_id
                        
                        # Push to inference queue
                        if self._inference_queue:
                            try:
                                inference_item = InferenceQueueItem(
                                    request=request,
                                    tokenized_batch=tokenized,
                                )
                                self._inference_queue.put(inference_item, block=False)
                            except queue.Full:
                                logger.warning("Inference queue full, dropping tokenized result")
                                request.error = RuntimeError("Inference queue full")
                                request.result_event.set()
                        else:
                            logger.error("Inference queue not set in pipeline mode")
                            request.error = RuntimeError("Inference queue not configured")
                            request.result_event.set()
                            
                    except Exception as e:
                        logger.error(f"Tokenization error: {e}")
                        request.error = e
                        request.result_event.set()
                except queue.Empty:
                    continue
        except Exception as e:
            logger.error(f"Tokenizer worker {worker.worker_id} error: {e}")

    def start(self, timeout_s: float = 120.0) -> None:
        if self._is_started:
            return

        for i in range(self.num_workers):
            work_queue = queue.Queue(maxsize=1000)
            self._work_queues.append(work_queue)
            worker = TokenizerWorker(i, self.model_name, self.max_length)
            self._worker_instances.append(worker)
            worker_thread = threading.Thread(
                target=self._worker_thread, args=(worker, work_queue), daemon=True
            )
            worker_thread.start()
            self._worker_threads.append(worker_thread)

        time.sleep(2.0)

        self._is_started = True
        logger.info(f"Tokenizer pool ready with {self.num_workers} workers")

    def stop(self, timeout_s: float = 30.0) -> None:
        if not self._is_started:
            return

        for work_queue in self._work_queues:
            work_queue.put(_STOP)

        deadline = time.time() + timeout_s
        for worker_thread in self._worker_threads:
            remaining = max(0, deadline - time.time())
            worker_thread.join(timeout=remaining)

        self._worker_threads.clear()
        self._work_queues.clear()
        self._worker_instances.clear()
        self._is_started = False
        logger.info("Tokenizer pool stopped")

    def set_inference_queue(self, inference_queue: queue.Queue) -> None:
        """
        Set the inference queue to automatically push tokenized results to.
        
        When set, tokenized batches will be automatically pushed to this queue
        instead of being returned directly. This enables the decoupled pipeline.
        """
        self._inference_queue = inference_queue

    def submit(self, work_item: TokenizationQueueItem) -> None:
        """
        Submit a tokenization work item (required by BaseWorkerPool abstract interface).
        
        In pipeline mode, this delegates to submit_pipeline().
        
        Args:
            work_item: TokenizationQueueItem to process
            
        Raises:
            RuntimeError: If tokenizer pool not started or queue is full
        """
        self.submit_pipeline(work_item)

    def submit_pipeline(self, tokenization_item: TokenizationQueueItem) -> None:
        """
        Submit a request to the tokenization queue for pipeline processing.
        
        This method is used in the queue-based pipeline mode where tokenization
        results are automatically pushed to the inference queue.
        
        Args:
            tokenization_item: Item containing request and pairs to tokenize
            
        Raises:
            RuntimeError: If tokenizer pool not started or queue is full
        """
        if not self._is_started:
            raise RuntimeError("Tokenizer pool not started")
        
        selected_worker_id = 0
        if self.num_workers == 1:
            selected_queue = self._work_queues[0]
            selected_worker_id = 0
        else:
            with self._round_robin_lock:
                idx = self._round_robin_idx
                self._round_robin_idx = (self._round_robin_idx + 1) % self.num_workers
                selected_queue = self._work_queues[idx]
                selected_worker_id = idx
        
        try:
            selected_queue.put_nowait(tokenization_item)
        except queue.Full:
            raise RuntimeError("Tokenizer pool queue full") from None


    def get_info(self) -> dict:
        queue_sizes = [q.qsize() for q in self._work_queues] if self._is_started else []
        return {
            "model_name": self.model_name,
            "num_workers": self.num_workers,
            "is_loaded": self._is_started,
            "queue_sizes": queue_sizes,
            "total_queue_size": sum(queue_sizes),
        }

    def get_worker_metrics(self) -> list[dict]:
        if not self._is_started:
            return []
        return [worker.get_metrics_stats() for worker in self._worker_instances]

    def get_worker_metrics_by_id(self, worker_id: int) -> dict:
        if not self._is_started or worker_id >= len(self._worker_instances):
            return {}
        return self._worker_instances[worker_id].get_metrics_stats()

    def reset_worker_metrics(self) -> None:
        if self._is_started:
            for worker in self._worker_instances:
                worker.reset_metrics()

    @property
    def is_loaded(self) -> bool:
        return self._is_started

    def __len__(self) -> int:
        return self.num_workers


__all__ = ["TokenizerPool"]
