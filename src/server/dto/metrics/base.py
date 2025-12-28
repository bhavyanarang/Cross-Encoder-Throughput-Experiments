import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.server.dto.metrics.utils import compute_latency_stats


@dataclass
class BaseWorkerMetrics(ABC):
    worker_id: int
    latencies: list = field(default_factory=list)
    request_count: int = 0
    start_time: float = field(default_factory=time.time)

    def record(self, latency_ms: float, **kwargs) -> None:
        self.latencies.append(latency_ms)
        self.request_count += 1
        self._record_additional(latency_ms, **kwargs)

    @abstractmethod
    def _record_additional(self, latency_ms: float, **kwargs) -> None:
        pass

    def get_stats(self) -> dict:
        stats = compute_latency_stats(self.latencies)
        elapsed = time.time() - self.start_time
        return {
            "worker_id": self.worker_id,
            **stats,
            "request_count": self.request_count,
            **self._get_additional_stats(elapsed),
        }

    @abstractmethod
    def _get_additional_stats(self, elapsed: float) -> dict:
        pass

    def reset(self) -> None:
        self.latencies = []
        self.request_count = 0
        self.start_time = time.time()
        self._reset_additional()

    @abstractmethod
    def _reset_additional(self) -> None:
        pass
