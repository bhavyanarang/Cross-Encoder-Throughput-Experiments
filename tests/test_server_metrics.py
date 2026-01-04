from src.server.dto.metrics import (
    MetricsCollector,
    StageMetrics,
)
from src.server.services.metrics_service import MetricsService
from src.server.services.process_monitor_service import ProcessMonitorService


class TestStageMetrics:
    def test_stage_metrics_record(self):
        metrics = StageMetrics()
        metrics.record(10.5)
        metrics.record(20.0)
        metrics.record(15.3)

        assert len(metrics.latencies) == 3
        assert 10.5 in metrics.latencies
        assert 20.0 in metrics.latencies
        assert 15.3 in metrics.latencies

    def test_stage_metrics_empty(self):
        metrics = StageMetrics()
        assert len(metrics.latencies) == 0

    def test_stage_metrics_reset(self):
        metrics = StageMetrics()
        metrics.record(10.0)
        assert len(metrics.latencies) == 1
        metrics.reset()
        assert len(metrics.latencies) == 0


class TestProcessMonitorService:
    def test_process_monitor_init(self):
        monitor = ProcessMonitorService()
        cpu = monitor.get_cpu_percent()

        assert isinstance(cpu, float)
        assert cpu >= 0


class TestMetricsCollector:
    def test_metrics_collector_record(self):
        collector = MetricsCollector()
        collector.record(10.5, num_queries=2)
        collector.record(20.0, num_queries=1)

        assert collector.query_count == 3
        assert collector.request_count == 2
        assert len(collector.latencies) == 2

    def test_metrics_collector_empty(self):
        collector = MetricsCollector()
        assert collector.query_count == 0
        assert collector.request_count == 0
        assert len(collector.latencies) == 0

    def test_metrics_collector_stage_timings(self):
        collector = MetricsCollector()

        collector.record(15.0)
        collector.record_stage_timings(
            t_tokenize=5.0,
            t_model_inference=10.0,
            t_tokenizer_queue_wait=2.0,
            total_ms=15.0,
        )

        tokenize_tracker = collector._stage_tracker_manager.get("tokenize")
        assert tokenize_tracker.last_value_ms == 5.0

        inference_tracker = collector._stage_tracker_manager.get("model_inference")
        assert inference_tracker.last_value_ms == 10.0

    def test_metrics_collector_padding_stats(self):
        collector = MetricsCollector()

        collector.record(10.0)
        collector.record_padding_stats(
            padding_ratio=0.25,
            padded_tokens=100,
            total_tokens=400,
            max_seq_length=512,
            avg_seq_length=384.0,
        )

        assert collector._padding_tracker.last_ratio == 0.25
        assert collector._padding_tracker.last_max_seq_length == 512
        assert collector._padding_tracker.last_avg_seq_length == 384.0

    def test_metrics_collector_experiment_info(self):
        collector = MetricsCollector()
        collector.set_experiment_info(
            name="test-exp",
            description="Test experiment",
            backend="pytorch",
            device="cpu",
        )

        assert collector.experiment_name == "test-exp"
        assert collector.experiment_description == "Test experiment"
        assert collector.backend_type == "pytorch"
        assert collector.device == "cpu"

    def test_metrics_collector_is_active(self):
        collector = MetricsCollector()
        assert len(collector.latencies) == 0

        collector.record(10.0)
        assert len(collector.latencies) == 1

    def test_metrics_collector_reset(self):
        collector = MetricsCollector()
        collector.record(10.0)
        collector.record_stage_timings(t_tokenize=5.0, total_ms=10.0)
        collector.reset()

        assert collector.query_count == 0
        assert collector.request_count == 0
        assert len(collector.latencies) == 0

    def test_metrics_collector_gpu_memory(self):
        service = MetricsService()
        memory = service.get_gpu_memory_mb()

        assert isinstance(memory, float)
        assert memory >= 0
