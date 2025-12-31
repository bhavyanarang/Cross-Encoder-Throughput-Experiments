"""Model worker for inference tasks."""

import logging
import time

from src.server.dto import ModelConfig, WorkItem, WorkResult
from src.server.dto.metrics.worker import WorkerMetrics
from src.server.worker.base import BaseWorker, get_worker_gpu_memory, setup_worker_environment

logger = logging.getLogger(__name__)


class ModelWorker(BaseWorker[WorkItem, WorkResult]):
    def __init__(self, worker_id: int, config: ModelConfig, metrics=None):
        if metrics is None:
            metrics = WorkerMetrics(worker_id=worker_id)
        super().__init__(worker_id, metrics=metrics)
        self.config = config
        self._backend = None

    def initialize(self) -> None:
        setup_worker_environment()
        from src.server.backends import create_backend
        self._backend = create_backend(self.config)
        self._backend.load_model()
        self._backend.warmup(3)

        try:
            initial_mem = get_worker_gpu_memory()
            logger.info(f"Worker {self.worker_id} ready - GPU memory: {initial_mem:.2f} MB")
        except Exception:
            pass

        self.set_ready()

    def process(self, work_item: WorkItem) -> WorkResult:
        if not self._backend:
            raise RuntimeError(f"Model worker {self.worker_id} not initialized")

        time.perf_counter()
        result = self._backend.infer_with_tokenized(work_item.tokenized_batch)
        latency_ms = result.t_model_inference_ms

        self._record_metrics(
            latency_ms=latency_ms,
            num_queries=result.batch_size,
        )

        return WorkResult(
            req_id=work_item.req_id,
            scores=result.scores,
            worker_id=self.worker_id,
            t_tokenize_ms=0.0,
            t_model_inference_ms=result.t_model_inference_ms,
            t_queue_wait_ms=0.0,
            total_ms=result.t_model_inference_ms,
            total_tokens=result.total_tokens,
            real_tokens=result.real_tokens,
            padded_tokens=result.padded_tokens,
            padding_ratio=result.padding_ratio,
            max_seq_length=result.max_seq_length,
            avg_seq_length=result.avg_seq_length,
            batch_size=result.batch_size,
        )

    def get_memory_mb(self) -> float:
        return get_worker_gpu_memory()


__all__ = ["ModelWorker"]
