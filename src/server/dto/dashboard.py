import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class DashboardMetrics:
    """
    DEPRECATED: Use Prometheus queries in Grafana instead.

    This class is kept for backward compatibility only.
    All metrics are now exposed via Prometheus at /metrics endpoint.

    Use Prometheus queries like:
    - histogram_quantile(0.95, request_latency_seconds)
    - rate(request_count_total[1m])
    - gpu_memory_mb
    """

    gpu_memory_mb: list = field(default_factory=list)
    gpu_utilization_pct: list = field(default_factory=list)
    cpu_percent: list = field(default_factory=list)
    latencies: list = field(default_factory=list)
    throughput: list = field(default_factory=list)
    tokenize_ms: list = field(default_factory=list)
    inference_ms: list = field(default_factory=list)
    queue_wait_ms: list = field(default_factory=list)
    tokenizer_queue_wait_ms: list = field(default_factory=list)
    model_queue_wait_ms: list = field(default_factory=list)
    tokenizer_queue_size: list = field(default_factory=list)
    model_queue_size: list = field(default_factory=list)
    batch_queue_size: list = field(default_factory=list)
    padding_pct: list = field(default_factory=list)
    overhead_ms: list = field(default_factory=list)
    worker_stats: list = field(default_factory=list)
    stage_percentages: dict = field(default_factory=dict)
    tokenizer_throughput_qps: list = field(default_factory=list)
    inference_throughput_qps: list = field(default_factory=list)
    overall_throughput_qps: list = field(default_factory=list)

    def get_summary(self) -> dict:
        """
        DEPRECATED: Use Prometheus queries in Grafana instead.

        This method is kept for backward compatibility only.
        All metric aggregation should be done via Prometheus queries.
        """
        logger.warning(
            "DashboardMetrics.get_summary() is deprecated. Use Prometheus queries instead."
        )
        return {}
