"""Minimal-overhead tokenizer pool using simple threading.

Optimized for low latency: direct tokenization with minimal synchronization.
"""

import logging
import queue
import threading
import time

from src.server.services.tokenizer import TokenizedBatch, TokenizerService

logger = logging.getLogger(__name__)

_STOP = object()


class TokenizerPool:
    """Minimal-overhead tokenizer pool with per-worker queues."""

    def __init__(self, model_name: str, num_workers: int = 1, max_length: int = 512):
        self.model_name = model_name
        self.num_workers = num_workers
        self.max_length = max_length
        self._work_queues: list[queue.Queue] = []
        self._workers: list[threading.Thread] = []
        self._is_started = False
        self._round_robin_idx = 0
        self._round_robin_lock = threading.Lock()

    def _worker_thread(self, worker_id: int, work_queue: queue.Queue) -> None:
        """Worker thread - minimal overhead."""
        try:
            tokenizer = TokenizerService(self.model_name, self.max_length)
            logger.info(f"Tokenizer worker {worker_id} loaded: {self.model_name}")

            while True:
                try:
                    item = work_queue.get(timeout=1.0)

                    if item is _STOP:
                        break

                    if isinstance(item, dict) and "pairs" in item:
                        pairs = item["pairs"]
                        result_container = item["result_container"]

                        try:
                            # Direct tokenization - no overhead
                            tokenized = tokenizer.tokenize(pairs, device="cpu")
                            result_container["result"] = tokenized
                            result_container["error"] = None
                        except Exception as e:
                            result_container["result"] = None
                            result_container["error"] = e
                        finally:
                            # Signal completion
                            result_container["event"].set()
                except queue.Empty:
                    continue
        except Exception as e:
            logger.error(f"Tokenizer worker {worker_id} error: {e}")

    def start(self, timeout_s: float = 120.0) -> None:
        """Start all tokenizer worker threads."""
        if self._is_started:
            return

        for i in range(self.num_workers):
            work_queue = queue.Queue(maxsize=1000)
            self._work_queues.append(work_queue)
            worker = threading.Thread(target=self._worker_thread, args=(i, work_queue), daemon=True)
            worker.start()
            self._workers.append(worker)

        # Wait for workers to load tokenizers
        time.sleep(2.0)

        self._is_started = True
        logger.info(f"Tokenizer pool ready with {self.num_workers} workers")

    def stop(self, timeout_s: float = 30.0) -> None:
        """Stop all tokenizer worker threads."""
        if not self._is_started:
            return

        for work_queue in self._work_queues:
            work_queue.put(_STOP)

        deadline = time.time() + timeout_s
        for worker in self._workers:
            remaining = max(0, deadline - time.time())
            worker.join(timeout=remaining)

        self._workers.clear()
        self._work_queues.clear()
        self._is_started = False
        logger.info("Tokenizer pool stopped")

    def tokenize(self, pairs: list[tuple[str, str]]) -> TokenizedBatch:
        """Tokenize with minimal overhead.

        Uses simple Event + dict for synchronization - no Future overhead.
        Returns tokenized batch with overhead tracking.
        """
        if not self._is_started:
            raise RuntimeError("Tokenizer pool not started")

        total_start = time.perf_counter()

        # Minimal synchronization objects
        event = threading.Event()
        result_container = {"result": None, "error": None, "event": event}

        # Optimized load balancing: use round-robin for speed (minimal overhead)
        # Track which worker will handle this request for metrics
        selected_worker_id = 0
        if self.num_workers == 1:
            selected_queue = self._work_queues[0]
            selected_worker_id = 0
        else:
            # Quick round-robin (faster than scanning all queues)
            with self._round_robin_lock:
                idx = self._round_robin_idx
                self._round_robin_idx = (self._round_robin_idx + 1) % self.num_workers
                selected_queue = self._work_queues[idx]
                selected_worker_id = idx

        queue_start = time.perf_counter()
        try:
            # Submit work (non-blocking if queue has space)
            selected_queue.put_nowait(
                {
                    "pairs": pairs,
                    "result_container": result_container,
                    "worker_id": selected_worker_id,  # Track which worker handles this
                }
            )
        except queue.Full:
            raise RuntimeError("Tokenizer pool queue full") from None

        (time.perf_counter() - queue_start) * 1000

        # Wait for completion (Event.wait is efficient)
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
        # Calculate overhead: total time - actual tokenize time
        overhead_ms = max(0.0, total_time - tokenized.tokenize_time_ms)

        # Set overhead and worker_id directly on existing object (avoid creating new object)
        tokenized.overhead_ms = overhead_ms
        tokenized.worker_id = selected_worker_id  # Track which worker handled this
        return tokenized

    def get_info(self) -> dict:
        """Get pool information."""
        queue_sizes = [q.qsize() for q in self._work_queues] if self._is_started else []
        return {
            "model_name": self.model_name,
            "num_workers": self.num_workers,
            "is_loaded": self._is_started,
            "queue_sizes": queue_sizes,
            "total_queue_size": sum(queue_sizes),
        }

    @property
    def is_loaded(self) -> bool:
        return self._is_started

    def __len__(self) -> int:
        return self.num_workers


__all__ = ["TokenizerPool"]
