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


class MetricsService(BaseService):
    def __init__(self, collection_interval_seconds: float = 5.0, prometheus_port: int = 8000):
        super().__init__()
        self._collector = MetricsCollector()
        self._process_monitor_service = ProcessMonitorService()
        self._orchestrator: OrchestratorService | None = None
        self._collection_interval = collection_interval_seconds
        self._collection_thread: threading.Thread | None = None
        self._shutdown_event = threading.Event()
        self._prometheus_port = prometheus_port

        self.prom_request_count = Counter("request_count", "Total number of requests")
        self.prom_request_latency = Histogram(
            "request_latency_seconds",
            "Request latency in seconds",
            buckets=[
                0.005,
                0.01,
                0.025,
                0.05,
                0.075,
                0.1,
                0.25,
                0.5,
                0.75,
                1.0,
                2.5,
                5.0,
                7.5,
                10.0,
            ],
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

        self.prom_worker_latency = Gauge(
            "worker_latency_ms", "Worker latency in ms", ["worker_id", "worker_type"]
        )
        self.prom_worker_requests = Counter(
            "worker_request_count", "Worker request count", ["worker_id", "worker_type"]
        )
        self.prom_worker_throughput = Gauge(
            "worker_throughput_qps", "Worker throughput QPS", ["worker_id", "worker_type"]
        )

        self.prom_overhead_latency = Histogram(
            "overhead_latency_seconds", "Pipeline overhead latency"
        )
        self.prom_padding_ratio = Gauge("padding_ratio", "Padding ratio (0-1)")

        self.prom_tokenizer_throughput = Gauge(
            "tokenizer_throughput_qps", "Tokenizer throughput in QPS"
        )
        self.prom_inference_throughput = Gauge(
            "inference_throughput_qps", "Inference throughput in QPS"
        )
        self.prom_overall_throughput = Gauge("overall_throughput_qps", "Overall throughput in QPS")

        self.prom_gpu_utilization = Gauge("gpu_utilization_pct", "GPU Utilization Percentage")

        self.prom_mp_queue_send_latency = Histogram(
            "mp_queue_send_latency_seconds", "Multiprocessing queue send latency"
        )
        self.prom_mp_queue_receive_latency = Histogram(
            "mp_queue_receive_latency_seconds", "Multiprocessing queue receive latency"
        )
        self.prom_grpc_serialize_latency = Histogram(
            "grpc_serialize_latency_seconds", "gRPC serialization latency"
        )
        self.prom_grpc_deserialize_latency = Histogram(
            "grpc_deserialize_latency_seconds", "gRPC deserialization latency"
        )
        self.prom_scheduler_latency = Histogram("scheduler_latency_seconds", "Scheduler latency")

        self.prom_padded_tokens = Counter("padded_tokens_total", "Total number of padded tokens")
        self.prom_total_tokens = Counter("total_tokens_total", "Total number of tokens processed")
        self.prom_max_seq_length = Gauge("max_seq_length", "Maximum sequence length")
        self.prom_avg_seq_length = Gauge("avg_seq_length", "Average sequence length")

        self.prom_tokenizer_queue_wait_latency = Histogram(
            "tokenizer_queue_wait_latency_seconds", "Tokenizer queue wait latency"
        )
        self.prom_model_queue_wait_latency = Histogram(
            "model_queue_wait_latency_seconds", "Model queue wait latency"
        )
        self.prom_pipeline_overhead_latency = Histogram(
            "pipeline_overhead_latency_seconds", "Pipeline overhead latency"
        )

    def start(self) -> None:
        self._is_started = True
        self._shutdown_event.clear()

        try:
            start_http_server(self._prometheus_port)
            logger.info(f"Prometheus metrics server started on port {self._prometheus_port}")
        except Exception as e:
            logger.warning(f"Failed to start Prometheus server: {e}")

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
        self._orchestrator = orchestrator
        self._process_monitor_service.set_inference_service(orchestrator)

    def set_tokenization_service(self, orchestrator: "OrchestratorService") -> None:
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

        self.prom_request_count.inc(num_queries)
        self.prom_request_latency.observe(duration_ms / 1000.0)

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

        if t_mp_queue_send > 0:
            self.prom_mp_queue_send_latency.observe(t_mp_queue_send / 1000.0)
        if t_mp_queue_receive > 0:
            self.prom_mp_queue_receive_latency.observe(t_mp_queue_receive / 1000.0)
        if t_grpc_serialize > 0:
            self.prom_grpc_serialize_latency.observe(t_grpc_serialize / 1000.0)
        if t_grpc_deserialize > 0:
            self.prom_grpc_deserialize_latency.observe(t_grpc_deserialize / 1000.0)
        if t_scheduler > 0:
            self.prom_scheduler_latency.observe(t_scheduler / 1000.0)

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

    def record_worker_stats(
        self, worker_id: int, latency_ms: float, num_queries: int = 1, throughput_qps: float = 0.0
    ) -> None:
        self.prom_worker_latency.labels(worker_id=str(worker_id), worker_type="model").set(
            latency_ms
        )
        self.prom_worker_requests.labels(worker_id=str(worker_id), worker_type="model").inc(
            num_queries
        )
        if throughput_qps > 0:
            self.prom_worker_throughput.labels(worker_id=str(worker_id), worker_type="model").set(
                throughput_qps
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

    def record_throughput_stats(
        self, tokenizer_qps: float = 0.0, inference_qps: float = 0.0, overall_qps: float = 0.0
    ) -> None:
        if tokenizer_qps > 0:
            self.prom_tokenizer_throughput.set(tokenizer_qps)
        if inference_qps > 0:
            self.prom_inference_throughput.set(inference_qps)
        if overall_qps > 0:
            self.prom_overall_throughput.set(overall_qps)

    def record_gpu_utilization(self, gpu_utilization_pct: float = 0.0) -> None:
        if gpu_utilization_pct >= 0:
            self.prom_gpu_utilization.set(gpu_utilization_pct)

    def _get_queue_sizes(self, collector: MetricsCollector) -> dict:
        tokenizer_queue_size = 0
        model_queue_size = 0

        if collector._tokenizer_pool:
            try:
                info = collector._tokenizer_pool.get_info()
                tokenizer_queue_size = info.get("total_queue_size", 0)
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
            cpu_pct = self._process_monitor_service.get_cpu_percent()
            self.prom_cpu_percent.set(cpu_pct)

            gpu_mem = self.get_gpu_memory_mb()
            self.prom_gpu_memory.set(gpu_mem)

            # Try to get GPU utilization if available
            try:
                gpu_util = self._process_monitor_service.get_gpu_utilization()
                if gpu_util is not None:
                    self.record_gpu_utilization(gpu_util)
            except (AttributeError, NotImplementedError):
                pass

            queue_info = self._get_queue_sizes(self._collector)
            self.prom_tokenizer_queue_size.set(queue_info.get("tokenizer_queue_size", 0))
            self.prom_model_queue_size.set(queue_info.get("model_queue_size", 0))
            self.prom_batch_queue_size.set(queue_info.get("batch_queue_size", 0))

            # Record throughput stats from pools
            if self._orchestrator:
                try:
                    tokenizer_qps = (
                        self._orchestrator.tokenizer_pool.get_aggregate_throughput_qps()
                        if self._orchestrator.tokenizer_pool
                        else 0.0
                    )
                    inference_qps = (
                        self._orchestrator.pool.get_aggregate_throughput_qps()
                        if self._orchestrator.pool
                        else 0.0
                    )
                    overall_qps = tokenizer_qps + inference_qps
                    self.record_throughput_stats(tokenizer_qps, inference_qps, overall_qps)
                except Exception as e:
                    logger.debug(f"Could not record throughput stats: {e}")
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
                            throughput_qps = worker_metrics.get("throughput_qps", 0.0)
                            if latency_ms > 0 and query_count > 0:
                                self.record_worker_stats(
                                    worker_id, latency_ms, query_count, throughput_qps
                                )
            except Exception as e:
                logger.warning(f"Failed to collect inference worker metrics: {e}")

        if self._orchestrator and self._orchestrator.tokenization_is_started:
            try:
                tokenizer_worker_metrics = self._orchestrator.get_tokenizer_worker_metrics()
                for worker_metrics in tokenizer_worker_metrics:
                    if worker_metrics:
                        worker_id = worker_metrics.get("worker_id", -1)
                        if worker_id >= 0:
                            latency_ms = worker_metrics.get("avg_ms", 0.0)
                            num_queries = worker_metrics.get("query_count", 0)
                            if latency_ms > 0 and num_queries > 0:
                                self.record_tokenizer_worker_stats(
                                    worker_id, latency_ms, 0, num_queries
                                )
            except Exception as e:
                logger.warning(f"Failed to collect tokenizer worker metrics: {e}")


__all__ = ["MetricsService"]
