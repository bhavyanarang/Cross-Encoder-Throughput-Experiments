"""Request scheduler with batching support."""

import logging
import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import InferenceResult
    from src.server.pool import ModelPool

logger = logging.getLogger(__name__)


@dataclass
class PendingRequest:
    pairs: list[tuple[str, str]]
    result_future: threading.Event
    result: "InferenceResult | None" = None
    submit_time: float = 0.0


class Scheduler:
    """Scheduler with optional dynamic batching."""

    def __init__(
        self,
        model_pool: "ModelPool",
        batching_enabled: bool = False,
        max_batch_size: int = 8,
        timeout_ms: float = 100,
        length_aware: bool = False,
    ):
        self._pool = model_pool
        self._batching = batching_enabled
        self._max_batch = max_batch_size
        self._timeout_ms = timeout_ms
        self._length_aware = length_aware
        self._queue: deque[PendingRequest] = deque()
        self._lock = threading.Lock()
        self._batch_thread: threading.Thread | None = None
        self._running = False

        if self._batching:
            self._running = True
            self._batch_thread = threading.Thread(target=self._batch_loop, daemon=True)
            self._batch_thread.start()

    def schedule(self, pairs: list[tuple[str, str]]) -> "InferenceResult":
        if not self._batching:
            return self._pool.infer(pairs)

        req = PendingRequest(
            pairs=pairs,
            result_future=threading.Event(),
            submit_time=time.perf_counter(),
        )

        with self._lock:
            self._queue.append(req)

        req.result_future.wait()
        return req.result

    def _batch_loop(self) -> None:
        while self._running:
            batch: list[PendingRequest] = []
            deadline = time.perf_counter() + (self._timeout_ms / 1000)

            while len(batch) < self._max_batch and time.perf_counter() < deadline:
                with self._lock:
                    if self._queue:
                        batch.append(self._queue.popleft())

                if not batch:
                    time.sleep(0.001)

            if batch:
                self._process_batch(batch)

    def _process_batch(self, batch: list[PendingRequest]) -> None:
        all_pairs = []
        for req in batch:
            all_pairs.extend(req.pairs)

        if self._length_aware:
            all_pairs.sort(key=lambda p: len(p[0]) + len(p[1]))

        try:
            result = self._pool.infer(all_pairs)

            idx = 0
            for req in batch:
                n = len(req.pairs)
                req.result = type(result)(
                    scores=result.scores[idx : idx + n],
                    t_tokenize_ms=result.t_tokenize_ms,
                    t_model_inference_ms=result.t_model_inference_ms,
                    total_ms=result.total_ms,
                    batch_size=n,
                )
                idx += n
                req.result_future.set()
        except Exception as e:
            logger.error(f"Batch error: {e}")
            for req in batch:
                req.result_future.set()

    def get_info(self) -> dict:
        return {
            "batching_enabled": self._batching,
            "max_batch_size": self._max_batch,
            "timeout_ms": self._timeout_ms,
            "length_aware": self._length_aware,
            "pending": len(self._queue),
        }

    def stop(self) -> None:
        self._running = False


__all__ = ["Scheduler"]
