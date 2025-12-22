import time
import os
import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Optional
from collections import deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

# Process monitoring
try:
    import psutil
    SERVER_PROCESS = psutil.Process(os.getpid())
    SERVER_PROCESS.cpu_percent()
except ImportError:
    SERVER_PROCESS = None


def get_cpu_percent() -> float:
    if SERVER_PROCESS:
        try:
            return SERVER_PROCESS.cpu_percent(interval=None)
        except:
            pass
    return 0.0


@dataclass
class MetricsCollector:
    latencies: list = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    request_count: int = 0
    query_count: int = 0  # Total number of queries (texts) processed
    last_update_time: float = field(default_factory=time.time)
    
    # For instantaneous metrics calculation (1-second windows)
    recent_queries: deque = field(default_factory=lambda: deque(maxlen=200))  # (timestamp, query_count)
    recent_latencies: deque = field(default_factory=lambda: deque(maxlen=200))  # (timestamp, latency_ms)
    
    # Frozen snapshot when experiment stops
    frozen_snapshot: Optional[dict] = None
    last_request_count: int = 0
    
    # Last instantaneous latency
    last_latency_ms: float = 0.0
    
    # Reference to model for GPU memory
    _model = None

    @classmethod
    def set_model(cls, model):
        """Set model reference for GPU memory tracking."""
        cls._model = model

    def is_active(self) -> bool:
        """Check if experiment is actively running."""
        return (time.time() - self.last_update_time) < 2.0 and self.request_count > 0

    def get_gpu_memory_mb(self) -> float:
        """Get GPU memory from PyTorch MPS."""
        try:
            import torch
            if torch.backends.mps.is_available():
                allocated = torch.mps.current_allocated_memory()
                return allocated / (1024 * 1024)
        except Exception as e:
            pass  # Silently fail - GPU memory tracking is optional
        return 0.0

    def record(self, duration_ms: float, num_queries: int = 1):
        now = time.time()
        self.latencies.append(duration_ms)
        self.request_count += 1
        self.query_count += num_queries
        self.last_update_time = now
        self.last_latency_ms = duration_ms
        self.frozen_snapshot = None  # Clear frozen snapshot on new data
        
        # Record for instantaneous metrics
        self.recent_queries.append((now, num_queries))
        self.recent_latencies.append((now, duration_ms))
        
        if self.request_count % 50 == 0:
            instant_qps = self._compute_instant_qps()
            logger.info(f"Processed {self.query_count} queries ({self.request_count} requests) | "
                       f"Latency: {duration_ms:.2f}ms | QPS: {instant_qps:.1f}")

    def _compute_instant_qps(self) -> float:
        """Compute instantaneous throughput based on last 1 second of data."""
        if not self.recent_queries:
            return 0.0
        
        now = time.time()
        window_sec = 1.0  # 1-second window
        
        # Sum queries in the time window
        queries_in_window = sum(
            q for t, q in self.recent_queries 
            if (now - t) <= window_sec
        )
        
        return queries_in_window / window_sec

    def _compute_instant_latency(self) -> float:
        """Compute instantaneous latency (average of last 1 second)."""
        if not self.recent_latencies:
            return self.last_latency_ms
        
        now = time.time()
        window_sec = 1.0  # 1-second window
        
        # Get latencies in the time window
        latencies_in_window = [
            lat for t, lat in self.recent_latencies 
            if (now - t) <= window_sec
        ]
        
        if latencies_in_window:
            return np.mean(latencies_in_window)
        return self.last_latency_ms

    def _compute_metrics(self) -> dict:
        """Compute current metrics."""
        if not self.latencies:
            return {}
        
        arr = np.array(self.latencies)
        elapsed = time.time() - self.start_time
        cpu_pct = get_cpu_percent()
        gpu_mem = self.get_gpu_memory_mb()
        
        # Compute instantaneous metrics
        instant_qps = self._compute_instant_qps()
        instant_latency = self._compute_instant_latency()
        
        return {
            "count": len(arr),
            "query_count": self.query_count,
            "instant_latency_ms": instant_latency,  # Instantaneous latency
            "avg_ms": float(np.mean(arr)),  # Average over experiment
            "p50_ms": float(np.percentile(arr, 50)),
            "p95_ms": float(np.percentile(arr, 95)),
            "p99_ms": float(np.percentile(arr, 99)),
            "min_ms": float(np.min(arr)),
            "max_ms": float(np.max(arr)),
            "std_ms": float(np.std(arr)),
            "throughput_qps": instant_qps,  # Instantaneous
            "avg_throughput_qps": self.query_count / elapsed if elapsed > 0 else 0,  # Average over experiment
            "total_time_s": elapsed,
            "cpu_percent": cpu_pct,
            "gpu_memory_mb": gpu_mem,
        }

    def summary(self) -> dict:
        is_running = self.is_active()
        
        if not self.latencies:
            return {
                "is_running": is_running,
                "cpu_percent": get_cpu_percent(),
                "gpu_memory_mb": self.get_gpu_memory_mb(),
            }
        
        # If not running and we have a frozen snapshot, return it
        if not is_running and self.frozen_snapshot is not None:
            return {**self.frozen_snapshot, "is_running": False}
        
        # Compute fresh metrics
        metrics = self._compute_metrics()
        metrics["is_running"] = is_running
        
        # Freeze snapshot when experiment stops
        if not is_running and self.frozen_snapshot is None:
            self.frozen_snapshot = metrics.copy()
            logger.info("Metrics frozen - experiment stopped")
        
        return metrics

    def reset(self):
        logger.info("Metrics reset")
        self.latencies = []
        self.start_time = time.time()
        self.request_count = 0
        self.query_count = 0
        self.last_update_time = time.time()
        self.frozen_snapshot = None
        self.last_request_count = 0
        self.last_latency_ms = 0.0
        self.recent_queries.clear()
        self.recent_latencies.clear()
