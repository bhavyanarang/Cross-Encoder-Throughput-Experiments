import logging
import threading
import time
from collections import deque
from typing import TYPE_CHECKING

import numpy as np

from src.server.dto.metrics import MetricsCollector
from src.server.services.process_monitor_service import ProcessMonitorService
from src.server.services.service_base import BaseService

if TYPE_CHECKING:
    from src.server.services.orchestrator_service import OrchestratorService

logger = logging.getLogger(__name__)


def compute_latency_stats(latencies: list) -> dict:
    if not latencies:
        return {"avg_ms": 0, "p50_ms": 0, "p95_ms": 0, "p99_ms": 0}
    arr = np.array(latencies)
    return {
        "avg_ms": float(np.mean(arr)),
        "p50_ms": float(np.percentile(arr, 50)),
        "p95_ms": float(np.percentile(arr, 95)),
        "p99_ms": float(np.percentile(arr, 99)),
    }


class MetricsService(BaseService):
    def __init__(self, collection_interval_seconds: float = 5.0):
        super().__init__()
        self._collector = MetricsCollector()
        self._process_monitor_service = ProcessMonitorService()
        self._orchestrator: OrchestratorService | None = None
        self._collection_interval = collection_interval_seconds
        self._collection_thread: threading.Thread | None = None
        self._shutdown_event = threading.Event()

    def start(self) -> None:
        self._is_started = True
        self._shutdown_event.clear()

        if self._orchestrator:
            self._collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
            self._collection_thread.start()
            logger.info(
                f"MetricsService started with worker metrics collection "
                f"(interval: {self._collection_interval}s)"
            )
        else:
            logger.info("MetricsService started (no orchestrator registered for worker metrics)")

    def stop(self) -> None:
        self._is_started = False
        self._shutdown_event.set()

        if self._collection_thread:
            self._collection_thread.join(timeout=2.0)
            self._collection_thread = None

        logger.info("MetricsService stopped")

    def set_inference_service(self, orchestrator: "OrchestratorService") -> None:
        """Set the orchestrator (which provides inference service functionality)."""
        self._orchestrator = orchestrator
        self._process_monitor_service.set_inference_service(orchestrator)

    def set_tokenization_service(self, orchestrator: "OrchestratorService") -> None:
        """Set the orchestrator (which provides tokenization service functionality)."""
        self._orchestrator = orchestrator

    def set_model_pool(self, pool) -> None:
        self._process_monitor_service.set_pool(pool)
        self._collector.set_pool(pool)

    def set_tokenizer_pool(self, pool) -> None:
        self._collector.set_tokenizer_pool(pool)

    def set_experiment_info(
        self, name: str = "", description: str = "", backend: str = "", device: str = ""
    ) -> None:
        self._collector.set_experiment_info(name, description, backend, device)

    def record(self, duration_ms: float, num_queries: int = 1) -> None:
        self._collector.record(duration_ms, num_queries)

    def record_stage_timings(
        self,
        t_tokenize: float = 0.0,
        t_tokenizer_queue_wait: float = 0.0,
        t_model_queue_wait: float = 0.0,
        t_model_inference: float = 0.0,
        t_overhead: float = 0.0,
        t_mp_queue_send: float = 0.0,
        t_mp_queue_receive: float = 0.0,
        t_grpc_serialize: float = 0.0,
        t_grpc_deserialize: float = 0.0,
        t_scheduler: float = 0.0,
        total_ms: float = 0.0,
    ) -> None:
        self._collector.record_stage_timings(
            t_tokenize=t_tokenize,
            t_tokenizer_queue_wait=t_tokenizer_queue_wait,
            t_model_queue_wait=t_model_queue_wait,
            t_model_inference=t_model_inference,
            t_overhead=t_overhead,
            t_mp_queue_send=t_mp_queue_send,
            t_mp_queue_receive=t_mp_queue_receive,
            t_grpc_serialize=t_grpc_serialize,
            t_grpc_deserialize=t_grpc_deserialize,
            t_scheduler=t_scheduler,
            total_ms=total_ms,
        )

    def record_padding_stats(
        self,
        padding_ratio: float = 0.0,
        padded_tokens: int = 0,
        total_tokens: int = 0,
        max_seq_length: int = 0,
        avg_seq_length: float = 0.0,
    ) -> None:
        self._collector.record_padding_stats(
            padding_ratio=padding_ratio,
            padded_tokens=padded_tokens,
            total_tokens=total_tokens,
            max_seq_length=max_seq_length,
            avg_seq_length=avg_seq_length,
        )

    def record_worker_stats(self, worker_id: int, latency_ms: float, num_queries: int = 1) -> None:
        pass

    def record_tokenizer_worker_stats(
        self, worker_id: int, latency_ms: float, total_tokens: int = 0, num_queries: int = 1
    ) -> None:
        pass

    def get_summary(self) -> dict:
        collector = self._collector
        is_running = self._is_active()
        cpu_pct = self._process_monitor_service.get_cpu_percent()

        if not collector.latencies:
            return {
                "experiment_name": collector.experiment_name,
                "experiment_description": collector.experiment_description,
                "backend_type": collector.backend_type,
                "device": collector.device,
                "is_running": is_running,
                "count": 0,
                "query_count": 0,
                "instant_latency_ms": 0,
                "avg_ms": 0,
                "p50_ms": 0,
                "p95_ms": 0,
                "p99_ms": 0,
                "throughput_qps": 0,
                "avg_throughput_qps": 0,
                "cpu_percent": cpu_pct,
                "gpu_memory_mb": self.get_gpu_memory_mb(),
                "gpu_utilization_pct": 0,
                "instance_metrics": {"avg_utilization_pct": 0},
                "stage_breakdown": {},
                "stage_percentages": {},
                "last_tokenize_ms": 0,
                "last_inference_ms": 0,
                "last_tokenizer_queue_wait_ms": 0,
                "last_model_queue_wait_ms": 0,
                "last_queue_wait_ms": 0,
                "last_overhead_ms": 0,
                "queue_sizes": self._get_queue_sizes(collector),
                "padding_analysis": {},
                "worker_stats": self._get_worker_stats(collector),
                "tokenizer_worker_stats": self._get_tokenizer_worker_stats(collector),
            }

        arr = np.array(collector.latencies)
        elapsed = time.time() - collector.start_time

        worker_stats = self._get_worker_stats(collector)
        total_worker_queries = sum(ws.get("query_count", 0) for ws in worker_stats)

        effective_query_count = (
            max(collector.query_count, total_worker_queries)
            if worker_stats
            else collector.query_count
        )

        stage_stats = self._compute_stage_stats(collector)
        total_avg = float(np.mean(arr)) if len(arr) > 0 else 1.0

        def _calc_pct(stats: dict) -> float:
            return (stats["avg_ms"] / total_avg * 100) if total_avg > 0 else 0

        stage_percentages = {f"{name}_pct": _calc_pct(stats) for name, stats in stage_stats.items()}

        actual_stage_sum = sum(stats["avg_ms"] for stats in stage_stats.values())
        diff_ms = abs(actual_stage_sum - total_avg)
        if total_avg > 0 and diff_ms > max(10.0, total_avg * 0.05):
            has_pipeline_overhead = "pipeline_overhead" in stage_stats
            if not has_pipeline_overhead:
                logger.debug(
                    f"Stage breakdown mismatch: stages sum to {actual_stage_sum:.1f}ms "
                    f"but total latency is {total_avg:.1f}ms (diff: {diff_ms:.1f}ms). "
                    f"Pipeline overhead not being tracked."
                )

        named_stages_sum = sum(v for k, v in stage_percentages.items() if k != "other_pct")

        other_pct = max(0, 100 - named_stages_sum)

        gpu_util = self._compute_gpu_utilization()
        last_values = collector._stage_tracker_manager.get_all_last_values()

        last_value_mapping = {
            "last_tokenize_ms": last_values.get("last_tokenize_ms", 0.0),
            "last_stage_tokenize_ms": last_values.get("last_tokenize_ms", 0.0),
            "last_inference_ms": last_values.get("last_model_inference_ms", 0.0),
            "last_stage_inference_ms": last_values.get("last_model_inference_ms", 0.0),
            "last_tokenizer_queue_wait_ms": last_values.get("last_tokenizer_queue_wait_ms", 0.0),
            "last_model_queue_wait_ms": last_values.get("last_model_queue_wait_ms", 0.0),
            "last_queue_wait_ms": (
                last_values.get("last_tokenizer_queue_wait_ms", 0.0)
                + last_values.get("last_model_queue_wait_ms", 0.0)
            ),
            "last_overhead_ms": last_values.get("last_overhead_ms", 0.0),
            "last_mp_queue_send_ms": last_values.get("last_mp_queue_send_ms", 0.0),
            "last_mp_queue_receive_ms": last_values.get("last_mp_queue_receive_ms", 0.0),
            "last_grpc_serialize_ms": last_values.get("last_grpc_serialize_ms", 0.0),
            "last_grpc_deserialize_ms": last_values.get("last_grpc_deserialize_ms", 0.0),
            "last_scheduler_ms": last_values.get("last_scheduler_ms", 0.0),
        }

        return {
            "experiment_name": collector.experiment_name,
            "experiment_description": collector.experiment_description,
            "backend_type": collector.backend_type,
            "device": collector.device,
            "is_running": is_running,
            "count": len(arr),
            "query_count": collector.query_count,
            "instant_latency_ms": self._compute_instant_latency(collector),
            "avg_ms": float(np.mean(arr)),
            "p50_ms": float(np.percentile(arr, 50)),
            "p95_ms": float(np.percentile(arr, 95)),
            "p99_ms": float(np.percentile(arr, 99)),
            "throughput_qps": self._compute_instant_qps(collector),
            "avg_throughput_qps": effective_query_count / elapsed if elapsed > 0 else 0,
            "cpu_percent": cpu_pct,
            "gpu_memory_mb": self.get_gpu_memory_mb(),
            "gpu_utilization_pct": gpu_util,
            "instance_metrics": {"avg_utilization_pct": gpu_util},
            "stage_breakdown": stage_stats,
            "stage_percentages": {
                "tokenize_pct": round(stage_percentages.get("tokenize_pct", 0), 1),
                "tokenizer_queue_wait_pct": round(
                    stage_percentages.get("tokenizer_queue_wait_pct", 0), 1
                ),
                "model_queue_wait_pct": round(stage_percentages.get("model_queue_wait_pct", 0), 1),
                "queue_wait_pct": round(
                    stage_percentages.get("tokenizer_queue_wait_pct", 0)
                    + stage_percentages.get("model_queue_wait_pct", 0),
                    1,
                ),
                "inference_pct": round(stage_percentages.get("model_inference_pct", 0), 1),
                "pipeline_overhead_pct": round(
                    stage_percentages.get("pipeline_overhead_pct", 0), 1
                ),
                "overhead_pct": round(stage_percentages.get("overhead_pct", 0), 1),
                "mp_queue_send_pct": round(stage_percentages.get("mp_queue_send_pct", 0), 1),
                "mp_queue_receive_pct": round(stage_percentages.get("mp_queue_receive_pct", 0), 1),
                "grpc_serialize_pct": round(stage_percentages.get("grpc_serialize_pct", 0), 1),
                "grpc_deserialize_pct": round(stage_percentages.get("grpc_deserialize_pct", 0), 1),
                "scheduler_pct": round(stage_percentages.get("scheduler_pct", 0), 1),
                "other_pct": round(other_pct, 1),
                "other_combined_pct": round(
                    stage_percentages.get("pipeline_overhead_pct", 0)
                    + stage_percentages.get("overhead_pct", 0)
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
            "tokenizer_queue_wait_analysis": {
                "avg_ms": stage_stats.get("tokenizer_queue_wait", {}).get("avg_ms", 0),
                "p95_ms": stage_stats.get("tokenizer_queue_wait", {}).get("p95_ms", 0),
            },
            "model_queue_wait_analysis": {
                "avg_ms": stage_stats.get("model_queue_wait", {}).get("avg_ms", 0),
                "p95_ms": stage_stats.get("model_queue_wait", {}).get("p95_ms", 0),
            },
            "queue_wait_analysis": {
                # Combined for backward compatibility
                "avg_ms": (
                    stage_stats.get("tokenizer_queue_wait", {}).get("avg_ms", 0)
                    + stage_stats.get("model_queue_wait", {}).get("avg_ms", 0)
                ),
                "p95_ms": max(
                    stage_stats.get("tokenizer_queue_wait", {}).get("p95_ms", 0),
                    stage_stats.get("model_queue_wait", {}).get("p95_ms", 0),
                ),
            },
            "queue_sizes": self._get_queue_sizes(collector),
            "padding_analysis": self._compute_padding_stats(collector),
            "worker_stats": self._get_worker_stats(collector),
            "tokenizer_worker_stats": self._get_tokenizer_worker_stats(collector),
        }

    def _is_active(self) -> bool:
        """Check if metrics collection is active."""
        collector = self._collector
        if collector.request_count == 0:
            return False

        time_since_update = time.time() - collector.last_update_time
        if time_since_update < 10.0:
            return True

        if collector.recent_latencies:
            most_recent_time, _ = collector.recent_latencies[-1]
            if (time.time() - most_recent_time) < 30.0:
                return True

        return False

    def _filter_recent(self, deque_data: deque, window_sec: float = 1.0) -> list:
        """Filter deque to only include items within the time window."""
        if not deque_data:
            return []
        now = time.time()
        return [(t, item) for t, item in deque_data if (now - t) <= window_sec]

    def _compute_instant_qps(self, collector: MetricsCollector) -> float:
        """Compute instant QPS from recent queries."""
        if not collector.recent_queries:
            return 0.0
        queries_in_window = self._filter_recent(collector.recent_queries)
        return sum(q for _, q in queries_in_window)

    def _compute_instant_latency(self, collector: MetricsCollector) -> float:
        """Compute instant latency from recent latencies."""
        if not collector.recent_latencies:
            return self._get_last_latency_ms(collector)
        lats = [lat for _, lat in self._filter_recent(collector.recent_latencies)]
        return float(np.mean(lats)) if lats else self._get_last_latency_ms(collector)

    def _get_last_latency_ms(self, collector: MetricsCollector) -> float:
        """Get the last recorded latency."""
        if collector.recent_latencies:
            _, last_lat = collector.recent_latencies[-1]
            return last_lat
        return 0.0

    def _compute_gpu_utilization(self) -> float:
        """Compute GPU utilization percentage from recent inference times."""
        try:
            collector = self._collector
            inference_tracker = collector._stage_tracker_manager.get("model_inference")
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

    def _compute_stage_stats(self, collector: MetricsCollector) -> dict[str, dict]:
        """Compute statistics for all stages."""
        computed_stats = {}
        for name, tracker in collector._stage_tracker_manager._trackers.items():
            if tracker.metrics.latencies:
                arr = np.array(tracker.metrics.latencies)
                computed_stats[name] = {
                    "p50_ms": float(np.percentile(arr, 50)),
                    "p95_ms": float(np.percentile(arr, 95)),
                    "p99_ms": float(np.percentile(arr, 99)),
                    "avg_ms": float(np.mean(arr)),
                    "count": len(arr),
                }
            else:
                computed_stats[name] = {
                    "p50_ms": 0,
                    "p95_ms": 0,
                    "p99_ms": 0,
                    "avg_ms": 0,
                    "count": 0,
                }

        # DEBUG: Log all stage stats to understand timing breakdown
        if computed_stats:
            logger.debug(f"Stage stats: {list(computed_stats.keys())}")
            total_avg = sum(s.get("avg_ms", 0) for s in computed_stats.values())
            logger.debug(f"Total of all measured stages: {total_avg:.1f}ms")

        return computed_stats

    def _compute_padding_stats(self, collector: MetricsCollector) -> dict:
        """Compute padding statistics."""
        tracker = collector._padding_tracker
        if not tracker.ratios:
            return {
                "avg_padding_pct": 0.0,
                "last_padding_pct": 0.0,
                "last_max_seq_length": 0,
                "last_avg_seq_length": 0.0,
            }
        arr = np.array(tracker.ratios) * 100
        return {
            "avg_padding_pct": round(float(np.mean(arr)), 1),
            "last_padding_pct": round(tracker.last_ratio * 100, 1),
            "last_max_seq_length": tracker.last_max_seq_length,
            "last_avg_seq_length": round(tracker.last_avg_seq_length, 1),
        }

    def _get_worker_stats(self, collector: MetricsCollector) -> list[dict]:
        """Get worker stats from model pool (workers track their own metrics)."""
        if collector._model_pool:
            try:
                return collector._model_pool.get_worker_metrics()
            except Exception as e:
                logger.warning(f"Failed to get worker stats from pool: {e}")
        return []

    def _get_tokenizer_worker_stats(self, collector: MetricsCollector) -> list[dict]:
        """Get tokenizer worker stats from tokenizer pool (workers track their own metrics)."""
        if collector._tokenizer_pool:
            try:
                return collector._tokenizer_pool.get_worker_metrics()
            except Exception as e:
                logger.warning(f"Failed to get tokenizer worker stats from pool: {e}")
        return []

    def _get_queue_sizes(self, collector: MetricsCollector) -> dict:
        """Get current queue sizes from pools."""
        tokenizer_queue_size = 0
        model_queue_size = 0

        if collector._tokenizer_pool:
            try:
                info = collector._tokenizer_pool.get_info()
                tokenizer_queue_size = info.get("total_queue_size", 0)
                # Also check inference queue size (output of tokenizer, input to model)
                inference_queue_size = info.get("inference_queue_size", 0)
                if tokenizer_queue_size > 0 or inference_queue_size > 0:
                    logger.debug(
                        f"Tokenizer queues - worker queues: {tokenizer_queue_size}, "
                        f"inference queue: {inference_queue_size}"
                    )
            except Exception as e:
                logger.warning(f"Failed to get tokenizer queue size: {e}", exc_info=True)

        if collector._model_pool:
            try:
                info = collector._model_pool.get_info()
                model_queue_size = info.get("queue_size", 0)
                if model_queue_size > 0:
                    logger.debug(f"Model queue size: {model_queue_size}")
            except Exception as e:
                logger.warning(f"Failed to get model queue size: {e}", exc_info=True)

        # Note: Model queue size should match tokenizer's inference_queue_size
        # since they both reference the same _inference_queue

        batch_queue_size = 0
        if self._orchestrator:
            batch_info = self._orchestrator.get_batching_info()
            batch_queue_size = batch_info.get("pending", 0)

        return {
            "tokenizer_queue_size": tokenizer_queue_size,
            "model_queue_size": model_queue_size,
            "batch_queue_size": batch_queue_size,
            "total_queue_size": tokenizer_queue_size + model_queue_size + batch_queue_size,
        }

    def reset(self) -> None:
        self._collector.reset()

        if self._orchestrator and self._orchestrator.inference_is_started:
            try:
                self._orchestrator.reset_inference_worker_metrics()
            except Exception as e:
                logger.warning(f"Failed to reset inference worker metrics: {e}")

        if self._orchestrator and self._orchestrator.tokenization_is_started:
            try:
                self._orchestrator.reset_tokenizer_worker_metrics()
            except Exception as e:
                logger.warning(f"Failed to reset tokenizer worker metrics: {e}")

    def get_gpu_memory_mb(self) -> float:
        return self._process_monitor_service.get_gpu_memory_mb()

    def get_gpu_utilization_pct(self) -> float:
        return self._compute_gpu_utilization()

    def is_active(self) -> bool:
        return self._is_active()

    @property
    def last_latency_ms(self) -> float:
        return self._get_last_latency_ms(self._collector)

    def get_collector(self) -> MetricsCollector:
        return self._collector

    def _collection_loop(self) -> None:
        while not self._shutdown_event.is_set():
            try:
                if self.is_started:
                    self._collect_worker_metrics()

                self._shutdown_event.wait(timeout=self._collection_interval)
            except Exception as e:
                logger.warning(f"Error in metrics collection loop: {e}")
                self._shutdown_event.wait(timeout=self._collection_interval)

    def _collect_worker_metrics(self) -> None:
        if self._orchestrator and self._orchestrator.inference_is_started:
            try:
                inference_worker_metrics = self._orchestrator.get_inference_worker_metrics()
                for worker_metrics in inference_worker_metrics:
                    if worker_metrics:
                        worker_id = worker_metrics.get("worker_id", -1)
                        if worker_id >= 0:
                            latency_ms = worker_metrics.get("avg_ms", 0.0)
                            query_count = worker_metrics.get("query_count", 0)
                            if latency_ms > 0 and query_count > 0:
                                self.record_worker_stats(worker_id, latency_ms, query_count)
            except Exception as e:
                logger.warning(f"Failed to collect inference worker metrics: {e}")

        if self._orchestrator and self._orchestrator.tokenization_is_started:
            try:
                self._orchestrator.get_tokenizer_worker_metrics()
                # Workers track their own metrics, no need to record here
                pass
            except Exception as e:
                logger.warning(f"Failed to collect tokenizer worker metrics: {e}")


__all__ = ["MetricsService", "compute_latency_stats"]
