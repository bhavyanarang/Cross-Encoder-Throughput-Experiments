import time
import os
import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Optional
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUESTS_TOTAL = Counter('inference_requests_total', 'Total inference requests')
LATENCY_HISTOGRAM = Histogram('inference_latency_seconds', 'Inference latency', 
                               buckets=[0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 1.0])
GPU_MEMORY_GAUGE = Gauge('gpu_memory_bytes', 'GPU memory allocated')
CPU_PERCENT_GAUGE = Gauge('cpu_percent', 'CPU usage percent')

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
    last_update_time: float = field(default_factory=time.time)
    
    # Frozen snapshot when experiment stops
    frozen_snapshot: Optional[dict] = None
    last_request_count: int = 0
    
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
                GPU_MEMORY_GAUGE.set(allocated)
                return allocated / (1024 * 1024)
        except Exception as e:
            pass  # Silently fail - GPU memory tracking is optional
        return 0.0

    def record(self, duration_ms: float):
        self.latencies.append(duration_ms)
        self.request_count += 1
        self.last_update_time = time.time()
        self.frozen_snapshot = None  # Clear frozen snapshot on new data
        
        # Prometheus metrics
        REQUESTS_TOTAL.inc()
        LATENCY_HISTOGRAM.observe(duration_ms / 1000.0)
        
        if self.request_count % 50 == 0:
            logger.info(f"Processed {self.request_count} requests | Last latency: {duration_ms:.2f}ms")

    def _compute_metrics(self) -> dict:
        """Compute current metrics."""
        if not self.latencies:
            return {}
        
        arr = np.array(self.latencies)
        elapsed = time.time() - self.start_time
        cpu_pct = get_cpu_percent()
        gpu_mem = self.get_gpu_memory_mb()
        
        CPU_PERCENT_GAUGE.set(cpu_pct)
        
        return {
            "count": len(arr),
            "avg_ms": float(np.mean(arr)),
            "p50_ms": float(np.percentile(arr, 50)),
            "p95_ms": float(np.percentile(arr, 95)),
            "p99_ms": float(np.percentile(arr, 99)),
            "throughput_rps": len(arr) / elapsed if elapsed > 0 else 0,
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

    def get_prometheus_metrics(self) -> bytes:
        """Get Prometheus format metrics."""
        return generate_latest()

    def reset(self):
        logger.info("Metrics reset")
        self.latencies = []
        self.start_time = time.time()
        self.request_count = 0
        self.last_update_time = time.time()
        self.frozen_snapshot = None
        self.last_request_count = 0
