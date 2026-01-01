from unittest.mock import MagicMock

import pytest

from src.server.dto import Config
from src.server.dto.config import PoolConfig, TokenizerPoolConfig
from src.server.services.orchestrator_service import OrchestratorService


class TestOrchestratorTokenizationMethods:
    def test_tokenization_methods_not_started(self):
        config = Config(
            model_pool=PoolConfig(instances=[]),
            tokenizer_pool=TokenizerPoolConfig(),
        )
        orchestrator = OrchestratorService(config)
        orchestrator.setup()

        assert orchestrator.tokenization_is_started is False
        assert orchestrator.get_tokenizer_worker_metrics() == []

        from src.server.dto.pipeline import PipelineRequest, TokenizationQueueItem

        item = TokenizationQueueItem(
            request=PipelineRequest(request_id=1, pairs=[], submit_time=0.0),
            pairs=[],
        )
        with pytest.raises(RuntimeError, match="not started"):
            orchestrator.submit_pipeline(item)

    def test_tokenization_methods_started(self):
        config = Config(
            model_pool=PoolConfig(instances=[]),
            tokenizer_pool=TokenizerPoolConfig(),
        )
        orchestrator = OrchestratorService(config)
        orchestrator.setup()

        # Mock pools to avoid actual initialization
        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = False
        orchestrator.tokenizer_pool.get_worker_metrics.return_value = []
        orchestrator.tokenizer_pool.reset_worker_metrics.return_value = None
        orchestrator.tokenizer_pool.set_inference_queue.return_value = None

        orchestrator._tokenization_started = True
        assert orchestrator.tokenization_is_started is True
        assert orchestrator.get_tokenizer_worker_metrics() == []


class TestOrchestratorInferenceMethods:
    def test_inference_methods_not_started(self):
        config = Config(
            model_pool=PoolConfig(instances=[]),
            tokenizer_pool=TokenizerPoolConfig(),
        )
        orchestrator = OrchestratorService(config)
        orchestrator.setup()

        assert orchestrator.inference_is_started is False
        assert orchestrator.get_gpu_memory_mb() == 0.0
        assert orchestrator.get_inference_worker_metrics() == []

    def test_inference_methods_started(self):
        config = Config(
            model_pool=PoolConfig(instances=[]),
            tokenizer_pool=TokenizerPoolConfig(),
        )
        orchestrator = OrchestratorService(config)
        orchestrator.setup()

        # Mock pools to avoid actual initialization
        orchestrator.pool = MagicMock()
        orchestrator.pool.is_loaded = False
        orchestrator.pool.get_gpu_memory_mb.return_value = 100.0
        orchestrator.pool.get_worker_metrics.return_value = []
        orchestrator.pool.reset_worker_metrics.return_value = None
        orchestrator.pool.set_inference_queue.return_value = None

        orchestrator._inference_started = True
        assert orchestrator.inference_is_started is True
        assert orchestrator.get_gpu_memory_mb() == 100.0
        assert orchestrator.get_inference_worker_metrics() == []
