import logging
import queue
import threading
import time
from itertools import count

from src.server.dto.pipeline import InferenceQueueItem, TokenizationQueueItem
from src.server.pool.base import BaseWorkerPool
from src.server.worker.tokenizer_worker import TokenizerWorker

logger = logging.getLogger(__name__)

_STOP = object()


class TokenizerPool(BaseWorkerPool):
    def __init__(self, model_name: str, num_workers: int = 1, max_length: int = 512):
        super().__init__(num_workers)
        self.model_name = model_name
        self.max_length = max_length
        self._work_queues: list[queue.Queue] = []
        self._worker_threads: list[threading.Thread] = []
        self._worker_instances: list[TokenizerWorker] = []
        self._round_robin_counter = count()  # Lock-free atomic counter

        self._inference_queue: queue.Queue | None = None
        self._total_batches = 0
        self._total_queries = 0
        self._start_time: float | None = None
        self._stats_lock = threading.Lock()

    def _worker_thread(self, worker: TokenizerWorker, work_queue: queue.Queue) -> None:
        try:
            worker.initialize()

            total_batches = 0
            total_queries = 0
            time.time()

            while True:
                try:
                    item = work_queue.get(timeout=1.0)

                    if item is _STOP:
                        break

                    if not isinstance(item, TokenizationQueueItem):
                        logger.warning(
                            "Received non-TokenizationQueueItem in pipeline mode, ignoring"
                        )
                        continue

                    tokenization_item = item
                    request = tokenization_item.request
                    pairs = tokenization_item.pairs
                    enqueue_time = tokenization_item.enqueue_time

                    try:
                        tokenized = worker.process(pairs)

                        total_batches += 1
                        total_queries += len(pairs)
                        with self._stats_lock:
                            self._total_batches += 1
                            self._total_queries += len(pairs)

                        queue_wait_ms = (time.perf_counter() - enqueue_time) * 1000
                        request.t_queue_tokenization_wait_ms = queue_wait_ms
                        request.tokenized_batch = tokenized
                        request.tokenizer_worker_id = worker.worker_id

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

        self._start_time = time.time()
        self._total_batches = 0
        self._total_queries = 0

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

        if self._start_time:
            elapsed = time.time() - self._start_time
            with self._stats_lock:
                batches = self._total_batches
                queries = self._total_queries
            if elapsed > 0 and batches > 0:
                throughput = queries / elapsed
                logger.info(
                    f"Tokenizer Pool Statistics: {batches} batches, {queries} queries "
                    f"processed in {elapsed:.1f}s ({throughput:.1f} q/s)"
                )

        logger.info("Tokenizer pool stopped")

    def set_inference_queue(self, inference_queue: queue.Queue) -> None:
        self._inference_queue = inference_queue

    def submit(self, work_item: TokenizationQueueItem) -> None:
        self.submit_pipeline(work_item)

    def submit_pipeline(self, tokenization_item: TokenizationQueueItem) -> None:
        if not self._is_started:
            raise RuntimeError("Tokenizer pool not started")

        # Lock-free round-robin using atomic counter
        selected_worker_id = next(self._round_robin_counter) % self.num_workers
        selected_queue = self._work_queues[selected_worker_id]

        try:
            selected_queue.put_nowait(tokenization_item)
        except queue.Full:
            raise RuntimeError(f"Tokenizer pool queue {selected_worker_id} full") from None

    def get_info(self) -> dict:
        queue_sizes = []
        total_worker_queue_size = 0
        inference_queue_size = 0

        if self._is_started:
            try:
                for q in self._work_queues:
                    size = q.qsize()
                    queue_sizes.append(size)
                    total_worker_queue_size += size

                if self._inference_queue:
                    inference_queue_size = self._inference_queue.qsize()
            except Exception as e:
                logger.debug(f"Error getting tokenizer queue sizes: {e}")

        return {
            "model_name": self.model_name,
            "num_workers": self.num_workers,
            "is_loaded": self._is_started,
            "queue_sizes": queue_sizes,
            "total_queue_size": total_worker_queue_size,
            "inference_queue_size": inference_queue_size,
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


__all__ = ["TokenizerPool"]
