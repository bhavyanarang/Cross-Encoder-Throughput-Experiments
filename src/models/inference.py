"""Inference DTOs."""

from dataclasses import dataclass

import numpy as np


@dataclass
class InferenceResult:
    scores: np.ndarray
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
    worker_id: int = -1


@dataclass
class WorkItem:
    req_id: int
    pairs: list[tuple[str, str]]


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
