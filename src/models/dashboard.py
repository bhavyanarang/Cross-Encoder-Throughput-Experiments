"""Dashboard models."""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class DashboardHistory:
    """Container for dashboard history data."""

    timestamps: list = field(default_factory=list)
    latencies: list = field(default_factory=list)
    throughput: list = field(default_factory=list)
    queries: list = field(default_factory=list)
    cpu_percent: list = field(default_factory=list)
    gpu_memory_mb: list = field(default_factory=list)
    gpu_utilization_pct: list = field(default_factory=list)
    queue_wait_ms: list = field(default_factory=list)
    tokenize_ms: list = field(default_factory=list)
    inference_ms: list = field(default_factory=list)
    padding_pct: list = field(default_factory=list)
    overhead_ms: list = field(default_factory=list)  # Tokenizer pool overhead
    tokenizer_worker_latencies: list = field(default_factory=list)
    tokenizer_worker_requests: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "timestamps": self.timestamps.copy(),
            "latencies": self.latencies.copy(),
            "throughput": self.throughput.copy(),
            "queries": self.queries.copy(),
            "cpu_percent": self.cpu_percent.copy(),
            "gpu_memory_mb": self.gpu_memory_mb.copy(),
            "gpu_utilization_pct": self.gpu_utilization_pct.copy(),
            "queue_wait_ms": self.queue_wait_ms.copy(),
            "tokenize_ms": self.tokenize_ms.copy(),
            "inference_ms": self.inference_ms.copy(),
            "padding_pct": self.padding_pct.copy(),
            "overhead_ms": self.overhead_ms.copy(),
            "tokenizer_worker_latencies": self.tokenizer_worker_latencies.copy(),
            "tokenizer_worker_requests": self.tokenizer_worker_requests.copy(),
        }

    def reset(self):
        self.timestamps.clear()
        self.latencies.clear()
        self.throughput.clear()
        self.queries.clear()
        self.cpu_percent.clear()
        self.gpu_memory_mb.clear()
        self.gpu_utilization_pct.clear()
        self.queue_wait_ms.clear()
        self.tokenize_ms.clear()
        self.inference_ms.clear()
        self.padding_pct.clear()
        self.overhead_ms.clear()
        self.tokenizer_worker_latencies.clear()
        self.tokenizer_worker_requests.clear()


@dataclass
class DashboardMetrics:
    """Container for dashboard metrics collected during experiment."""

    gpu_memory_mb: list = field(default_factory=list)
    gpu_utilization_pct: list = field(default_factory=list)
    cpu_percent: list = field(default_factory=list)
    latencies: list = field(default_factory=list)
    throughput: list = field(default_factory=list)
    tokenize_ms: list = field(default_factory=list)
    inference_ms: list = field(default_factory=list)
    queue_wait_ms: list = field(default_factory=list)
    padding_pct: list = field(default_factory=list)
    overhead_ms: list = field(default_factory=list)  # Tokenizer pool overhead
    worker_stats: list = field(default_factory=list)  # Per-worker/per-model stats
    stage_percentages: dict = field(default_factory=dict)  # Stage breakdown percentages

    def get_summary(self) -> dict:
        """Get summary statistics for all metrics."""

        def stats(arr):
            if not arr:
                return {"avg": 0, "min": 0, "max": 0, "p50": 0, "p95": 0}
            a = np.array(arr)
            return {
                "avg": float(np.mean(a)),
                "min": float(np.min(a)),
                "max": float(np.max(a)),
                "p50": float(np.percentile(a, 50)),
                "p95": float(np.percentile(a, 95)),
            }

        return {
            "gpu_memory_mb": stats(self.gpu_memory_mb),
            "gpu_utilization_pct": stats(self.gpu_utilization_pct),
            "cpu_percent": stats(self.cpu_percent),
            "tokenize_ms": stats(self.tokenize_ms),
            "inference_ms": stats(self.inference_ms),
            "queue_wait_ms": stats(self.queue_wait_ms),
            "padding_pct": stats(self.padding_pct),
            "overhead_ms": stats(self.overhead_ms),
        }
