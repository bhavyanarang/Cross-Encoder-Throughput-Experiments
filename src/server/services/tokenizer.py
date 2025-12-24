"""Tokenization service - centralized tokenization for all backends."""

import logging
import time
from dataclasses import dataclass

import torch
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)


@dataclass
class TokenizedBatch:
    """Result of tokenization with padding analysis."""

    features: dict[str, torch.Tensor]
    batch_size: int
    max_seq_length: int
    total_tokens: int
    real_tokens: int
    padded_tokens: int
    padding_ratio: float
    avg_seq_length: float
    tokenize_time_ms: float


class TokenizerService:
    """Centralized tokenization service."""

    def __init__(self, model_name: str, max_length: int = 512):
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._max_length = max_length
        logger.info(f"Tokenizer loaded: {model_name}")

    def tokenize(self, pairs: list[tuple[str, str]], device: str = "cpu") -> TokenizedBatch:
        """Tokenize query-document pairs with padding analysis."""
        start = time.perf_counter()

        texts = [[p[0], p[1]] for p in pairs]
        features = self._tokenizer(
            texts,
            padding=True,
            truncation="longest_first",
            return_tensors="pt",
            max_length=self._max_length,
        )

        # Analyze padding
        mask = features["attention_mask"]
        batch_size, max_seq = mask.shape
        real_per_seq = mask.sum(dim=1)
        total_real = int(real_per_seq.sum().item())
        total_tokens = batch_size * max_seq
        padded = total_tokens - total_real

        # Move to device
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
