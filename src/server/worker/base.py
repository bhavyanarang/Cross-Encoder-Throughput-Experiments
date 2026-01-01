import logging
import time
from abc import ABC, abstractmethod
from collections import deque
from typing import Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


def setup_worker_environment() -> None:
    import os

    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


def get_worker_gpu_memory() -> float:
    try:
        import torch

        if torch.backends.mps.is_available():
            driver_mem = torch.mps.driver_allocated_memory() / (1024 * 1024)
            if driver_mem > 0:
                return driver_mem

            current_mem = torch.mps.current_allocated_memory() / (1024 * 1024)
            if current_mem > 0:
                return current_mem
    except Exception as e:
        logger.error(f"Error getting GPU memory in worker: {e}")
    return 0.0


class BaseWorker(ABC, Generic[T, R]):
    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self._is_initialized = False

        self._latencies: list[float] = []
        self._request_count = 0
        self._query_count = 0
        self._start_time = time.time()

        self._query_timestamps: deque = deque(maxlen=2000)
        self._last_throughput_window_start: float = time.time()
        self._last_throughput_query_count: int = 0
        self._last_throughput_qps: float = 0.0

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def process(self, work_item: T) -> R:
        pass

    @abstractmethod
    def get_memory_mb(self) -> float:
        pass

    def _record_metrics(self, latency_ms: float, **kwargs) -> None:
        self._latencies.append(latency_ms)
        self._request_count += 1

        num_queries = kwargs.get("num_queries", 1)
        self._query_count += num_queries

        current_time = time.time()
        for _ in range(num_queries):
            self._query_timestamps.append(current_time)

        self._record_additional_metrics(latency_ms, **kwargs)

    def _record_additional_metrics(self, latency_ms: float, **kwargs) -> None:
        pass

    def get_metrics_stats(self) -> dict:
        from src.server.services.metrics_service import compute_latency_stats

        elapsed = time.time() - self._start_time
        latency_stats = compute_latency_stats(self._latencies)
        throughput_qps = self._calculate_throughput_qps()

        stats = {
            "worker_id": self.worker_id,
            **latency_stats,
            "request_count": self._request_count,
            "query_count": self._query_count,
            "uptime_seconds": elapsed,
            "throughput_qps": throughput_qps,
        }

        additional_stats = self._get_additional_stats(elapsed)
        stats.update(additional_stats)

        return stats

    def _get_additional_stats(self, elapsed: float) -> dict:
        return {}

    def _calculate_throughput_qps(self) -> float:
        current_time = time.time()
        window_seconds = 1.0
        window_start = current_time - window_seconds

        while self._query_timestamps and self._query_timestamps[0] < window_start:
            self._query_timestamps.popleft()

        queries_in_window = len(self._query_timestamps)
        instantaneous_throughput = queries_in_window / window_seconds if window_seconds > 0 else 0

        if queries_in_window == 0 or (queries_in_window < 10 and self._query_count > 100):
            query_count = self._query_count

            time_since_last = current_time - self._last_throughput_window_start

            if time_since_last > 0 and query_count > 0:
                if self._last_throughput_query_count == 0:
                    self._last_throughput_query_count = query_count
                    self._last_throughput_window_start = current_time
                    elapsed = current_time - self._start_time
                    if elapsed > 0:
                        avg_throughput = query_count / elapsed
                        self._last_throughput_qps = avg_throughput
                        return avg_throughput
                    return 0.0

                queries_since_last = query_count - self._last_throughput_query_count
                if queries_since_last > 0:
                    rate_based_throughput = queries_since_last / time_since_last
                    alpha = 0.3
                    instantaneous_throughput = (
                        alpha * rate_based_throughput + (1 - alpha) * self._last_throughput_qps
                    )

                self._last_throughput_window_start = current_time
                self._last_throughput_query_count = query_count

        if instantaneous_throughput > 0:
            alpha = 0.5
            self._last_throughput_qps = (
                alpha * instantaneous_throughput + (1 - alpha) * self._last_throughput_qps
            )
            return self._last_throughput_qps

        return instantaneous_throughput

    def reset_metrics(self) -> None:
        self._latencies = []
        self._request_count = 0
        self._query_count = 0
        self._start_time = time.time()
        self._query_timestamps.clear()
        self._last_throughput_window_start = time.time()
        self._last_throughput_query_count = 0
        self._last_throughput_qps = 0.0
        self._reset_additional_metrics()

    def _reset_additional_metrics(self) -> None:
        pass

    def is_ready(self) -> bool:
        return self._is_initialized

    def set_ready(self) -> None:
        self._is_initialized = True


__all__ = [
    "BaseWorker",
    "setup_worker_environment",
    "get_worker_gpu_memory",
    "T",
    "R",
]
