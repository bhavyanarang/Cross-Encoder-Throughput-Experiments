import logging
import queue
import threading
import time
from typing import TYPE_CHECKING

import torch

from src.server.dto import Config, InferenceResult, PendingRequest
from src.server.dto.inference import TokenizedBatch
from src.server.dto.pipeline import InferenceQueueItem, PipelineRequest, TokenizationQueueItem
from src.server.pipeline.base import BasePipeline
from src.server.services.metrics_service import MetricsService

if TYPE_CHECKING:
    from src.server.pool import ModelPool, TokenizerPool

logger = logging.getLogger(__name__)


class QueueBasedPipeline(BasePipeline):
    def __init__(
        self,
        config: Config,
        tokenizer_pool: "TokenizerPool",
        model_pool: "ModelPool",
        metrics_service: MetricsService,
        experiment_name: str = "default",
    ):
        super().__init__(config, tokenizer_pool, model_pool, metrics_service, experiment_name)

        self._inference_queue: queue.Queue | None = None

        self._batching_enabled = False
        self._max_batch_size = 8
        self._timeout_ms = 100
        self._length_aware = False
        self._batch_queue: queue.Queue[PendingRequest] = queue.Queue()
        self._batch_condition = threading.Condition()
        self._batch_thread: threading.Thread | None = None
        self._batching_running = False
        self._batch_shutdown_event = threading.Event()

    def setup(self) -> None:
        logger.info(f"Setting up queue-based pipeline for experiment: {self.experiment_name}")

        self._inference_queue = queue.Queue()

        if not self.tokenizer_pool or not self.model_pool or not self.metrics:
            raise RuntimeError(
                "Pipeline setup requires pools and metrics to be initialized by orchestrator"
            )

        if self.config.batching.enabled:
            self._batching_enabled = True
            self._max_batch_size = self.config.batching.max_batch_size
            self._timeout_ms = self.config.batching.timeout_ms
            self._length_aware = self.config.batching.length_aware

            self._batching_running = True
            self._batch_shutdown_event.clear()
            self._batch_thread = threading.Thread(target=self._batch_loop, daemon=True)
            self._batch_thread.start()
            logger.info(
                f"Batching enabled: max_batch_size={self._max_batch_size}, "
                f"timeout_ms={self._timeout_ms}, "
                f"length_aware={self._length_aware}"
            )
        else:
            logger.info("Batching disabled - using direct pipeline processing")

        logger.info("Queue-based pipeline setup complete")

    def start(self) -> None:
        self._setup_signal_handlers()

        mode = self.config.pipeline.mode
        logger.info(f"Starting Queue-Based Pipeline in mode: {mode}")

        if mode == "full":
            logger.info("Starting tokenization pool...")
            if not self.tokenizer_pool.is_loaded:
                self.tokenizer_pool.start()
            self._tokenization_started = True
        elif mode == "tokenization_only":
            logger.info("Starting tokenization pool...")
            if not self.tokenizer_pool.is_loaded:
                self.tokenizer_pool.start()
            self._tokenization_started = True
        else:
            logger.info("Tokenization pool disabled in inference_only mode")

        if mode in ["full", "inference_only"]:
            logger.info(
                f"Starting inference pool with {len(self.config.model_pool.instances)} instances..."
            )
            if not self.model_pool.is_loaded:
                self.model_pool.start()
            self._inference_started = True
        else:
            logger.info("Inference pool disabled in tokenization_only mode")

        if mode == "full":
            self.tokenizer_pool.set_inference_queue(self._inference_queue)
            self.model_pool.set_inference_queue(self._inference_queue)
            logger.info("Pipeline setup complete - tokenization → inference queue connected")
        elif mode == "tokenization_only":
            logger.info("Pipeline setup complete - tokenization only mode")
        elif mode == "inference_only":
            self.model_pool.set_inference_queue(self._inference_queue)
            logger.info("Pipeline setup complete - inference only mode")

        self.metrics.start()

    def stop(self) -> None:
        self.shutdown_event.set()

        if self.metrics:
            self.metrics.stop()

        self._batching_running = False
        self._batch_shutdown_event.set()
        with self._batch_condition:
            self._batch_condition.notify_all()
        if self._batch_thread and self._batch_thread.is_alive():
            self._batch_thread.join(timeout=5.0)
            if self._batch_thread.is_alive():
                logger.warning("Batch thread did not exit cleanly within timeout")

        self._inference_started = False
        if self.model_pool:
            self.model_pool.stop()
        self._tokenization_started = False
        if self.tokenizer_pool:
            self.tokenizer_pool.stop()

    def schedule(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        if self._batching_enabled:
            queue_size = self._batch_queue.qsize()

            if queue_size == 0:
                return self._schedule_direct(pairs)

            req = PendingRequest(
                pairs=pairs,
                result_future=threading.Event(),
                submit_time=time.perf_counter(),
            )

            self._batch_queue.put(req)

            with self._batch_condition:
                self._batch_condition.notify()

            if not req.result_future.wait(timeout=30.0):
                raise RuntimeError("Scheduler request timed out after 30s")

            if hasattr(req, "error") and req.error:
                raise req.error

            if req.result is None:
                raise RuntimeError("Scheduler returned None result (unexpected error)")

            return req.result

        return self._schedule_direct(pairs)

    def _schedule_direct(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        mode = self.config.pipeline.mode
        if mode == "full" and (not self._tokenization_started or not self._inference_started):
            raise RuntimeError("Pipeline services not started")
        elif mode == "tokenization_only" and not self._tokenization_started:
            raise RuntimeError("Tokenization service not started")
        elif mode == "inference_only" and not self._inference_started:
            raise RuntimeError("Inference service not started")

        request = self._create_request(pairs)
        req_id = request.request_id

        try:
            tokenization_item = TokenizationQueueItem(
                request=request,
                pairs=pairs,
            )

            if mode == "tokenization_only":
                self.tokenizer_pool.submit_pipeline(tokenization_item)
            elif mode == "inference_only":
                max_len = 512
                if self.tokenizer_pool:
                    max_len = self.tokenizer_pool.max_length

                estimated_len = int(len(pairs[0][0] + pairs[0][1]) / 4)
                if estimated_len > max_len:
                    estimated_len = max_len
                if estimated_len < 1:
                    estimated_len = 1

                batch_size = len(pairs)

                input_ids = torch.randint(0, 1000, (batch_size, estimated_len), dtype=torch.long)
                attention_mask = torch.ones((batch_size, estimated_len), dtype=torch.long)

                tokenized_batch = TokenizedBatch(
                    features={"input_ids": input_ids, "attention_mask": attention_mask},
                    batch_size=batch_size,
                    max_seq_length=estimated_len,
                    total_tokens=batch_size * estimated_len,
                    real_tokens=batch_size * estimated_len,
                    padded_tokens=0,
                    padding_ratio=0.0,
                    avg_seq_length=float(estimated_len),
                    tokenize_time_ms=0.0,
                )

                inference_item = InferenceQueueItem(
                    request=request,
                    tokenized_batch=tokenized_batch,
                )

                self._inference_queue.put(inference_item)
            else:
                self.tokenizer_pool.submit_pipeline(tokenization_item)

            if mode == "tokenization_only":
                timeout_sec = 30.0
                if not request.result_event.wait(timeout=timeout_sec):
                    raise RuntimeError(f"Pipeline request {req_id} timed out after {timeout_sec}s")

                if request.error:
                    raise request.error

                if request.tokenized_batch is None:
                    raise RuntimeError(
                        f"Pipeline request {req_id} completed with no tokenized result"
                    )

                result = InferenceResult(
                    scores=[],
                    t_tokenize_ms=0.0,
                    t_model_inference_ms=0.0,
                    t_queue_wait_ms=0.0,
                    total_ms=(time.perf_counter() - request.submit_time) * 1000,
                    total_tokens=0,
                    real_tokens=0,
                    padded_tokens=0,
                    padding_ratio=0.0,
                    max_seq_length=0,
                    avg_seq_length=0.0,
                    batch_size=0,
                    worker_id=-1,
                    tokenizer_worker_id=-1,
                    status_code=204,
                )
                request.inference_result = result
            else:
                timeout_sec = 300.0
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
            self._cleanup_request(req_id)

    def _batch_loop(self) -> None:
        while not self._batch_shutdown_event.is_set():
            batch: list[PendingRequest] = []

            try:
                while not self._batch_shutdown_event.is_set():
                    try:
                        first_item = self._batch_queue.get(timeout=0.01)
                        batch.append(first_item)
                        break
                    except queue.Empty:
                        continue
            except Exception:
                pass

            if not batch or self._batch_shutdown_event.is_set():
                if self._batch_shutdown_event.is_set():
                    break
                continue

            deadline = time.perf_counter() + (self._timeout_ms / 1000.0)

            while len(batch) < self._max_batch_size and not self._batch_shutdown_event.is_set():
                remaining = deadline - time.perf_counter()
                if remaining <= 0:
                    break

                try:
                    item = self._batch_queue.get(timeout=remaining)
                    batch.append(item)
                except queue.Empty:
                    break

            if batch:
                logger.debug(
                    f"Processing batch of {len(batch)} requests "
                    f"(total pairs: {sum(len(req.pairs) for req in batch)})"
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

            self.tokenizer_pool.submit_pipeline(tokenization_item)

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
                batch_queue_wait_ms = (batch_start_time - req.submit_time) * 1000
                total_queue_wait_ms = batch_queue_wait_ms + result.t_queue_wait_ms

                req.result = type(result)(
                    scores=result.scores[idx : idx + n],
                    t_tokenize_ms=result.t_tokenize_ms,
                    t_model_inference_ms=result.t_model_inference_ms,
                    t_queue_wait_ms=total_queue_wait_ms,
                    total_ms=result.total_ms,
                    total_tokens=result.total_tokens,
                    real_tokens=result.real_tokens,
                    padded_tokens=result.padded_tokens,
                    padding_ratio=result.padding_ratio,
                    max_seq_length=result.max_seq_length,
                    avg_seq_length=result.avg_seq_length,
                    batch_size=len(all_pairs),
                    worker_id=getattr(result, "worker_id", -1),
                    tokenizer_worker_id=getattr(result, "tokenizer_worker_id", -1),
                    t_tokenizer_queue_wait_ms=getattr(result, "t_tokenizer_queue_wait_ms", 0.0),
                    t_model_queue_wait_ms=getattr(result, "t_model_queue_wait_ms", 0.0),
                )
                idx += n
                req.result_future.set()

        except Exception as e:
            logger.error(f"Batch processing error: {e}", exc_info=True)
            for req in batch:
                req.error = e
                req.result_future.set()

    def get_batching_info(self) -> dict:
        return {
            "batching_enabled": self._batching_enabled,
            "max_batch_size": self._max_batch_size,
            "timeout_ms": self._timeout_ms,
            "length_aware": self._length_aware,
            "pending": self._batch_queue.qsize(),
        }

    def set_inference_queue(self, inference_queue: queue.Queue) -> None:
        self._inference_queue = inference_queue
        if self.tokenizer_pool:
            self.tokenizer_pool.set_inference_queue(inference_queue)
        logger.info("Tokenization pipeline queue set")

    def submit_pipeline(self, tokenization_item: TokenizationQueueItem) -> None:
        if not self._tokenization_started:
            raise RuntimeError("Tokenization service not started")
        self.tokenizer_pool.submit_pipeline(tokenization_item)
