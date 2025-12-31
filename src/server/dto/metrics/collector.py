import logging
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from src.server.dto.metrics.gpu import GPUMemoryProvider
from src.server.dto.metrics.padding import PaddingTracker
from src.server.dto.metrics.process import ProcessMonitor
from src.server.dto.metrics.stage import StageTrackerManager
from src.server.dto.metrics.worker import (
    TokenizerWorkerMetrics,
    WorkerMetrics,
    WorkerStatsManager,
)

if TYPE_CHECKING:
    from src.server.services.inference_service import InferenceService
    from src.server.pool.model_pool import ModelPool

logger = logging.getLogger(__name__)


@dataclass
class MetricsCollector:
    latencies: list = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    request_count: int = 0
    query_count: int = 0
    last_update_time: float = field(default_factory=time.time)

    experiment_name: str = ""
    experiment_description: str = ""
    backend_type: str = ""
    device: str = ""

    recent_queries: deque = field(default_factory=lambda: deque(maxlen=200))
    recent_latencies: deque = field(default_factory=lambda: deque(maxlen=200))

    _lock: threading.Lock = field(default_factory=threading.Lock)

    _stage_tracker_manager: StageTrackerManager = field(default_factory=StageTrackerManager)
    _padding_tracker: PaddingTracker = field(default_factory=PaddingTracker)
    _worker_stats_manager: WorkerStatsManager = field(
        default_factory=lambda: WorkerStatsManager(WorkerMetrics)
    )
    _tokenizer_worker_stats_manager: WorkerStatsManager = field(
        default_factory=lambda: WorkerStatsManager(TokenizerWorkerMetrics)
    )
    _gpu_memory_provider: GPUMemoryProvider = field(default_factory=GPUMemoryProvider)
    _process_monitor: ProcessMonitor = field(default_factory=ProcessMonitor)

    def __post_init__(self):
        self._stage_tracker_manager.register("tokenize", track_recent=True)
        self._stage_tracker_manager.register("queue_wait", track_recent=True)
        self._stage_tracker_manager.register("model_inference", track_recent=True)
        self._stage_tracker_manager.register("overhead")
        self._stage_tracker_manager.register("mp_queue_send")
        self._stage_tracker_manager.register("mp_queue_receive")
        self._stage_tracker_manager.register("grpc_serialize")
        self._stage_tracker_manager.register("grpc_deserialize")
        self._stage_tracker_manager.register("scheduler")

    def set_pool(self, pool: "ModelPool") -> None:
        self._gpu_memory_provider.set_pool(pool)

    def set_inference_service(self, inference_service: "InferenceService") -> None:
        self._gpu_memory_provider.set_inference_service(inference_service)

    def set_experiment_info(
        self, name: str = "", description: str = "", backend: str = "", device: str = ""
    ) -> None:
        self.experiment_name = name
        self.experiment_description = description
        self.backend_type = backend
        self.device = device
        logger.info(f"Experiment: {name} | Backend: {backend} | Device: {device}")

    def is_active(self) -> bool:
        if self.request_count == 0:
            return False

        time_since_update = time.time() - self.last_update_time
        if time_since_update < 10.0:
            return True

        if self.recent_latencies:
            most_recent_time, _ = self.recent_latencies[-1]
            if (time.time() - most_recent_time) < 30.0:
                return True

        return False

    def get_gpu_memory_mb(self) -> float:
        return self._gpu_memory_provider.get_memory_mb()

    def get_gpu_utilization_pct(self) -> float:
        try:
            inference_tracker = self._stage_tracker_manager.get("model_inference")
            if not inference_tracker.recent_history:
                return 0.0

            recent_inf_times = [
                inf_ms for _, inf_ms in self._filter_recent(inference_tracker.recent_history)
            ]
            if not recent_inf_times:
                return 0.0

            total_inf_ms = sum(recent_inf_times)
            return min(100.0, total_inf_ms / 10.0)
        except (KeyError, AttributeError, Exception):
            pass
        return 0.0

    @property
    def last_latency_ms(self) -> float:
        if self.recent_latencies:
            _, last_lat = self.recent_latencies[-1]
            return last_lat
        return 0.0

    def record(self, duration_ms: float, num_queries: int = 1):
        now = time.time()
        with self._lock:
            self.latencies.append(duration_ms)
            self.request_count += 1
            self.query_count += num_queries
            self.last_update_time = now
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
            stage_values = {
                "tokenize": t_tokenize,
                "queue_wait": t_queue_wait,
                "model_inference": t_model_inference,
                "overhead": t_overhead,
                "mp_queue_send": t_mp_queue_send,
                "mp_queue_receive": t_mp_queue_receive,
                "grpc_serialize": t_grpc_serialize,
                "grpc_deserialize": t_grpc_deserialize,
                "scheduler": t_scheduler,
            }
            for name, value in stage_values.items():
                tracker = self._stage_tracker_manager.get(name)
                tracker.record(value, now if tracker.recent_history is not None else None)

    def record_padding_stats(
        self,
        padding_ratio: float = 0.0,
        padded_tokens: int = 0,
        total_tokens: int = 0,
        max_seq_length: int = 0,
        avg_seq_length: float = 0.0,
    ) -> None:
        with self._lock:
            self._padding_tracker.record(
                padding_ratio, padded_tokens, total_tokens, max_seq_length, avg_seq_length
            )

    def record_worker_stats(self, worker_id: int, latency_ms: float, num_queries: int = 1) -> None:
        self._worker_stats_manager.record(worker_id, latency_ms, num_queries=num_queries)

    def record_tokenizer_worker_stats(
        self, worker_id: int, latency_ms: float, total_tokens: int = 0, num_queries: int = 1
    ) -> None:
        self._tokenizer_worker_stats_manager.record(
            worker_id, latency_ms, total_tokens=total_tokens, num_queries=num_queries
        )

    def _filter_recent(self, deque_data: deque, window_sec: float = 1.0) -> list:
        if not deque_data:
            return []
        now = time.time()
        return [(t, item) for t, item in deque_data if (now - t) <= window_sec]

    def _compute_instant_qps(self) -> float:
        if not self.recent_queries:
            return 0.0
        queries_in_window = self._filter_recent(self.recent_queries)
        return sum(q for _, q in queries_in_window)

    def _compute_instant_latency(self) -> float:
        if not self.recent_latencies:
            return self.last_latency_ms
        lats = [lat for _, lat in self._filter_recent(self.recent_latencies)]
        return float(np.mean(lats)) if lats else self.last_latency_ms

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
        
        # Calculate overall throughput from all workers' combined query counts
        # This ensures overall throughput = sum of per-worker throughputs
        worker_stats = self._worker_stats_manager.get_all_stats()
        total_worker_queries = sum(ws.get("query_count", 0) for ws in worker_stats)
        
        # Use total_worker_queries if available and greater than query_count
        # (query_count may only count requests, not individual queries in batches)
        effective_query_count = max(self.query_count, total_worker_queries) if worker_stats else self.query_count

        stage_stats = self._stage_tracker_manager.get_all_stats()
        total_avg = float(np.mean(arr)) if len(arr) > 0 else 1.0

        def _calc_pct(stats: dict) -> float:
            return (stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0

        # Calculate percentages for all stages
        stage_percentages = {f"{name}_pct": _calc_pct(stats) for name, stats in stage_stats.items()}
        
        # Validate that stage breakdown sums to approximately total latency
        actual_stage_sum = sum(stats["avg_ms"] for stats in stage_stats.values())
        if total_avg > 0 and abs(actual_stage_sum - total_avg) > 1.0:
            logger.warning(
                f"Stage breakdown mismatch: stages sum to {actual_stage_sum:.1f}ms "
                f"but total latency is {total_avg:.1f}ms (diff: {abs(actual_stage_sum - total_avg):.1f}ms). "
                f"This suggests unmeasured latency in the request pipeline."
            )
        
        # Calculate the sum of named stages (excluding 'other')
        named_stages_sum = sum(v for k, v in stage_percentages.items() if k != "other_pct")
        
        # Other percentage fills the gap to reach 100%
        other_pct = max(0, 100 - named_stages_sum)

        gpu_util = self.get_gpu_utilization_pct()
        last_values = self._stage_tracker_manager.get_all_last_values()

        last_value_mapping = {
            "last_tokenize_ms": last_values.get("last_tokenize_ms", 0.0),
            "last_stage_tokenize_ms": last_values.get("last_tokenize_ms", 0.0),
            "last_inference_ms": last_values.get("last_model_inference_ms", 0.0),
            "last_stage_inference_ms": last_values.get("last_model_inference_ms", 0.0),
            "last_queue_wait_ms": last_values.get("last_queue_wait_ms", 0.0),
            "last_overhead_ms": last_values.get("last_overhead_ms", 0.0),
            "last_mp_queue_send_ms": last_values.get("last_mp_queue_send_ms", 0.0),
            "last_mp_queue_receive_ms": last_values.get("last_mp_queue_receive_ms", 0.0),
            "last_grpc_serialize_ms": last_values.get("last_grpc_serialize_ms", 0.0),
            "last_grpc_deserialize_ms": last_values.get("last_grpc_deserialize_ms", 0.0),
            "last_scheduler_ms": last_values.get("last_scheduler_ms", 0.0),
        }

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
            "avg_throughput_qps": effective_query_count / elapsed if elapsed > 0 else 0,
            "cpu_percent": cpu_pct,
            "gpu_memory_mb": self.get_gpu_memory_mb(),
            "gpu_utilization_pct": gpu_util,
            "instance_metrics": {"avg_utilization_pct": gpu_util},
            "stage_breakdown": stage_stats,
            "stage_percentages": {
                # Frontend-friendly mappings (convert model_inference_pct to inference_pct)
                "tokenize_pct": round(stage_percentages.get("tokenize_pct", 0), 1),
                "queue_wait_pct": round(stage_percentages.get("queue_wait_pct", 0), 1),
                "inference_pct": round(stage_percentages.get("model_inference_pct", 0), 1),
                "overhead_pct": round(stage_percentages.get("overhead_pct", 0), 1),
                "mp_queue_send_pct": round(stage_percentages.get("mp_queue_send_pct", 0), 1),
                "mp_queue_receive_pct": round(stage_percentages.get("mp_queue_receive_pct", 0), 1),
                "grpc_serialize_pct": round(stage_percentages.get("grpc_serialize_pct", 0), 1),
                "grpc_deserialize_pct": round(stage_percentages.get("grpc_deserialize_pct", 0), 1),
                "scheduler_pct": round(stage_percentages.get("scheduler_pct", 0), 1),
                "other_pct": round(other_pct, 1),
                "other_combined_pct": round(
                    stage_percentages.get("overhead_pct", 0)
                    + stage_percentages.get("mp_queue_send_pct", 0)
                    + stage_percentages.get("mp_queue_receive_pct", 0)
                    + stage_percentages.get("grpc_serialize_pct", 0)
                    + stage_percentages.get("grpc_deserialize_pct", 0)
                    + stage_percentages.get("scheduler_pct", 0)
                    + other_pct,
                    1,
                ),
            },
            **last_value_mapping,
            "queue_wait_analysis": {
                "avg_ms": stage_stats["queue_wait"]["avg_ms"],
                "p95_ms": stage_stats["queue_wait"]["p95_ms"],
            },
            "padding_analysis": self._padding_tracker.get_stats(),
            "worker_stats": self._worker_stats_manager.get_all_stats(),
            "tokenizer_worker_stats": self._tokenizer_worker_stats_manager.get_all_stats(),
        }

    def reset(self):
        logger.info("Metrics reset")
        now = time.time()

        with self._lock:
            self.latencies = []
            self.start_time = now
            self.request_count = 0
            self.query_count = 0
            self.last_update_time = now

            self.recent_queries.clear()
            self.recent_latencies.clear()

            self._stage_tracker_manager.reset_all()
            self._padding_tracker.reset()
            self._worker_stats_manager.reset_all()
            self._tokenizer_worker_stats_manager.reset_all()
