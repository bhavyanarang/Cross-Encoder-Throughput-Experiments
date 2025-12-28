"""Inference service - handles all inference requests with tokenized data."""

import logging
import threading
from collections.abc import Callable

from src.models import InferenceResult
from src.server.pool import ModelPool
from src.server.services.tokenizer import TokenizedBatch

logger = logging.getLogger(__name__)


class InferenceService:
    """Service that handles all inference requests with pre-tokenized data."""

    def __init__(self, model_pool: ModelPool):
        self._model_pool = model_pool
        self._is_started = False

    def start(self) -> None:
        """Start the inference service."""
        if not self._model_pool.is_loaded:
            self._model_pool.start()
        self._is_started = True
        logger.info("Inference service started")

    def stop(self) -> None:
        """Stop the inference service."""
        self._is_started = False
        logger.info("Inference service stopped")

    def infer_async(
        self,
        tokenized_batch: TokenizedBatch,
        callback: Callable[[InferenceResult | None, Exception | None], None],
    ) -> None:
        """Run inference asynchronously with pre-tokenized data.

        Args:
            tokenized_batch: Pre-tokenized batch with features
            callback: Function called with (result, error) when done
        """
        if not self._is_started:
            callback(None, RuntimeError("Inference service not started"))
            return

        def _infer():
            try:
                # Use the model pool's infer_with_tokenized method
                result = self._model_pool.infer_with_tokenized(tokenized_batch)
                callback(result, None)
            except Exception as e:
                logger.error(f"Inference error: {e}")
                callback(None, e)

        # Run inference in a separate thread (non-blocking)
        thread = threading.Thread(target=_infer, daemon=True)
        thread.start()

    def infer_sync(self, tokenized_batch: TokenizedBatch) -> InferenceResult:
        """Run inference synchronously with pre-tokenized data.

        Args:
            tokenized_batch: Pre-tokenized batch with features

        Returns:
            InferenceResult with scores and timing
        """
        if not self._is_started:
            raise RuntimeError("Inference service not started")
        return self._model_pool.infer_with_tokenized(tokenized_batch)

    @property
    def is_started(self) -> bool:
        return self._is_started


__all__ = ["InferenceService"]
