import threading
from unittest.mock import MagicMock, patch

import pytest

from src.server.dto import BatchConfig, Config
from src.server.services.orchestrator_service import OrchestratorService


class TestOrchestratorServiceInit:
    def test_init_with_defaults(self):
        config = Config()
        orchestrator = OrchestratorService(config, "test-experiment")
        assert orchestrator.config == config
        assert orchestrator.experiment_name == "test-experiment"
        assert orchestrator.tokenizer_pool is None
        assert orchestrator.pool is None
        assert orchestrator.metrics is None
        assert orchestrator._batching_enabled is False

    def test_init_batching_state(self):
        config = Config()
        orchestrator = OrchestratorService(config)
        assert orchestrator._batching_enabled is False
        assert orchestrator._max_batch_size == 8
        assert orchestrator._batch_queue is not None
        assert orchestrator._batch_thread is None


class TestOrchestratorServiceSetup:
    def test_setup_creates_pools(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator.tokenizer_pool is not None
        assert orchestrator.pool is not None
        assert orchestrator.metrics is not None
        assert orchestrator._inference_queue is not None

        orchestrator.stop()

    def test_setup_with_batching_enabled(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True, max_batch_size=16)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator._batching_enabled is True
        assert orchestrator._batch_thread is not None
        assert orchestrator._batch_thread.is_alive()

        orchestrator.stop()

    def test_setup_with_batching_disabled(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=False)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator._batching_enabled is False
        assert orchestrator._batch_thread is None

        orchestrator.stop()

    def test_setup_tokenizer_model_fallback(self, minimal_config):
        minimal_config.tokenizer_pool.model_name = ""
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator.tokenizer_pool.model_name == minimal_config.model_pool.instances[0].name

        orchestrator.stop()


class TestOrchestratorServiceStartStop:
    def test_start_initializes_pools(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator._tokenization_started is False
        assert orchestrator._inference_started is False

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = False
        orchestrator.tokenizer_pool.start = MagicMock()
        orchestrator.tokenizer_pool.set_inference_queue = MagicMock()

        orchestrator.pool = MagicMock()
        orchestrator.pool.is_loaded = False
        orchestrator.pool.start = MagicMock()
        orchestrator.pool.set_inference_queue = MagicMock()

        orchestrator.metrics = MagicMock()
        orchestrator.metrics.start = MagicMock()

        with patch("src.server.services.orchestrator_service.start_dashboard"):
            orchestrator.start()

        assert orchestrator._tokenization_started is True
        assert orchestrator._inference_started is True
        orchestrator.tokenizer_pool.start.assert_called_once()
        orchestrator.pool.start.assert_called_once()

        orchestrator.stop()

    def test_stop_cleans_up_resources(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=True)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.stop = MagicMock()
        orchestrator.pool = MagicMock()
        orchestrator.pool.stop = MagicMock()
        orchestrator.metrics = MagicMock()
        orchestrator.metrics.stop = MagicMock()

        orchestrator._tokenization_started = True
        orchestrator._inference_started = True
        orchestrator._batch_thread = threading.Thread(target=lambda: None, daemon=True)
        orchestrator._batch_thread.start()

        orchestrator.stop()

        orchestrator.tokenizer_pool.stop.assert_called_once()
        orchestrator.pool.stop.assert_called_once()
        orchestrator.metrics.stop.assert_called_once()
        assert orchestrator._tokenization_started is False
        assert orchestrator._inference_started is False


class TestOrchestratorServiceSchedule:
    def test_schedule_without_batching(self, minimal_config):
        minimal_config.batching = BatchConfig(enabled=False)
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = True
        orchestrator.pool = MagicMock()
        orchestrator.pool.is_loaded = True
        orchestrator._tokenization_started = True
        orchestrator._inference_started = True

        with patch.object(orchestrator, "_schedule_direct") as mock_direct:
            mock_result = MagicMock()
            mock_direct.return_value = mock_result

            result = orchestrator.schedule([("query", "document")])

            mock_direct.assert_called_once_with([("query", "document")])
            assert result == mock_result

        orchestrator.stop()

    def test_schedule_not_started_raises_error(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        with pytest.raises(RuntimeError, match="not started"):
            orchestrator.schedule([("query", "document")])

        orchestrator.stop()

    def test_schedule_direct_creates_request(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = True
        orchestrator.pool = MagicMock()
        orchestrator.pool.is_loaded = True
        orchestrator._tokenization_started = True
        orchestrator._inference_started = True

        mock_request = MagicMock()
        mock_request.result_event = threading.Event()
        mock_request.inference_result = MagicMock()
        mock_request.error = None
        mock_request.t_queue_tokenization_wait_ms = 1.0
        mock_request.t_queue_inference_wait_ms = 2.0

        with patch.object(orchestrator, "submit_pipeline") as mock_submit:

            def submit_side_effect(item):
                item.request.inference_result = mock_request.inference_result
                item.request.result_event.set()

            mock_submit.side_effect = submit_side_effect

            result = orchestrator._schedule_direct([("q", "d")])

            assert result is not None
            mock_submit.assert_called_once()

        orchestrator.stop()

    def test_schedule_direct_handles_timeout(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = True
        orchestrator.pool = MagicMock()
        orchestrator.pool.is_loaded = True
        orchestrator._tokenization_started = True
        orchestrator._inference_started = True

        mock_request = MagicMock()
        mock_request.result_event = threading.Event()

        with patch.object(orchestrator, "submit_pipeline"):
            with patch("signal.signal"):
                with pytest.raises(RuntimeError, match="timed out"):
                    orchestrator._schedule_direct([("q", "d")])

        orchestrator.stop()

    def test_schedule_direct_handles_error(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.is_loaded = True
        orchestrator.pool = MagicMock()
        orchestrator.pool.is_loaded = True
        orchestrator._tokenization_started = True
        orchestrator._inference_started = True

        mock_request = MagicMock()
        mock_request.result_event = threading.Event()
        mock_request.error = RuntimeError("Test error")
        mock_request.result_event.set()

        with patch.object(orchestrator, "submit_pipeline") as mock_submit:

            def submit_side_effect(item):
                item.request.error = mock_request.error
                item.request.result_event.set()

            mock_submit.side_effect = submit_side_effect

            with pytest.raises(RuntimeError, match="Test error"):
                orchestrator._schedule_direct([("q", "d")])

        orchestrator.stop()


class TestOrchestratorServiceMethods:
    def test_get_metrics_not_setup(self):
        config = Config()
        orchestrator = OrchestratorService(config, "test")
        with pytest.raises(RuntimeError, match="not set up"):
            orchestrator.get_metrics()

    def test_get_metrics_after_setup(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        metrics = orchestrator.get_metrics()
        assert metrics is not None

        orchestrator.stop()

    def test_set_inference_queue(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        import queue

        test_queue = queue.Queue()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.set_inference_queue = MagicMock()

        orchestrator.set_inference_queue(test_queue)

        assert orchestrator._inference_queue == test_queue
        orchestrator.tokenizer_pool.set_inference_queue.assert_called_once_with(test_queue)

        orchestrator.stop()

    def test_submit_pipeline_not_started(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        from src.server.dto.pipeline import PipelineRequest, TokenizationQueueItem

        item = TokenizationQueueItem(
            request=PipelineRequest(request_id=1, pairs=[], submit_time=0.0),
            pairs=[],
        )

        with pytest.raises(RuntimeError, match="not started"):
            orchestrator.submit_pipeline(item)

        orchestrator.stop()

    def test_get_tokenizer_worker_metrics(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator.get_tokenizer_worker_metrics() == []

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.get_worker_metrics.return_value = [{"worker_id": 0}]
        orchestrator._tokenization_started = True

        metrics = orchestrator.get_tokenizer_worker_metrics()
        assert len(metrics) == 1

        orchestrator.stop()

    def test_get_inference_worker_metrics(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator.get_inference_worker_metrics() == []

        orchestrator.pool = MagicMock()
        orchestrator.pool.get_worker_metrics.return_value = [{"worker_id": 0}]
        orchestrator._inference_started = True

        metrics = orchestrator.get_inference_worker_metrics()
        assert len(metrics) == 1

        orchestrator.stop()

    def test_get_gpu_memory_mb(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator.get_gpu_memory_mb() == 0.0

        orchestrator.pool = MagicMock()
        orchestrator.pool.get_gpu_memory_mb.return_value = 512.0
        orchestrator._inference_started = True

        assert orchestrator.get_gpu_memory_mb() == 512.0

        orchestrator.stop()

    def test_reset_worker_metrics(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.tokenizer_pool = MagicMock()
        orchestrator.tokenizer_pool.reset_worker_metrics = MagicMock()
        orchestrator._tokenization_started = True

        orchestrator.reset_tokenizer_worker_metrics()
        orchestrator.tokenizer_pool.reset_worker_metrics.assert_called_once()

        orchestrator.pool = MagicMock()
        orchestrator.pool.reset_worker_metrics = MagicMock()
        orchestrator._inference_started = True

        orchestrator.reset_inference_worker_metrics()
        orchestrator.pool.reset_worker_metrics.assert_called_once()

        orchestrator.stop()

    def test_compatibility_properties(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        assert orchestrator.tokenization_service == orchestrator
        assert orchestrator.inference_service == orchestrator
        assert orchestrator.is_started == (
            orchestrator._tokenization_started and orchestrator._inference_started
        )

        orchestrator.stop()
