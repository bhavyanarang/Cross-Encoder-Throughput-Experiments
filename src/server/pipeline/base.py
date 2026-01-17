import logging
import os
import signal
import sys
import threading
import time
from abc import ABC, abstractmethod
from itertools import count
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.server.dto import Config, InferenceResult
    from src.server.dto.pipeline import PipelineRequest
    from src.server.pool import ModelPool, TokenizerPool
    from src.server.services import MetricsService

logger = logging.getLogger(__name__)


class BasePipeline(ABC):
    def __init__(
        self,
        config: "Config",
        tokenizer_pool: "TokenizerPool",
        model_pool: "ModelPool",
        metrics_service: "MetricsService",
        experiment_name: str = "default",
    ):
        self.config = config
        self.tokenizer_pool = tokenizer_pool
        self.model_pool = model_pool
        self.metrics = metrics_service
        self.experiment_name = experiment_name
        self.shutdown_event = threading.Event()
        self._tokenization_started = False
        self._inference_started = False

        self._next_request_id_counter = count()
        self._pending_requests: dict[int, PipelineRequest] = {}
        self._pending_requests_lock = threading.Lock()

    def _get_next_request_id(self) -> int:
        return next(self._next_request_id_counter)

    def _create_request(self, pairs: list[tuple[str, str]]) -> "PipelineRequest":
        from src.server.dto.pipeline import PipelineRequest

        req_id = self._get_next_request_id()
        request = PipelineRequest(
            request_id=req_id,
            pairs=pairs,
            submit_time=time.perf_counter(),
        )

        with self._pending_requests_lock:
            self._pending_requests[req_id] = request

        return request

    def _cleanup_request(self, req_id: int) -> None:
        with self._pending_requests_lock:
            self._pending_requests.pop(req_id, None)

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    def _setup_signal_handlers(self) -> None:
        if os.getenv("PYTEST_CURRENT_TEST"):
            return

        def handle_signal(signum, frame):
            logger.info("Shutdown signal received")
            self.shutdown_event.set()
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def schedule(self, pairs: list[tuple[str, str]]) -> "InferenceResult":
        raise NotImplementedError

    @property
    def tokenization_is_started(self) -> bool:
        return self._tokenization_started

    @property
    def inference_is_started(self) -> bool:
        return self._inference_started

    @property
    def is_started(self) -> bool:
        return self._tokenization_started and self._inference_started

    def get_batching_info(self) -> dict:
        return {}

    def get_metrics(self) -> "MetricsService":
        if self.metrics is None:
            raise RuntimeError("Pipeline not set up. Call setup() first.")
        return self.metrics

    def get_tokenizer_worker_metrics(self) -> list[dict]:
        if not self._tokenization_started:
            return []
        return self.tokenizer_pool.get_worker_metrics()

    def get_inference_worker_metrics(self) -> list[dict]:
        if not self._inference_started:
            return []
        return self.model_pool.get_worker_metrics()

    def get_worker_metrics(self) -> list[dict]:
        return self.get_tokenizer_worker_metrics()

    def get_gpu_memory_mb(self) -> float:
        if not self._inference_started:
            return 0.0
        return self.model_pool.get_gpu_memory_mb()

    @property
    def tokenization_service(self):
        return self

    @property
    def inference_service(self):
        return self
