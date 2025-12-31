"""Tokenizer worker for tokenization tasks."""

import logging
import time

from transformers import AutoTokenizer

from src.server.dto.inference import TokenizedBatch
from src.server.dto.metrics.worker import TokenizerWorkerMetrics
from src.server.worker.base import BaseWorker, setup_worker_environment

logger = logging.getLogger(__name__)


class TokenizerService:
    def __init__(self, model_name: str, max_length: int = 512):
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._max_length = max_length
        logger.info(f"Tokenizer loaded: {model_name}")

    def tokenize(self, pairs: list[tuple[str, str]], device: str = "cpu") -> TokenizedBatch:
        start = time.perf_counter()

        texts = [[p[0], p[1]] for p in pairs]
        features = self._tokenizer(
            texts,
            padding=True,
            truncation="longest_first",
            return_tensors="pt",
            max_length=self._max_length,
        )

        mask = features["attention_mask"]
        batch_size, max_seq = mask.shape
        real_per_seq = mask.sum(dim=1)
        total_real = int(real_per_seq.sum().item())
        total_tokens = batch_size * max_seq
        padded = total_tokens - total_real

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


class TokenizerWorker(BaseWorker[list[tuple[str, str]], TokenizedBatch]):
    def __init__(self, worker_id: int, model_name: str, max_length: int = 512, metrics=None):
        if metrics is None:
            metrics = TokenizerWorkerMetrics(worker_id=worker_id)
        super().__init__(worker_id, metrics=metrics)
        self.model_name = model_name
        self.max_length = max_length
        self._tokenizer: TokenizerService | None = None

    def initialize(self) -> None:
        setup_worker_environment()
        self._tokenizer = TokenizerService(self.model_name, self.max_length)
        logger.info(f"Tokenizer worker {self.worker_id} loaded: {self.model_name}")
        self.set_ready()

    def process(self, pairs: list[tuple[str, str]]) -> TokenizedBatch:
        if not self._tokenizer:
            raise RuntimeError(f"Tokenizer worker {self.worker_id} not initialized")

        start_time = time.perf_counter()
        result = self._tokenizer.tokenize(pairs, device="cpu")
        latency_ms = (time.perf_counter() - start_time) * 1000

        self._record_metrics(
            latency_ms=latency_ms,
            total_tokens=result.total_tokens,
        )

        return result

    def get_memory_mb(self) -> float:
        return 0.0


__all__ = ["TokenizerWorker", "TokenizerService"]
