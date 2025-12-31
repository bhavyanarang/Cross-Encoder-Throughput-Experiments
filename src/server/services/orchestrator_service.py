import logging
import queue
import signal
import sys
import threading
import time

from src.frontend.server import start_dashboard
from src.server.dto import Config, InferenceResult
from src.server.dto.pipeline import PipelineRequest, TokenizationQueueItem
from src.server.pool import ModelPool, TokenizerPool
from src.server.services.inference_service import InferenceService
from src.server.services.metrics_service import MetricsService
from src.server.services.tokenization_service import TokenizationService

logger = logging.getLogger(__name__)


class OrchestratorService:
    """
    Orchestrator service that manages the pipeline-based inference architecture.
    
    This service implements a queue-based pipeline that decouples tokenization and inference:
    1. Request arrives → Pushed to tokenization queue
    2. Tokenization workers process → Push to inference queue
    3. Inference workers process → Return result to caller
    
    This design ensures GPU resources are never starved because work flows
    continuously through both stages independently.
    """

    def __init__(self, config: Config, experiment_name: str = "default"):
        self.config = config
        self.experiment_name = experiment_name
        self.shutdown_event = threading.Event()

        # Services will be initialized in setup()
        self.tokenization_service = None
        self.inference_service = None
        self.tokenizer_pool = None
        self.pool = None
        self.metrics = None

        # Pipeline state
        self._next_request_id = 0
        self._request_id_lock = threading.Lock()
        self._pending_requests: dict[int, PipelineRequest] = {}
        self._pending_requests_lock = threading.Lock()
        self._inference_queue: queue.Queue = None

    def _get_next_request_id(self) -> int:
        with self._request_id_lock:
            req_id = self._next_request_id
            self._next_request_id += 1
            return req_id

    def setup(self) -> None:
        """Setup the orchestrator and all services."""
        logger.info(f"Setting up orchestrator for experiment: {self.experiment_name}")

        # Create inference queue for pipeline
        self._inference_queue = queue.Queue()

        # Create tokenizer pool
        # Use inference model name if tokenizer model_name is not specified
        tokenizer_model = self.config.tokenizer_pool.model_name
        if not tokenizer_model and self.config.model_pool.instances:
            tokenizer_model = self.config.model_pool.instances[0].name
        
        self.tokenizer_pool = TokenizerPool(
            model_name=tokenizer_model,
            num_workers=self.config.tokenizer_pool.num_workers,
            max_length=512,  # Default max token length
        )

        # Create tokenization service
        self.tokenization_service = TokenizationService(self.tokenizer_pool)

        # Create model pool
        self.pool = ModelPool(self.config.model_pool)

        # Create inference service
        self.inference_service = InferenceService(self.pool)

        # Create metrics service
        self.metrics = MetricsService()
        self.metrics.set_inference_service(self.inference_service)
        self.metrics.set_tokenization_service(self.tokenization_service)
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

        logger.info("Orchestrator setup complete - pipeline architecture ready")

    def start(self) -> None:
        """Start all services and the orchestrator."""
        def handle_signal(signum, frame):
            logger.info("Shutdown signal received")
            self.shutdown_event.set()
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        logger.info("Starting tokenization service...")
        self.tokenization_service.start()

        logger.info(
            f"Starting inference service with {len(self.config.model_pool.instances)} instances..."
        )
        self.inference_service.start()

        # Setup pipeline after services are started
        self.tokenizer_pool.set_inference_queue(self._inference_queue)
        self.inference_service.set_inference_queue(self._inference_queue)
        logger.info("Pipeline setup complete - tokenization → inference queue connected")

        self.metrics.start()

        start_dashboard(self.config.server.http_port, self.metrics.get_collector())

    def stop(self) -> None:
        """Stop all services."""
        self.shutdown_event.set()

        if self.metrics:
            self.metrics.stop()
        if self.inference_service:
            self.inference_service.stop()
        if self.pool:
            self.pool.stop()
        if self.tokenization_service:
            self.tokenization_service.stop()
        if self.tokenizer_pool:
            self.tokenizer_pool.stop()

    def schedule(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """
        Schedule a request through the pipeline.
        
        This method:
        1. Creates a PipelineRequest
        2. Pushes to tokenization queue
        3. Waits for result through the pipeline
        4. Returns the inference result
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            InferenceResult with scores and timing information
            
        Raises:
            RuntimeError: If request times out or services not started
        """
        if not self.tokenization_service.is_started or not self.inference_service.is_started:
            raise RuntimeError("Pipeline services not started")

        # Create pipeline request
        req_id = self._get_next_request_id()
        request = PipelineRequest(
            request_id=req_id,
            pairs=pairs,
            submit_time=time.perf_counter(),
        )

        with self._pending_requests_lock:
            self._pending_requests[req_id] = request

        try:
            # Create and submit tokenization item to pipeline
            tokenization_item = TokenizationQueueItem(
                request=request,
                pairs=pairs,
            )

            # Submit to tokenization service
            self.tokenization_service.submit_pipeline(tokenization_item)

            # Wait for result with timeout
            timeout_sec = 30.0  # 30 second timeout
            if not request.result_event.wait(timeout=timeout_sec):
                raise RuntimeError(
                    f"Pipeline request {req_id} timed out after {timeout_sec}s"
                )

            # Check for errors
            if request.error:
                raise request.error

            if request.inference_result is None:
                raise RuntimeError(f"Pipeline request {req_id} completed with no result")

            # Build timing information
            total_ms = (time.perf_counter() - request.submit_time) * 1000
            result = request.inference_result
            result.t_queue_wait_ms = (
                request.t_queue_tokenization_wait_ms or 0
            ) + (request.t_queue_inference_wait_ms or 0)
            result.total_ms = total_ms

            return result

        except Exception as e:
            logger.error(f"Pipeline request {req_id} failed: {e}")
            raise

        finally:
            # Clean up pending request
            with self._pending_requests_lock:
                self._pending_requests.pop(req_id, None)

    def get_metrics(self) -> MetricsService:
        if self.metrics is None:
            raise RuntimeError("Orchestrator not set up. Call setup() first.")
        return self.metrics


__all__ = [
    "OrchestratorService",
]

