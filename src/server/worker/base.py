import logging
import os
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


def setup_worker_environment(tokenizers_parallelism: bool = False) -> None:
    os.environ["TOKENIZERS_PARALLELISM"] = "true" if tokenizers_parallelism else "false"


def get_worker_gpu_memory() -> float:
    try:
        import torch

        if torch.backends.mps.is_available():
            mem = torch.mps.driver_allocated_memory() / (1024 * 1024)
            return mem if mem > 0 else torch.mps.current_allocated_memory() / (1024 * 1024)
    except Exception:
        pass
    return 0.0


class BaseWorker(ABC, Generic[T, R]):
    def __init__(self, worker_id: int, worker_type: str = "generic"):
        self.worker_id = worker_id
        self.worker_type = worker_type
        self._is_initialized = False
        self._metrics = None
        self._setup_metrics()

    def _setup_metrics(self) -> None:
        from src.server.worker.metrics import WorkerMetricsCollector

        self._metrics = WorkerMetricsCollector(self.worker_id, self.worker_type)

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def process(self, work_item: T) -> R:
        raise NotImplementedError

    @abstractmethod
    def get_memory_mb(self) -> float:
        raise NotImplementedError

    def _record_metrics(self, latency_ms: float, **kwargs) -> None:
        if not self._metrics:
            return
        self._metrics.record_latency(latency_ms / 1000.0)
        self._metrics.record_request(kwargs.get("num_queries", 1))
        if "total_tokens" in kwargs:
            self._metrics.record_tokens(kwargs["total_tokens"])

    def get_metrics(self) -> dict:
        return (
            self._metrics.get_metrics()
            if self._metrics
            else {"worker_id": self.worker_id, "query_count": 0}
        )

    def is_ready(self) -> bool:
        return self._is_initialized

    def set_ready(self) -> None:
        self._is_initialized = True


__all__ = ["BaseWorker", "setup_worker_environment", "get_worker_gpu_memory", "T", "R"]
