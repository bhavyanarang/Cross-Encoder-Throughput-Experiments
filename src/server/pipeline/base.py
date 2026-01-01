"""
Base pipeline class defining the interface for different pipeline implementations.
"""

import logging
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
    """
    Abstract base class for pipeline implementations.

    A pipeline orchestrates the flow of requests through tokenization and inference stages.
    Different implementations can use different strategies (queue-based, synchronous, etc.).
    """

    def __init__(
        self,
        config: "Config",
        tokenizer_pool: "TokenizerPool",
        model_pool: "ModelPool",
        metrics_service: "MetricsService",
        experiment_name: str = "default",
    ):
        """
        Initialize the pipeline.

        Args:
            config: Configuration object
            tokenizer_pool: Tokenizer worker pool
            model_pool: Model inference worker pool
            metrics_service: Metrics collection service
            experiment_name: Name of the experiment for logging
        """
        self.config = config
        self.tokenizer_pool = tokenizer_pool
        self.model_pool = model_pool
        self.metrics = metrics_service
        self.experiment_name = experiment_name
        self.shutdown_event = threading.Event()
        self._tokenization_started = False
        self._inference_started = False

        # Common request tracking
        self._next_request_id_counter = count()
        self._pending_requests: dict[int, PipelineRequest] = {}
        self._pending_requests_lock = threading.Lock()

        # Metrics/Logging
        self._request_count = 0
        self._request_count_lock = threading.Lock()
        self._last_log_time = time.time()
        self._requests_in_window = 0
        self._pairs_in_window = 0

    def _get_next_request_id(self) -> int:
        """Get the next unique request ID."""
        return next(self._next_request_id_counter)

    def _track_request_metrics(self, num_pairs: int) -> None:
        """Track metrics for incoming request."""
        with self._request_count_lock:
            self._request_count += 1
            self._requests_in_window += 1
            self._pairs_in_window += num_pairs
            current_time = time.time()
            time_elapsed = current_time - self._last_log_time

            if time_elapsed >= 1.0:
                self._last_log_time = current_time
                self._requests_in_window = 0
                self._pairs_in_window = 0

    def _create_request(self, pairs: list[tuple[str, str]]) -> "PipelineRequest":
        """Create and register a new pipeline request."""
        from src.server.dto.pipeline import PipelineRequest

        self._track_request_metrics(len(pairs))
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
        """Remove request from pending list."""
        with self._pending_requests_lock:
            self._pending_requests.pop(req_id, None)

    @abstractmethod
    def setup(self) -> None:
        """
        Set up the pipeline infrastructure.

        This should initialize any worker threads, queues, or other resources
        needed by the pipeline.
        """
        pass

    def _setup_signal_handlers(self) -> None:
        """
        Set up signal handlers for graceful shutdown.

        This is called in start() to handle SIGINT and SIGTERM.
        """

        def handle_signal(signum, frame):
            logger.info("Shutdown signal received")
            self.shutdown_event.set()
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

    @abstractmethod
    def start(self) -> None:
        """
        Start the pipeline services.

        This should start tokenizer pool, model pool, metrics, and dashboard
        according to the configured pipeline mode.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the pipeline services gracefully.

        This should shut down all worker pools, queues, and services.
        """
        pass

    @abstractmethod
    def schedule(self, pairs: list[tuple[str, str]]) -> "InferenceResult":
        """
        Schedule a request for processing through the pipeline.

        Args:
            pairs: List of (query, document) string pairs to process

        Returns:
            InferenceResult with scores and timing information

        Raises:
            RuntimeError: If the pipeline is not properly initialized or times out
        """
        pass

    @property
    def tokenization_is_started(self) -> bool:
        """Check if tokenization service is running."""
        return self._tokenization_started

    @property
    def inference_is_started(self) -> bool:
        """Check if inference service is running."""
        return self._inference_started

    @property
    def is_started(self) -> bool:
        """Check if all required services are running."""
        return self._tokenization_started and self._inference_started

    def get_batching_info(self) -> dict:
        """Get information about batching configuration."""
        return {}

    def get_metrics(self) -> "MetricsService":
        """Get the metrics service."""
        if self.metrics is None:
            raise RuntimeError("Pipeline not set up. Call setup() first.")
        return self.metrics

    def get_tokenizer_worker_metrics(self) -> list[dict]:
        """Get metrics for tokenizer workers."""
        if not self._tokenization_started:
            return []
        return self.tokenizer_pool.get_worker_metrics()

    def reset_tokenizer_worker_metrics(self) -> None:
        """Reset tokenizer worker metrics."""
        if self._tokenization_started:
            self.tokenizer_pool.reset_worker_metrics()

    def get_inference_worker_metrics(self) -> list[dict]:
        """Get metrics for inference workers."""
        if not self._inference_started:
            return []
        return self.model_pool.get_worker_metrics()

    def reset_inference_worker_metrics(self) -> None:
        """Reset inference worker metrics."""
        if self._inference_started:
            self.model_pool.reset_worker_metrics()

    def get_worker_metrics(self) -> list[dict]:
        """Get worker metrics (defaults to tokenizer)."""
        return self.get_tokenizer_worker_metrics()

    def reset_worker_metrics(self) -> None:
        """Reset worker metrics (defaults to tokenizer)."""
        self.reset_tokenizer_worker_metrics()

    def get_gpu_memory_mb(self) -> float:
        """Get GPU memory usage in MB."""
        if not self._inference_started:
            return 0.0
        return self.model_pool.get_gpu_memory_mb()

    @property
    def tokenization_service(self):
        """Return self as tokenization service."""
        return self

    @property
    def inference_service(self):
        """Return self as inference service."""
        return self
