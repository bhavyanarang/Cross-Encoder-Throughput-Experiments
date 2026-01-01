import logging
import time

from transformers import AutoTokenizer

from src.server.dto.inference import TokenizedBatch

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
