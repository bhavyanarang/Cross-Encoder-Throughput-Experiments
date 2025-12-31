import threading
from dataclasses import dataclass

from src.server.dto.metrics.base import BaseWorkerMetrics


@dataclass
class WorkerMetrics(BaseWorkerMetrics):
    query_count: int = 0

    def _record_additional(self, latency_ms: float, num_queries: int = 1, **kwargs) -> None:
        self.query_count += num_queries

    def _get_additional_stats(self, elapsed: float) -> dict:
        return {
            "query_count": self.query_count,
            "throughput_qps": self.query_count / elapsed if elapsed > 0 else 0,
        }

    def _reset_additional(self) -> None:
        self.query_count = 0


@dataclass
class TokenizerWorkerMetrics(BaseWorkerMetrics):
    total_tokens_processed: int = 0
    query_count: int = 0

    def _record_additional(self, latency_ms: float, total_tokens: int = 0, num_queries: int = 1, **kwargs) -> None:
        self.total_tokens_processed += total_tokens
        self.query_count += num_queries

    def _get_additional_stats(self, elapsed: float) -> dict:
        return {
            "total_tokens_processed": self.total_tokens_processed,
            "throughput_tokens_per_sec": (
                self.total_tokens_processed / elapsed if elapsed > 0 else 0
            ),
            # Query throughput: accumulated query count from metrics recording
            "query_count": self.query_count,
            "throughput_qps": self.query_count / elapsed if elapsed > 0 else 0,
        }

    def _reset_additional(self) -> None:
        self.total_tokens_processed = 0
        self.query_count = 0


class WorkerStatsManager:
    def __init__(self, worker_metrics_class: type[BaseWorkerMetrics]):
        self._worker_metrics_class = worker_metrics_class
        self._stats: dict[int, BaseWorkerMetrics] = {}
        self._lock = threading.Lock()

    def get_or_create(self, worker_id: int) -> BaseWorkerMetrics:
        if worker_id not in self._stats:
            self._stats[worker_id] = self._worker_metrics_class(worker_id=worker_id)
        return self._stats[worker_id]

    def record(self, worker_id: int, latency_ms: float, **kwargs) -> None:
        with self._lock:
            worker = self.get_or_create(worker_id)
            worker.record(latency_ms, **kwargs)

    def get_all_stats(self) -> list[dict]:
        with self._lock:
            return [ws.get_stats() for ws in self._stats.values()]

    def reset_all(self) -> None:
        with self._lock:
            # Clear all worker stats and reset counters
            self._stats.clear()
