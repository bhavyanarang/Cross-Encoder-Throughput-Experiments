"""Base worker pool class for managing pools of workers."""

import queue
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class BaseWorkerPool(ABC, Generic[T, R]):
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self._is_started = False
        self._inference_queue: queue.Queue | None = None

    @abstractmethod
    def start(self, timeout_s: float = 120.0) -> None:
        pass

    @abstractmethod
    def stop(self, timeout_s: float = 30.0) -> None:
        pass

    @abstractmethod
    def get_worker_metrics(self) -> list[dict]:
        pass

    def submit(self, work_item: T) -> R:
        if not self._is_started:
            raise RuntimeError(f"{self.__class__.__name__} not started")
        raise NotImplementedError("Subclass must implement submit() or override with custom logic")

    def set_inference_queue(self, inference_queue: queue.Queue) -> None:
        self._inference_queue = inference_queue

    @property
    def is_loaded(self) -> bool:
        return self._is_started

    def get_info(self) -> dict:
        return {
            "num_workers": self.num_workers,
            "is_loaded": self._is_started,
        }

    def get_worker_metrics_by_id(self, worker_id: int) -> dict:
        if not self._is_started or worker_id >= self.num_workers:
            return {}

        all_metrics = self.get_worker_metrics()
        if worker_id < len(all_metrics):
            return all_metrics[worker_id]
        return {}

    def reset_worker_metrics(self) -> None:
        pass

    def get_aggregate_throughput_qps(self) -> float:
        worker_metrics = self.get_worker_metrics()
        if not worker_metrics:
            return 0.0

        total_throughput = sum(ws.get("throughput_qps", 0) for ws in worker_metrics)
        return total_throughput

    def __len__(self) -> int:
        return self.num_workers


__all__ = [
    "BaseWorkerPool",
    "T",
    "R",
]
