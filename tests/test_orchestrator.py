import pytest

from src.server.dto import Config, ModelConfig, PoolConfig
from src.server.services import OrchestratorService


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

        # Pipeline orchestrator is always used (batching config is passed but not used in pipeline mode)
        assert hasattr(orchestrator, 'schedule')
        assert callable(orchestrator.schedule)
        
        # Cleanup to prevent hanging threads
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

        # Verify orchestrator has schedule method for pipeline
        assert hasattr(orchestrator, 'schedule')
        assert callable(orchestrator.schedule)
        
        # Cleanup to prevent hanging threads
        orchestrator.stop()

    def test_orchestrator_service_schedule_not_started(self):
        from src.server.dto import TokenizerPoolConfig

        config = Config(
            model_pool=PoolConfig(
                instances=[ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")]
            ),
            tokenizer_pool=TokenizerPoolConfig(enabled=True, num_workers=1),
        )
        orchestrator = OrchestratorService(config, "test")
        orchestrator.setup()
        
        # Should raise error because services not started
        with pytest.raises(RuntimeError, match="not started"):
            orchestrator.schedule([("query", "document")])
        
        orchestrator.stop()

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
