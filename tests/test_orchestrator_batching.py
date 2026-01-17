import time
from unittest.mock import MagicMock

from src.server.dto import BatchConfig
from src.server.services.orchestrator_service import OrchestratorService


class TestOrchestratorBatching:
    def test_batching_enabled_on_setup(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=16, timeout_ms=50.0)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator._batching_enabled is True
        assert orchestrator._max_batch_size == 16
        assert orchestrator._timeout_ms == 50.0
        assert orchestrator.pipeline is not None

        orchestrator.stop()

    def test_batching_disabled_on_setup(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=False)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator._batching_enabled is False

    def test_get_batching_info(self, minimal_config):
        minimal_config.batching = BatchConfig(
            enabled=True, max_batch_size=32, timeout_ms=200.0, length_aware=True
        )
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        info = orchestrator.get_batching_info()
        assert info["batching_enabled"] is True
        assert info["max_batch_size"] == 32
        assert info["timeout_ms"] == 200.0
        assert info["length_aware"] is True
        assert "pending" in info

        orchestrator.stop()

    def test_schedule_delegates_to_pipeline(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=8)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        mock_result = MagicMock()
        orchestrator.pipeline = MagicMock()
        orchestrator.pipeline.schedule.return_value = mock_result

        result = orchestrator.schedule([("query", "doc")])

        orchestrator.pipeline.schedule.assert_called_once_with([("query", "doc")])
        assert result == mock_result

        orchestrator.stop()

    def test_batch_loop_stops_on_shutdown(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=8)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator.pipeline is not None

        orchestrator.stop()
        time.sleep(0.1)
