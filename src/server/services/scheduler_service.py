import logging
import queue
import threading
import time
from typing import TYPE_CHECKING

from src.server.models import PendingRequest

if TYPE_CHECKING:
    from src.server.models import InferenceResult
    from src.server.services.inference_service import InferenceService
    from src.server.services.tokenization_service import TokenizationService

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(
        self,
        tokenization_service: "TokenizationService",
        inference_service: "InferenceService",
        batching_enabled: bool = False,
        max_batch_size: int = 8,
        timeout_ms: float = 100,
        length_aware: bool = False,
    ):
        self._tokenization_service = tokenization_service
        self._inference_service = inference_service
        self._batching = batching_enabled
        self._max_batch = max_batch_size
        self._timeout_ms = timeout_ms
        self._length_aware = length_aware

        self._queue: queue.Queue[PendingRequest] = queue.Queue()

        self._condition = threading.Condition()

        self._batch_thread: threading.Thread | None = None
        self._running = False

        if self._batching:
            self._running = True
            self._batch_thread = threading.Thread(target=self._batch_loop, daemon=True)
            self._batch_thread.start()
            logger.info(
                f"Scheduler service created with batching: max_batch={max_batch_size}, timeout_ms={timeout_ms}"
            )

    def schedule(self, pairs: list[tuple[str, str]]) -> "InferenceResult":
        if not self._batching:
            tokenized_batch = self._tokenization_service.tokenize_sync(pairs)
            return self._inference_service.infer_sync(tokenized_batch)

        req = PendingRequest(
            pairs=pairs,
            result_future=threading.Event(),
            submit_time=time.perf_counter(),
        )

        self._queue.put(req)

        with self._condition:
            self._condition.notify()

        req.result_future.wait()
        return req.result

    def _batch_loop(self) -> None:
        while self._running:
            batch: list[PendingRequest] = []
            timeout_sec = self._timeout_ms / 1000.0

            try:
                first_item = self._queue.get(timeout=timeout_sec)
                batch.append(first_item)
            except queue.Empty:
                continue

            deadline = time.perf_counter() + timeout_sec
            while len(batch) < self._max_batch:
                remaining = deadline - time.perf_counter()
                if remaining <= 0:
                    break
                try:
                    item = self._queue.get(timeout=min(0.001, remaining))
                    batch.append(item)
                except queue.Empty:
                    break

            if batch:
                self._process_batch(batch)

    def _process_batch(self, batch: list[PendingRequest]) -> None:
        batch_start_time = time.perf_counter()

        all_pairs = []
        for req in batch:
            all_pairs.extend(req.pairs)

        if self._length_aware:
            all_pairs.sort(key=lambda p: len(p[0]) + len(p[1]))

        try:
            tokenized_batch = self._tokenization_service.tokenize_sync(all_pairs)

            result = self._inference_service.infer_sync(tokenized_batch)

            idx = 0
            for req in batch:
                n = len(req.pairs)

                queue_wait_ms = (batch_start_time - req.submit_time) * 1000

                req.result = type(result)(
                    scores=result.scores[idx : idx + n],
                    t_tokenize_ms=result.t_tokenize_ms,
                    t_model_inference_ms=result.t_model_inference_ms,
                    t_queue_wait_ms=queue_wait_ms,
                    total_ms=result.total_ms,
                    total_tokens=result.total_tokens,
                    real_tokens=result.real_tokens,
                    padded_tokens=result.padded_tokens,
                    padding_ratio=result.padding_ratio,
                    max_seq_length=result.max_seq_length,
                    avg_seq_length=result.avg_seq_length,
                    batch_size=len(all_pairs),
                    worker_id=getattr(result, "worker_id", -1),
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
            "pending": self._queue.qsize(),
        }

    def stop(self) -> None:
        self._running = False

        with self._condition:
            self._condition.notify_all()


__all__ = ["SchedulerService"]
