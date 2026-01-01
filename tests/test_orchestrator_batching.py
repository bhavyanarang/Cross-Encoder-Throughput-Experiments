import threading
import time
from unittest.mock import MagicMock, patch

from src.server.dto import BatchConfig
from src.server.dto.pipeline import PipelineRequest
from src.server.services.orchestrator_service import OrchestratorService


class TestOrchestratorBatching:
    def test_batching_enabled_on_setup(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=16, timeout_ms=50.0)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator._batching_enabled is True
        assert orchestrator._max_batch_size == 16
        assert orchestrator._timeout_ms == 50.0
        assert orchestrator._batch_thread is not None
        assert orchestrator._batch_thread.is_alive()

        orchestrator.stop()
        time.sleep(0.1)
        assert not orchestrator._batch_thread.is_alive()

    def test_batching_disabled_on_setup(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=False)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator._batching_enabled is False
        assert orchestrator._batch_thread is None

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

    def test_schedule_with_batching_empty_queue(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=8)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator._batch_queue.qsize() == 0

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = True
        orchestrator.pool = MagicMock()
        orchestrator.pool.is_loaded = True
        orchestrator._tokenization_started = True
        orchestrator._inference_started = True

        with patch.object(orchestrator, "_schedule_direct") as mock_direct:
            mock_result = MagicMock()
            mock_direct.return_value = mock_result

            result = orchestrator.schedule([("query", "doc")])

            mock_direct.assert_called_once_with([("query", "doc")])
            assert result == mock_result

    def test_schedule_with_batching_concurrent_requests(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=4)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = True
        orchestrator.pool = MagicMock()
        orchestrator.pool.is_loaded = True
        orchestrator._tokenization_started = True
        orchestrator._inference_started = True

        from src.server.dto import PendingRequest

        req1 = PendingRequest(
            pairs=[("q1", "d1")],
            result_future=threading.Event(),
            submit_time=time.perf_counter(),
        )
        orchestrator._batch_queue.put(req1)

        assert orchestrator._batch_queue.qsize() > 0

        with patch.object(orchestrator, "submit_pipeline") as mock_submit:

            def process_batch_side_effect(item):
                time.sleep(0.01)
                import numpy as np

                from src.server.dto import InferenceResult

                item.request.inference_result = InferenceResult(
                    scores=np.array([0.5, 0.6]),
                    t_tokenize_ms=1.0,
                    t_model_inference_ms=2.0,
                    total_ms=3.0,
                )
                item.request.result_event.set()

            mock_submit.side_effect = process_batch_side_effect

            result = orchestrator.schedule([("q2", "d2")])

            assert result is not None

    def test_batch_loop_processes_immediately(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=2)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        from src.server.dto import PendingRequest

        req = PendingRequest(
            pairs=[("q", "d")],
            result_future=threading.Event(),
            submit_time=time.perf_counter(),
        )
        orchestrator._batch_queue.put(req)

        time.sleep(0.1)

        assert orchestrator._batch_queue.qsize() == 0

    def test_batch_loop_stops_on_shutdown(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=8)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator._batch_thread.is_alive()

        orchestrator.stop()
        time.sleep(0.2)
        assert not orchestrator._batch_thread.is_alive()

    def test_process_batch_distributes_results(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=4)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = True
        orchestrator.pool = MagicMock()
        orchestrator.pool.is_loaded = True
        orchestrator._tokenization_started = True
        orchestrator._inference_started = True

        import numpy as np

        from src.server.dto import InferenceResult, PendingRequest

        req1 = PendingRequest(
            pairs=[("q1", "d1")],
            result_future=threading.Event(),
            submit_time=time.perf_counter(),
        )
        req2 = PendingRequest(
            pairs=[("q2", "d2"), ("q3", "d3")],
            result_future=threading.Event(),
            submit_time=time.perf_counter(),
        )

        mock_request = PipelineRequest(
            request_id=1,
            pairs=[("q1", "d1"), ("q2", "d2"), ("q3", "d3")],
            submit_time=time.perf_counter(),
        )
        mock_request.inference_result = InferenceResult(
            scores=np.array([0.1, 0.2, 0.3]),
            t_tokenize_ms=5.0,
            t_model_inference_ms=10.0,
            total_ms=15.0,
        )
        mock_request.result_event = threading.Event()
        mock_request.result_event.set()

        with patch.object(orchestrator, "submit_pipeline") as mock_submit:

            def submit_side_effect(item):
                item.request.inference_result = mock_request.inference_result
                item.request.result_event.set()

            mock_submit.side_effect = submit_side_effect

            batch = [req1, req2]
            orchestrator._process_batch(batch)

            assert req1.result is not None
            assert req2.result is not None
            assert len(req1.result.scores) == 1
            assert len(req2.result.scores) == 2

    def test_process_batch_handles_errors(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=2)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = True
        orchestrator.pool = MagicMock()
        orchestrator.pool.is_loaded = True
        orchestrator._tokenization_started = True
        orchestrator._inference_started = True

        from src.server.dto import PendingRequest

        req = PendingRequest(
            pairs=[("q", "d")],
            result_future=threading.Event(),
            submit_time=time.perf_counter(),
        )

        test_error = RuntimeError("Test error")

        with patch.object(orchestrator, "submit_pipeline", side_effect=test_error):
            batch = [req]
            orchestrator._process_batch(batch)

            assert req.error == test_error
            assert req.result_future.is_set()

    def test_length_aware_batching(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=4, length_aware=True)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator._length_aware is True

        pairs = [
            ("long query " * 100, "long doc " * 100),
            ("short", "doc"),
            ("medium " * 50, "medium " * 50),
        ]

        from src.server.dto import PendingRequest

        batch = [
            PendingRequest(
                pairs=[p], result_future=threading.Event(), submit_time=time.perf_counter()
            )
            for p in pairs
        ]

        orchestrator._process_batch(batch)
