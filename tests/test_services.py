"""Tests for tokenization and inference services."""

from unittest.mock import MagicMock

import pytest

from src.server.pool import ModelPool
from src.server.services.inference_service import InferenceService
from src.server.services.tokenization_service import TokenizationService
from src.server.tokenizer_pool import TokenizerPool


class TestTokenizationService:
    def test_tokenization_service_init(self):
        """Test TokenizationService initialization."""
        mock_pool = MagicMock(spec=TokenizerPool)
        service = TokenizationService(mock_pool)
        assert service._tokenizer_pool == mock_pool
        assert service.is_started is False

    def test_tokenization_service_start_stop(self):
        """Test starting and stopping tokenization service."""
        mock_pool = MagicMock(spec=TokenizerPool)
        mock_pool.is_loaded = False
        service = TokenizationService(mock_pool)
        service.start()
        assert service.is_started is True
        mock_pool.start.assert_called_once()

        service.stop()
        assert service.is_started is False

    def test_tokenization_service_tokenize_sync_not_started(self):
        """Test tokenize_sync raises error when not started."""
        mock_pool = MagicMock(spec=TokenizerPool)
        service = TokenizationService(mock_pool)
        with pytest.raises(RuntimeError, match="not started"):
            service.tokenize_sync([("query", "document")])


class TestInferenceService:
    def test_inference_service_init(self):
        """Test InferenceService initialization."""
        mock_pool = MagicMock(spec=ModelPool)
        service = InferenceService(mock_pool)
        assert service._model_pool == mock_pool
        assert service.is_started is False

    def test_inference_service_start_stop(self):
        """Test starting and stopping inference service."""
        mock_pool = MagicMock(spec=ModelPool)
        mock_pool.is_loaded = False
        service = InferenceService(mock_pool)
        service.start()
        assert service.is_started is True
        mock_pool.start.assert_called_once()

        service.stop()
        assert service.is_started is False

    def test_inference_service_infer_sync_not_started(self):
        """Test infer_sync raises error when not started."""
        mock_pool = MagicMock(spec=ModelPool)
        service = InferenceService(mock_pool)

        # Create a mock tokenized batch
        class MockTokenizedBatch:
            pass

        tokenized_batch = MockTokenizedBatch()
        with pytest.raises(RuntimeError, match="not started"):
            service.infer_sync(tokenized_batch)
