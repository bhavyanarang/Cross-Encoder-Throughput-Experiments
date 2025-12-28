"""Inference DTOs."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from src.server.services.tokenizer import TokenizedBatch


@dataclass
class InferenceResult:
    scores: np.ndarray
    t_tokenize_ms: float = 0.0
    t_model_inference_ms: float = 0.0
    t_queue_wait_ms: float = 0.0
    t_overhead_ms: float = 0.0  # Tokenizer pool overhead
    t_mp_queue_send_ms: float = 0.0  # Multiprocessing queue send time
    t_mp_queue_receive_ms: float = 0.0  # Multiprocessing queue receive/wait time
    t_grpc_serialize_ms: float = 0.0  # gRPC request serialization time
    t_grpc_deserialize_ms: float = 0.0  # gRPC response deserialization time
    t_scheduler_ms: float = 0.0  # Scheduler overhead
    total_ms: float = 0.0
    total_tokens: int = 0
    real_tokens: int = 0
    padded_tokens: int = 0
    padding_ratio: float = 0.0
    max_seq_length: int = 0
    avg_seq_length: float = 0.0
    batch_size: int = 0
    worker_id: int = -1


@dataclass
class WorkItem:
    req_id: int
    tokenized_batch: "TokenizedBatch"  # Tokenized features (required)


@dataclass
class WorkResult:
    req_id: int
    scores: np.ndarray
    worker_id: int
    t_tokenize_ms: float = 0.0
    t_model_inference_ms: float = 0.0
    t_queue_wait_ms: float = 0.0
    total_ms: float = 0.0
    total_tokens: int = 0
    real_tokens: int = 0
    padded_tokens: int = 0
    padding_ratio: float = 0.0
    max_seq_length: int = 0
    avg_seq_length: float = 0.0
    batch_size: int = 0
