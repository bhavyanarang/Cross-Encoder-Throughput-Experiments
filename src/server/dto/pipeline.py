"""
Queue-based pipeline DTOs for decoupled tokenization and inference stages.

This module defines the data structures used to represent requests as they flow
through the tokenization and inference queues. This design ensures that:
1. Tokenization workers can process independently without blocking on inference
2. Inference workers can batch results from multiple tokenization workers
3. GPU resources are never starved - work flows continuously through the pipeline
"""

import threading
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.server.dto import InferenceResult, TokenizedBatch


@dataclass
class PipelineRequest:
    """
    A user request entering the pipeline.

    This is created when a request arrives and is placed in the tokenization queue.
    It carries the original pairs and metadata needed to track the request through
    both tokenization and inference stages.
    """

    request_id: int
    pairs: list[tuple[str, str]]
    submit_time: float = field(default_factory=time.perf_counter)

    # Future to signal when inference result is ready
    result_event: threading.Event = field(default_factory=threading.Event)

    # Will be set after tokenization
    tokenized_batch: "TokenizedBatch | None" = None
    tokenizer_worker_id: int = -1

    # Will be set after inference
    inference_result: "InferenceResult | None" = None
    inference_worker_id: int = -1

    # Error tracking
    error: Exception | None = None

    # Timing - populated as request progresses
    t_queue_tokenization_wait_ms: float = 0.0
    t_queue_inference_wait_ms: float = 0.0


@dataclass
class TokenizationQueueItem:
    """
    Item in the tokenization queue.

    Contains the request and its pairs, ready for tokenization workers to process.
    """

    request: PipelineRequest
    pairs: list[tuple[str, str]]
    enqueue_time: float = field(default_factory=time.perf_counter)


@dataclass
class InferenceQueueItem:
    """
    Item in the inference queue.

    Contains the tokenized batch and metadata needed for inference workers.
    After inference, the result will be stored in the request object.
    """

    request: PipelineRequest
    tokenized_batch: "TokenizedBatch"
    enqueue_time: float = field(default_factory=time.perf_counter)


__all__ = [
    "PipelineRequest",
    "TokenizationQueueItem",
    "InferenceQueueItem",
]
