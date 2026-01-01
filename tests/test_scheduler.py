import threading
import time

from src.server.dto import PendingRequest


class TestPendingRequest:
    def test_pending_request_creation(self):
        event = threading.Event()
        pairs = [("query", "document")]
        req = PendingRequest(pairs=pairs, result_future=event, submit_time=time.perf_counter())
        assert req.pairs == pairs
        assert req.result_future == event
        assert req.result is None


class TestBatching:
    def test_batching_info(self):
        """Test batching configuration through orchestrator."""
        from src.server.dto import Config
        from src.server.services.orchestrator_service import OrchestratorService

        config = Config()
        config.batching.enabled = True
        config.batching.max_batch_size = 16
        config.batching.timeout_ms = 100
        config.batching.length_aware = True

        orchestrator = OrchestratorService(config)
        assert not orchestrator._batching_enabled  # Not enabled until setup

        orchestrator.setup()
        assert orchestrator._batching_enabled

        info = orchestrator.get_batching_info()
        assert info["batching_enabled"] is True
        assert info["max_batch_size"] == 16
        assert info["timeout_ms"] == 100
        assert info["length_aware"] is True

    def test_batching_disabled(self):
        """Test that batching can be disabled."""
        from src.server.dto import Config
        from src.server.services.orchestrator_service import OrchestratorService

        config = Config()
        config.batching.enabled = False

        orchestrator = OrchestratorService(config)
        orchestrator.setup()
        assert not orchestrator._batching_enabled

    def test_batching_stop(self):
        """Test that batching stops cleanly."""
        from src.server.dto import Config
        from src.server.services.orchestrator_service import OrchestratorService

        config = Config()
        config.batching.enabled = True

        orchestrator = OrchestratorService(config)
        orchestrator.setup()
        orchestrator.stop()
