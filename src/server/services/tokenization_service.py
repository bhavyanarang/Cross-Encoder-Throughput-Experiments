import concurrent.futures
import logging
import queue
import threading
import time
from collections.abc import Callable

from transformers import AutoTokenizer

from src.server.dto.inference import TokenizedBatch
from src.server.dto.metrics.worker import TokenizerWorkerMetrics
from src.server.services.base import BaseWorker, BaseWorkerPool, setup_worker_environment
from src.server.services.service_base import PoolBasedService

logger = logging.getLogger(__name__)

_STOP = object()


class TokenizerService:
    def __init__(self, model_name: str, max_length: int = 512):
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._max_length = max_length
        logger.info(f"Tokenizer loaded: {model_name}")

    def tokenize(self, pairs: list[tuple[str, str]], device: str = "cpu") -> TokenizedBatch:
        start = time.perf_counter()

        texts = [[p[0], p[1]] for p in pairs]
        features = self._tokenizer(
            texts,
            padding=True,
            truncation="longest_first",
            return_tensors="pt",
            max_length=self._max_length,
        )

        mask = features["attention_mask"]
        batch_size, max_seq = mask.shape
        real_per_seq = mask.sum(dim=1)
        total_real = int(real_per_seq.sum().item())
        total_tokens = batch_size * max_seq
        padded = total_tokens - total_real

        features = {k: v.to(device) for k, v in features.items()}

        return TokenizedBatch(
            features=features,
            batch_size=batch_size,
            max_seq_length=max_seq,
            total_tokens=total_tokens,
            real_tokens=total_real,
            padded_tokens=padded,
            padding_ratio=padded / total_tokens if total_tokens > 0 else 0.0,
            avg_seq_length=float(real_per_seq.float().mean().item()),
            tokenize_time_ms=(time.perf_counter() - start) * 1000,
        )

    @property
    def max_length(self) -> int:
        return self._max_length


class TokenizerWorker(BaseWorker[list[tuple[str, str]], TokenizedBatch]):
    def __init__(self, worker_id: int, model_name: str, max_length: int = 512, metrics=None):
        if metrics is None:
            metrics = TokenizerWorkerMetrics(worker_id=worker_id)
        super().__init__(worker_id, metrics=metrics)
        self.model_name = model_name
        self.max_length = max_length
        self._tokenizer: TokenizerService | None = None

    def initialize(self) -> None:
        setup_worker_environment()
        self._tokenizer = TokenizerService(self.model_name, self.max_length)
        logger.info(f"Tokenizer worker {self.worker_id} loaded: {self.model_name}")
        self.set_ready()

    def process(self, pairs: list[tuple[str, str]]) -> TokenizedBatch:
        if not self._tokenizer:
            raise RuntimeError(f"Tokenizer worker {self.worker_id} not initialized")

        start_time = time.perf_counter()
        result = self._tokenizer.tokenize(pairs, device="cpu")
        latency_ms = (time.perf_counter() - start_time) * 1000

        self._record_metrics(
            latency_ms=latency_ms,
            total_tokens=result.total_tokens,
        )

        return result

    def get_memory_mb(self) -> float:
        return 0.0


class TokenizerPool(BaseWorkerPool[list[tuple[str, str]], TokenizedBatch]):
    def __init__(self, model_name: str, num_workers: int = 1, max_length: int = 512):
        super().__init__(num_workers)
        self.model_name = model_name
        self.max_length = max_length
        self._work_queues: list[queue.Queue] = []
        self._worker_threads: list[threading.Thread] = []
        self._worker_instances: list[TokenizerWorker] = []
        self._round_robin_idx = 0
        self._round_robin_lock = threading.Lock()

    def _worker_thread(self, worker: TokenizerWorker, work_queue: queue.Queue) -> None:
        try:
            worker.initialize()

            while True:
                try:
                    item = work_queue.get(timeout=1.0)

                    if item is _STOP:
                        break

                    if isinstance(item, dict) and "pairs" in item:
                        pairs = item["pairs"]
                        result_container = item["result_container"]

                        try:
                            tokenized = worker.process(pairs)
                            result_container["result"] = tokenized
                            result_container["error"] = None
                        except Exception as e:
                            result_container["result"] = None
                            result_container["error"] = e
                        finally:
                            result_container["event"].set()
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

    def submit(self, pairs: list[tuple[str, str]]) -> TokenizedBatch:
        return self.tokenize(pairs)

    def tokenize(self, pairs: list[tuple[str, str]]) -> TokenizedBatch:
        if not self._is_started:
            raise RuntimeError("Tokenizer pool not started")

        total_start = time.perf_counter()

        event = threading.Event()
        result_container = {"result": None, "error": None, "event": event}

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

        queue_start = time.perf_counter()
        try:
            selected_queue.put_nowait(
                {
                    "pairs": pairs,
                    "result_container": result_container,
                    "worker_id": selected_worker_id,
                }
            )
        except queue.Full:
            raise RuntimeError("Tokenizer pool queue full") from None

        (time.perf_counter() - queue_start) * 1000

        wait_start = time.perf_counter()
        if not event.wait(timeout=30.0):
            raise RuntimeError("Tokenizer pool timeout - worker did not respond") from None
        (time.perf_counter() - wait_start) * 1000

        total_time = (time.perf_counter() - total_start) * 1000

        if result_container["error"]:
            raise result_container["error"]

        if result_container["result"] is None:
            raise RuntimeError("Tokenizer pool returned None result")

        tokenized = result_container["result"]

        overhead_ms = max(0.0, total_time - tokenized.tokenize_time_ms)

        tokenized.overhead_ms = overhead_ms
        tokenized.worker_id = selected_worker_id
        return tokenized

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


class TokenizationService(PoolBasedService):
    def __init__(self, tokenizer_pool: TokenizerPool, max_async_workers: int = 10):
        super().__init__(tokenizer_pool)
        self._tokenizer_pool = tokenizer_pool
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_async_workers, thread_name_prefix="tokenization-async-"
        )

    def tokenize_async(
        self,
        pairs: list[tuple[str, str]],
        callback: Callable[[TokenizedBatch | None, Exception | None], None],
    ) -> None:
        """Tokenize pairs asynchronously with bounded worker threads.

        Args:
            pairs: List of (query, document) tuples to tokenize
            callback: Function to call with (result, error) when done
        """
        if not self._is_started:
            callback(None, RuntimeError("Tokenization service not started"))
            return

        def _tokenize():
            try:
                tokenized = self._tokenizer_pool.tokenize(pairs)
                callback(tokenized, None)
            except Exception as e:
                logger.error(f"Tokenization error: {e}", exc_info=True)
                callback(None, e)

        self._executor.submit(_tokenize)

    def tokenize_sync(self, pairs: list[tuple[str, str]]) -> TokenizedBatch:
        if not self.is_started:
            raise RuntimeError("Tokenization service not started")
        return self._tokenizer_pool.tokenize(pairs)

    def get_worker_metrics(self) -> list[dict]:
        if not self.is_started:
            return []
        return self._tokenizer_pool.get_worker_metrics()

    def reset_worker_metrics(self) -> None:
        if self.is_started:
            self._tokenizer_pool.reset_worker_metrics()

    def stop(self, timeout_s: float = 30.0) -> None:
        """Stop the tokenization service and clean up executor."""
        super().stop()
        try:
            # Note: timeout parameter was added in Python 3.9
            # Using wait=True to block until all tasks complete
            self._executor.shutdown(wait=True)
        except Exception as e:
            logger.warning(f"Error shutting down executor: {e}")


__all__ = [
    "TokenizationService",
    "TokenizerService",
    "TokenizerPool",
    "TokenizerWorker",
]
