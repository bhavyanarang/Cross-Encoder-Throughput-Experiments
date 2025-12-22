import time
import threading
from queue import Queue, Empty
from typing import Tuple
import numpy as np

from backends import BaseBackend
from metrics import MetricsCollector


class Scheduler:
    def __init__(
        self,
        backend: BaseBackend,
        metrics: MetricsCollector,
        batching_enabled: bool = False,
        max_batch_size: int = 8,
        timeout_ms: float = 100,
        enable_stage_timing: bool = True,  # Enable per-stage timing
    ):
        self.backend = backend
        self.metrics = metrics
        self.batching_enabled = batching_enabled
        self.max_batch_size = max_batch_size
        self.timeout_ms = timeout_ms
        self.enable_stage_timing = enable_stage_timing

    def schedule(self, pairs: list[tuple[str, str]]) -> Tuple[np.ndarray, float]:
        """
        Schedule cross-encoder inference for query-document pairs.
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            Tuple of (scores array, latency in ms)
        """
        start = time.perf_counter()
        
        if self.enable_stage_timing and hasattr(self.backend, 'infer_with_timing'):
            # Use timing-aware inference for bottleneck analysis
            result = self.backend.infer_with_timing(pairs)
            scores = result.scores
            elapsed_ms = result.total_ms
            
            # Record stage timings
            self.metrics.record_stage_timings(
                t_tokenize=result.t_tokenize_ms,
                t_model_inference=result.t_model_inference_ms,
            )
        else:
            # Fallback to standard inference
            scores = self.backend.infer(pairs)
            elapsed_ms = (time.perf_counter() - start) * 1000
        
        self.metrics.record(elapsed_ms, num_queries=len(pairs))
        return scores, elapsed_ms
