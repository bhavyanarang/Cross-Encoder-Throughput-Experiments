import logging
import signal
import sys
import threading
from typing import Optional

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
            backend=(
                self.config.model_pool.instances[0].backend
                if self.config.model_pool.instances
                else "pytorch"
            ),
            device=(
                self.config.model_pool.instances[0].device
                if self.config.model_pool.instances
                else "cpu"
            ),
        )

        self.pipeline = QueueBasedPipeline(
            config=self.config,
            tokenizer_pool=self.tokenizer_pool,
            model_pool=self.pool,
            metrics_service=self.metrics,
            experiment_name=self.experiment_name,
        )
        self.pipeline.setup()

        logger.info("Orchestrator setup complete - pipeline architecture ready")

    def start(self) -> None:
        def handle_signal(signum, frame):
            logger.info("Shutdown signal received")
            self.shutdown_event.set()
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

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
        if self.pipeline:
            return self.pipeline.get_tokenizer_worker_metrics()
        return []

    def reset_tokenizer_worker_metrics(self) -> None:
        if self.pipeline:
            self.pipeline.reset_tokenizer_worker_metrics()

    @property
    def tokenization_is_started(self) -> bool:
        return self.pipeline.tokenization_is_started if self.pipeline else False

    def get_gpu_memory_mb(self) -> float:
        if self.pipeline:
            return self.pipeline.get_gpu_memory_mb()
        return 0.0

    def get_inference_worker_metrics(self) -> list[dict]:
        if self.pipeline:
            return self.pipeline.get_inference_worker_metrics()
        return []

    def reset_inference_worker_metrics(self) -> None:
        if self.pipeline:
            self.pipeline.reset_inference_worker_metrics()

    @property
    def inference_is_started(self) -> bool:
        return self.pipeline.inference_is_started if self.pipeline else False

    @property
    def is_started(self) -> bool:
        return self.pipeline.is_started if self.pipeline else False

    def get_worker_metrics(self) -> list[dict]:
        if self.pipeline:
            return self.pipeline.get_worker_metrics()
        return []

    def reset_worker_metrics(self) -> None:
        if self.pipeline:
            self.pipeline.reset_worker_metrics()

    @property
    def tokenization_service(self):
        return self

    @property
    def inference_service(self):
        return self

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
    def _batching_enabled(self) -> bool:
        if self.pipeline:
            return self.pipeline._batching_enabled
        return False

    @property
    def _max_batch_size(self) -> int:
        if self.pipeline:
            return self.pipeline._max_batch_size
        return self.config.batching.max_batch_size

    @property
    def _timeout_ms(self) -> float:
        if self.pipeline:
            return self.pipeline._timeout_ms
        return self.config.batching.timeout_ms

    @property
    def _batch_thread(self) -> Optional[threading.Thread]:
        if self.pipeline:
            return self.pipeline._batch_thread
        return None

    @property
    def _batch_queue(self):
        if self.pipeline:
            return self.pipeline._batch_queue
        if not hasattr(self, "_dummy_batch_queue"):
            import queue

            self._dummy_batch_queue = queue.Queue()
        return self._dummy_batch_queue

    @property
    def _inference_queue(self):
        if self.pipeline:
            return self.pipeline._inference_queue
        return None

    @property
    def _tokenization_started(self) -> bool:
        if self.pipeline:
            return self.pipeline._tokenization_started
        if not hasattr(self, "_local_tokenization_started"):
            self._local_tokenization_started = False
        return self._local_tokenization_started

    @_tokenization_started.setter
    def _tokenization_started(self, value: bool) -> None:
        if self.pipeline:
            self.pipeline._tokenization_started = value
        else:
            self._local_tokenization_started = value

    @property
    def _inference_started(self) -> bool:
        if self.pipeline:
            return self.pipeline._inference_started
        if not hasattr(self, "_local_inference_started"):
            self._local_inference_started = False
        return self._local_inference_started

    @_inference_started.setter
    def _inference_started(self, value: bool) -> None:
        if self.pipeline:
            self.pipeline._inference_started = value
        else:
            self._local_inference_started = value


__all__ = [
    "OrchestratorService",
]
