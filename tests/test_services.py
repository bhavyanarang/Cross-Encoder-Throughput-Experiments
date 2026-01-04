from unittest.mock import MagicMock

import pytest

from src.server.services.orchestrator_service import OrchestratorService


class TestOrchestratorTokenizationMethods:
    def test_tokenization_methods_not_started(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config)
        orchestrator.setup()

        assert orchestrator.tokenization_is_started is False
        assert orchestrator.get_tokenizer_worker_metrics() == []

        from src.server.dto.pipeline import PipelineRequest, TokenizationQueueItem

        item = TokenizationQueueItem(
            request=PipelineRequest(request_id=1, pairs=[], submit_time=0.0),
            pairs=[],
        )
        with pytest.raises(RuntimeError, match="not started"):
            orchestrator.tokenizer_pool.submit_pipeline(item)

        orchestrator.stop()

    def test_tokenization_methods_started(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config)
        orchestrator.setup()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = False
        orchestrator.tokenizer_pool.get_worker_metrics.return_value = []
        orchestrator.tokenizer_pool.reset_worker_metrics.return_value = None
        orchestrator.tokenizer_pool.set_inference_queue.return_value = None

        orchestrator._tokenization_started = True
        assert orchestrator.tokenization_is_started is True
        assert orchestrator.get_tokenizer_worker_metrics() == []

        orchestrator.stop()


class TestOrchestratorInferenceMethods:
    def test_inference_methods_not_started(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config)
        orchestrator.setup()

        assert orchestrator.inference_is_started is False
        assert orchestrator.get_gpu_memory_mb() == 0.0
        assert orchestrator.get_inference_worker_metrics() == []

        orchestrator.stop()

    def test_inference_methods_started(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config)
        orchestrator.setup()

        original_get_gpu_memory_mb = orchestrator.pool.get_gpu_memory_mb
        orchestrator.pool.get_gpu_memory_mb = MagicMock(return_value=100.0)

        orchestrator.pipeline._inference_started = True
        assert orchestrator.inference_is_started is True
        assert orchestrator.get_gpu_memory_mb() == 100.0
        assert orchestrator.get_inference_worker_metrics() == []

        orchestrator.stop()
