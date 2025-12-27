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


@dataclass
class WorkerMetrics:
    """Per-worker/per-model metrics tracking."""

    worker_id: int
    latencies: list = field(default_factory=list)
    query_count: int = 0
    request_count: int = 0
    start_time: float = field(default_factory=time.time)

    def record(self, latency_ms: float, num_queries: int = 1) -> None:
        self.latencies.append(latency_ms)
        self.query_count += num_queries
        self.request_count += 1

    def get_stats(self) -> dict:
        if not self.latencies:
            return {
                "worker_id": self.worker_id,
                "avg_ms": 0,
                "p50_ms": 0,
                "p95_ms": 0,
                "p99_ms": 0,
                "query_count": 0,
                "request_count": 0,
                "throughput_qps": 0,
            }
        arr = np.array(self.latencies)
        elapsed = time.time() - self.start_time
        return {
            "worker_id": self.worker_id,
            "avg_ms": float(np.mean(arr)),
            "p50_ms": float(np.percentile(arr, 50)),
            "p95_ms": float(np.percentile(arr, 95)),
            "p99_ms": float(np.percentile(arr, 99)),
            "query_count": self.query_count,
            "request_count": self.request_count,
            "throughput_qps": self.query_count / elapsed if elapsed > 0 else 0,
        }

    def reset(self) -> None:
        self.latencies = []
        self.query_count = 0
        self.request_count = 0
        self.start_time = time.time()


@dataclass
class TokenizerWorkerMetrics:
    """Per-tokenizer-worker metrics tracking."""

    worker_id: int
    latencies: list = field(default_factory=list)
    request_count: int = 0
    total_tokens_processed: int = 0
    start_time: float = field(default_factory=time.time)

    def record(self, latency_ms: float, total_tokens: int = 0) -> None:
        self.latencies.append(latency_ms)
        self.request_count += 1
        self.total_tokens_processed += total_tokens

    def get_stats(self) -> dict:
        if not self.latencies:
            return {
                "worker_id": self.worker_id,
                "avg_ms": 0,
                "p50_ms": 0,
                "p95_ms": 0,
                "p99_ms": 0,
                "request_count": 0,
                "throughput_tokens_per_sec": 0,
            }
        arr = np.array(self.latencies)
        elapsed = time.time() - self.start_time
        return {
            "worker_id": self.worker_id,
            "avg_ms": float(np.mean(arr)),
            "p50_ms": float(np.percentile(arr, 50)),
            "p95_ms": float(np.percentile(arr, 95)),
            "p99_ms": float(np.percentile(arr, 99)),
            "request_count": self.request_count,
            "throughput_tokens_per_sec": (
                self.total_tokens_processed / elapsed if elapsed > 0 else 0
            ),
        }

    def reset(self) -> None:
        self.latencies = []
        self.request_count = 0
        self.total_tokens_processed = 0
        self.start_time = time.time()


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
    stage_overhead: StageMetrics = field(default_factory=StageMetrics)  # Tokenizer pool overhead
    stage_mp_queue_send: StageMetrics = field(default_factory=StageMetrics)  # MP queue send
    stage_mp_queue_receive: StageMetrics = field(default_factory=StageMetrics)  # MP queue receive
    stage_grpc_serialize: StageMetrics = field(default_factory=StageMetrics)  # gRPC serialize
    stage_grpc_deserialize: StageMetrics = field(default_factory=StageMetrics)  # gRPC deserialize
    stage_scheduler: StageMetrics = field(default_factory=StageMetrics)  # Scheduler overhead

    # Recent stage timings for charts
    recent_stage_tokenize: deque = field(default_factory=lambda: deque(maxlen=200))
    recent_stage_inference: deque = field(default_factory=lambda: deque(maxlen=200))
    recent_queue_wait: deque = field(default_factory=lambda: deque(maxlen=200))

    # Last values for live display
    last_latency_ms: float = 0.0
    last_stage_tokenize_ms: float = 0.0
    last_stage_inference_ms: float = 0.0
    last_queue_wait_ms: float = 0.0
    last_overhead_ms: float = 0.0  # Tokenizer pool overhead
    last_mp_queue_send_ms: float = 0.0
    last_mp_queue_receive_ms: float = 0.0
    last_grpc_serialize_ms: float = 0.0
    last_grpc_deserialize_ms: float = 0.0
    last_scheduler_ms: float = 0.0

    # Padding analysis
    padding_ratios: list = field(default_factory=list)
    padded_tokens_total: int = 0
    real_tokens_total: int = 0
    max_seq_lengths: list = field(default_factory=list)
    avg_seq_lengths: list = field(default_factory=list)
    last_padding_ratio: float = 0.0
    last_max_seq_length: int = 0
    last_avg_seq_length: float = 0.0

    # Per-worker/per-model stats (dict keyed by worker_id)
    _worker_stats: dict[int, WorkerMetrics] = field(default_factory=dict)

    # Per-tokenizer-worker stats (dict keyed by worker_id)
    _tokenizer_worker_stats: dict[int, TokenizerWorkerMetrics] = field(default_factory=dict)

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
        """Check if experiment is currently active.

        An experiment is considered active if:
        1. There have been requests recorded, AND
        2. Either:
           - Last update was within 10 seconds (recent activity), OR
           - There are recent latencies in the deque (ongoing activity)
        """
        if self.request_count == 0:
            return False

        time_since_update = time.time() - self.last_update_time

        # If we have recent activity (within 10 seconds), definitely active
        if time_since_update < 10.0:
            return True

        # If we have recent latencies in the deque, still consider active
        # (this handles cases where requests come in bursts with gaps)
        if self.recent_latencies:
            most_recent_time, _ = self.recent_latencies[-1]
            if (time.time() - most_recent_time) < 30.0:
                return True

        return False

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
        t_overhead: float = 0.0,
        t_mp_queue_send: float = 0.0,
        t_mp_queue_receive: float = 0.0,
        t_grpc_serialize: float = 0.0,
        t_grpc_deserialize: float = 0.0,
        t_scheduler: float = 0.0,
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
            if t_overhead > 0:
                self.stage_overhead.record(t_overhead)
                self.last_overhead_ms = t_overhead
            if t_mp_queue_send > 0:
                self.stage_mp_queue_send.record(t_mp_queue_send)
                self.last_mp_queue_send_ms = t_mp_queue_send
            if t_mp_queue_receive > 0:
                self.stage_mp_queue_receive.record(t_mp_queue_receive)
                self.last_mp_queue_receive_ms = t_mp_queue_receive
            if t_grpc_serialize > 0:
                self.stage_grpc_serialize.record(t_grpc_serialize)
                self.last_grpc_serialize_ms = t_grpc_serialize
            if t_grpc_deserialize > 0:
                self.stage_grpc_deserialize.record(t_grpc_deserialize)
                self.last_grpc_deserialize_ms = t_grpc_deserialize
            if t_scheduler > 0:
                self.stage_scheduler.record(t_scheduler)
                self.last_scheduler_ms = t_scheduler

    def record_padding_stats(
        self,
        padding_ratio: float = 0.0,
        padded_tokens: int = 0,
        total_tokens: int = 0,
        max_seq_length: int = 0,
        avg_seq_length: float = 0.0,
    ) -> None:
        with self._lock:
            # Record padding stats even if padding_ratio is 0 (valid case with no padding)
            self.padding_ratios.append(padding_ratio)
            self.last_padding_ratio = padding_ratio
            if padded_tokens >= 0:
                self.padded_tokens_total += padded_tokens
                self.real_tokens_total += total_tokens - padded_tokens
            if max_seq_length > 0:
                self.max_seq_lengths.append(max_seq_length)
                self.last_max_seq_length = max_seq_length
            if avg_seq_length > 0:
                self.avg_seq_lengths.append(avg_seq_length)
                self.last_avg_seq_length = avg_seq_length

    def record_worker_stats(
        self,
        worker_id: int,
        latency_ms: float,
        num_queries: int = 1,
    ) -> None:
        """Record per-worker/per-model statistics."""
        with self._lock:
            if worker_id not in self._worker_stats:
                self._worker_stats[worker_id] = WorkerMetrics(worker_id=worker_id)
            self._worker_stats[worker_id].record(latency_ms, num_queries)

    def record_tokenizer_worker_stats(
        self,
        worker_id: int,
        latency_ms: float,
        total_tokens: int = 0,
    ) -> None:
        """Record per-tokenizer-worker statistics."""
        with self._lock:
            if worker_id not in self._tokenizer_worker_stats:
                self._tokenizer_worker_stats[worker_id] = TokenizerWorkerMetrics(
                    worker_id=worker_id
                )
            self._tokenizer_worker_stats[worker_id].record(latency_ms, total_tokens)

    def _get_worker_stats(self) -> list[dict]:
        """Get stats for all workers."""
        with self._lock:
            return [ws.get_stats() for ws in self._worker_stats.values()]

    def _get_tokenizer_worker_stats(self) -> list[dict]:
        """Get stats for all tokenizer workers."""
        with self._lock:
            return [ws.get_stats() for ws in self._tokenizer_worker_stats.values()]

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
        queue_wait_stats = self.stage_queue_wait.get_stats()
        overhead_stats = self.stage_overhead.get_stats()
        mp_queue_send_stats = self.stage_mp_queue_send.get_stats()
        mp_queue_receive_stats = self.stage_mp_queue_receive.get_stats()
        grpc_serialize_stats = self.stage_grpc_serialize.get_stats()
        grpc_deserialize_stats = self.stage_grpc_deserialize.get_stats()
        scheduler_stats = self.stage_scheduler.get_stats()
        total_avg = float(np.mean(arr)) if len(arr) > 0 else 1.0

        # Calculate stage percentages including all overhead components
        tokenize_pct = (tokenize_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        inference_pct = (inference_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        queue_wait_pct = (queue_wait_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        overhead_pct = (overhead_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        mp_queue_send_pct = (
            (mp_queue_send_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        )
        mp_queue_receive_pct = (
            (mp_queue_receive_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        )
        grpc_serialize_pct = (
            (grpc_serialize_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        )
        grpc_deserialize_pct = (
            (grpc_deserialize_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0
        )
        scheduler_pct = (scheduler_stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0

        # Other is what's left after accounting for all tracked components
        other_pct = max(
            0,
            100
            - tokenize_pct
            - inference_pct
            - queue_wait_pct
            - overhead_pct
            - mp_queue_send_pct
            - mp_queue_receive_pct
            - grpc_serialize_pct
            - grpc_deserialize_pct
            - scheduler_pct,
        )

        gpu_util = self.get_gpu_utilization_pct()

        # Get per-worker stats for multi-model experiments
        worker_stats = self._get_worker_stats()

        # Get per-tokenizer-worker stats
        tokenizer_worker_stats = self._get_tokenizer_worker_stats()

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
                "queue_wait": queue_wait_stats,
                "model_inference": inference_stats,
                "overhead": overhead_stats,
                "mp_queue_send": mp_queue_send_stats,
                "mp_queue_receive": mp_queue_receive_stats,
                "grpc_serialize": grpc_serialize_stats,
                "grpc_deserialize": grpc_deserialize_stats,
                "scheduler": scheduler_stats,
            },
            "stage_percentages": {
                "tokenize_pct": round(tokenize_pct, 1),
                "queue_wait_pct": round(queue_wait_pct, 1),
                "inference_pct": round(inference_pct, 1),
                "overhead_pct": round(overhead_pct, 1),
                "mp_queue_send_pct": round(mp_queue_send_pct, 1),
                "mp_queue_receive_pct": round(mp_queue_receive_pct, 1),
                "grpc_serialize_pct": round(grpc_serialize_pct, 1),
                "grpc_deserialize_pct": round(grpc_deserialize_pct, 1),
                "scheduler_pct": round(scheduler_pct, 1),
                # Calculate other_pct as truly unaccounted time, and also calculate
                # a combined "other" that includes all overhead for frontend display
                "other_pct": round(other_pct, 1),
                # Combined overhead for frontend (all overhead components + truly unaccounted)
                "other_combined_pct": round(
                    overhead_pct
                    + mp_queue_send_pct
                    + mp_queue_receive_pct
                    + grpc_serialize_pct
                    + grpc_deserialize_pct
                    + scheduler_pct
                    + other_pct,
                    1,
                ),
            },
            "last_tokenize_ms": self.last_stage_tokenize_ms,
            "last_inference_ms": self.last_stage_inference_ms,
            "last_queue_wait_ms": self.last_queue_wait_ms,
            "last_overhead_ms": self.last_overhead_ms,
            "last_mp_queue_send_ms": self.last_mp_queue_send_ms,
            "last_mp_queue_receive_ms": self.last_mp_queue_receive_ms,
            "last_grpc_serialize_ms": self.last_grpc_serialize_ms,
            "last_grpc_deserialize_ms": self.last_grpc_deserialize_ms,
            "last_scheduler_ms": self.last_scheduler_ms,
            "queue_wait_analysis": {
                "avg_ms": queue_wait_stats["avg_ms"],
                "p95_ms": queue_wait_stats["p95_ms"],
            },
            "padding_analysis": self._compute_padding_stats(),
            "worker_stats": worker_stats,
            "tokenizer_worker_stats": tokenizer_worker_stats,
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
        self.stage_overhead.reset()
        self.stage_mp_queue_send.reset()
        self.stage_mp_queue_receive.reset()
        self.stage_grpc_serialize.reset()
        self.stage_grpc_deserialize.reset()
        self.stage_scheduler.reset()
        self.recent_stage_tokenize.clear()
        self.recent_stage_inference.clear()
        self.recent_queue_wait.clear()
        self.last_stage_tokenize_ms = 0.0
        self.last_stage_inference_ms = 0.0
        self.last_queue_wait_ms = 0.0
        self.last_overhead_ms = 0.0
        self.last_mp_queue_send_ms = 0.0
        self.last_mp_queue_receive_ms = 0.0
        self.last_grpc_serialize_ms = 0.0
        self.last_grpc_deserialize_ms = 0.0
        self.last_scheduler_ms = 0.0
        self.padding_ratios = []
        self.padded_tokens_total = 0
        # Reset worker stats
        for ws in self._worker_stats.values():
            ws.reset()
        # Reset tokenizer worker stats
        for tws in self._tokenizer_worker_stats.values():
            tws.reset()
        self.real_tokens_total = 0
        self.max_seq_lengths = []
        self.avg_seq_lengths = []
        self.last_padding_ratio = 0.0
        self.last_max_seq_length = 0
        self.last_avg_seq_length = 0.0
