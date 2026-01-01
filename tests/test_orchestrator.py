import pytest

from src.server.dto import BatchConfig, Config
from src.server.services import OrchestratorService


class TestOrchestratorServiceBasic:
    def test_orchestrator_service_init(self):
        config = Config()
        orchestrator = OrchestratorService(config, "test-experiment")
        assert orchestrator.config == config
        assert orchestrator.experiment_name == "test-experiment"
        assert orchestrator.tokenizer_pool is None
        assert orchestrator.pool is None

    def test_orchestrator_service_setup(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator.tokenizer_pool is not None
        assert orchestrator.tokenization_service is not None
        assert orchestrator.pool is not None
        assert orchestrator.inference_service is not None
        assert orchestrator.metrics is not None

        orchestrator.stop()

    def test_orchestrator_service_setup_with_batching(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=16)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert hasattr(orchestrator, "schedule")
        assert callable(orchestrator.schedule)
        assert orchestrator._batching_enabled is True

        orchestrator.stop()

    def test_orchestrator_service_setup_without_batching(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=False)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert hasattr(orchestrator, "schedule")
        assert callable(orchestrator.schedule)
        assert orchestrator._batching_enabled is False

        orchestrator.stop()

    def test_orchestrator_service_schedule_not_started(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        with pytest.raises(RuntimeError, match="not started"):
            orchestrator.schedule([("query", "document")])

        orchestrator.stop()

    def test_orchestrator_service_get_metrics_not_setup(self):
        config = Config()
        orchestrator = OrchestratorService(config, "test")
        with pytest.raises(RuntimeError, match="not set up"):
            orchestrator.get_metrics()

    def test_orchestrator_service_stop(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()
        orchestrator.stop()
