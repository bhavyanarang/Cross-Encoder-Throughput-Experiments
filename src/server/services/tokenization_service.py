"""Async tokenization service - handles all tokenization requests."""

import logging
import threading
from collections.abc import Callable

from src.server.services.tokenizer import TokenizedBatch
from src.server.tokenizer_pool import TokenizerPool

logger = logging.getLogger(__name__)


class TokenizationService:
    """Service that handles all tokenization requests asynchronously."""

    def __init__(self, tokenizer_pool: TokenizerPool):
        self._tokenizer_pool = tokenizer_pool
        self._is_started = False

    def start(self) -> None:
        """Start the tokenization service."""
        if not self._tokenizer_pool.is_loaded:
            self._tokenizer_pool.start()
        self._is_started = True
        logger.info("Tokenization service started")

    def stop(self) -> None:
        """Stop the tokenization service."""
        self._is_started = False
        logger.info("Tokenization service stopped")

    def tokenize_async(
        self,
        pairs: list[tuple[str, str]],
        callback: Callable[[TokenizedBatch | None, Exception | None], None],
    ) -> None:
        """Tokenize pairs asynchronously and call callback with result.

        Args:
            pairs: Query-document pairs to tokenize
            callback: Function called with (tokenized_batch, error) when done
        """
        if not self._is_started:
            callback(None, RuntimeError("Tokenization service not started"))
            return

        def _tokenize():
            try:
                tokenized = self._tokenizer_pool.tokenize(pairs)
                callback(tokenized, None)
            except Exception as e:
                logger.error(f"Tokenization error: {e}")
                callback(None, e)

        # Run tokenization in a separate thread (non-blocking)
        thread = threading.Thread(target=_tokenize, daemon=True)
        thread.start()

    def tokenize_sync(self, pairs: list[tuple[str, str]]) -> TokenizedBatch:
        """Tokenize pairs synchronously (for backward compatibility).

        Args:
            pairs: Query-document pairs to tokenize

        Returns:
            TokenizedBatch with tokenized features
        """
        if not self._is_started:
            raise RuntimeError("Tokenization service not started")
        return self._tokenizer_pool.tokenize(pairs)

    @property
    def is_started(self) -> bool:
        return self._is_started


__all__ = ["TokenizationService"]
