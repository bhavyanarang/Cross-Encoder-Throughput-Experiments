import logging

from prometheus_client import Counter, Gauge, Histogram

logger = logging.getLogger(__name__)


class WorkerMetricsCollector:
    def __init__(self, worker_id: int, worker_type: str):
        self.worker_id = worker_id
        self.worker_type = worker_type

        self.latency_histogram = Histogram(
            "worker_latency_seconds",
            "Worker processing latency",
            labelnames=["worker_id", "worker_type"],
            buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
        )

        self.request_counter = Counter(
            "worker_requests_total",
            "Total number of requests processed",
            labelnames=["worker_id", "worker_type"],
        )

        self.query_counter = Counter(
            "worker_queries_total",
            "Total number of queries processed",
            labelnames=["worker_id", "worker_type"],
        )

        self.total_latency_counter = Counter(
            "worker_total_latency_seconds",
            "Total cumulative latency in seconds",
            labelnames=["worker_id", "worker_type"],
        )

        self.throughput_gauge = Gauge(
            "worker_throughput_qps",
            "Worker throughput in queries per second",
            labelnames=["worker_id", "worker_type"],
        )

        self.tokens_counter = Counter(
            "worker_tokens_total",
            "Total tokens processed (for tokenizer workers)",
            labelnames=["worker_id", "worker_type"],
        )

    def record_latency(self, latency_seconds: float) -> None:
        try:
            labels = {"worker_id": str(self.worker_id), "worker_type": self.worker_type}
            self.latency_histogram.labels(**labels).observe(latency_seconds)
            self.total_latency_counter.labels(**labels).inc(latency_seconds)
        except Exception as e:
            logger.warning(f"Failed to record latency metric: {e}")

    def record_request(self, num_queries: int = 1) -> None:
        try:
            labels = {"worker_id": str(self.worker_id), "worker_type": self.worker_type}
            self.request_counter.labels(**labels).inc(1)
            self.query_counter.labels(**labels).inc(num_queries)
        except Exception as e:
            logger.warning(f"Failed to record request metric: {e}")

    def record_throughput(self, throughput_qps: float) -> None:
        try:
            labels = {"worker_id": str(self.worker_id), "worker_type": self.worker_type}
            self.throughput_gauge.labels(**labels).set(throughput_qps)
        except Exception as e:
            logger.warning(f"Failed to record throughput metric: {e}")

    def record_tokens(self, num_tokens: int) -> None:
        try:
            labels = {"worker_id": str(self.worker_id), "worker_type": self.worker_type}
            self.tokens_counter.labels(**labels).inc(num_tokens)
        except Exception as e:
            logger.warning(f"Failed to record tokens metric: {e}")

    def get_metrics(self) -> dict:
        try:
            (str(self.worker_id), self.worker_type)

            request_count = 0
            query_count = 0
            total_latency_ms = 0.0

            for sample in self.request_counter.collect():
                for metric in sample.samples:
                    if (
                        metric.labels.get("worker_id") == str(self.worker_id)
                        and metric.labels.get("worker_type") == self.worker_type
                    ):
                        request_count = int(metric.value)

            for sample in self.query_counter.collect():
                for metric in sample.samples:
                    if (
                        metric.labels.get("worker_id") == str(self.worker_id)
                        and metric.labels.get("worker_type") == self.worker_type
                    ):
                        query_count = int(metric.value)

            for sample in self.total_latency_counter.collect():
                for metric in sample.samples:
                    if (
                        metric.labels.get("worker_id") == str(self.worker_id)
                        and metric.labels.get("worker_type") == self.worker_type
                    ):
                        total_latency_ms = metric.value * 1000.0

            avg_ms = (total_latency_ms / request_count) if request_count > 0 else 0.0
            throughput_qps = (
                (query_count / (total_latency_ms / 1000.0)) if total_latency_ms > 0 else 0.0
            )

            return {
                "worker_id": self.worker_id,
                "avg_ms": avg_ms,
                "query_count": query_count,
                "throughput_qps": throughput_qps,
            }
        except Exception as e:
            logger.warning(f"Failed to get metrics: {e}")
            return {
                "worker_id": self.worker_id,
                "avg_ms": 0.0,
                "query_count": 0,
                "throughput_qps": 0.0,
            }


__all__ = ["WorkerMetricsCollector"]
