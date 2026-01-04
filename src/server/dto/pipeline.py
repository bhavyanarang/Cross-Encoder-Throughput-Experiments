import threading
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.server.dto import InferenceResult, TokenizedBatch


@dataclass
class PipelineRequest:
    request_id: int
    pairs: list[tuple[str, str]]
    submit_time: float = field(default_factory=time.perf_counter)

    result_event: threading.Event = field(default_factory=threading.Event)

    tokenized_batch: Optional["TokenizedBatch"] = None
    tokenizer_worker_id: int = -1

    inference_result: Optional["InferenceResult"] = None
    inference_worker_id: int = -1

    error: Exception | None = None

    t_queue_tokenization_wait_ms: float = 0.0
    t_queue_inference_wait_ms: float = 0.0


@dataclass
class TokenizationQueueItem:
    request: PipelineRequest
    pairs: list[tuple[str, str]]
    enqueue_time: float = field(default_factory=time.perf_counter)


@dataclass
class InferenceQueueItem:
    request: PipelineRequest
    tokenized_batch: "TokenizedBatch"
    enqueue_time: float = field(default_factory=time.perf_counter)


__all__ = [
    "PipelineRequest",
    "TokenizationQueueItem",
    "InferenceQueueItem",
]
