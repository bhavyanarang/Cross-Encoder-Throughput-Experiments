"""
Metrics Collector - Composed metrics collection for inference server.

Aggregates metrics from modular components:
- LatencyTracker: Request latencies with percentiles
- ThroughputTracker: QPS with sliding window
- PaddingAnalyzer: Padding waste analysis
- StageMetricsGroup: Per-stage timing breakdown
"""

import time
import os
import threading
import logging
from dataclasses import dataclass, field
from typing import Optional

from .components import (
    LatencyTracker,
    ThroughputTracker,
    PaddingAnalyzer,
    StageMetricsGroup,
)

logger = logging.getLogger(__name__)

# Process monitoring
try:
    import psutil
    _SERVER_PROCESS = psutil.Process(os.getpid())
    _SERVER_PROCESS.cpu_percent()
except ImportError:
    _SERVER_PROCESS = None


def get_cpu_percent() -> float:
    """Get current process CPU percentage."""
    if _SERVER_PROCESS:
        try:
            return _SERVER_PROCESS.cpu_percent(interval=None)
        except Exception:
            pass
    return 0.0


@dataclass
class ExperimentInfo:
    """Experiment metadata for dashboard display."""
    name: str = ""
    description: str = ""
    backend_type: str = ""
    device: str = ""


@dataclass
class MetricsCollector:
    """
    Composed metrics collector for inference server.
    
    Aggregates metrics from modular components for:
    - Request latencies
    - Throughput (QPS)
    - Padding waste analysis
    - Per-stage timing breakdown
    - Per-instance model metrics
    
    Thread-safe: uses internal locking for all operations.
    """
    
    # Modular components
    latency: LatencyTracker = field(default_factory=LatencyTracker)
    throughput: ThroughputTracker = field(default_factory=ThroughputTracker)
    padding: PaddingAnalyzer = field(default_factory=PaddingAnalyzer)
    stages: StageMetricsGroup = field(default_factory=StageMetricsGroup)
    
    # Experiment metadata
    experiment: ExperimentInfo = field(default_factory=ExperimentInfo)
    
    # Timing
    start_time: float = field(default_factory=time.time)
    last_update_time: float = field(default_factory=time.time)
    
    # Frozen snapshot when experiment stops
    frozen_snapshot: Optional[dict] = None
    
    # Thread lock
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    # Model reference for GPU memory tracking
    _model = None
    
    # Model pool reference for per-instance metrics
    _model_pool = None
    
    @classmethod
    def set_model(cls, model):
        """Set model reference for GPU memory tracking."""
        cls._model = model
    
    @classmethod
    def set_model_pool(cls, model_pool):
        """Set model pool reference for per-instance metrics."""
        cls._model_pool = model_pool
    
    def set_experiment_info(
        self,
        name: str = "",
        description: str = "",
        backend: str = "",
        device: str = ""
    ) -> None:
        """Set experiment metadata for dashboard display."""
        self.experiment = ExperimentInfo(
            name=name,
            description=description,
            backend_type=backend,
            device=device,
        )
        logger.info(f"Experiment: {name} | Backend: {backend} | Device: {device}")
    
    def is_active(self) -> bool:
        """Check if experiment is actively running."""
        return (time.time() - self.last_update_time) < 2.0 and self.latency.count > 0
    
    def get_gpu_memory_mb(self) -> float:
        """Get GPU memory from PyTorch MPS."""
        try:
            import torch
            if torch.backends.mps.is_available():
                allocated = torch.mps.current_allocated_memory()
                return allocated / (1024 * 1024)
        except Exception:
            pass
        return 0.0
    
    def record(self, duration_ms: float, num_queries: int = 1) -> None:
        """
        Record a completed request.
        
        Args:
            duration_ms: Total request latency in milliseconds
            num_queries: Number of queries in the request
        """
        with self._lock:
            self.latency.record(duration_ms)
            self.throughput.record(num_queries)
            self.last_update_time = time.time()
            self.frozen_snapshot = None  # Clear frozen snapshot on new data
            
            if self.throughput.request_count % 50 == 0:
                instant_qps = self.throughput.get_instant_qps()
                logger.info(
                    f"Processed {self.throughput.query_count} queries "
                    f"({self.throughput.request_count} requests) | "
                    f"Latency: {duration_ms:.2f}ms | QPS: {instant_qps:.1f}"
                )
    
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
        
        Args:
            t_grpc_receive: Time to deserialize gRPC request (ms)
            t_tokenize: Time to tokenize pairs (ms)
            t_queue_wait: Time request waited in queue (ms)
            t_model_inference: GPU forward pass time (ms)
            t_grpc_send: Time to serialize + send response (ms)
        """
        self.stages.record(
            t_grpc_receive=t_grpc_receive,
            t_tokenize=t_tokenize,
            t_queue_wait=t_queue_wait,
            t_model_inference=t_model_inference,
            t_grpc_send=t_grpc_send,
        )
    
    def record_padding_stats(
        self,
        padding_ratio: float = 0.0,
        padded_tokens: int = 0,
        total_tokens: int = 0,
        max_seq_length: int = 0,
        avg_seq_length: float = 0.0,
    ) -> None:
        """
        Record padding analysis statistics per batch.
        
        Args:
            padding_ratio: Fraction of tokens that are padding (0-1)
            padded_tokens: Number of padding tokens in batch
            total_tokens: Total tokens in batch (including padding)
            max_seq_length: Longest sequence in batch
            avg_seq_length: Average sequence length before padding
        """
        self.padding.record_batch(
            padding_ratio=padding_ratio,
            padded_tokens=padded_tokens,
            total_tokens=total_tokens,
            max_seq_length=max_seq_length,
            avg_seq_length=avg_seq_length,
        )
    
    def _compute_metrics(self) -> dict:
        """Compute current metrics."""
        latency_stats = self.latency.get_stats()
        throughput_stats = self.throughput.get_stats()
        padding_stats = self.padding.get_stats()
        stage_breakdown = self.stages.get_all_stats()
        
        if latency_stats.count == 0:
            return {}
        
        # Get instance metrics if model pool is available
        instance_metrics = {}
        if self._model_pool is not None:
            try:
                instance_metrics = self._model_pool.get_instance_metrics_summary()
            except Exception:
                pass
        
        return {
            # Experiment metadata
            "experiment_name": self.experiment.name,
            "experiment_description": self.experiment.description,
            "backend_type": self.experiment.backend_type,
            "device": self.experiment.device,
            
            # Core latency metrics
            "count": latency_stats.count,
            "query_count": throughput_stats.total_queries,
            "instant_latency_ms": self.latency.get_instant_latency(),
            "avg_ms": latency_stats.avg_ms,
            "p50_ms": latency_stats.p50_ms,
            "p95_ms": latency_stats.p95_ms,
            "p99_ms": latency_stats.p99_ms,
            "min_ms": latency_stats.min_ms,
            "max_ms": latency_stats.max_ms,
            "std_ms": latency_stats.std_ms,
            
            # Throughput metrics
            "throughput_qps": throughput_stats.instant_qps,
            "avg_throughput_qps": throughput_stats.avg_qps,
            "total_time_s": throughput_stats.elapsed_seconds,
            
            # System metrics
            "cpu_percent": get_cpu_percent(),
            "gpu_memory_mb": self.get_gpu_memory_mb(),
            
            # Stage breakdown
            "stage_breakdown": {
                name: {
                    "p50_ms": stats.p50_ms,
                    "p95_ms": stats.p95_ms,
                    "p99_ms": stats.p99_ms,
                    "avg_ms": stats.avg_ms,
                    "count": stats.count,
                }
                for name, stats in stage_breakdown.items()
            },
            "stage_percentages": self.stages.get_percentages(latency_stats.avg_ms),
            
            # Last stage timings
            "last_tokenize_ms": self.stages.last_tokenize_ms,
            "last_inference_ms": self.stages.last_inference_ms,
            "last_queue_wait_ms": self.stages.last_queue_wait_ms,
            
            # Queue wait analysis
            "queue_wait_analysis": self.stages.get_queue_wait_analysis(latency_stats.avg_ms),
            
            # Padding analysis
            "padding_analysis": {
                "avg_padding_pct": padding_stats.avg_padding_pct,
                "p50_padding_pct": padding_stats.p50_padding_pct,
                "p95_padding_pct": padding_stats.p95_padding_pct,
                "total_wasted_compute_pct": padding_stats.total_wasted_compute_pct,
                "last_padding_pct": padding_stats.last_padding_pct,
                "avg_max_seq_length": padding_stats.avg_max_seq_length,
                "avg_avg_seq_length": padding_stats.avg_avg_seq_length,
                "last_max_seq_length": padding_stats.last_max_seq_length,
                "last_avg_seq_length": padding_stats.last_avg_seq_length,
            },
            
            # Per-instance model metrics
            "instance_metrics": instance_metrics,
        }
    
    def summary(self) -> dict:
        """
        Get metrics summary for dashboard.
        
        Returns frozen snapshot when experiment is not active.
        """
        is_running = self.is_active()
        
        if self.latency.count == 0:
            return {
                "experiment_name": self.experiment.name,
                "experiment_description": self.experiment.description,
                "backend_type": self.experiment.backend_type,
                "device": self.experiment.device,
                "is_running": is_running,
                "cpu_percent": get_cpu_percent(),
                "gpu_memory_mb": self.get_gpu_memory_mb(),
            }
        
        # Return frozen snapshot if not running
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
    
    def reset(self) -> None:
        """Reset all metrics."""
        logger.info("Metrics reset")
        with self._lock:
            self.latency.reset()
            self.throughput.reset()
            self.padding.reset()
            self.stages.reset()
            self.start_time = time.time()
            self.last_update_time = time.time()
            self.frozen_snapshot = None


__all__ = ["MetricsCollector", "ExperimentInfo", "get_cpu_percent"]
