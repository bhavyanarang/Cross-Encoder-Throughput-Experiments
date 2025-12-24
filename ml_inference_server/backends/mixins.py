"""
Mixins for backend functionality.

Provides reusable functionality that can be mixed into backend implementations:
- TimedInferenceMixin: Standardized inference with timing and padding analysis
- ThreadSafeInferenceMixin: Thread-safe inference with locking
"""

import logging
import threading
import time
from functools import wraps
from typing import TYPE_CHECKING

import numpy as np
import torch

from .device_utils import sync_device

if TYPE_CHECKING:
    from .base_backend import InferenceResult

logger = logging.getLogger(__name__)


def with_inference_mode(func):
    """Decorator to run inference in torch.inference_mode for better performance."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            with torch.inference_mode():
                return func(self, *args, **kwargs)
        except ImportError:
            return func(self, *args, **kwargs)

    return wrapper


class ThreadSafeInferenceMixin:
    """
    Mixin providing thread-safe inference through locking.

    MPS and other GPU backends are not thread-safe, so we need to serialize
    inference calls to prevent race conditions.

    Attributes:
        _inference_lock: Threading lock for serializing inference
        _is_busy: Flag indicating if backend is processing
        _pending_requests: Count of pending requests
    """

    def __init_thread_safety__(self) -> None:
        """Initialize thread safety attributes. Call in __init__."""
        self._inference_lock = threading.Lock()
        self._is_busy = False
        self._pending_requests = 0
        self._pending_lock = threading.Lock()

    @property
    def is_busy(self) -> bool:
        """Check if backend is currently processing a request."""
        return self._is_busy

    @property
    def pending_requests(self) -> int:
        """Get number of pending requests."""
        return self._pending_requests

    def _acquire_for_inference(self) -> None:
        """Acquire lock and mark as busy."""
        with self._pending_lock:
            self._pending_requests += 1
        self._inference_lock.acquire()
        self._is_busy = True

    def _release_after_inference(self) -> None:
        """Release lock and mark as not busy."""
        self._is_busy = False
        self._inference_lock.release()
        with self._pending_lock:
            self._pending_requests -= 1


class TimedInferenceMixin(ThreadSafeInferenceMixin):
    """
    Mixin providing standardized inference with timing and padding analysis.

    Extracts the common ~90 lines of code from MPSBackend and MLXBackend
    for measuring tokenization time, inference time, and padding statistics.

    Requirements:
        - self._tokenizer: HuggingFace tokenizer
        - self._max_length: Max sequence length
        - self.device: Target device string
        - self.model: CrossEncoder model with .model attribute
    """

    # These must be set by the implementing class
    _tokenizer = None
    _max_length: int = 512
    device: str = "cpu"
    model = None

    @with_inference_mode
    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> "InferenceResult":
        """
        Run inference with separate timing for tokenization and model forward pass.

        This method manually performs tokenization and model inference to
        get accurate timing breakdown for bottleneck analysis.
        Thread-safe: uses lock to serialize GPU operations.

        Args:
            pairs: List of (query, document) tuples

        Returns:
            InferenceResult with scores, timing breakdown, and padding analysis
        """
        from .base_backend import InferenceResult

        self._acquire_for_inference()
        try:
            total_start = time.perf_counter()

            # Stage 1: Tokenization
            tokenize_start = time.perf_counter()

            # Use batch tokenization for better performance
            texts = [[pair[0], pair[1]] for pair in pairs]
            features = self._tokenizer(
                texts,
                padding=True,
                truncation="longest_first",
                return_tensors="pt",
                max_length=self._max_length,
            )

            # === PADDING ANALYSIS ===
            attention_mask = features["attention_mask"]
            batch_size, max_seq_length = attention_mask.shape

            # Real tokens per sequence (where attention_mask == 1)
            real_tokens_per_seq = attention_mask.sum(dim=1)
            total_real_tokens = int(real_tokens_per_seq.sum().item())
            total_tokens = batch_size * max_seq_length
            padded_tokens = total_tokens - total_real_tokens
            padding_ratio = padded_tokens / total_tokens if total_tokens > 0 else 0.0
            avg_seq_length = float(real_tokens_per_seq.float().mean().item())

            # Move to device
            features = {k: v.to(self.device) for k, v in features.items()}

            t_tokenize_ms = (time.perf_counter() - tokenize_start) * 1000

            # Stage 2: Model inference
            inference_start = time.perf_counter()

            # Sync before inference for accurate timing
            sync_device(self.device)

            # Forward pass
            model_predictions = self.model.model(**features, return_dict=True)
            logits = model_predictions.logits

            # Apply activation function based on model config
            if self.model.config.num_labels == 1:
                scores = torch.sigmoid(logits).squeeze(-1)
            else:
                scores = torch.softmax(logits, dim=-1)[:, 1]

            # Sync after inference for accurate timing
            sync_device(self.device)

            t_model_inference_ms = (time.perf_counter() - inference_start) * 1000

            # Convert to numpy
            scores_np = scores.cpu().numpy()

            total_ms = (time.perf_counter() - total_start) * 1000

            return InferenceResult(
                scores=scores_np,
                t_tokenize_ms=t_tokenize_ms,
                t_model_inference_ms=t_model_inference_ms,
                total_ms=total_ms,
                # Padding analysis
                total_tokens=total_tokens,
                real_tokens=total_real_tokens,
                padded_tokens=padded_tokens,
                padding_ratio=padding_ratio,
                max_seq_length=max_seq_length,
                avg_seq_length=avg_seq_length,
                batch_size=batch_size,
            )
        finally:
            self._release_after_inference()

    def _infer_with_lock(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        """
        Run standard inference with thread safety.

        Args:
            pairs: List of (query, document) tuples

        Returns:
            Array of relevance scores
        """
        self._acquire_for_inference()
        try:
            return self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
        finally:
            self._release_after_inference()


class SimpleTimedInferenceMixin(ThreadSafeInferenceMixin):
    """
    Simplified timed inference mixin for backends without manual tokenization.

    Uses the model's built-in predict() method and wraps it with timing.
    Suitable for PyTorchBackend, CompiledBackend where we don't need
    detailed tokenization timing.
    """

    model = None
    device: str = "cpu"

    @with_inference_mode
    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> "InferenceResult":
        """
        Run inference with timing (no tokenization breakdown).

        Args:
            pairs: List of (query, document) tuples

        Returns:
            InferenceResult with scores and total timing
        """
        from .base_backend import InferenceResult

        self._acquire_for_inference()
        try:
            start = time.perf_counter()

            sync_device(self.device)
            scores = self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
            sync_device(self.device)

            total_ms = (time.perf_counter() - start) * 1000

            return InferenceResult(
                scores=scores,
                t_tokenize_ms=0.0,  # Not measured separately
                t_model_inference_ms=total_ms,
                total_ms=total_ms,
                batch_size=len(pairs),
            )
        finally:
            self._release_after_inference()
