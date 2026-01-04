from unittest.mock import MagicMock

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
    def test_start_initializes_pipeline(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.pipeline = MagicMock()
        orchestrator.pipeline.start = MagicMock()

        orchestrator.start()

        orchestrator.pipeline.start.assert_called_once()

        orchestrator.stop()

    def test_stop_cleans_up_resources(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.pipeline = MagicMock()
        orchestrator.pipeline.stop = MagicMock()

        orchestrator.stop()

        orchestrator.pipeline.stop.assert_called_once()


class TestOrchestratorServiceSchedule:
    def test_schedule_delegates_to_pipeline(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        mock_result = MagicMock()
        orchestrator.pipeline = MagicMock()
        orchestrator.pipeline.schedule.return_value = mock_result

        result = orchestrator.schedule([("query", "document")])

        orchestrator.pipeline.schedule.assert_called_once_with([("query", "document")])
        assert result == mock_result

        orchestrator.stop()

    def test_schedule_without_pipeline_raises_error(self):
        config = Config()
        orchestrator = OrchestratorService(config, "test")

        with pytest.raises(RuntimeError, match="not initialized"):
            orchestrator.schedule([("query", "document")])

    def test_get_tokenizer_worker_metrics(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.pipeline = MagicMock()
        orchestrator.pipeline.get_tokenizer_worker_metrics.return_value = [{"worker_id": 0}]

        metrics = orchestrator.get_tokenizer_worker_metrics()
        assert len(metrics) == 1

        orchestrator.stop()

    def test_get_inference_worker_metrics(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.pipeline = MagicMock()
        orchestrator.pipeline.get_inference_worker_metrics.return_value = [{"worker_id": 0}]

        metrics = orchestrator.get_inference_worker_metrics()
        assert len(metrics) == 1

        orchestrator.stop()

    def test_get_gpu_memory_mb(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.pipeline = MagicMock()
        orchestrator.pipeline.get_gpu_memory_mb.return_value = 512.0

        assert orchestrator.get_gpu_memory_mb() == 512.0

        orchestrator.stop()

    def test_reset_worker_metrics(self, minimal_config):
        orchestrator = OrchestratorService(minimal_config, "test")
        orchestrator.setup()

        orchestrator.pipeline = MagicMock()
        orchestrator.pipeline.reset_tokenizer_worker_metrics = MagicMock()
        orchestrator.pipeline.reset_inference_worker_metrics = MagicMock()

        orchestrator.reset_tokenizer_worker_metrics()
        orchestrator.pipeline.reset_tokenizer_worker_metrics.assert_called_once()

        orchestrator.reset_inference_worker_metrics()
        orchestrator.pipeline.reset_inference_worker_metrics.assert_called_once()

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
