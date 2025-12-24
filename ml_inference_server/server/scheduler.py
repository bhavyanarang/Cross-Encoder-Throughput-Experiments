"""
Scheduler - Routes inference requests to model pool with batching support.

Handles:
- Request routing to model pool
- Length-aware batching (optional)
- Per-stage timing and metrics collection
"""

import logging
import time

import numpy as np
from metrics import MetricsCollector
from utils.length_aware_batching import LengthAwareBatcher

from .model_pool import ModelPool

logger = logging.getLogger(__name__)


class Scheduler:
    """
    Scheduler for cross-encoder inference requests.

    Routes requests to a process-based ModelPool for true parallel inference.
    """

    def __init__(
        self,
        model_pool: ModelPool,
        metrics: MetricsCollector | None = None,
        batching_enabled: bool = False,
        max_batch_size: int = 8,
        timeout_ms: float = 100,
        enable_stage_timing: bool = True,
        enable_length_aware_batching: bool = False,
    ):
        """
        Initialize scheduler.

        Args:
            model_pool: ModelPool for multi-model support (process-based)
            metrics: MetricsCollector for recording stats
            batching_enabled: Enable dynamic batching
            max_batch_size: Maximum batch size
            timeout_ms: Batch timeout in milliseconds
            enable_stage_timing: Enable per-stage timing
            enable_length_aware_batching: Sort pairs by length to reduce padding
        """
        self.model_pool = model_pool
        self.metrics = metrics or MetricsCollector()
        self.batching_enabled = batching_enabled
        self.max_batch_size = max_batch_size
        self.timeout_ms = timeout_ms
        self.enable_stage_timing = enable_stage_timing
        self.enable_length_aware_batching = enable_length_aware_batching

        if enable_length_aware_batching:
            logger.info("Length-aware batching ENABLED - pairs will be sorted by length")

    def schedule(
        self,
        pairs: list[tuple[str, str]],
        request_arrival_time: float | None = None,
    ) -> tuple[np.ndarray, float]:
        """
        Schedule cross-encoder inference for query-document pairs.

        If length_aware_batching is enabled, pairs are sorted by estimated
        token length to reduce padding waste. Scores are returned in original order.

        Args:
            pairs: List of (query, document) tuples
            request_arrival_time: Time when request arrived (for queue wait analysis)

        Returns:
            Tuple of (scores array, latency in ms)
        """
        start = time.perf_counter()

        # Calculate queue wait time
        if request_arrival_time is not None:
            queue_wait_ms = (start - request_arrival_time) * 1000
            self.metrics.record_stage_timings(t_queue_wait=queue_wait_ms)

        # Optionally apply length-aware batching
        unsort_fn = None
        if self.enable_length_aware_batching and len(pairs) > 1:
            batcher = LengthAwareBatcher(pairs)
            pairs, unsort_fn = batcher.get_sorted_pairs()

        # Run inference through model pool
        result = self.model_pool.infer_with_timing(pairs)

        scores = result.scores
        elapsed_ms = result.total_ms

        # Record stage timings
        self.metrics.record_stage_timings(
            t_tokenize=result.t_tokenize_ms,
            t_model_inference=result.t_model_inference_ms,
        )

        # Record padding statistics
        self.metrics.record_padding_stats(
            padding_ratio=result.padding_ratio,
            padded_tokens=result.padded_tokens,
            total_tokens=result.total_tokens,
            max_seq_length=result.max_seq_length,
            avg_seq_length=result.avg_seq_length,
        )

        # Restore original order if we sorted
        if unsort_fn is not None:
            scores = unsort_fn(scores)

        self.metrics.record(elapsed_ms, num_queries=len(pairs))
        return scores, elapsed_ms

    def get_info(self) -> dict:
        """Get scheduler information."""
        return {
            "batching_enabled": self.batching_enabled,
            "max_batch_size": self.max_batch_size,
            "timeout_ms": self.timeout_ms,
            "enable_stage_timing": self.enable_stage_timing,
            "enable_length_aware_batching": self.enable_length_aware_batching,
            "pool_info": self.model_pool.get_pool_info(),
        }


__all__ = ["Scheduler"]
