import threading
from collections import deque
from dataclasses import dataclass, field

import numpy as np


@dataclass
class StageMetrics:
    latencies: list = field(default_factory=list)

    def record(self, duration_ms: float) -> None:
        self.latencies.append(duration_ms)

    def get_stats(self) -> dict:
        if not self.latencies:
            return {"p50_ms": 0, "p95_ms": 0, "p99_ms": 0, "avg_ms": 0, "count": 0}
        arr = np.array(self.latencies)
        return {
            "p50_ms": float(np.percentile(arr, 50)),
            "p95_ms": float(np.percentile(arr, 95)),
            "p99_ms": float(np.percentile(arr, 99)),
            "avg_ms": float(np.mean(arr)),
            "count": len(arr),
        }

    def reset(self) -> None:
        self.latencies = []


class StageTracker:
    def __init__(self, name: str, track_recent: bool = False, recent_maxlen: int = 200):
        self.name = name
        self.metrics = StageMetrics()
        self.last_value_ms = 0.0
        self.recent_history: deque | None = deque(maxlen=recent_maxlen) if track_recent else None

    def record(self, value_ms: float, timestamp: float | None = None) -> None:
        # Only record non-zero values to maintain consistency
        # Zero values (e.g., no queue wait) don't consume time and shouldn't affect averages
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

    def get_stats(self) -> dict:
        return self.metrics.get_stats()


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

    def get(self, name: str) -> StageTracker:
        return self._trackers[name]

    def record(self, name: str, value_ms: float, timestamp: float | None = None) -> None:
        if name in self._trackers:
            self._trackers[name].record(value_ms, timestamp)

    def reset_all(self) -> None:
        for tracker in self._trackers.values():
            tracker.reset()

    def get_all_stats(self) -> dict[str, dict]:
        return {name: tracker.get_stats() for name, tracker in self._trackers.items()}

    def get_all_last_values(self) -> dict[str, float]:
        return {
            f"last_{name}_ms": tracker.last_value_ms for name, tracker in self._trackers.items()
        }
