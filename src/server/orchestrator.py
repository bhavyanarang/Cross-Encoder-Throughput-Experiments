"""Server orchestrator for managing all components."""

import logging
import signal
import sys
import threading
from typing import Protocol

from src.frontend.server import start_dashboard
from src.models import Config, InferenceResult
from src.server.metrics import MetricsCollector
from src.server.pool import ModelPool
from src.server.scheduler import Scheduler
from src.server.services.inference_service import InferenceService
from src.server.services.tokenization_service import TokenizationService
from src.server.tokenizer_pool import TokenizerPool

logger = logging.getLogger(__name__)


class InferenceInterface(Protocol):
    """Protocol for inference interface (scheduler or pool)."""

    def schedule(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """Schedule inference request."""
        ...


class OrchestratorWrapper:
    """Wrapper that coordinates async tokenization -> inference flow."""

    def __init__(
        self,
        tokenization_service: TokenizationService,
        inference_service: InferenceService,
    ):
        self._tokenization_service = tokenization_service
        self._inference_service = inference_service

    def schedule(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """Schedule inference request: tokenize -> infer."""
        # Synchronous flow: tokenize then infer
        # Tokenization is async internally but we wait for it
        tokenized_batch = self._tokenization_service.tokenize_sync(pairs)

        # Inference is async internally but we wait for it
        result = self._inference_service.infer_sync(tokenized_batch)

        return result


class ServerOrchestrator:
    """Orchestrates all server components."""

    def __init__(self, config: Config, experiment_name: str):
        """Initialize orchestrator with configuration."""
        self.config = config
        self.experiment_name = experiment_name
        self.tokenizer_pool: TokenizerPool | None = None
        self.tokenization_service: TokenizationService | None = None
        self.pool: ModelPool | None = None
        self.inference_service: InferenceService | None = None
        self.scheduler: Scheduler | None = None
        self.metrics: MetricsCollector | None = None
        self.inference_handler: InferenceInterface | None = None
        self.shutdown_event = threading.Event()

    def setup(self) -> None:
        """Set up all server components."""
        # Create tokenizer pool (required)
        tokenizer_model = self.config.tokenizer_pool.model_name
        if not tokenizer_model:
            # Use same model as first instance if not specified
            tokenizer_model = (
                self.config.model_pool.instances[0].name
                if self.config.model_pool.instances
                else "cross-encoder/ms-marco-MiniLM-L-6-v2"
            )
        self.tokenizer_pool = TokenizerPool(
            model_name=tokenizer_model,
            num_workers=self.config.tokenizer_pool.num_workers,
            max_length=(
                self.config.model_pool.instances[0].max_length
                if self.config.model_pool.instances
                else 512
            ),
        )
        # Create tokenization service
        self.tokenization_service = TokenizationService(self.tokenizer_pool)
        logger.info(
            f"Tokenizer pool created: {self.config.tokenizer_pool.num_workers} workers, "
            f"model: {tokenizer_model}"
        )

        # Create model pool
        self.pool = ModelPool(self.config.model_pool)

        # Create inference service
        self.inference_service = InferenceService(self.pool)

        # Create metrics collector
        self.metrics = MetricsCollector()
        self.metrics.set_pool(self.pool)  # Pass pool reference for GPU memory queries
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

        # Create scheduler only if batching is enabled
        if self.config.batching.enabled:
            self.scheduler = Scheduler(
                self.pool,
                self.tokenization_service,
                self.inference_service,
                batching_enabled=self.config.batching.enabled,
                max_batch_size=self.config.batching.max_batch_size,
                timeout_ms=self.config.batching.timeout_ms,
                length_aware=self.config.batching.length_aware,
            )
            self.inference_handler = self.scheduler
            logger.info("Scheduler created with dynamic batching enabled")
        else:
            # Use orchestrator wrapper for async flow: tokenization -> inference
            self.inference_handler = OrchestratorWrapper(
                self.tokenization_service, self.inference_service
            )
            logger.info("Using orchestrator wrapper for async tokenization -> inference flow")

    def start(self) -> None:
        """Start all server components."""

        # Setup signal handlers
        def handle_signal(signum, frame):
            logger.info("Shutdown signal received")
            self.shutdown_event.set()
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        # Start tokenization service
        logger.info("Starting tokenization service...")
        self.tokenization_service.start()

        # Start inference service
        logger.info(
            f"Starting inference service with {len(self.config.model_pool.instances)} instances..."
        )
        self.inference_service.start()

        # Start dashboard
        start_dashboard(self.config.server.http_port, self.metrics)

    def stop(self) -> None:
        """Stop all server components."""
        if self.inference_service:
            self.inference_service.stop()
        if self.pool:
            self.pool.stop()
        if self.tokenization_service:
            self.tokenization_service.stop()
        if self.tokenizer_pool:
            self.tokenizer_pool.stop()
        if self.scheduler:
            self.scheduler.stop()

    def get_inference_handler(self) -> InferenceInterface:
        """Get the inference handler (scheduler or pool wrapper)."""
        if self.inference_handler is None:
            raise RuntimeError("Orchestrator not set up. Call setup() first.")
        return self.inference_handler

    def get_metrics(self) -> MetricsCollector:
        """Get metrics collector."""
        if self.metrics is None:
            raise RuntimeError("Orchestrator not set up. Call setup() first.")
        return self.metrics


__all__ = ["ServerOrchestrator", "InferenceInterface", "OrchestratorWrapper"]
