"""
Model Pool - Process-based multi-model inference for true parallelism on MPS.

Key Apple Silicon rule:
- Do NOT initialize torch/MPS in the parent process.
- Import torch and load the model *inside* each worker process.

This enables true parallelism by giving each worker its own MPS context,
avoiding the Metal command buffer conflicts that occur with thread-based
concurrency.
"""

from __future__ import annotations

import logging
import multiprocessing as mp
import os
import queue
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import numpy as np
from backends.base_backend import InferenceResult

if TYPE_CHECKING:
    from core.config import ModelPoolConfig

logger = logging.getLogger(__name__)

# Sentinel for stopping workers
_STOP = "__STOP__"


@dataclass
class WorkItem:
    """A single inference request."""

    req_id: int
    pairs: list[tuple[str, str]]


@dataclass
class WorkResult:
    """Result from a worker process."""

    req_id: int
    scores: np.ndarray
    worker_id: int
    t_tokenize_ms: float = 0.0
    t_model_inference_ms: float = 0.0
    total_ms: float = 0.0
    # Padding metrics
    total_tokens: int = 0
    real_tokens: int = 0
    padded_tokens: int = 0
    padding_ratio: float = 0.0
    max_seq_length: int = 0
    avg_seq_length: float = 0.0
    batch_size: int = 0


def _worker_main(
    worker_id: int,
    input_queue: mp.Queue[WorkItem | str],
    output_queue: mp.Queue[WorkResult],
    config_dict: dict[str, Any],
    ready_event: mp.Event,
) -> None:
    """
    Worker process entry point.

    IMPORTANT: torch is imported HERE, not in the parent process.
    This gives each worker its own MPS context for true parallelism.
    """
    import warnings

    warnings.filterwarnings("ignore", category=UserWarning)

    # Set worker identifier for debugging
    os.environ["MPS_WORKER_ID"] = str(worker_id)

    pid = os.getpid()
    logger.info(f"[Worker {worker_id}] PID={pid} starting...")

    try:
        # NOW we can import torch - each process gets its own context
        import torch
        from sentence_transformers import CrossEncoder

        model_name = config_dict["name"]
        device = config_dict["device"]
        use_fp16 = config_dict.get("use_fp16", True)
        max_length = config_dict.get("max_length")

        # Resolve device
        if device == "auto" or device == "mps":
            if torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"

        logger.info(f"[Worker {worker_id}] Loading model: {model_name}")
        logger.info(f"[Worker {worker_id}] Device: {device}, FP16: {use_fp16}")

        # Load model
        model = CrossEncoder(model_name, device=device)
        tokenizer = model.tokenizer

        # Apply FP16 if requested
        if use_fp16 and device == "mps":
            model.model = model.model.half()
            logger.info(f"[Worker {worker_id}] Applied FP16 precision")

        # Determine max_length
        effective_max_length = max_length if max_length else model.max_length
        if max_length:
            logger.info(
                f"[Worker {worker_id}] Using configured max_length: {max_length} (model default: {model.max_length})"
            )

        # Warmup
        logger.info(f"[Worker {worker_id}] Warming up...")
        for _ in range(5):
            _ = model.predict([("warmup", "warmup")])
        if device == "mps":
            torch.mps.synchronize()

        logger.info(f"[Worker {worker_id}] Ready")
        ready_event.set()

        # Main loop
        while True:
            try:
                item = input_queue.get(timeout=1.0)
            except queue.Empty:
                continue

            if item == _STOP:
                break

            assert isinstance(item, WorkItem)

            total_start = time.perf_counter()

            # Stage 1: Tokenization
            tokenize_start = time.perf_counter()
            texts = [[p[0], p[1]] for p in item.pairs]
            features = tokenizer(
                texts,
                padding=True,
                truncation="longest_first",
                return_tensors="pt",
                max_length=effective_max_length,
            )

            # Padding analysis
            attention_mask = features["attention_mask"]
            batch_size, max_seq_length = attention_mask.shape
            real_tokens_per_seq = attention_mask.sum(dim=1)
            total_real_tokens = int(real_tokens_per_seq.sum().item())
            total_tokens = batch_size * max_seq_length
            padded_tokens = total_tokens - total_real_tokens
            padding_ratio = padded_tokens / total_tokens if total_tokens > 0 else 0.0
            avg_seq_length = float(real_tokens_per_seq.float().mean().item())

            t_tokenize_ms = (time.perf_counter() - tokenize_start) * 1000

            # Stage 2: Model inference
            inference_start = time.perf_counter()

            features = {k: v.to(device) for k, v in features.items()}

            if device == "mps":
                torch.mps.synchronize()

            with torch.inference_mode():
                model_predictions = model.model(**features, return_dict=True)
                logits = model_predictions.logits

                if model.config.num_labels == 1:
                    scores = torch.sigmoid(logits).squeeze(-1)
                else:
                    scores = torch.softmax(logits, dim=-1)[:, 1]

            if device == "mps":
                torch.mps.synchronize()

            scores_np = scores.cpu().numpy()

            t_model_inference_ms = (time.perf_counter() - inference_start) * 1000
            total_ms = (time.perf_counter() - total_start) * 1000

            output_queue.put(
                WorkResult(
                    req_id=item.req_id,
                    scores=scores_np,
                    worker_id=worker_id,
                    t_tokenize_ms=t_tokenize_ms,
                    t_model_inference_ms=t_model_inference_ms,
                    total_ms=total_ms,
                    total_tokens=total_tokens,
                    real_tokens=total_real_tokens,
                    padded_tokens=padded_tokens,
                    padding_ratio=padding_ratio,
                    max_seq_length=max_seq_length,
                    avg_seq_length=avg_seq_length,
                    batch_size=batch_size,
                )
            )

        logger.info(f"[Worker {worker_id}] Shutting down")

    except Exception as e:
        logger.exception(f"[Worker {worker_id}] Fatal error: {e}")
        ready_event.set()  # Unblock parent even on error
        raise


class ModelPool:
    """
    Process-based model pool for true parallelism on MPS.

    Each model instance runs in a separate process with its own MPS context,
    enabling true parallel inference without Metal command buffer conflicts.

    Usage:
        pool = ModelPool(config)
        pool.start()

        result = pool.infer(pairs)

        pool.stop()
    """

    def __init__(self, config: ModelPoolConfig):
        """
        Initialize model pool.

        Args:
            config: ModelPoolConfig with instance configurations
        """
        self.config = config
        self.num_workers = len(config.instances)

        # Use spawn to avoid inheriting any torch state
        self._ctx = mp.get_context("spawn")

        # Shared queues for all workers
        self._input_queue: mp.Queue = self._ctx.Queue()
        self._output_queue: mp.Queue = self._ctx.Queue()

        self._processes: list[mp.Process] = []
        self._ready_events: list[mp.Event] = []
        self._is_started = False

        # Request ID counter
        self._next_req_id = 0

        # Per-instance metrics (simplified tracking)
        self._worker_request_counts: dict[int, int] = {}
        self._worker_busy: dict[int, bool] = {}

        logger.info(
            f"ModelPool initialized with {self.num_workers} instance(s), "
            f"routing={config.routing_strategy}"
        )

    def start(self, timeout_s: float = 120.0) -> None:
        """
        Start all worker processes and wait for them to be ready.

        Args:
            timeout_s: Maximum time to wait for workers to initialize
        """
        if self._is_started:
            return

        logger.info(f"Starting {self.num_workers} worker process(es)...")

        for i, instance_config in enumerate(self.config.instances):
            # Convert config to dict for pickling
            config_dict = {
                "name": instance_config.name,
                "device": instance_config.device,
                "backend": instance_config.backend,
                "use_fp16": instance_config.use_fp16,
                "max_length": instance_config.max_length,
            }

            ready_event = self._ctx.Event()
            self._ready_events.append(ready_event)

            p = self._ctx.Process(
                target=_worker_main,
                args=(i, self._input_queue, self._output_queue, config_dict, ready_event),
                daemon=True,
            )
            p.start()
            self._processes.append(p)
            self._worker_request_counts[i] = 0
            self._worker_busy[i] = False

            logger.info(f"Started worker {i} (PID={p.pid})")

        # Wait for all workers to be ready
        deadline = time.time() + timeout_s
        for i, event in enumerate(self._ready_events):
            remaining = max(0.0, deadline - time.time())
            if not event.wait(timeout=remaining):
                raise RuntimeError(f"Worker {i} failed to start within {timeout_s}s")

        self._is_started = True
        logger.info(f"ModelPool ready with {self.num_workers} worker(s)")

    def stop(self, timeout_s: float = 30.0) -> None:
        """Stop all worker processes gracefully."""
        if not self._is_started:
            return

        logger.info("Stopping worker processes...")

        # Send stop signals
        for _ in range(self.num_workers):
            self._input_queue.put(_STOP)

        # Wait for processes to exit
        deadline = time.time() + timeout_s
        for p in self._processes:
            remaining = max(0.0, deadline - time.time())
            p.join(timeout=remaining)
            if p.is_alive():
                logger.warning(f"Force killing worker PID={p.pid}")
                p.kill()
                p.join(timeout=5)

        self._processes.clear()
        self._ready_events.clear()
        self._is_started = False

        logger.info("ModelPool stopped")

    def infer(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """
        Run inference on query-document pairs.

        Sends work to the next available worker and waits for result.

        Args:
            pairs: List of (query, document) tuples

        Returns:
            InferenceResult with scores and timing
        """
        if not self._is_started:
            raise RuntimeError("ModelPool not started. Call start() first.")

        req_id = self._next_req_id
        self._next_req_id += 1

        # Send work
        self._input_queue.put(WorkItem(req_id=req_id, pairs=pairs))

        # Wait for result
        result = self._output_queue.get()

        # Update metrics
        self._worker_request_counts[result.worker_id] = (
            self._worker_request_counts.get(result.worker_id, 0) + 1
        )

        return InferenceResult(
            scores=result.scores,
            t_tokenize_ms=result.t_tokenize_ms,
            t_model_inference_ms=result.t_model_inference_ms,
            total_ms=result.total_ms,
            total_tokens=result.total_tokens,
            real_tokens=result.real_tokens,
            padded_tokens=result.padded_tokens,
            padding_ratio=result.padding_ratio,
            max_seq_length=result.max_seq_length,
            avg_seq_length=result.avg_seq_length,
            batch_size=result.batch_size,
        )

    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """Alias for infer() - timing is always included."""
        return self.infer(pairs)

    def get_pool_info(self) -> dict:
        """Get information about the process pool."""
        return {
            "num_instances": self.num_workers,
            "routing_strategy": self.config.routing_strategy,
            "execution_mode": "process",
            "is_loaded": self._is_started,
            "worker_request_counts": dict(self._worker_request_counts),
            "instances": [
                {
                    "worker_id": i,
                    "name": inst.name,
                    "device": inst.device,
                    "backend": inst.backend,
                    "request_count": self._worker_request_counts.get(i, 0),
                }
                for i, inst in enumerate(self.config.instances)
            ],
        }

    def get_instance_metrics_summary(self) -> dict:
        """Get per-instance metrics summary for dashboard."""
        total_requests = sum(self._worker_request_counts.values())
        instances = []

        for i, inst in enumerate(self.config.instances):
            req_count = self._worker_request_counts.get(i, 0)
            # In process mode, we can't easily track real-time busy state
            # from the parent, so we estimate based on request distribution
            util_pct = (req_count / total_requests * 100) if total_requests > 0 else 0.0

            instances.append(
                {
                    "id": i,
                    "name": f"{inst.backend}-{i}",
                    "request_count": req_count,
                    "utilization_pct": round(util_pct, 2),
                    "idle_pct": round(100.0 - util_pct, 2),
                    "is_busy": False,  # Can't track in real-time across processes
                    "avg_latency_ms": 0.0,
                }
            )

        avg_util = (
            sum(inst["utilization_pct"] for inst in instances) / len(instances)
            if instances
            else 0.0
        )

        return {
            "num_instances": self.num_workers,
            "instances": instances,
            "avg_utilization_pct": round(avg_util, 2),
            "avg_idle_pct": round(100.0 - avg_util, 2),
            "total_requests": total_requests,
        }

    def get_instance_metrics_history(self) -> dict:
        """Get per-instance metrics for charts."""
        return {
            "utilization_pct": [0.0] * self.num_workers,
            "idle_pct": [100.0] * self.num_workers,
            "request_counts": [
                self._worker_request_counts.get(i, 0) for i in range(self.num_workers)
            ],
            "is_busy": [False] * self.num_workers,
        }

    @property
    def is_loaded(self) -> bool:
        """Check if pool is started."""
        return self._is_started

    @property
    def num_backends(self) -> int:
        """Get number of worker instances."""
        return self.num_workers

    def __len__(self) -> int:
        """Get number of worker instances."""
        return self.num_workers


__all__ = ["ModelPool", "WorkItem", "WorkResult"]
