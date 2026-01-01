import logging
import time
from collections import deque

from transformers import AutoTokenizer

from src.server.dto.inference import TokenizedBatch
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
    def __init__(self, worker_id: int, model_name: str, max_length: int = 512):
        super().__init__(worker_id)
        self.model_name = model_name
        self.max_length = max_length
        self._tokenizer: TokenizerService | None = None
        self._token_timestamps: deque = deque(maxlen=100)
        self._last_token_throughput_window_start: float = time.time()
        self._last_token_count: int = 0
        self._total_tokens_processed: int = 0

    def _record_additional_metrics(self, latency_ms: float, **kwargs) -> None:
        total_tokens = kwargs.get("total_tokens", 0)
        if total_tokens > 0:
            self._total_tokens_processed += total_tokens
            current_time = time.time()
            self._token_timestamps.append((current_time, total_tokens))

    def _get_additional_stats(self, elapsed: float) -> dict:
        return {
            "total_tokens_processed": self._total_tokens_processed,
        }

    def _reset_additional_metrics(self) -> None:
        self._total_tokens_processed = 0
        self._token_timestamps.clear()
        self._last_token_throughput_window_start = time.time()
        self._last_token_count = 0

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
            num_queries=len(pairs),
        )

        return result

    def get_memory_mb(self) -> float:
        return 0.0

    def get_metrics_stats(self) -> dict:
        stats = super().get_metrics_stats()
        token_throughput_tps = self._calculate_token_throughput_tps()
        stats.update(
            {
                "throughput_tokens_per_sec": token_throughput_tps,
                "total_tokens_processed": self._total_tokens_processed,
            }
        )
        return stats

    def _calculate_token_throughput_tps(self) -> float:
        current_time = time.time()
        window_seconds = 1.0
        window_start = current_time - window_seconds

        tokens_in_window = sum(
            tokens for ts, tokens in self._token_timestamps if ts >= window_start
        )
        instantaneous_token_throughput = (
            tokens_in_window / window_seconds if window_seconds > 0 else 0
        )

        if tokens_in_window == 0 and len(self._token_timestamps) > 0:
            time_since_last = current_time - self._last_token_throughput_window_start
            if time_since_last > 0:
                tokens_since_last = self._total_tokens_processed - self._last_token_count
                instantaneous_token_throughput = tokens_since_last / time_since_last
                self._last_token_throughput_window_start = current_time
                self._last_token_count = self._total_tokens_processed

        return instantaneous_token_throughput


__all__ = ["TokenizerWorker", "TokenizerService"]
