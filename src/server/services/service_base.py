import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseService(ABC):
    def __init__(self):
        self._is_started = False

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @property
    def is_started(self) -> bool:
        return self._is_started


class PoolBasedService(BaseService):
    def __init__(self, pool):
        super().__init__()
        self._pool = pool

    def start(self) -> None:
        if not self._pool.is_loaded:
            self._pool.start()
        self._is_started = True
        logger.info(f"{self.__class__.__name__} started")

    def stop(self) -> None:
        self._is_started = False
        logger.info(f"{self.__class__.__name__} stopped")


__all__ = ["BaseService", "PoolBasedService"]
