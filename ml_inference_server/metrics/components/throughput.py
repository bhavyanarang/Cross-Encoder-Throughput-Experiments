"""
Throughput Tracker - Tracks queries-per-second with sliding window.
"""

import threading
import time
from collections import deque
from dataclasses import dataclass, field


@dataclass
class ThroughputStats:
    """Statistics for throughput measurements."""
    instant_qps: float = 0.0
    avg_qps: float = 0.0
    total_queries: int = 0
    total_requests: int = 0
    elapsed_seconds: float = 0.0


@dataclass
class ThroughputTracker:
    """
    Tracks queries-per-second with sliding window calculations.
    
    Thread-safe: all operations use internal locking.
    """
    
    start_time: float = field(default_factory=time.time)
    query_count: int = 0
    request_count: int = 0
    recent_queries: deque = field(default_factory=lambda: deque(maxlen=200))
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    def record(self, num_queries: int = 1) -> None:
        """
        Record queries processed.
        
        Args:
            num_queries: Number of queries in this request
        """
        now = time.time()
        with self._lock:
            self.query_count += num_queries
            self.request_count += 1
            self.recent_queries.append((now, num_queries))
    
    def get_instant_qps(self, window_sec: float = 1.0) -> float:
        """
        Get instantaneous QPS based on sliding window.
        
        Args:
            window_sec: Time window in seconds
            
        Returns:
            Queries per second in the window
        """
        with self._lock:
            if not self.recent_queries:
                return 0.0
            
            now = time.time()
            queries_in_window = sum(
                q for t, q in self.recent_queries 
                if (now - t) <= window_sec
            )
            
            return queries_in_window / window_sec
    
    def get_avg_qps(self) -> float:
        """
        Get average QPS since start.
        
        Returns:
            Average queries per second
        """
        with self._lock:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                return self.query_count / elapsed
            return 0.0
    
    def get_stats(self) -> ThroughputStats:
        """
        Get throughput statistics.
        
        Returns:
            ThroughputStats with instant and average QPS
        """
        with self._lock:
            elapsed = time.time() - self.start_time
            avg_qps = self.query_count / elapsed if elapsed > 0 else 0.0
            
            # Calculate instant QPS inline to avoid lock re-entry deadlock
            now = time.time()
            if self.recent_queries:
                queries_in_window = sum(
                    q for t, q in self.recent_queries 
                    if (now - t) <= 1.0
                )
                instant_qps = queries_in_window / 1.0
            else:
                instant_qps = 0.0
            
            return ThroughputStats(
                instant_qps=instant_qps,
                avg_qps=avg_qps,
                total_queries=self.query_count,
                total_requests=self.request_count,
                elapsed_seconds=elapsed,
            )
    
    def reset(self) -> None:
        """Reset all throughput measurements."""
        with self._lock:
            self.start_time = time.time()
            self.query_count = 0
            self.request_count = 0
            self.recent_queries.clear()


__all__ = ["ThroughputTracker", "ThroughputStats"]

