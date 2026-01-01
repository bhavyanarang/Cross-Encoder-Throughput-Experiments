import logging
import queue
import signal
import sys
import threading
import time
from itertools import count

from src.frontend.server import start_dashboard
from src.server.dto import Config, InferenceResult, PendingRequest
from src.server.dto.pipeline import PipelineRequest, TokenizationQueueItem
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
        self._next_request_id_counter = count()  # Lock-free atomic counter
        self._pending_requests: dict[int, PipelineRequest] = {}
        self._pending_requests_lock = threading.Lock()
        self._inference_queue: queue.Queue = None
        self._request_count = 0
        self._request_count_lock = threading.Lock()
        self._last_log_time = time.time()
        self._requests_in_window = 0
        self._pairs_in_window = 0
        self._tokenization_started = False
        self._inference_started = False

        # Batching configuration (moved from SchedulerService)
        self._batching_enabled = False
        self._max_batch_size = 8
        self._timeout_ms = 100
        self._length_aware = False
        self._batch_queue: queue.Queue[PendingRequest] = queue.Queue()
        self._batch_condition = threading.Condition()
        self._batch_thread: threading.Thread | None = None
        self._batching_running = False
        self._batch_shutdown_event = threading.Event()

    def _get_next_request_id(self) -> int:
        # Lock-free request ID generation using atomic counter
        return next(self._next_request_id_counter)

    def setup(self) -> None:
        logger.info(f"Setting up orchestrator for experiment: {self.experiment_name}")

        self._inference_queue = queue.Queue()

        tokenizer_model = self.config.tokenizer_pool.model_name
        if not tokenizer_model and self.config.model_pool.instances:
            tokenizer_model = self.config.model_pool.instances[0].name

        self.tokenizer_pool = TokenizerPool(
            model_name=tokenizer_model,
            num_workers=self.config.tokenizer_pool.num_workers,
            max_length=512,
        )

        self.pool = ModelPool(self.config.model_pool)
        self.metrics = MetricsService()
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

        # Setup batching if enabled
        if self.config.batching.enabled:
            self._batching_enabled = True
            self._max_batch_size = self.config.batching.max_batch_size
            self._timeout_ms = self.config.batching.timeout_ms
            self._length_aware = self.config.batching.length_aware

            self._batching_running = True
            self._batch_shutdown_event.clear()
            self._batch_thread = threading.Thread(target=self._batch_loop, daemon=False)
            self._batch_thread.start()
            logger.info(
                f"Batching enabled: max_batch_size={self._max_batch_size}, "
                f"timeout_disabled=True (processes immediately), "
                f"length_aware={self._length_aware}"
            )
            logger.info(
                "Batch thread started - batching is ACTIVE (no timeout, processes immediately)"
            )
        else:
            logger.info("Batching disabled - using direct pipeline processing")

        logger.info("Orchestrator setup complete - pipeline architecture ready")

    def start(self) -> None:
        def handle_signal(signum, frame):
            logger.info("Shutdown signal received")
            self.shutdown_event.set()
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        logger.info("Starting tokenization pool...")
        if not self.tokenizer_pool.is_loaded:
            self.tokenizer_pool.start()
        self._tokenization_started = True

        logger.info(
            f"Starting inference pool with {len(self.config.model_pool.instances)} instances..."
        )
        if not self.pool.is_loaded:
            self.pool.start()
        self._inference_started = True

        self.tokenizer_pool.set_inference_queue(self._inference_queue)
        self.pool.set_inference_queue(self._inference_queue)
        logger.info("Pipeline setup complete - tokenization → inference queue connected")

        self.metrics.start()

        start_dashboard(self.config.server.http_port, self.metrics)

    def stop(self) -> None:
        self.shutdown_event.set()

        if self.metrics:
            self.metrics.stop()

        # Stop batching thread
        self._batching_running = False
        self._batch_shutdown_event.set()
        with self._batch_condition:
            self._batch_condition.notify_all()
        if self._batch_thread and self._batch_thread.is_alive():
            self._batch_thread.join(timeout=5.0)
            if self._batch_thread.is_alive():
                logger.warning("Batch thread did not exit cleanly within timeout")

        self._inference_started = False
        if self.pool:
            self.pool.stop()
        self._tokenization_started = False
        if self.tokenizer_pool:
            self.tokenizer_pool.stop()

    def schedule(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """Schedule inference request. Uses batching if enabled, otherwise direct pipeline."""
        # If batching is enabled, queue the request for batch processing
        if self._batching_enabled:
            req = PendingRequest(
                pairs=pairs,
                result_future=threading.Event(),
                submit_time=time.perf_counter(),
            )

            self._batch_queue.put(req)

            with self._batch_condition:
                self._batch_condition.notify()

            # Wait for result without timeout (batching processes immediately)
            # Use a long timeout as safety net (30 seconds)
            if not req.result_future.wait(timeout=30.0):
                raise RuntimeError("Scheduler request timed out after 30s")

            if hasattr(req, "error") and req.error:
                raise req.error

            if req.result is None:
                raise RuntimeError("Scheduler returned None result (unexpected error)")

            return req.result

        # Otherwise, use direct pipeline processing
        if not self._tokenization_started or not self._inference_started:
            raise RuntimeError("Pipeline services not started")

        num_pairs = len(pairs)
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

        req_id = self._get_next_request_id()
        request = PipelineRequest(
            request_id=req_id,
            pairs=pairs,
            submit_time=time.perf_counter(),
        )

        with self._pending_requests_lock:
            self._pending_requests[req_id] = request

        try:
            tokenization_item = TokenizationQueueItem(
                request=request,
                pairs=pairs,
            )

            self.submit_pipeline(tokenization_item)

            timeout_sec = 30.0
            if not request.result_event.wait(timeout=timeout_sec):
                raise RuntimeError(f"Pipeline request {req_id} timed out after {timeout_sec}s")

            if request.error:
                raise request.error

            if request.inference_result is None:
                raise RuntimeError(f"Pipeline request {req_id} completed with no result")

            total_ms = (time.perf_counter() - request.submit_time) * 1000
            result = request.inference_result
            result.t_queue_wait_ms = (request.t_queue_tokenization_wait_ms or 0) + (
                request.t_queue_inference_wait_ms or 0
            )
            result.t_tokenizer_queue_wait_ms = request.t_queue_tokenization_wait_ms or 0
            result.t_model_queue_wait_ms = request.t_queue_inference_wait_ms or 0
            result.total_ms = total_ms

            return result

        except Exception as e:
            logger.error(f"Pipeline request {req_id} failed: {e}")
            raise

        finally:
            with self._pending_requests_lock:
                self._pending_requests.pop(req_id, None)

    def _batch_loop(self) -> None:
        """Process batches immediately without timeout - batches when max_batch_size is reached or immediately if queue is empty."""
        while not self._batch_shutdown_event.is_set():
            batch: list[PendingRequest] = []

            # Get first item (block until available)
            try:
                first_item = self._batch_queue.get(timeout=0.1)
                batch.append(first_item)
            except queue.Empty:
                if self._batch_shutdown_event.is_set():
                    break
                continue

            # Collect additional items up to max_batch_size without waiting
            # Process immediately when max_batch_size is reached
            while len(batch) < self._max_batch_size and not self._batch_shutdown_event.is_set():
                try:
                    # Non-blocking get - process immediately if no more items available
                    item = self._batch_queue.get(block=False)
                    batch.append(item)
                except queue.Empty:
                    # No more items available, process what we have
                    break

            if batch:
                logger.debug(
                    f"Processing batch of {len(batch)} requests (total pairs: {sum(len(req.pairs) for req in batch)})"
                )
                self._process_batch(batch)

    def _process_batch(self, batch: list[PendingRequest]) -> None:
        batch_start_time = time.perf_counter()

        all_pairs = []
        pair_counts = []
        for req in batch:
            n = len(req.pairs)
            pair_counts.append(n)
            all_pairs.extend(req.pairs)

        if self._length_aware:
            all_pairs.sort(key=lambda p: len(p[0]) + len(p[1]))

        try:
            req_id = self._get_next_request_id()
            pipeline_request = PipelineRequest(
                request_id=req_id,
                pairs=all_pairs,
                submit_time=batch_start_time,
            )

            tokenization_item = TokenizationQueueItem(
                request=pipeline_request,
                pairs=all_pairs,
            )

            self.submit_pipeline(tokenization_item)

            # Wait for pipeline result (no timeout - should complete quickly)
            if not pipeline_request.result_event.wait(timeout=30.0):
                raise RuntimeError(f"Pipeline request {req_id} timed out after 30s")

            if pipeline_request.error:
                raise pipeline_request.error

            if pipeline_request.inference_result is None:
                raise RuntimeError(f"Pipeline request {req_id} completed with no result")

            result = pipeline_request.inference_result

            idx = 0
            for i, req in enumerate(batch):
                n = pair_counts[i]
                queue_wait_ms = (batch_start_time - req.submit_time) * 1000

                req.result = type(result)(
                    scores=result.scores[idx : idx + n],
                    t_tokenize_ms=result.t_tokenize_ms,
                    t_model_inference_ms=result.t_model_inference_ms,
                    t_queue_wait_ms=queue_wait_ms,
                    total_ms=result.total_ms,
                    total_tokens=result.total_tokens,
                    real_tokens=result.real_tokens,
                    padded_tokens=result.padded_tokens,
                    padding_ratio=result.padding_ratio,
                    max_seq_length=result.max_seq_length,
                    avg_seq_length=result.avg_seq_length,
                    batch_size=len(all_pairs),
                    worker_id=getattr(result, "worker_id", -1),
                )
                idx += n
                req.result_future.set()

        except Exception as e:
            logger.error(f"Batch processing error: {e}", exc_info=True)
            for req in batch:
                req.error = e
                req.result_future.set()

    def get_batching_info(self) -> dict:
        """Get batching configuration and status."""
        return {
            "batching_enabled": self._batching_enabled,
            "max_batch_size": self._max_batch_size,
            "timeout_ms": self._timeout_ms,
            "length_aware": self._length_aware,
            "pending": self._batch_queue.qsize(),
        }

    def get_metrics(self) -> MetricsService:
        if self.metrics is None:
            raise RuntimeError("Orchestrator not set up. Call setup() first.")
        return self.metrics

    # TokenizationService methods
    def set_inference_queue(self, inference_queue: queue.Queue) -> None:
        """Set the inference queue for tokenization pipeline."""
        self._inference_queue = inference_queue
        if self.tokenizer_pool:
            self.tokenizer_pool.set_inference_queue(inference_queue)
        logger.info("Tokenization pipeline queue set")

    def submit_pipeline(self, tokenization_item: TokenizationQueueItem) -> None:
        """Submit a tokenization item to the pipeline."""
        if not self._tokenization_started:
            raise RuntimeError("Tokenization service not started")
        self.tokenizer_pool.submit_pipeline(tokenization_item)

    def get_tokenizer_worker_metrics(self) -> list[dict]:
        """Get tokenizer worker metrics."""
        if not self._tokenization_started:
            return []
        return self.tokenizer_pool.get_worker_metrics()

    def reset_tokenizer_worker_metrics(self) -> None:
        """Reset tokenizer worker metrics."""
        if self._tokenization_started:
            self.tokenizer_pool.reset_worker_metrics()

    @property
    def tokenization_is_started(self) -> bool:
        """Check if tokenization service is started."""
        return self._tokenization_started

    # InferenceService methods
    def get_gpu_memory_mb(self) -> float:
        """Get GPU memory usage in MB."""
        if not self._inference_started:
            return 0.0
        return self.pool.get_gpu_memory_mb()

    def get_inference_worker_metrics(self) -> list[dict]:
        """Get inference worker metrics."""
        if not self._inference_started:
            return []
        return self.pool.get_worker_metrics()

    def reset_inference_worker_metrics(self) -> None:
        """Reset inference worker metrics."""
        if self._inference_started:
            self.pool.reset_worker_metrics()

    @property
    def inference_is_started(self) -> bool:
        """Check if inference service is started."""
        return self._inference_started

    # Compatibility properties for metrics service
    @property
    def is_started(self) -> bool:
        """Check if both services are started (for compatibility)."""
        return self._tokenization_started and self._inference_started

    def get_worker_metrics(self) -> list[dict]:
        """Get worker metrics (tokenizer) - for compatibility with metrics service."""
        return self.get_tokenizer_worker_metrics()

    def reset_worker_metrics(self) -> None:
        """Reset worker metrics (tokenizer) - for compatibility with metrics service."""
        self.reset_tokenizer_worker_metrics()

    # Backwards compatibility properties (for tests that expect separate services)
    @property
    def tokenization_service(self):
        """Backwards compatibility: return self as tokenization service."""
        return self

    @property
    def inference_service(self):
        """Backwards compatibility: return self as inference service."""
        return self


__all__ = [
    "OrchestratorService",
]
