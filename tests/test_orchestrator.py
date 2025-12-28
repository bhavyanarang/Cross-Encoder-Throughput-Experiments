"""Tests for orchestrator."""

import pytest

from src.models import Config, ModelConfig, PoolConfig
from src.server.orchestrator import OrchestratorWrapper, ServerOrchestrator


class TestOrchestratorWrapper:
    def test_orchestrator_wrapper_init(self):
        """Test OrchestratorWrapper initialization."""

        class MockTokenizationService:
            pass

        class MockInferenceService:
            pass

        wrapper = OrchestratorWrapper(
            MockTokenizationService(),
            MockInferenceService(),
        )
        assert wrapper._tokenization_service is not None
        assert wrapper._inference_service is not None

    def test_orchestrator_wrapper_schedule(self):
        """Test OrchestratorWrapper schedule method."""
        import numpy as np

        from src.models import InferenceResult
        from src.server.services.tokenizer import TokenizedBatch

        class MockTokenizedBatch(TokenizedBatch):
            def __init__(self):
                self.features = {}
                self.tokenize_time_ms = 5.0

        class MockTokenizationService:
            def tokenize_sync(self, pairs):
                return MockTokenizedBatch()

        class MockInferenceService:
            def infer_sync(self, tokenized_batch):
                return InferenceResult(
                    scores=np.array([0.5, 0.8]),
                    t_model_inference_ms=10.0,
                    total_ms=15.0,
                )

        wrapper = OrchestratorWrapper(
            MockTokenizationService(),
            MockInferenceService(),
        )
        result = wrapper.schedule([("query", "document")])
        assert isinstance(result, InferenceResult)
        assert len(result.scores) == 2


class TestServerOrchestrator:
    def test_server_orchestrator_init(self):
        """Test ServerOrchestrator initialization."""
        config = Config()
        orchestrator = ServerOrchestrator(config, "test-experiment")
        assert orchestrator.config == config
        assert orchestrator.experiment_name == "test-experiment"
        assert orchestrator.tokenizer_pool is None
        assert orchestrator.pool is None

    def test_server_orchestrator_setup(self):
        """Test ServerOrchestrator setup."""
        from src.models import TokenizerPoolConfig

        config = Config(
            model_pool=PoolConfig(
                instances=[ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")]
            ),
            tokenizer_pool=TokenizerPoolConfig(enabled=True, num_workers=1),
        )
        orchestrator = ServerOrchestrator(config, "test")
        orchestrator.setup()

        assert orchestrator.tokenizer_pool is not None
        assert orchestrator.tokenization_service is not None
        assert orchestrator.pool is not None
        assert orchestrator.inference_service is not None
        assert orchestrator.metrics is not None

    def test_server_orchestrator_setup_with_batching(self):
        """Test ServerOrchestrator setup with batching enabled."""
        from src.models import BatchConfig

        config = Config(
            model_pool=PoolConfig(
                instances=[ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")]
            ),
            batching=BatchConfig(enabled=True, max_batch_size=16),
        )
        orchestrator = ServerOrchestrator(config, "test")
        orchestrator.setup()

        assert orchestrator.scheduler is not None
        assert orchestrator.inference_handler == orchestrator.scheduler

    def test_server_orchestrator_setup_without_batching(self):
        """Test ServerOrchestrator setup without batching."""
        from src.models import BatchConfig

        config = Config(
            model_pool=PoolConfig(
                instances=[ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")]
            ),
            batching=BatchConfig(enabled=False),
        )
        orchestrator = ServerOrchestrator(config, "test")
        orchestrator.setup()

        assert orchestrator.scheduler is None
        assert isinstance(orchestrator.inference_handler, OrchestratorWrapper)

    def test_server_orchestrator_get_inference_handler_not_setup(self):
        """Test get_inference_handler raises error when not setup."""
        config = Config()
        orchestrator = ServerOrchestrator(config, "test")
        with pytest.raises(RuntimeError, match="not set up"):
            orchestrator.get_inference_handler()

    def test_server_orchestrator_get_metrics_not_setup(self):
        """Test get_metrics raises error when not setup."""
        config = Config()
        orchestrator = ServerOrchestrator(config, "test")
        with pytest.raises(RuntimeError, match="not set up"):
            orchestrator.get_metrics()

    def test_server_orchestrator_stop(self):
        """Test stopping orchestrator."""
        config = Config(
            model_pool=PoolConfig(
                instances=[ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")]
            ),
        )
        orchestrator = ServerOrchestrator(config, "test")
        orchestrator.setup()
        # Should not raise
        orchestrator.stop()
