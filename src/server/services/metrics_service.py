import logging
import threading
from typing import TYPE_CHECKING

from prometheus_client import Counter, Gauge, Histogram, start_http_server

from src.server.dto.metrics import MetricsCollector
from src.server.services.process_monitor_service import ProcessMonitorService
from src.server.services.service_base import BaseService

if TYPE_CHECKING:
    from src.server.services.orchestrator_service import OrchestratorService

logger = logging.getLogger(__name__)

LATENCY_BUCKETS = [0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]


class MetricsService(BaseService):
    def __init__(self, collection_interval_seconds: float = 1.0, prometheus_port: int = 8000):
        super().__init__()
        self._collector = MetricsCollector()
        self._process_monitor = ProcessMonitorService()
        self._orchestrator: OrchestratorService | None = None
        self._collection_interval = collection_interval_seconds
        self._collection_thread: threading.Thread | None = None
        self._shutdown_event = threading.Event()
        self._prometheus_port = prometheus_port

        self.prom_request_count = Counter("request_count", "Total requests")
        self.prom_request_latency = Histogram(
            "request_latency_seconds", "Request latency", buckets=LATENCY_BUCKETS
        )
        self.prom_inference_latency = Histogram("inference_latency_seconds", "Inference latency")
        self.prom_tokenization_latency = Histogram(
            "tokenization_latency_seconds", "Tokenization latency"
        )
        self.prom_queue_wait_latency = Histogram("queue_wait_latency_seconds", "Queue wait latency")
        self.prom_tokenizer_queue_wait_latency = Histogram(
            "tokenizer_queue_wait_latency_seconds", "Tokenizer queue wait"
        )
        self.prom_model_queue_wait_latency = Histogram(
            "model_queue_wait_latency_seconds", "Model queue wait"
        )
        self.prom_pipeline_overhead_latency = Histogram(
            "pipeline_overhead_latency_seconds", "Pipeline overhead"
        )

        self.prom_gpu_memory = Gauge("gpu_memory_mb", "GPU Memory MB")
        self.prom_cpu_percent = Gauge("cpu_percent", "CPU %")
        self.prom_tokenizer_queue_size = Gauge("tokenizer_queue_size", "Tokenizer Queue Size")
        self.prom_model_queue_size = Gauge("model_queue_size", "Model Queue Size")
        self.prom_batch_queue_size = Gauge("batch_queue_size", "Batch Queue Size")
        self.prom_padding_ratio = Gauge("padding_ratio", "Padding ratio")
        self.prom_max_seq_length = Gauge("max_seq_length", "Max sequence length")
        self.prom_avg_seq_length = Gauge("avg_seq_length", "Avg sequence length")

        self.prom_worker_latency = Gauge(
            "worker_latency_ms", "Worker latency ms", ["worker_id", "worker_type"]
        )
        self.prom_worker_requests = Counter(
            "worker_request_count", "Worker requests", ["worker_id", "worker_type"]
        )
        self.prom_worker_tokens = Counter(
            "worker_tokens", "Worker tokens", ["worker_id", "worker_type"]
        )

        self.prom_padded_tokens = Counter("padded_tokens_total", "Padded tokens")
        self.prom_total_tokens = Counter("total_tokens_total", "Total tokens")

    def start(self) -> None:
        self._is_started = True
        self._shutdown_event.clear()
        try:
            start_http_server(self._prometheus_port)
            logger.info(f"Prometheus metrics server started on port {self._prometheus_port}")
        except Exception as e:
            logger.warning(f"Failed to start Prometheus server: {e}")

        if self._orchestrator:
            self._collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
            self._collection_thread.start()
            logger.info(f"MetricsService started (interval: {self._collection_interval}s)")
        else:
            logger.info("MetricsService started")

    def stop(self) -> None:
        self._is_started = False
        self._shutdown_event.set()
        if self._collection_thread:
            self._collection_thread.join(timeout=2.0)
            self._collection_thread = None
        logger.info("MetricsService stopped")

    def set_inference_service(self, orchestrator: "OrchestratorService") -> None:
        self._orchestrator = orchestrator
        self._process_monitor.set_inference_service(orchestrator)

    def set_tokenization_service(self, orchestrator: "OrchestratorService") -> None:
        self._orchestrator = orchestrator

    def set_model_pool(self, pool) -> None:
        self._process_monitor.set_pool(pool)
        self._collector.set_pool(pool)

    def set_tokenizer_pool(self, pool) -> None:
        self._collector.set_tokenizer_pool(pool)

    def set_experiment_info(
        self, name: str = "", description: str = "", backend: str = "", device: str = ""
    ) -> None:
        self._collector.set_experiment_info(name, description, backend, device)

    def record(self, duration_ms: float, num_queries: int = 1) -> None:
        self.prom_request_count.inc(num_queries)
        self.prom_request_latency.observe(duration_ms / 1000.0)

    def record_stage_timings(
        self,
        t_tokenize: float = 0.0,
        t_tokenizer_queue_wait: float = 0.0,
        t_model_queue_wait: float = 0.0,
        t_model_inference: float = 0.0,
        t_overhead: float = 0.0,
        **kwargs,
    ) -> None:
        if t_model_inference > 0:
            self.prom_inference_latency.observe(t_model_inference / 1000.0)
        if t_tokenize > 0:
            self.prom_tokenization_latency.observe(t_tokenize / 1000.0)
        if t_tokenizer_queue_wait > 0:
            self.prom_tokenizer_queue_wait_latency.observe(t_tokenizer_queue_wait / 1000.0)
        if t_model_queue_wait > 0:
            self.prom_model_queue_wait_latency.observe(t_model_queue_wait / 1000.0)
        total_queue = t_tokenizer_queue_wait + t_model_queue_wait
        if total_queue > 0:
            self.prom_queue_wait_latency.observe(total_queue / 1000.0)
        if t_overhead > 0:
            self.prom_pipeline_overhead_latency.observe(t_overhead / 1000.0)

    def record_padding_stats(
        self,
        padding_ratio: float = 0.0,
        padded_tokens: int = 0,
        total_tokens: int = 0,
        max_seq_length: int = 0,
        avg_seq_length: float = 0.0,
    ) -> None:
        if padding_ratio >= 0:
            self.prom_padding_ratio.set(padding_ratio)
        if padded_tokens > 0:
            self.prom_padded_tokens.inc(padded_tokens)
        if total_tokens > 0:
            self.prom_total_tokens.inc(total_tokens)
        if max_seq_length > 0:
            self.prom_max_seq_length.set(max_seq_length)
        if avg_seq_length > 0:
            self.prom_avg_seq_length.set(avg_seq_length)

    def record_worker_stats(self, worker_id: int, latency_ms: float, num_queries: int = 1) -> None:
        self.prom_worker_latency.labels(worker_id=str(worker_id), worker_type="model").set(
            latency_ms
        )
        self.prom_worker_requests.labels(worker_id=str(worker_id), worker_type="model").inc(
            num_queries
        )

    def record_tokenizer_worker_stats(
        self, worker_id: int, latency_ms: float, total_tokens: int = 0, num_queries: int = 1
    ) -> None:
        self.prom_worker_latency.labels(worker_id=str(worker_id), worker_type="tokenizer").set(
            latency_ms
        )
        self.prom_worker_requests.labels(worker_id=str(worker_id), worker_type="tokenizer").inc(
            num_queries
        )
        if total_tokens > 0:
            self.prom_worker_tokens.labels(worker_id=str(worker_id), worker_type="tokenizer").inc(
                total_tokens
            )

    def _get_queue_sizes(self) -> dict:
        tokenizer_queue_size = model_queue_size = batch_queue_size = 0
        if self._collector._tokenizer_pool:
            try:
                info = self._collector._tokenizer_pool.get_info()
                tokenizer_queue_size = info.get("total_queue_size", 0)
            except Exception:
                pass
        if self._collector._model_pool:
            try:
                info = self._collector._model_pool.get_info()
                model_queue_size = info.get("queue_size", 0)
            except Exception:
                pass
        if self._orchestrator:
            batch_queue_size = self._orchestrator.get_batching_info().get("pending", 0)
        return {
            "tokenizer_queue_size": tokenizer_queue_size,
            "model_queue_size": model_queue_size,
            "batch_queue_size": batch_queue_size,
        }

    def reset(self) -> None:
        self.prom_gpu_memory.set(0)
        self.prom_cpu_percent.set(0)
        self.prom_tokenizer_queue_size.set(0)
        self.prom_model_queue_size.set(0)
        self.prom_batch_queue_size.set(0)

    def get_gpu_memory_mb(self) -> float:
        return self._process_monitor.get_gpu_memory_mb()

    def get_collector(self) -> MetricsCollector:
        return self._collector

    def _collection_loop(self) -> None:
        while not self._shutdown_event.is_set():
            try:
                if self.is_started:
                    self._update_system_metrics()
                self._shutdown_event.wait(timeout=self._collection_interval)
            except Exception as e:
                logger.warning(f"Error in metrics collection loop: {e}")
                self._shutdown_event.wait(timeout=self._collection_interval)

    def _update_system_metrics(self) -> None:
        try:
            self.prom_cpu_percent.set(self._process_monitor.get_cpu_percent())
            self.prom_gpu_memory.set(self._process_monitor.get_gpu_memory_mb())
            queue_info = self._get_queue_sizes()
            self.prom_tokenizer_queue_size.set(queue_info["tokenizer_queue_size"])
            self.prom_model_queue_size.set(queue_info["model_queue_size"])
            self.prom_batch_queue_size.set(queue_info["batch_queue_size"])
        except Exception as e:
            logger.warning(f"Error updating system metrics: {e}")


__all__ = ["MetricsService"]
