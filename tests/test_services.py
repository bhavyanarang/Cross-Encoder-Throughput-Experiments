from unittest.mock import MagicMock

import pytest

from src.server.services.inference_service import InferenceService, ModelPool
from src.server.services.tokenization_service import TokenizationService, TokenizerPool


class TestTokenizationService:
    def test_tokenization_service_init(self):
        mock_pool = MagicMock(spec=TokenizerPool)
        service = TokenizationService(mock_pool)
        assert service._tokenizer_pool == mock_pool
        assert service.is_started is False

    def test_tokenization_service_start_stop(self):
        mock_pool = MagicMock(spec=TokenizerPool)
        mock_pool.is_loaded = False
        service = TokenizationService(mock_pool)
        service.start()
        assert service.is_started is True
        mock_pool.start.assert_called_once()

        service.stop()
        assert service.is_started is False

    def test_tokenization_service_tokenize_sync_not_started(self):
        mock_pool = MagicMock(spec=TokenizerPool)
        service = TokenizationService(mock_pool)
        with pytest.raises(RuntimeError, match="not started"):
            service.tokenize_sync([("query", "document")])


class TestInferenceService:
    def test_inference_service_init(self):
        mock_pool = MagicMock(spec=ModelPool)
        service = InferenceService(mock_pool)
        assert service._model_pool == mock_pool
        assert service.is_started is False

    def test_inference_service_start_stop(self):
        mock_pool = MagicMock(spec=ModelPool)
        mock_pool.is_loaded = False
        service = InferenceService(mock_pool)
        service.start()
        assert service.is_started is True
        mock_pool.start.assert_called_once()

        service.stop()
        assert service.is_started is False

    def test_inference_service_infer_sync_not_started(self):
        mock_pool = MagicMock(spec=ModelPool)
        service = InferenceService(mock_pool)

        class MockTokenizedBatch:
            pass

        tokenized_batch = MockTokenizedBatch()
        with pytest.raises(RuntimeError, match="not started"):
            service.infer_sync(tokenized_batch)
