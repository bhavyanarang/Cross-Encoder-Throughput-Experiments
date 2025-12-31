import pytest

from src.server.dto import Config, ModelConfig, PoolConfig
from src.server.services.orchestrator_service import OrchestratorService, OrchestratorWrapper


class TestOrchestratorWrapper:
    def test_orchestrator_wrapper_init(self):
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
        import numpy as np

        from src.server.dto import InferenceResult, TokenizedBatch

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


class TestOrchestratorService:
    def test_orchestrator_service_init(self):
        config = Config()
        orchestrator = OrchestratorService(config, "test-experiment")
        assert orchestrator.config == config
        assert orchestrator.experiment_name == "test-experiment"
        assert orchestrator.tokenizer_pool is None
        assert orchestrator.pool is None

    def test_orchestrator_service_setup(self):
        from src.server.dto import TokenizerPoolConfig

        config = Config(
            model_pool=PoolConfig(
                instances=[ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")]
            ),
            tokenizer_pool=TokenizerPoolConfig(enabled=True, num_workers=1),
        )
        orchestrator = OrchestratorService(config, "test")
        orchestrator.setup()

        assert orchestrator.tokenizer_pool is not None
        assert orchestrator.tokenization_service is not None
        assert orchestrator.pool is not None
        assert orchestrator.inference_service is not None
        assert orchestrator.metrics is not None
        
        # Cleanup to prevent hanging threads
        orchestrator.stop()

    def test_orchestrator_service_setup_with_batching(self):
        from src.server.dto import BatchConfig

        config = Config(
            model_pool=PoolConfig(
                instances=[ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")]
            ),
            batching=BatchConfig(enabled=True, max_batch_size=16),
        )
        orchestrator = OrchestratorService(config, "test")
        orchestrator.setup()

        assert orchestrator.scheduler is not None
        assert orchestrator.inference_handler == orchestrator.scheduler
        
        # Cleanup to prevent hanging threads (scheduler has non-daemon thread)
        orchestrator.stop()

    def test_orchestrator_service_setup_without_batching(self):
        from src.server.dto import BatchConfig

        config = Config(
            model_pool=PoolConfig(
                instances=[ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")]
            ),
            batching=BatchConfig(enabled=False),
        )
        orchestrator = OrchestratorService(config, "test")
        orchestrator.setup()

        assert orchestrator.scheduler is None
        assert isinstance(orchestrator.inference_handler, OrchestratorWrapper)
        
        # Cleanup to prevent hanging threads
        orchestrator.stop()

    def test_orchestrator_service_get_inference_handler_not_setup(self):
        config = Config()
        orchestrator = OrchestratorService(config, "test")
        with pytest.raises(RuntimeError, match="not set up"):
            orchestrator.get_inference_handler()

    def test_orchestrator_service_get_metrics_not_setup(self):
        config = Config()
        orchestrator = OrchestratorService(config, "test")
        with pytest.raises(RuntimeError, match="not set up"):
            orchestrator.get_metrics()

    def test_orchestrator_service_stop(self):
        config = Config(
            model_pool=PoolConfig(
                instances=[ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")]
            ),
        )
        orchestrator = OrchestratorService(config, "test")
        orchestrator.setup()

        orchestrator.stop()
