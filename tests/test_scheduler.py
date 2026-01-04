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
    def test_batching_info(self, minimal_config):
        from src.server.services.orchestrator_service import OrchestratorService

        minimal_config.batching.enabled = True
        minimal_config.batching.max_batch_size = 16
        minimal_config.batching.timeout_ms = 100
        minimal_config.batching.length_aware = True

        orchestrator = OrchestratorService(minimal_config)
        assert not orchestrator._batching_enabled

        orchestrator.setup()
        assert orchestrator._batching_enabled

        info = orchestrator.get_batching_info()
        assert info["batching_enabled"] is True
        assert info["max_batch_size"] == 16
        assert info["timeout_ms"] == 100
        assert info["length_aware"] is True

        orchestrator.stop()

    def test_batching_disabled(self, minimal_config):
        from src.server.services.orchestrator_service import OrchestratorService

        minimal_config.batching.enabled = False

        orchestrator = OrchestratorService(minimal_config)
        orchestrator.setup()
        assert not orchestrator._batching_enabled

        orchestrator.stop()

    def test_batching_stop(self, minimal_config):
        from src.server.services.orchestrator_service import OrchestratorService

        minimal_config.batching.enabled = True

        orchestrator = OrchestratorService(minimal_config)
        orchestrator.setup()
        orchestrator.stop()
