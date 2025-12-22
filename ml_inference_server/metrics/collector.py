import time
import os
import logging
import threading
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
class StageMetrics:
    """Container for per-stage timing statistics."""
    latencies: list = field(default_factory=list)
    
    def record(self, duration_ms: float) -> None:
        """Record a timing measurement."""
        self.latencies.append(duration_ms)
    
    def get_stats(self) -> dict:
        """Get P50/P95/P99 statistics."""
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
        """Reset all measurements."""
        self.latencies = []


@dataclass
class MetricsCollector:
    latencies: list = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    request_count: int = 0
    query_count: int = 0  # Total number of queries (texts) processed
    last_update_time: float = field(default_factory=time.time)
    
    # Experiment metadata
    experiment_name: str = ""
    experiment_description: str = ""
    backend_type: str = ""
    device: str = ""
    
    # For instantaneous metrics calculation (1-second windows)
    recent_queries: deque = field(default_factory=lambda: deque(maxlen=200))  # (timestamp, query_count)
    recent_latencies: deque = field(default_factory=lambda: deque(maxlen=200))  # (timestamp, latency_ms)
    
    # Per-stage timing metrics
    stage_grpc_receive: StageMetrics = field(default_factory=StageMetrics)
    stage_tokenize: StageMetrics = field(default_factory=StageMetrics)
    stage_queue_wait: StageMetrics = field(default_factory=StageMetrics)
    stage_model_inference: StageMetrics = field(default_factory=StageMetrics)
    stage_grpc_send: StageMetrics = field(default_factory=StageMetrics)
    
    # Recent stage timings for history charts
    recent_stage_tokenize: deque = field(default_factory=lambda: deque(maxlen=200))
    recent_stage_inference: deque = field(default_factory=lambda: deque(maxlen=200))
    
    # Frozen snapshot when experiment stops
    frozen_snapshot: Optional[dict] = None
    last_request_count: int = 0
    
    # Last instantaneous latency
    last_latency_ms: float = 0.0
    
    # Last stage timings for live display
    last_stage_tokenize_ms: float = 0.0
    last_stage_inference_ms: float = 0.0
    
    # Reference to model for GPU memory
    _model = None
    
    # Thread lock for concurrent access (gRPC uses multiple threads)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    @classmethod
    def set_model(cls, model):
        """Set model reference for GPU memory tracking."""
        cls._model = model
    
    def set_experiment_info(
        self,
        name: str = "",
        description: str = "",
        backend: str = "",
        device: str = ""
    ) -> None:
        """Set experiment metadata for dashboard display."""
        self.experiment_name = name
        self.experiment_description = description
        self.backend_type = backend
        self.device = device
        logger.info(f"Experiment: {name} | Backend: {backend} | Device: {device}")

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
        with self._lock:
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
    
    def record_stage_timings(
        self,
        t_grpc_receive: float = 0.0,
        t_tokenize: float = 0.0,
        t_queue_wait: float = 0.0,
        t_model_inference: float = 0.0,
        t_grpc_send: float = 0.0,
    ) -> None:
        """
        Record per-stage timing measurements.
        Thread-safe: uses lock for concurrent gRPC calls.
        
        Args:
            t_grpc_receive: Time to deserialize gRPC request (ms)
            t_tokenize: Time to tokenize pairs (ms)
            t_queue_wait: Time request waited in queue (ms)
            t_model_inference: GPU forward pass time (ms)
            t_grpc_send: Time to serialize + send response (ms)
        """
        now = time.time()
        
        with self._lock:
            if t_grpc_receive > 0:
                self.stage_grpc_receive.record(t_grpc_receive)
            if t_tokenize > 0:
                self.stage_tokenize.record(t_tokenize)
                self.last_stage_tokenize_ms = t_tokenize
                self.recent_stage_tokenize.append((now, t_tokenize))
            if t_queue_wait > 0:
                self.stage_queue_wait.record(t_queue_wait)
            if t_model_inference > 0:
                self.stage_model_inference.record(t_model_inference)
                self.last_stage_inference_ms = t_model_inference
                self.recent_stage_inference.append((now, t_model_inference))
            if t_grpc_send > 0:
                self.stage_grpc_send.record(t_grpc_send)

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
        
        # Compute stage breakdown percentages
        tokenize_stats = self.stage_tokenize.get_stats()
        inference_stats = self.stage_model_inference.get_stats()
        total_avg = float(np.mean(arr)) if len(arr) > 0 else 1.0
        
        tokenize_pct = (tokenize_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        inference_pct = (inference_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        
        return {
            # Experiment metadata
            "experiment_name": self.experiment_name,
            "experiment_description": self.experiment_description,
            "backend_type": self.backend_type,
            "device": self.device,
            # Core metrics
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
            # Stage breakdown
            "stage_breakdown": {
                "grpc_receive": self.stage_grpc_receive.get_stats(),
                "tokenize": tokenize_stats,
                "queue_wait": self.stage_queue_wait.get_stats(),
                "model_inference": inference_stats,
                "grpc_send": self.stage_grpc_send.get_stats(),
            },
            "stage_percentages": {
                "tokenize_pct": round(tokenize_pct, 1),
                "inference_pct": round(inference_pct, 1),
                "other_pct": round(100 - tokenize_pct - inference_pct, 1),
            },
            # Last stage timings for live display
            "last_tokenize_ms": self.last_stage_tokenize_ms,
            "last_inference_ms": self.last_stage_inference_ms,
        }

    def summary(self) -> dict:
        is_running = self.is_active()
        
        if not self.latencies:
            return {
                "experiment_name": self.experiment_name,
                "experiment_description": self.experiment_description,
                "backend_type": self.backend_type,
                "device": self.device,
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
        
        # Reset stage metrics
        self.stage_grpc_receive.reset()
        self.stage_tokenize.reset()
        self.stage_queue_wait.reset()
        self.stage_model_inference.reset()
        self.stage_grpc_send.reset()
        self.recent_stage_tokenize.clear()
        self.recent_stage_inference.clear()
        self.last_stage_tokenize_ms = 0.0
        self.last_stage_inference_ms = 0.0
