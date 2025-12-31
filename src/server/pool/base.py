"""Base worker pool class for managing pools of workers."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


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
    "BaseWorkerPool",
    "T",
    "R",
]
