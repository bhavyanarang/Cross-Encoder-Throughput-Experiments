import logging
import threading
import time
from collections import deque
from typing import TYPE_CHECKING, Optional

import numpy as np
from prometheus_client import Counter, Gauge, Histogram, start_http_server

from src.server.dto.metrics import MetricsCollector
from src.server.services.process_monitor_service import ProcessMonitorService
from src.server.services.service_base import BaseService

if TYPE_CHECKING:
    from src.server.services.orchestrator_service import OrchestratorService

logger = logging.getLogger(__name__)





class MetricsService(BaseService):
    def __init__(self, collection_interval_seconds: float = 5.0, prometheus_port: int = 8000):
        super().__init__()
        self._collector = MetricsCollector()
        self._process_monitor_service = ProcessMonitorService()
        self._orchestrator: Optional["OrchestratorService"] = None
        self._collection_interval = collection_interval_seconds
        self._collection_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        self._prometheus_port = prometheus_port

        # Prometheus Metrics
        self.prom_request_count = Counter("request_count", "Total number of requests")
        self.prom_request_latency = Histogram(
            "request_latency_seconds", "Request latency in seconds", buckets=[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]
        )
        self.prom_inference_latency = Histogram(
             "inference_latency_seconds", "Model inference latency in seconds"
        )
        self.prom_tokenization_latency = Histogram(
             "tokenization_latency_seconds", "Tokenization latency in seconds"
        )
        self.prom_queue_wait_latency = Histogram(
             "queue_wait_latency_seconds", "Total queue wait latency in seconds"
        )
        
        self.prom_gpu_memory = Gauge("gpu_memory_mb", "GPU Memory Usage in MB")
        self.prom_cpu_percent = Gauge("cpu_percent", "CPU Usage Percentage")
        
        self.prom_tokenizer_queue_size = Gauge("tokenizer_queue_size", "Tokenizer Queue Size")
        self.prom_model_queue_size = Gauge("model_queue_size", "Model Queue Size")
        self.prom_batch_queue_size = Gauge("batch_queue_size", "Batch Queue Size")
        
        # Worker-level metrics
        self.prom_worker_latency = Gauge("worker_latency_ms", "Worker latency in ms", ["worker_id", "worker_type"])
        self.prom_worker_requests = Counter("worker_request_count", "Worker request count", ["worker_id", "worker_type"])
        self.prom_worker_throughput = Gauge("worker_throughput_qps", "Worker throughput QPS", ["worker_id", "worker_type"])
        
        # Overhead and padding metrics
        self.prom_overhead_latency = Histogram("overhead_latency_seconds", "Pipeline overhead latency")
        self.prom_padding_ratio = Gauge("padding_ratio", "Padding ratio (0-1)")


    def start(self) -> None:
        self._is_started = True
        self._shutdown_event.clear()

        # Start Prometheus HTTP server
        try:
            start_http_server(self._prometheus_port)
            logger.info(f"Prometheus metrics server started on port {self._prometheus_port}")
        except Exception as e:
            logger.warning(f"Failed to start Prometheus server: {e}")

        # Check pipeline mode and disable unrelated stages in collector
        if self._orchestrator and hasattr(self._orchestrator, "config"):
            mode = self._orchestrator.config.pipeline.mode
            if hasattr(self._collector, "set_pipeline_mode"):
                self._collector.set_pipeline_mode(mode)

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
        
        # Prometheus updates
        self.prom_request_count.inc(num_queries)
        self.prom_request_latency.observe(duration_ms / 1000.0) # Convert to seconds


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
        
        # Prometheus updates for stages
        if t_model_inference > 0:
            self.prom_inference_latency.observe(t_model_inference / 1000.0)
        if t_tokenize > 0:
            self.prom_tokenization_latency.observe(t_tokenize / 1000.0)
        
        total_queue = t_tokenizer_queue_wait + t_model_queue_wait
        if total_queue > 0:
            self.prom_queue_wait_latency.observe(total_queue / 1000.0)


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
        self.prom_worker_latency.labels(worker_id=str(worker_id), worker_type="model").set(latency_ms)
        self.prom_worker_requests.labels(worker_id=str(worker_id), worker_type="model").inc(num_queries)

    def record_tokenizer_worker_stats(
        self, worker_id: int, latency_ms: float, total_tokens: int = 0, num_queries: int = 1
    ) -> None:
        self.prom_worker_latency.labels(worker_id=str(worker_id), worker_type="tokenizer").set(latency_ms)
        self.prom_worker_requests.labels(worker_id=str(worker_id), worker_type="tokenizer").inc(num_queries)

    def get_summary(self) -> dict:
        return {}

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
        self.prom_gpu_memory.set(0)
        self.prom_cpu_percent.set(0)
        self.prom_tokenizer_queue_size.set(0)
        self.prom_model_queue_size.set(0)
        self.prom_batch_queue_size.set(0)
        self.prom_batch_queue_size.set(0)

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



    def is_active(self) -> bool:
        return self._is_active()



    def get_collector(self) -> MetricsCollector:
        return self._collector

    def _collection_loop(self) -> None:
        while not self._shutdown_event.is_set():
            try:
                if self.is_started:
                    self._collect_worker_metrics()
                    self._update_system_metrics()

                self._shutdown_event.wait(timeout=self._collection_interval)
            except Exception as e:
                logger.warning(f"Error in metrics collection loop: {e}")
                self._shutdown_event.wait(timeout=self._collection_interval)

    def _update_system_metrics(self) -> None:
        try:
            # CPU
            cpu_pct = self._process_monitor_service.get_cpu_percent()
            self.prom_cpu_percent.set(cpu_pct)
            
            # GPU
            gpu_mem = self.get_gpu_memory_mb()
            self.prom_gpu_memory.set(gpu_mem)
            
            # Queue sizes
            queue_info = self._get_queue_sizes(self._collector)
            self.prom_tokenizer_queue_size.set(queue_info.get("tokenizer_queue_size", 0))
            self.prom_model_queue_size.set(queue_info.get("model_queue_size", 0))
            self.prom_batch_queue_size.set(queue_info.get("batch_queue_size", 0))
        except Exception as e:
            logger.warning(f"Error updating system metrics: {e}")

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


__all__ = ["MetricsService"]
