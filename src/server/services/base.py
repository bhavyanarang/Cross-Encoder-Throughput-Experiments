import logging
import os
import time
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


def setup_worker_environment() -> None:
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
    def __init__(self, worker_id: int, metrics: object | None = None):
        self.worker_id = worker_id
        self._is_initialized = False
        self._metrics = metrics
        self._request_count = 0
        self._start_time = time.time()

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
        if self._metrics and hasattr(self._metrics, "record"):
            try:
                self._metrics.record(latency_ms, **kwargs)
            except Exception as e:
                logger.warning(f"Failed to record metrics for worker {self.worker_id}: {e}")
        self._request_count += 1

    def get_metrics_stats(self) -> dict:
        if self._metrics and hasattr(self._metrics, "get_stats"):
            try:
                return self._metrics.get_stats()
            except Exception as e:
                logger.warning(f"Failed to get metrics stats for worker {self.worker_id}: {e}")
        return {
            "worker_id": self.worker_id,
            "request_count": self._request_count,
            "uptime_seconds": time.time() - self._start_time,
        }

    def reset_metrics(self) -> None:
        if self._metrics and hasattr(self._metrics, "reset"):
            try:
                self._metrics.reset()
            except Exception as e:
                logger.warning(f"Failed to reset metrics for worker {self.worker_id}: {e}")
        self._request_count = 0
        self._start_time = time.time()

    def is_ready(self) -> bool:
        return self._is_initialized

    def set_ready(self) -> None:
        self._is_initialized = True


class BaseWorkerPool(ABC, Generic[T, R]):
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self._is_started = False

    @abstractmethod
    def start(self, timeout_s: float = 120.0) -> None:
        pass

    @abstractmethod
    def stop(self, timeout_s: float = 30.0) -> None:
        pass

    @abstractmethod
    def submit(self, work_item: T) -> R:
        pass

    @property
    def is_loaded(self) -> bool:
        return self._is_started

    def get_info(self) -> dict:
        return {
            "num_workers": self.num_workers,
            "is_loaded": self._is_started,
        }


__all__ = [
    "BaseWorker",
    "BaseWorkerPool",
    "setup_worker_environment",
    "get_worker_gpu_memory",
    "T",
    "R",
]
