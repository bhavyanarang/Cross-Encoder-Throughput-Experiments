import logging
import queue
import threading
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


class BaseWorkerPool(ABC, Generic[T, R]):
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self._is_started = False
        self._inference_queue: queue.Queue | None = None
        self._shutdown_event = threading.Event()
        self._workers: list = []

    @abstractmethod
    def start(self, timeout_s: float = 120.0) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self, timeout_s: float = 30.0) -> None:
        raise NotImplementedError

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

    def get_worker_metrics(self) -> list[dict]:
        metrics_list = []
        for i in range(self.num_workers):
            try:
                metrics = self.get_worker_metrics_by_id(i)
                metrics_list.append(metrics if metrics else {})
            except Exception as e:
                logger.debug(f"Failed to get metrics for worker {i}: {e}")
                metrics_list.append({})
        return metrics_list

    @abstractmethod
    def get_worker_metrics_by_id(self, worker_id: int) -> dict:
        raise NotImplementedError

    def get_aggregate_throughput_qps(self) -> float:
        worker_metrics = self.get_worker_metrics()
        if not worker_metrics:
            return 0.0

        total_throughput = sum(ws.get("throughput_qps", 0) for ws in worker_metrics)
        return total_throughput

    def __len__(self) -> int:
        return self.num_workers
