"""
Padding Analyzer - Tracks padding waste across batches.
"""

import threading
from dataclasses import dataclass, field

import numpy as np


@dataclass
class PaddingStats:
    """Statistics for padding analysis."""
    avg_padding_pct: float = 0.0
    p50_padding_pct: float = 0.0
    p95_padding_pct: float = 0.0
    total_wasted_compute_pct: float = 0.0
    last_padding_pct: float = 0.0
    avg_max_seq_length: int = 0
    avg_avg_seq_length: float = 0.0
    last_max_seq_length: int = 0
    last_avg_seq_length: float = 0.0


@dataclass
class PaddingAnalyzer:
    """
    Tracks padding waste across batches.
    
    Measures how much computation is wasted on padding tokens
    due to variable-length sequences in batches.
    
    Thread-safe: all operations use internal locking.
    """
    
    padding_ratios: list = field(default_factory=list)
    padded_tokens_total: int = 0
    real_tokens_total: int = 0
    max_seq_lengths: list = field(default_factory=list)
    avg_seq_lengths: list = field(default_factory=list)
    last_padding_ratio: float = 0.0
    last_max_seq_length: int = 0
    last_avg_seq_length: float = 0.0
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    def record_batch(
        self,
        padding_ratio: float = 0.0,
        padded_tokens: int = 0,
        total_tokens: int = 0,
        max_seq_length: int = 0,
        avg_seq_length: float = 0.0,
    ) -> None:
        """
        Record padding statistics for a batch.
        
        Args:
            padding_ratio: Fraction of tokens that are padding (0-1)
            padded_tokens: Number of padding tokens in batch
            total_tokens: Total tokens in batch (including padding)
            max_seq_length: Longest sequence in batch
            avg_seq_length: Average sequence length before padding
        """
        with self._lock:
            if padding_ratio > 0:
                self.padding_ratios.append(padding_ratio)
                self.last_padding_ratio = padding_ratio
            
            if padded_tokens > 0:
                self.padded_tokens_total += padded_tokens
                real_tokens = total_tokens - padded_tokens
                self.real_tokens_total += real_tokens
            
            if max_seq_length > 0:
                self.max_seq_lengths.append(max_seq_length)
                self.last_max_seq_length = max_seq_length
            
            if avg_seq_length > 0:
                self.avg_seq_lengths.append(avg_seq_length)
                self.last_avg_seq_length = avg_seq_length
    
    def get_stats(self) -> PaddingStats:
        """
        Get padding analysis statistics.
        
        Returns:
            PaddingStats with averages, percentiles, and waste metrics
        """
        with self._lock:
            if not self.padding_ratios:
                return PaddingStats()
            
            arr = np.array(self.padding_ratios) * 100  # Convert to percentage
            
            total_all_tokens = self.padded_tokens_total + self.real_tokens_total
            total_wasted_pct = (
                self.padded_tokens_total / total_all_tokens * 100
            ) if total_all_tokens > 0 else 0.0
            
            return PaddingStats(
                avg_padding_pct=round(float(np.mean(arr)), 1),
                p50_padding_pct=round(float(np.percentile(arr, 50)), 1),
                p95_padding_pct=round(float(np.percentile(arr, 95)), 1),
                total_wasted_compute_pct=round(total_wasted_pct, 1),
                last_padding_pct=round(self.last_padding_ratio * 100, 1),
                avg_max_seq_length=int(np.mean(self.max_seq_lengths)) if self.max_seq_lengths else 0,
                avg_avg_seq_length=round(float(np.mean(self.avg_seq_lengths)), 1) if self.avg_seq_lengths else 0.0,
                last_max_seq_length=self.last_max_seq_length,
                last_avg_seq_length=round(self.last_avg_seq_length, 1),
            )
    
    def reset(self) -> None:
        """Reset all padding measurements."""
        with self._lock:
            self.padding_ratios = []
            self.padded_tokens_total = 0
            self.real_tokens_total = 0
            self.max_seq_lengths = []
            self.avg_seq_lengths = []
            self.last_padding_ratio = 0.0
            self.last_max_seq_length = 0
            self.last_avg_seq_length = 0.0


__all__ = ["PaddingAnalyzer", "PaddingStats"]

