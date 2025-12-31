import numpy as np


class PaddingTracker:
    def __init__(self):
        self.ratios: list = []
        self.padded_tokens_total: int = 0
        self.real_tokens_total: int = 0
        self.max_seq_lengths: list = []
        self.avg_seq_lengths: list = []
        self.last_ratio: float = 0.0
        self.last_max_seq_length: int = 0
        self.last_avg_seq_length: float = 0.0

    def record(
        self,
        padding_ratio: float = 0.0,
        padded_tokens: int = 0,
        total_tokens: int = 0,
        max_seq_length: int = 0,
        avg_seq_length: float = 0.0,
    ) -> None:
        # Validate inputs
        if not (0.0 <= padding_ratio <= 1.0):
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Invalid padding_ratio {padding_ratio}, must be in [0.0, 1.0]")
            return
        
        if not (0 <= padded_tokens <= total_tokens):
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                f"Invalid padding tokens: padded_tokens={padded_tokens} > total_tokens={total_tokens}"
            )
            return
        
        self.ratios.append(padding_ratio)
        self.last_ratio = padding_ratio
        if padded_tokens >= 0:
            self.padded_tokens_total += padded_tokens
            self.real_tokens_total += total_tokens - padded_tokens
        if max_seq_length > 0:
            self.max_seq_lengths.append(max_seq_length)
            self.last_max_seq_length = max_seq_length
        if avg_seq_length > 0:
            self.avg_seq_lengths.append(avg_seq_length)
            self.last_avg_seq_length = avg_seq_length

    def get_stats(self) -> dict:
        if not self.ratios:
            return {
                "avg_padding_pct": 0.0,
                "last_padding_pct": 0.0,
                "last_max_seq_length": 0,
                "last_avg_seq_length": 0.0,
            }
        arr = np.array(self.ratios) * 100
        return {
            "avg_padding_pct": round(float(np.mean(arr)), 1),
            "last_padding_pct": round(self.last_ratio * 100, 1),
            "last_max_seq_length": self.last_max_seq_length,
            "last_avg_seq_length": round(self.last_avg_seq_length, 1),
        }

    def reset(self) -> None:
        self.ratios = []
        self.padded_tokens_total = 0
        self.real_tokens_total = 0
        self.max_seq_lengths = []
        self.avg_seq_lengths = []
        self.last_ratio = 0.0
        self.last_max_seq_length = 0
        self.last_avg_seq_length = 0.0
