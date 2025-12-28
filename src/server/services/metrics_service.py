import logging
import threading
from typing import TYPE_CHECKING

from src.server.dto.metrics import MetricsCollector
from src.server.services.service_base import BaseService

if TYPE_CHECKING:
    from src.server.services.inference_service import InferenceService
    from src.server.services.tokenization_service import TokenizationService

logger = logging.getLogger(__name__)


class MetricsService(BaseService):
    def __init__(self, collection_interval_seconds: float = 5.0):
        super().__init__()
        self._collector = MetricsCollector()
        self._inference_service: InferenceService | None = None
        self._tokenization_service: TokenizationService | None = None
        self._collection_interval = collection_interval_seconds
        self._collection_thread: threading.Thread | None = None
        self._shutdown_event = threading.Event()

    def start(self) -> None:
        self._is_started = True
        self._shutdown_event.clear()

        if self._inference_service or self._tokenization_service:
            self._collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
            self._collection_thread.start()
            logger.info(
                f"MetricsService started with worker metrics collection "
                f"(interval: {self._collection_interval}s)"
            )
        else:
            logger.info("MetricsService started (no services registered for worker metrics)")

    def stop(self) -> None:
        self._is_started = False
        self._shutdown_event.set()

        if self._collection_thread:
            self._collection_thread.join(timeout=2.0)
            self._collection_thread = None

        logger.info("MetricsService stopped")

    def set_inference_service(self, inference_service: "InferenceService") -> None:
        self._inference_service = inference_service
        self._collector.set_inference_service(inference_service)

    def set_tokenization_service(self, tokenization_service: "TokenizationService") -> None:
        self._tokenization_service = tokenization_service

    def set_experiment_info(
        self, name: str = "", description: str = "", backend: str = "", device: str = ""
    ) -> None:
        self._collector.set_experiment_info(name, description, backend, device)

    def record(self, duration_ms: float, num_queries: int = 1) -> None:
        self._collector.record(duration_ms, num_queries)

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
        self._collector.record_stage_timings(
            t_tokenize=t_tokenize,
            t_queue_wait=t_queue_wait,
            t_model_inference=t_model_inference,
            t_overhead=t_overhead,
            t_mp_queue_send=t_mp_queue_send,
            t_mp_queue_receive=t_mp_queue_receive,
            t_grpc_serialize=t_grpc_serialize,
            t_grpc_deserialize=t_grpc_deserialize,
            t_scheduler=t_scheduler,
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
        self._collector.record_worker_stats(worker_id, latency_ms, num_queries)

    def record_tokenizer_worker_stats(
        self, worker_id: int, latency_ms: float, total_tokens: int = 0
    ) -> None:
        self._collector.record_tokenizer_worker_stats(worker_id, latency_ms, total_tokens)

    def get_summary(self) -> dict:
        return self._collector.summary()

    def reset(self) -> None:
        self._collector.reset()

        if self._inference_service and self._inference_service.is_started:
            try:
                self._inference_service.reset_worker_metrics()
            except Exception as e:
                logger.warning(f"Failed to reset inference worker metrics: {e}")

        if self._tokenization_service and self._tokenization_service.is_started:
            try:
                self._tokenization_service.reset_worker_metrics()
            except Exception as e:
                logger.warning(f"Failed to reset tokenizer worker metrics: {e}")

    def get_gpu_memory_mb(self) -> float:
        return self._collector.get_gpu_memory_mb()

    def get_gpu_utilization_pct(self) -> float:
        return self._collector.get_gpu_utilization_pct()

    def is_active(self) -> bool:
        return self._collector.is_active()

    @property
    def last_latency_ms(self) -> float:
        return self._collector.last_latency_ms

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
        if self._inference_service and self._inference_service.is_started:
            try:
                inference_worker_metrics = self._inference_service.get_worker_metrics()
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

        if self._tokenization_service and self._tokenization_service.is_started:
            try:
                tokenizer_worker_metrics = self._tokenization_service.get_worker_metrics()
                for worker_metrics in tokenizer_worker_metrics:
                    if worker_metrics:
                        worker_id = worker_metrics.get("worker_id", -1)
                        if worker_id >= 0:
                            latency_ms = worker_metrics.get("avg_ms", 0.0)
                            total_tokens = worker_metrics.get("total_tokens_processed", 0)
                            if latency_ms > 0:
                                self.record_tokenizer_worker_stats(
                                    worker_id, latency_ms, total_tokens
                                )
            except Exception as e:
                logger.warning(f"Failed to collect tokenizer worker metrics: {e}")


__all__ = ["MetricsService"]
