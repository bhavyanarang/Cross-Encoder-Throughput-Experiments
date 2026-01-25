from prometheus_client import REGISTRY, Counter, Histogram


def _get_counter(name: str, description: str, labels: list[str]) -> Counter:
    existing = REGISTRY._names_to_collectors.get(name)
    if existing:
        return existing
    return Counter(name, description, labelnames=labels)


def _get_histogram(
    name: str, description: str, labels: list[str], buckets: list[float]
) -> Histogram:
    existing = REGISTRY._names_to_collectors.get(name)
    if existing:
        return existing
    return Histogram(name, description, labelnames=labels, buckets=buckets)


WORKER_LATENCY = _get_histogram(
    "worker_latency_seconds",
    "Worker processing latency",
    ["worker_id", "worker_type"],
    [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)
WORKER_REQUESTS = _get_counter(
    "worker_requests_total",
    "Total requests processed",
    ["worker_id", "worker_type"],
)
WORKER_QUERIES = _get_counter(
    "worker_queries_total",
    "Total queries processed",
    ["worker_id", "worker_type"],
)
WORKER_TOKENS = _get_counter(
    "worker_tokens_total",
    "Total tokens processed",
    ["worker_id", "worker_type"],
)


class WorkerMetricsCollector:
    def __init__(self, worker_id: int, worker_type: str):
        self.worker_id = worker_id
        self.worker_type = worker_type
        self._labels = {"worker_id": str(worker_id), "worker_type": worker_type}

    def record_latency(self, latency_seconds: float) -> None:
        WORKER_LATENCY.labels(**self._labels).observe(latency_seconds)

    def record_request(self, num_queries: int = 1) -> None:
        WORKER_REQUESTS.labels(**self._labels).inc(1)
        WORKER_QUERIES.labels(**self._labels).inc(num_queries)

    def record_tokens(self, num_tokens: int) -> None:
        WORKER_TOKENS.labels(**self._labels).inc(num_tokens)

    def get_metrics(self) -> dict:
        query_count = 0
        for sample in WORKER_QUERIES.collect():
            for metric in sample.samples:
                if (
                    metric.labels.get("worker_id") == self._labels["worker_id"]
                    and metric.labels.get("worker_type") == self._labels["worker_type"]
                ):
                    query_count = int(metric.value)
        return {"worker_id": self.worker_id, "query_count": query_count}


__all__ = ["WorkerMetricsCollector"]
