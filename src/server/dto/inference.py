from dataclasses import dataclass

import numpy as np
import torch


@dataclass
class InferenceResult:
    scores: np.ndarray
    t_tokenize_ms: float = 0.0
    t_model_inference_ms: float = 0.0
    t_queue_wait_ms: float = 0.0
    t_tokenizer_queue_wait_ms: float = 0.0
    t_model_queue_wait_ms: float = 0.0
    t_overhead_ms: float = 0.0
    t_mp_queue_send_ms: float = 0.0
    t_mp_queue_receive_ms: float = 0.0
    t_grpc_serialize_ms: float = 0.0
    t_grpc_deserialize_ms: float = 0.0
    t_scheduler_ms: float = 0.0
    total_ms: float = 0.0
    total_tokens: int = 0
    real_tokens: int = 0
    padded_tokens: int = 0
    padding_ratio: float = 0.0
    max_seq_length: int = 0
    avg_seq_length: float = 0.0
    batch_size: int = 0
    worker_id: int = -1
    tokenizer_worker_id: int = -1
    status_code: int = 200


@dataclass
class TokenizedBatch:
    features: dict[str, torch.Tensor]
    batch_size: int
    max_seq_length: int
    total_tokens: int
    real_tokens: int
    padded_tokens: int
    padding_ratio: float
    avg_seq_length: float
    tokenize_time_ms: float
    overhead_ms: float = 0.0


@dataclass
class WorkItem:
    req_id: int
    tokenized_batch: TokenizedBatch


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
