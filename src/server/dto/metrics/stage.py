import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StageMetrics:
    latencies: list = field(default_factory=list)

    def record(self, duration_ms: float) -> None:
        self.latencies.append(duration_ms)

    def reset(self) -> None:
        self.latencies = []


class StageTracker:
    def __init__(self, name: str, track_recent: bool = False, recent_maxlen: int = 200):
        self.name = name
        self.metrics = StageMetrics()
        self.last_value_ms = 0.0
        self.recent_history: Optional[deque] = deque(maxlen=recent_maxlen) if track_recent else None

    def record(self, value_ms: float, timestamp: Optional[float] = None) -> None:
        if value_ms <= 0:
            return

        self.metrics.record(value_ms)
        self.last_value_ms = value_ms
        if self.recent_history is not None and timestamp is not None:
            self.recent_history.append((timestamp, value_ms))

    def reset(self) -> None:
        self.metrics.reset()
        self.last_value_ms = 0.0
        if self.recent_history is not None:
            self.recent_history.clear()


class StageTrackerManager:
    def __init__(self):
        self._trackers: dict[str, StageTracker] = {}
        self._lock = threading.Lock()

    def register(
        self, name: str, track_recent: bool = False, recent_maxlen: int = 200
    ) -> StageTracker:
        tracker = StageTracker(name, track_recent, recent_maxlen)
        self._trackers[name] = tracker
        return tracker

    def unregister(self, name: str) -> None:
        if name in self._trackers:
            del self._trackers[name]

    def get(self, name: str) -> StageTracker:
        return self._trackers[name]

    def record(self, name: str, value_ms: float, timestamp: Optional[float] = None) -> None:
        if name in self._trackers:
            self._trackers[name].record(value_ms, timestamp)

    def reset_all(self) -> None:
        for tracker in self._trackers.values():
            tracker.reset()

    def get_all_last_values(self) -> dict[str, float]:
        return {
            f"last_{name}_ms": tracker.last_value_ms for name, tracker in self._trackers.items()
        }
