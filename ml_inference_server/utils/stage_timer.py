"""
Stage Timer - Utilities for measuring per-stage latencies in the inference pipeline.

Measures:
- t_grpc_receive: Time to deserialize gRPC request
- t_tokenize: Time to tokenize (query, doc) pairs
- t_queue_wait: Time request waits in batch queue
- t_model_inference: GPU forward pass time
- t_grpc_send: Time to serialize + send gRPC response
"""

import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class StageTimings:
    """Container for timing measurements of a single request."""

    t_grpc_receive: float = 0.0
    t_tokenize: float = 0.0
    t_queue_wait: float = 0.0
    t_model_inference: float = 0.0
    t_grpc_send: float = 0.0
    total_ms: float = 0.0
    num_pairs: int = 0

    def to_dict(self) -> dict:
        return {
            "t_grpc_receive_ms": self.t_grpc_receive,
            "t_tokenize_ms": self.t_tokenize,
            "t_queue_wait_ms": self.t_queue_wait,
            "t_model_inference_ms": self.t_model_inference,
            "t_grpc_send_ms": self.t_grpc_send,
            "total_ms": self.total_ms,
            "num_pairs": self.num_pairs,
        }

    def log_breakdown(self, sample_rate: int = 1, request_id: int = 0) -> None:
        """Log timing breakdown, optionally sampling 1-in-N requests."""
        if request_id % sample_rate != 0:
            return

        total = self.total_ms
        if total == 0:
            return

        pct_tokenize = (self.t_tokenize / total) * 100 if total > 0 else 0
        pct_inference = (self.t_model_inference / total) * 100 if total > 0 else 0
        pct_grpc = ((self.t_grpc_receive + self.t_grpc_send) / total) * 100 if total > 0 else 0
        pct_queue = (self.t_queue_wait / total) * 100 if total > 0 else 0

        logger.info(
            f"Stage breakdown ({self.num_pairs} pairs, {total:.1f}ms total): "
            f"tokenize={self.t_tokenize:.2f}ms ({pct_tokenize:.0f}%) | "
            f"inference={self.t_model_inference:.2f}ms ({pct_inference:.0f}%) | "
            f"grpc={self.t_grpc_receive + self.t_grpc_send:.2f}ms ({pct_grpc:.0f}%) | "
            f"queue={self.t_queue_wait:.2f}ms ({pct_queue:.0f}%)"
        )


class StageTimer:
    """
    Context manager for timing individual stages of the inference pipeline.

    Usage:
        timer = StageTimer()

        with timer.stage("grpc_receive"):
            # deserialize request

        with timer.stage("tokenize"):
            # tokenize pairs

        timings = timer.get_timings()
    """

    def __init__(self):
        self._start_time = time.perf_counter()
        self._timings = StageTimings()
        self._stage_starts: dict[str, float] = {}

    @contextmanager
    def stage(self, name: str):
        """Time a named stage."""
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self._record_stage(name, elapsed_ms)

    def _record_stage(self, name: str, elapsed_ms: float) -> None:
        """Record timing for a stage."""
        if name == "grpc_receive":
            self._timings.t_grpc_receive = elapsed_ms
        elif name == "tokenize":
            self._timings.t_tokenize = elapsed_ms
        elif name == "queue_wait":
            self._timings.t_queue_wait = elapsed_ms
        elif name == "model_inference":
            self._timings.t_model_inference = elapsed_ms
        elif name == "grpc_send":
            self._timings.t_grpc_send = elapsed_ms

    def set_num_pairs(self, num_pairs: int) -> None:
        """Set the number of pairs processed."""
        self._timings.num_pairs = num_pairs

    def finalize(self) -> StageTimings:
        """Finalize and return the timings."""
        self._timings.total_ms = (time.perf_counter() - self._start_time) * 1000
        return self._timings

    def get_timings(self) -> StageTimings:
        """Get current timings (alias for finalize)."""
        return self.finalize()


# Simple timing decorator for functions
def timed_stage(stage_name: str):
    """Decorator to time a function as a named stage."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - start) * 1000
            return result, elapsed_ms

        return wrapper

    return decorator
