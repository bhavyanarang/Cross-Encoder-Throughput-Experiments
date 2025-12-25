"""Server metrics models and collector."""

import logging
import os
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from src.server.pool import ModelPool

logger = logging.getLogger(__name__)


@dataclass
class StageMetrics:
    """Container for per-stage timing statistics."""

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


class ProcessMonitor:
    """Encapsulates process monitoring to avoid global state."""

    def __init__(self):
        self._process = None
        self._initialized = False

    def _init_process(self) -> None:
        if self._initialized:
            return
        try:
            import psutil

            self._process = psutil.Process(os.getpid())
            self._process.cpu_percent()  # Initial call to start measuring
        except ImportError:
            self._process = None
        self._initialized = True

    def get_cpu_percent(self) -> float:
        self._init_process()
        if self._process:
            try:
                return self._process.cpu_percent(interval=None)
            except Exception:
                pass
        return 0.0


@dataclass
class MetricsCollector:
    """Full metrics collector with stage timing and history."""

    latencies: list = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    request_count: int = 0
    query_count: int = 0
    last_update_time: float = field(default_factory=time.time)

    # Experiment metadata
    experiment_name: str = ""
    experiment_description: str = ""
    backend_type: str = ""
    device: str = ""

    # Recent data for instantaneous metrics
    recent_queries: deque = field(default_factory=lambda: deque(maxlen=200))
    recent_latencies: deque = field(default_factory=lambda: deque(maxlen=200))

    # Per-stage timing
    stage_tokenize: StageMetrics = field(default_factory=StageMetrics)
    stage_queue_wait: StageMetrics = field(default_factory=StageMetrics)
    stage_model_inference: StageMetrics = field(default_factory=StageMetrics)

    # Recent stage timings for charts
    recent_stage_tokenize: deque = field(default_factory=lambda: deque(maxlen=200))
    recent_stage_inference: deque = field(default_factory=lambda: deque(maxlen=200))
    recent_queue_wait: deque = field(default_factory=lambda: deque(maxlen=200))

    # Last values for live display
    last_latency_ms: float = 0.0
    last_stage_tokenize_ms: float = 0.0
    last_stage_inference_ms: float = 0.0
    last_queue_wait_ms: float = 0.0

    # Padding analysis
    padding_ratios: list = field(default_factory=list)
    padded_tokens_total: int = 0
    real_tokens_total: int = 0
    max_seq_lengths: list = field(default_factory=list)
    avg_seq_lengths: list = field(default_factory=list)
    last_padding_ratio: float = 0.0
    last_max_seq_length: int = 0
    last_avg_seq_length: float = 0.0

    # Thread lock
    _lock: threading.Lock = field(default_factory=threading.Lock)

    # Pool reference for GPU memory queries
    _pool: "ModelPool | None" = None

    # Process monitor (encapsulated)
    _process_monitor: ProcessMonitor = field(default_factory=ProcessMonitor)

    def set_pool(self, pool: "ModelPool") -> None:
        """Set the model pool reference for GPU memory queries."""
        self._pool = pool

    def set_experiment_info(
        self, name: str = "", description: str = "", backend: str = "", device: str = ""
    ) -> None:
        self.experiment_name = name
        self.experiment_description = description
        self.backend_type = backend
        self.device = device
        logger.info(f"Experiment: {name} | Backend: {backend} | Device: {device}")

    def is_active(self) -> bool:
        return (time.time() - self.last_update_time) < 2.0 and self.request_count > 0

    def get_gpu_memory_mb(self) -> float:
        """Get GPU memory usage in MB.

        Queries GPU memory from worker processes via the model pool.
        Falls back to driver_allocated_memory() if pool is not available.
        """
        # Try to get memory from pool (worker processes) - they have models loaded
        if self._pool is not None:
            try:
                pool_memory = self._pool.get_gpu_memory_mb()
                if pool_memory > 0:
                    return pool_memory
                logger.debug("Pool returned 0 GPU memory - workers may not have models loaded yet")
            except Exception as e:
                logger.debug(f"Error getting GPU memory from pool: {e}")

        # Fallback: try driver_allocated_memory from main process
        try:
            import torch

            if torch.backends.mps.is_available():
                driver_mem = torch.mps.driver_allocated_memory() / (1024 * 1024)
                if driver_mem > 0:
                    logger.debug(f"Fallback: Got GPU memory from main process: {driver_mem:.2f} MB")
                    return driver_mem
                current_mem = torch.mps.current_allocated_memory() / (1024 * 1024)
                if current_mem > 0:
                    return current_mem
        except Exception as e:
            logger.debug(f"Error getting GPU memory from main process: {e}")

        return 0.0

    def get_gpu_utilization_pct(self) -> float:
        """Get GPU utilization percentage.

        On macOS with MPS, we estimate utilization based on inference activity.
        """
        try:
            if not self.recent_stage_inference:
                return 0.0

            now = time.time()
            recent_inf_times = [
                inf_ms for t, inf_ms in self.recent_stage_inference if (now - t) <= 1.0
            ]

            if not recent_inf_times:
                return 0.0

            total_inf_ms = sum(recent_inf_times)
            return min(100.0, total_inf_ms / 10.0)
        except Exception:
            pass
        return 0.0

    def record(self, duration_ms: float, num_queries: int = 1):
        now = time.time()
        with self._lock:
            self.latencies.append(duration_ms)
            self.request_count += 1
            self.query_count += num_queries
            self.last_update_time = now
            self.last_latency_ms = duration_ms
            self.recent_queries.append((now, num_queries))
            self.recent_latencies.append((now, duration_ms))

    def record_stage_timings(
        self,
        t_tokenize: float = 0.0,
        t_queue_wait: float = 0.0,
        t_model_inference: float = 0.0,
    ) -> None:
        now = time.time()
        with self._lock:
            if t_tokenize > 0:
                self.stage_tokenize.record(t_tokenize)
                self.last_stage_tokenize_ms = t_tokenize
                self.recent_stage_tokenize.append((now, t_tokenize))
            if t_queue_wait > 0:
                self.stage_queue_wait.record(t_queue_wait)
                self.last_queue_wait_ms = t_queue_wait
                self.recent_queue_wait.append((now, t_queue_wait))
            if t_model_inference > 0:
                self.stage_model_inference.record(t_model_inference)
                self.last_stage_inference_ms = t_model_inference
                self.recent_stage_inference.append((now, t_model_inference))

    def record_padding_stats(
        self,
        padding_ratio: float = 0.0,
        padded_tokens: int = 0,
        total_tokens: int = 0,
        max_seq_length: int = 0,
        avg_seq_length: float = 0.0,
    ) -> None:
        with self._lock:
            if padding_ratio > 0:
                self.padding_ratios.append(padding_ratio)
                self.last_padding_ratio = padding_ratio
            if padded_tokens > 0:
                self.padded_tokens_total += padded_tokens
                self.real_tokens_total += total_tokens - padded_tokens
            if max_seq_length > 0:
                self.max_seq_lengths.append(max_seq_length)
                self.last_max_seq_length = max_seq_length
            if avg_seq_length > 0:
                self.avg_seq_lengths.append(avg_seq_length)
                self.last_avg_seq_length = avg_seq_length

    def _compute_instant_qps(self) -> float:
        if not self.recent_queries:
            return 0.0
        now = time.time()
        queries_in_window = sum(q for t, q in self.recent_queries if (now - t) <= 1.0)
        return queries_in_window

    def _compute_instant_latency(self) -> float:
        if not self.recent_latencies:
            return self.last_latency_ms
        now = time.time()
        lats = [lat for t, lat in self.recent_latencies if (now - t) <= 1.0]
        return float(np.mean(lats)) if lats else self.last_latency_ms

    def _compute_padding_stats(self) -> dict:
        if not self.padding_ratios:
            return {
                "avg_padding_pct": 0.0,
                "last_padding_pct": 0.0,
                "last_max_seq_length": 0,
                "last_avg_seq_length": 0.0,
            }
        arr = np.array(self.padding_ratios) * 100
        return {
            "avg_padding_pct": round(float(np.mean(arr)), 1),
            "last_padding_pct": round(self.last_padding_ratio * 100, 1),
            "last_max_seq_length": self.last_max_seq_length,
            "last_avg_seq_length": round(self.last_avg_seq_length, 1),
        }

    def summary(self) -> dict:
        is_running = self.is_active()
        cpu_pct = self._process_monitor.get_cpu_percent()

        if not self.latencies:
            return {
                "experiment_name": self.experiment_name,
                "experiment_description": self.experiment_description,
                "backend_type": self.backend_type,
                "device": self.device,
                "is_running": is_running,
                "query_count": 0,
                "cpu_percent": cpu_pct,
                "gpu_memory_mb": self.get_gpu_memory_mb(),
            }

        arr = np.array(self.latencies)
        elapsed = time.time() - self.start_time

        tokenize_stats = self.stage_tokenize.get_stats()
        inference_stats = self.stage_model_inference.get_stats()
        total_avg = float(np.mean(arr)) if len(arr) > 0 else 1.0

        tokenize_pct = (tokenize_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        inference_pct = (inference_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0

        gpu_util = self.get_gpu_utilization_pct()

        return {
            "experiment_name": self.experiment_name,
            "experiment_description": self.experiment_description,
            "backend_type": self.backend_type,
            "device": self.device,
            "is_running": is_running,
            "count": len(arr),
            "query_count": self.query_count,
            "instant_latency_ms": self._compute_instant_latency(),
            "avg_ms": float(np.mean(arr)),
            "p50_ms": float(np.percentile(arr, 50)),
            "p95_ms": float(np.percentile(arr, 95)),
            "p99_ms": float(np.percentile(arr, 99)),
            "throughput_qps": self._compute_instant_qps(),
            "avg_throughput_qps": self.query_count / elapsed if elapsed > 0 else 0,
            "cpu_percent": cpu_pct,
            "gpu_memory_mb": self.get_gpu_memory_mb(),
            "gpu_utilization_pct": gpu_util,
            "instance_metrics": {
                "avg_utilization_pct": gpu_util,
            },
            "stage_breakdown": {
                "tokenize": tokenize_stats,
                "queue_wait": self.stage_queue_wait.get_stats(),
                "model_inference": inference_stats,
            },
            "stage_percentages": {
                "tokenize_pct": round(tokenize_pct, 1),
                "inference_pct": round(inference_pct, 1),
                "other_pct": round(100 - tokenize_pct - inference_pct, 1),
            },
            "last_tokenize_ms": self.last_stage_tokenize_ms,
            "last_inference_ms": self.last_stage_inference_ms,
            "last_queue_wait_ms": self.last_queue_wait_ms,
            "queue_wait_analysis": {
                "avg_ms": self.stage_queue_wait.get_stats()["avg_ms"],
                "p95_ms": self.stage_queue_wait.get_stats()["p95_ms"],
            },
            "padding_analysis": self._compute_padding_stats(),
        }

    def reset(self):
        logger.info("Metrics reset")
        self.latencies = []
        self.start_time = time.time()
        self.request_count = 0
        self.query_count = 0
        self.last_update_time = time.time()
        self.last_latency_ms = 0.0
        self.recent_queries.clear()
        self.recent_latencies.clear()
        self.stage_tokenize.reset()
        self.stage_queue_wait.reset()
        self.stage_model_inference.reset()
        self.recent_stage_tokenize.clear()
        self.recent_stage_inference.clear()
        self.recent_queue_wait.clear()
        self.last_stage_tokenize_ms = 0.0
        self.last_stage_inference_ms = 0.0
        self.last_queue_wait_ms = 0.0
        self.padding_ratios = []
        self.padded_tokens_total = 0
        self.real_tokens_total = 0
        self.max_seq_lengths = []
        self.avg_seq_lengths = []
        self.last_padding_ratio = 0.0
        self.last_max_seq_length = 0
        self.last_avg_seq_length = 0.0
