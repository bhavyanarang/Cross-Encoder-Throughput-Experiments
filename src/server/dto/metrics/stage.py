import threading
from dataclasses import dataclass


@dataclass
class StageMetrics:
    def record(self, duration_ms: float) -> None:
        pass

    def reset(self) -> None:
        pass


class StageTracker:
    def __init__(self, name: str, track_recent: bool = False, recent_maxlen: int = 200):
        self.name = name
        self.metrics = StageMetrics()
        self.last_value_ms = 0.0

    def record(self, value_ms: float, timestamp: float | None = None) -> None:
        if value_ms <= 0:
            return

        self.metrics.record(value_ms)
        self.last_value_ms = value_ms

    def reset(self) -> None:
        self.metrics.reset()
        self.last_value_ms = 0.0


class StageTrackerManager:
    def __init__(self):
        self._trackers: dict[str, StageTracker] = {}
        self._lock = threading.Lock()

    def register(
        self, name: str, track_recent: bool = False, recent_maxlen: int = 200
    ) -> StageTracker:
        tracker = StageTracker(name)
        self._trackers[name] = tracker
        return tracker

    def unregister(self, name: str) -> None:
        if name in self._trackers:
            del self._trackers[name]

    def get(self, name: str) -> StageTracker:
        return self._trackers[name]

    def record(self, name: str, value_ms: float, timestamp: float | None = None) -> None:
        if name in self._trackers:
            self._trackers[name].record(value_ms, timestamp)

    def reset_all(self) -> None:
        for tracker in self._trackers.values():
            tracker.reset()

    def get_all_last_values(self) -> dict[str, float]:
        return {
            f"last_{name}_ms": tracker.last_value_ms for name, tracker in self._trackers.items()
        }
