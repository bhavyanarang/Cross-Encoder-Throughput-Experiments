import logging
import multiprocessing as mp
import queue
import threading
import time
from typing import Optional

from src.server.dto.pipeline import InferenceQueueItem, TokenizationQueueItem
from src.server.pool.base import BaseWorkerPool
from src.server.worker.tokenizer_worker import TokenizerWorker

logger = logging.getLogger(__name__)

_STOP = "__STOP__"
_GET_METRICS = "__GET_METRICS__"


def _tokenizer_worker_main(
    worker_id: int,
    model_name: str,
    max_length: int,
    input_queue: mp.Queue,
    output_queue: mp.Queue,
    metrics_queue: mp.Queue,
    ready_event: mp.Event,
):
    try:
        worker = TokenizerWorker(worker_id, model_name, max_length)
        worker.initialize()
        ready_event.set()

        while True:
            try:
                item = input_queue.get()

                if item == _STOP:
                    break

                if item == _GET_METRICS:
                    try:
                        metrics = worker.get_metrics_stats()
                        metrics_queue.put((worker_id, metrics), block=False)
                    except Exception:
                        pass
                    continue

                req_id, pairs, enqueue_time = item

                try:
                    tokenized = worker.process(pairs)
                    output_queue.put((req_id, tokenized, None, enqueue_time, worker_id))
                except Exception as e:
                    logger.error(
                        f"Tokenizer worker {worker_id} error processing request {req_id}: {e}"
                    )
                    output_queue.put((req_id, None, e, enqueue_time, worker_id))

            except Exception as e:
                logger.error(f"Tokenizer worker {worker_id} loop error: {e}")

    except Exception as e:
        logger.error(f"Tokenizer worker {worker_id} initialization failed: {e}")
        ready_event.set()


class TokenizerPool(BaseWorkerPool):
    def __init__(self, model_name: str, num_workers: int = 1, max_length: int = 512):
        super().__init__(num_workers)
        self.model_name = model_name
        self.max_length = max_length

        self._processes: list[mp.Process] = []
        self._input_queue: Optional[mp.Queue] = None
        self._output_queue = mp.Queue()
        self._metrics_queue = mp.Queue()
        self._ready_events: list[mp.Event] = []

        self._result_thread: Optional[threading.Thread] = None

        self._inference_queue: Optional[queue.Queue] = None

        self._pending_items: dict[int, TokenizationQueueItem] = {}
        self._pending_lock = threading.Lock()

        self._total_batches = 0
        self._total_queries = 0
        self._start_time: Optional[float] = None
        self._stats_lock = threading.Lock()

    def start(self, timeout_s: float = 120.0) -> None:
        if self._is_started:
            return

        self._start_time = time.time()
        self._total_batches = 0
        self._total_queries = 0
        self._shutdown_event.clear()

        self._input_queue = mp.Queue()

        for i in range(self.num_workers):
            ready_event = mp.Event()
            self._ready_events.append(ready_event)

            p = mp.Process(
                target=_tokenizer_worker_main,
                args=(
                    i,
                    self.model_name,
                    self.max_length,
                    self._input_queue,
                    self._output_queue,
                    self._metrics_queue,
                    ready_event,
                ),
                daemon=True,
            )
            p.start()
            self._processes.append(p)

        for i, ev in enumerate(self._ready_events):
            if not ev.wait(timeout=30.0):
                logger.warning(f"Tokenizer worker {i} failed to start within timeout")

        self._result_thread = threading.Thread(target=self._result_loop, daemon=True)
        self._result_thread.start()

        self.start_metrics_thread()

        self._is_started = True
        logger.info(f"Tokenizer pool ready with {self.num_workers} workers (MP, Shared Queue)")

    def stop(self, timeout_s: float = 30.0) -> None:
        if not self._is_started:
            return

        self._shutdown_event.set()

        if self._input_queue:
            for _ in range(self.num_workers):
                try:
                    self._input_queue.put(_STOP)
                except Exception:
                    pass

        deadline = time.time() + timeout_s
        for p in self._processes:
            remaining = max(0, deadline - time.time())
            p.join(timeout=remaining)
            if p.is_alive():
                p.terminate()

        if self._result_thread:
            self._result_thread.join(timeout=1.0)

        self.stop_metrics_thread(timeout_s=1.0)

        self._processes.clear()
        self._input_queue = None
        self._ready_events.clear()

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
        if not self._is_started or not self._input_queue:
            raise RuntimeError("Tokenizer pool not started")

        req_id = tokenization_item.request.request_id

        if not self._input_queue:
            raise RuntimeError("Tokenizer pool input queue not initialized")

        with self._pending_lock:
            self._pending_items[req_id] = tokenization_item

        try:
            self._input_queue.put_nowait(
                (req_id, tokenization_item.pairs, tokenization_item.enqueue_time)
            )
        except queue.Full:
            with self._pending_lock:
                self._pending_items.pop(req_id, None)
            raise RuntimeError("Tokenizer pool shared queue full") from None

    def _result_loop(self) -> None:
        while not self._shutdown_event.is_set():
            try:
                try:
                    result = self._output_queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                req_id, tokenized_batch, error, enqueue_time, worker_id = result

                tokenization_item = None
                with self._pending_lock:
                    tokenization_item = self._pending_items.pop(req_id, None)

                if not tokenization_item:
                    logger.warning(f"Received result for unknown/cancelled request {req_id}")
                    continue

                request = tokenization_item.request

                if error:
                    logger.error(f"Tokenization error for {req_id}: {error}")
                    request.error = error
                    request.result_event.set()
                    continue

                num_pairs = len(tokenization_item.pairs)
                with self._stats_lock:
                    self._total_batches += 1
                    self._total_queries += num_pairs

                queue_wait_ms = (time.perf_counter() - enqueue_time) * 1000
                request.t_queue_tokenization_wait_ms = queue_wait_ms
                request.tokenized_batch = tokenized_batch
                request.tokenizer_worker_id = worker_id

                if self._inference_queue:
                    try:
                        inference_item = InferenceQueueItem(
                            request=request,
                            tokenized_batch=tokenized_batch,
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
                logger.error(f"Tokenizer pool result loop error: {e}", exc_info=True)

    def get_info(self) -> dict:
        total_worker_queue_size = 0
        inference_queue_size = 0

        if self._is_started and self._input_queue:
            try:
                try:
                    total_worker_queue_size = self._input_queue.qsize()
                except NotImplementedError:
                    total_worker_queue_size = 0

                if self._inference_queue:
                    inference_queue_size = self._inference_queue.qsize()
            except Exception as e:
                logger.debug(f"Error getting tokenizer queue sizes: {e}")

        queue_sizes = [total_worker_queue_size] + [0] * (self.num_workers - 1)

        return {
            "model_name": self.model_name,
            "num_workers": self.num_workers,
            "is_loaded": self._is_started,
            "queue_sizes": queue_sizes,
            "total_queue_size": total_worker_queue_size,
            "inference_queue_size": inference_queue_size,
        }

    def get_worker_metrics(self) -> list[dict]:
        if not self._is_started or not self._input_queue:
            return []

        for _ in range(self.num_workers):
            try:
                self._input_queue.put(_GET_METRICS)
            except Exception:
                pass

        return super().get_worker_metrics()

    def get_worker_metrics_by_id(self, worker_id: int) -> dict:
        return super().get_worker_metrics_by_id(worker_id)
