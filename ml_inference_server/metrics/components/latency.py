"""
Latency Tracker - Tracks request latencies with percentile calculations.
"""

import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Optional
import time

import numpy as np


@dataclass
class LatencyStats:
    """Statistics for latency measurements."""
    count: int = 0
    avg_ms: float = 0.0
    min_ms: float = 0.0
    max_ms: float = 0.0
    std_ms: float = 0.0
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0


@dataclass
class LatencyTracker:
    """
    Tracks request latencies with percentile calculations.
    
    Thread-safe: all operations use internal locking.
    """
    
    latencies: list = field(default_factory=list)
    recent_latencies: deque = field(default_factory=lambda: deque(maxlen=200))
    last_latency_ms: float = 0.0
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    def record(self, duration_ms: float) -> None:
        """
        Record a latency measurement.
        
        Args:
            duration_ms: Latency in milliseconds
        """
        now = time.time()
        with self._lock:
            self.latencies.append(duration_ms)
            self.recent_latencies.append((now, duration_ms))
            self.last_latency_ms = duration_ms
    
    def get_instant_latency(self, window_sec: float = 1.0) -> float:
        """
        Get instantaneous latency (average of recent window).
        
        Args:
            window_sec: Time window in seconds
            
        Returns:
            Average latency in the window, or last latency if window is empty
        """
        with self._lock:
            if not self.recent_latencies:
                return self.last_latency_ms
            
            now = time.time()
            latencies_in_window = [
                lat for t, lat in self.recent_latencies 
                if (now - t) <= window_sec
            ]
            
            if latencies_in_window:
                return float(np.mean(latencies_in_window))
            return self.last_latency_ms
    
    def get_stats(self) -> LatencyStats:
        """
        Get latency statistics.
        
        Returns:
            LatencyStats with count, avg, percentiles, etc.
        """
        with self._lock:
            if not self.latencies:
                return LatencyStats()
            
            arr = np.array(self.latencies)
            return LatencyStats(
                count=len(arr),
                avg_ms=float(np.mean(arr)),
                min_ms=float(np.min(arr)),
                max_ms=float(np.max(arr)),
                std_ms=float(np.std(arr)),
                p50_ms=float(np.percentile(arr, 50)),
                p95_ms=float(np.percentile(arr, 95)),
                p99_ms=float(np.percentile(arr, 99)),
            )
    
    def reset(self) -> None:
        """Reset all latency measurements."""
        with self._lock:
            self.latencies = []
            self.recent_latencies.clear()
            self.last_latency_ms = 0.0
    
    @property
    def count(self) -> int:
        """Get number of recorded latencies."""
        with self._lock:
            return len(self.latencies)


__all__ = ["LatencyTracker", "LatencyStats"]

