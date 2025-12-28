"""Request scheduler with optimized batching support.

Optimizations applied:
1. Use queue.Queue instead of deque with manual locking (thread-safe with blocking)
2. Use threading.Condition for efficient signaling (no busy polling)
3. Batch collection without per-item locking
4. Reduced synchronization overhead
"""

import logging
import queue
import threading
import time
from typing import TYPE_CHECKING

from src.models import PendingRequest

if TYPE_CHECKING:
    from src.models import InferenceResult
    from src.server.pool import ModelPool
    from src.server.services.inference_service import InferenceService
    from src.server.services.tokenization_service import TokenizationService

logger = logging.getLogger(__name__)


class Scheduler:
    """Optimized scheduler with dynamic batching."""

    def __init__(
        self,
        model_pool: "ModelPool",
        tokenization_service: "TokenizationService",
        inference_service: "InferenceService",
        batching_enabled: bool = False,
        max_batch_size: int = 8,
        timeout_ms: float = 100,
        length_aware: bool = False,
    ):
        self._pool = model_pool
        self._tokenization_service = tokenization_service
        self._inference_service = inference_service
        self._batching = batching_enabled
        self._max_batch = max_batch_size
        self._timeout_ms = timeout_ms
        self._length_aware = length_aware

        # Use thread-safe queue instead of deque + lock
        self._queue: queue.Queue[PendingRequest] = queue.Queue()

        # Condition for efficient waiting (no busy polling)
        self._condition = threading.Condition()

        self._batch_thread: threading.Thread | None = None
        self._running = False

        if self._batching:
            self._running = True
            self._batch_thread = threading.Thread(target=self._batch_loop, daemon=True)
            self._batch_thread.start()
            logger.info(
                f"Scheduler created with batching: max_batch={max_batch_size}, timeout_ms={timeout_ms}"
            )

    def schedule(self, pairs: list[tuple[str, str]]) -> "InferenceResult":
        """Schedule inference request."""
        if not self._batching:
            # Non-batching: tokenize then infer
            tokenized_batch = self._tokenization_service.tokenize_sync(pairs)
            return self._inference_service.infer_sync(tokenized_batch)

        # Create request with event for completion signaling
        req = PendingRequest(
            pairs=pairs,
            result_future=threading.Event(),
            submit_time=time.perf_counter(),
        )

        # Add to queue (thread-safe, no explicit locking needed)
        self._queue.put(req)

        # Signal batch thread that new request is available
        with self._condition:
            self._condition.notify()

        # Wait for result
        req.result_future.wait()
        return req.result

    def _batch_loop(self) -> None:
        """Optimized batch collection loop."""
        while self._running:
            batch: list[PendingRequest] = []
            timeout_sec = self._timeout_ms / 1000.0

            # Wait for first item with condition (no busy polling)
            try:
                first_item = self._queue.get(timeout=timeout_sec)
                batch.append(first_item)
            except queue.Empty:
                continue

            # Collect more items if available (non-blocking)
            deadline = time.perf_counter() + timeout_sec
            while len(batch) < self._max_batch:
                remaining = deadline - time.perf_counter()
                if remaining <= 0:
                    break
                try:
                    # Short timeout to check for more items
                    item = self._queue.get(timeout=min(0.001, remaining))
                    batch.append(item)
                except queue.Empty:
                    # No more items available, process what we have
                    break

            if batch:
                self._process_batch(batch)

    def _process_batch(self, batch: list[PendingRequest]) -> None:
        """Process a batch of requests."""
        # Calculate queue wait time for each request
        batch_start_time = time.perf_counter()

        all_pairs = []
        for req in batch:
            all_pairs.extend(req.pairs)

        if self._length_aware:
            all_pairs.sort(key=lambda p: len(p[0]) + len(p[1]))

        try:
            # Tokenize the combined batch
            tokenized_batch = self._tokenization_service.tokenize_sync(all_pairs)
            # Infer with tokenized batch
            result = self._inference_service.infer_sync(tokenized_batch)

            idx = 0
            for req in batch:
                n = len(req.pairs)
                # Calculate queue wait time for this request
                queue_wait_ms = (batch_start_time - req.submit_time) * 1000

                req.result = type(result)(
                    scores=result.scores[idx : idx + n],
                    t_tokenize_ms=result.t_tokenize_ms,
                    t_model_inference_ms=result.t_model_inference_ms,
                    t_queue_wait_ms=queue_wait_ms,
                    total_ms=result.total_ms,
                    # Copy padding stats from the batched result
                    total_tokens=result.total_tokens,
                    real_tokens=result.real_tokens,
                    padded_tokens=result.padded_tokens,
                    padding_ratio=result.padding_ratio,
                    max_seq_length=result.max_seq_length,
                    avg_seq_length=result.avg_seq_length,
                    batch_size=len(all_pairs),  # Actual batch size used
                    worker_id=getattr(result, "worker_id", -1),
                )
                idx += n
                req.result_future.set()
        except Exception as e:
            logger.error(f"Batch error: {e}")
            for req in batch:
                req.result_future.set()

    def get_info(self) -> dict:
        """Get scheduler info."""
        return {
            "batching_enabled": self._batching,
            "max_batch_size": self._max_batch,
            "timeout_ms": self._timeout_ms,
            "length_aware": self._length_aware,
            "pending": self._queue.qsize(),
        }

    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        # Wake up the batch thread if it's waiting
        with self._condition:
            self._condition.notify_all()


__all__ = ["Scheduler"]
