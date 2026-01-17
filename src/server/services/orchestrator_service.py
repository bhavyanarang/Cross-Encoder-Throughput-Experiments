import logging
import threading

from src.server.dto import Config, InferenceResult
from src.server.pipeline.queue_based import QueueBasedPipeline
from src.server.pool import ModelPool, TokenizerPool
from src.server.services.metrics_service import MetricsService

logger = logging.getLogger(__name__)


class OrchestratorService:
    def __init__(self, config: Config, experiment_name: str = "default"):
        self.config = config
        self.experiment_name = experiment_name
        self.shutdown_event = threading.Event()
        self.tokenizer_pool = None
        self.pool = None
        self.metrics = None
        self.pipeline = None

    def setup(self) -> None:
        logger.info(f"Setting up orchestrator for experiment: {self.experiment_name}")

        tokenizer_model = self.config.tokenizer_pool.model_name
        if not tokenizer_model and self.config.model_pool.instances:
            tokenizer_model = self.config.model_pool.instances[0].name

        self.tokenizer_pool = TokenizerPool(
            model_name=tokenizer_model,
            num_workers=self.config.tokenizer_pool.num_workers,
            max_length=512,
        )
        self.pool = ModelPool(self.config.model_pool)
        self.metrics = MetricsService(prometheus_port=self.config.server.prometheus_port)
        self.metrics.set_inference_service(self)
        self.metrics.set_tokenization_service(self)
        self.metrics.set_model_pool(self.pool)
        self.metrics.set_tokenizer_pool(self.tokenizer_pool)
        self.metrics.set_experiment_info(
            name=self.experiment_name,
            description=self.config.description,
            backend=self.config.model_pool.instances[0].backend
            if self.config.model_pool.instances
            else "pytorch",
            device=self.config.model_pool.instances[0].device
            if self.config.model_pool.instances
            else "cpu",
        )

        self.pipeline = QueueBasedPipeline(
            config=self.config,
            tokenizer_pool=self.tokenizer_pool,
            model_pool=self.pool,
            metrics_service=self.metrics,
            experiment_name=self.experiment_name,
        )
        self.pipeline.setup()
        logger.info("Orchestrator setup complete")

    def start(self) -> None:
        if self.pipeline:
            self.pipeline.start()

    def stop(self) -> None:
        self.shutdown_event.set()
        if self.pipeline:
            self.pipeline.stop()

    def schedule(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        if not self.pipeline:
            raise RuntimeError("Pipeline not initialized")
        return self.pipeline.schedule(pairs)

    def get_metrics(self) -> MetricsService:
        if self.metrics is None:
            raise RuntimeError("Orchestrator not set up. Call setup() first.")
        return self.metrics

    def get_tokenizer_worker_metrics(self) -> list[dict]:
        return self.pipeline.get_tokenizer_worker_metrics() if self.pipeline else []

    def get_gpu_memory_mb(self) -> float:
        return self.pipeline.get_gpu_memory_mb() if self.pipeline else 0.0

    def get_inference_worker_metrics(self) -> list[dict]:
        return self.pipeline.get_inference_worker_metrics() if self.pipeline else []

    def get_worker_metrics(self) -> list[dict]:
        return self.pipeline.get_worker_metrics() if self.pipeline else []

    def get_batching_info(self) -> dict:
        if self.pipeline:
            return self.pipeline.get_batching_info()
        return {
            "batching_enabled": False,
            "max_batch_size": 0,
            "timeout_ms": 0,
            "length_aware": False,
            "pending": 0,
        }

    @property
    def is_started(self) -> bool:
        return self.pipeline.is_started if self.pipeline else False

    @property
    def tokenization_is_started(self) -> bool:
        return self.pipeline.tokenization_is_started if self.pipeline else False

    @property
    def inference_is_started(self) -> bool:
        return self.pipeline.inference_is_started if self.pipeline else False

    @property
    def _batching_enabled(self) -> bool:
        return self.pipeline._batching_enabled if self.pipeline else False

    @property
    def _max_batch_size(self) -> int:
        return (
            self.pipeline._max_batch_size if self.pipeline else self.config.batching.max_batch_size
        )

    @property
    def _timeout_ms(self) -> float:
        return self.pipeline._timeout_ms if self.pipeline else self.config.batching.timeout_ms

    @property
    def _batch_thread(self):
        return self.pipeline._batch_thread if self.pipeline else None

    @property
    def _batch_queue(self):
        return self.pipeline._batch_queue if self.pipeline else None

    @property
    def _inference_queue(self):
        return self.pipeline._inference_queue if self.pipeline else None

    @property
    def _tokenization_started(self) -> bool:
        return (
            self.pipeline._tokenization_started
            if self.pipeline
            else getattr(self, "_local_tokenization_started", False)
        )

    @_tokenization_started.setter
    def _tokenization_started(self, value: bool) -> None:
        if self.pipeline:
            self.pipeline._tokenization_started = value
        else:
            self._local_tokenization_started = value

    @property
    def _inference_started(self) -> bool:
        return (
            self.pipeline._inference_started
            if self.pipeline
            else getattr(self, "_local_inference_started", False)
        )

    @_inference_started.setter
    def _inference_started(self, value: bool) -> None:
        if self.pipeline:
            self.pipeline._inference_started = value
        else:
            self._local_inference_started = value

    @property
    def tokenization_service(self):
        return self

    @property
    def inference_service(self):
        return self


__all__ = ["OrchestratorService"]
