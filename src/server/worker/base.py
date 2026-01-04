import logging
from abc import ABC, abstractmethod
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
    def __init__(self, worker_id: int, worker_type: str = "generic"):
        self.worker_id = worker_id
        self.worker_type = worker_type
        self._is_initialized = False

        self._prometheus_metrics: object | None = None
        self._setup_prometheus_metrics()

    def _setup_prometheus_metrics(self) -> None:
        try:
            from src.server.worker.metrics import WorkerMetricsCollector

            self._prometheus_metrics = WorkerMetricsCollector(self.worker_id, self.worker_type)
        except Exception as e:
            logger.warning(f"Failed to initialize Prometheus metrics: {e}")

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
        if not self._prometheus_metrics:
            logger.warning("Prometheus metrics not initialized")
            return

        try:
            num_queries = kwargs.get("num_queries", 1)

            self._prometheus_metrics.record_latency(latency_ms / 1000.0)
            self._prometheus_metrics.record_request(num_queries)

            if "total_tokens" in kwargs:
                self._prometheus_metrics.record_tokens(kwargs["total_tokens"])

            throughput_qps = self._prometheus_metrics.get_metrics().get("throughput_qps", 0.0)
            if throughput_qps > 0:
                self._prometheus_metrics.record_throughput(throughput_qps)
        except Exception as e:
            logger.debug(f"Failed to record Prometheus metrics: {e}")

        self._record_additional_metrics(latency_ms, **kwargs)

    def _record_additional_metrics(self, latency_ms: float, **kwargs) -> None:
        pass

    def reset_metrics(self) -> None:
        if self._prometheus_metrics:
            try:
                self._prometheus_metrics = None
                self._setup_prometheus_metrics()
            except Exception as e:
                logger.debug(f"Failed to reset metrics: {e}")

    def _reset_additional_metrics(self) -> None:
        pass

    def get_metrics(self) -> dict:
        if self._prometheus_metrics:
            try:
                return self._prometheus_metrics.get_metrics()
            except Exception as e:
                logger.debug(f"Failed to get metrics from Prometheus: {e}")

        return {
            "worker_id": self.worker_id,
            "avg_ms": 0.0,
            "query_count": 0,
            "throughput_qps": 0.0,
        }

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
