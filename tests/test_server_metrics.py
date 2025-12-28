from unittest.mock import patch

from src.server.models.server_metrics import (
    MetricsCollector,
    ProcessMonitor,
    StageMetrics,
    TokenizerWorkerMetrics,
    WorkerMetrics,
)


class TestStageMetrics:
    def test_stage_metrics_record(self):
        metrics = StageMetrics()
        metrics.record(10.5)
        metrics.record(20.0)
        metrics.record(15.3)

        stats = metrics.get_stats()
        assert stats["count"] == 3
        assert stats["avg_ms"] > 0
        assert stats["p50_ms"] > 0
        assert stats["p95_ms"] > 0

    def test_stage_metrics_empty(self):
        metrics = StageMetrics()
        stats = metrics.get_stats()
        assert stats["count"] == 0
        assert stats["avg_ms"] == 0
        assert stats["p50_ms"] == 0
        assert stats["p95_ms"] == 0

    def test_stage_metrics_reset(self):
        metrics = StageMetrics()
        metrics.record(10.0)
        metrics.reset()
        stats = metrics.get_stats()
        assert stats["count"] == 0


class TestWorkerMetrics:
    def test_worker_metrics_record(self):
        metrics = WorkerMetrics(worker_id=0)
        metrics.record(10.5, num_queries=2)
        metrics.record(20.0, num_queries=1)

        stats = metrics.get_stats()
        assert stats["worker_id"] == 0
        assert stats["query_count"] == 3
        assert stats["request_count"] == 2
        assert stats["avg_ms"] > 0

    def test_worker_metrics_empty(self):
        metrics = WorkerMetrics(worker_id=1)
        stats = metrics.get_stats()
        assert stats["worker_id"] == 1
        assert stats["query_count"] == 0
        assert stats["request_count"] == 0
        assert stats["avg_ms"] == 0

    def test_worker_metrics_reset(self):
        metrics = WorkerMetrics(worker_id=0)
        metrics.record(10.0)
        metrics.reset()
        stats = metrics.get_stats()
        assert stats["query_count"] == 0
        assert stats["request_count"] == 0


class TestTokenizerWorkerMetrics:
    def test_tokenizer_worker_metrics_record(self):
        metrics = TokenizerWorkerMetrics(worker_id=0)
        metrics.record(5.5, total_tokens=100)
        metrics.record(8.0, total_tokens=200)

        stats = metrics.get_stats()
        assert stats["worker_id"] == 0
        assert stats["request_count"] == 2
        assert stats["total_tokens_processed"] == 300
        assert stats["avg_ms"] > 0

    def test_tokenizer_worker_metrics_empty(self):
        metrics = TokenizerWorkerMetrics(worker_id=1)
        stats = metrics.get_stats()
        assert stats["worker_id"] == 1
        assert stats["request_count"] == 0
        assert stats["avg_ms"] == 0

    def test_tokenizer_worker_metrics_reset(self):
        metrics = TokenizerWorkerMetrics(worker_id=0)
        metrics.record(10.0, total_tokens=100)
        metrics.reset()
        stats = metrics.get_stats()
        assert stats["request_count"] == 0
        assert stats["total_tokens_processed"] == 0


class TestProcessMonitor:
    def test_process_monitor_init(self):
        monitor = ProcessMonitor()
        cpu = monitor.get_cpu_percent()

        assert isinstance(cpu, float)
        assert cpu >= 0


class TestMetricsCollector:
    def test_metrics_collector_record(self):
        collector = MetricsCollector()
        collector.record(10.5, num_queries=2)
        collector.record(20.0, num_queries=1)

        summary = collector.summary()
        assert summary["query_count"] == 3
        assert summary["count"] == 2

    def test_metrics_collector_empty(self):
        collector = MetricsCollector()
        summary = collector.summary()
        assert summary["query_count"] == 0

        assert "count" not in summary
        assert "is_running" in summary

    def test_metrics_collector_stage_timings(self):
        collector = MetricsCollector()

        collector.record(15.0)
        collector.record_stage_timings(
            t_tokenize=5.0,
            t_model_inference=10.0,
            t_queue_wait=2.0,
        )

        summary = collector.summary()
        assert summary["last_tokenize_ms"] == 5.0
        assert summary["last_inference_ms"] == 10.0
        assert summary["last_queue_wait_ms"] == 2.0

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

        summary = collector.summary()
        padding = summary["padding_analysis"]
        assert padding["last_padding_pct"] == 25.0
        assert padding["last_max_seq_length"] == 512
        assert padding["last_avg_seq_length"] == 384.0

    def test_metrics_collector_worker_stats(self):
        collector = MetricsCollector()

        collector.record(10.0)
        collector.record_worker_stats(worker_id=0, latency_ms=10.0, num_queries=1)
        collector.record_worker_stats(worker_id=1, latency_ms=20.0, num_queries=2)

        summary = collector.summary()
        worker_stats = summary["worker_stats"]
        assert len(worker_stats) == 2
        assert worker_stats[0]["worker_id"] == 0
        assert worker_stats[1]["worker_id"] == 1

    def test_metrics_collector_tokenizer_worker_stats(self):
        collector = MetricsCollector()

        collector.record(5.0)
        collector.record_tokenizer_worker_stats(worker_id=0, latency_ms=5.0, total_tokens=100)

        summary = collector.summary()
        tokenizer_stats = summary["tokenizer_worker_stats"]
        assert len(tokenizer_stats) == 1
        assert tokenizer_stats[0]["worker_id"] == 0

    def test_metrics_collector_experiment_info(self):
        collector = MetricsCollector()
        collector.set_experiment_info(
            name="test-exp",
            description="Test experiment",
            backend="pytorch",
            device="cpu",
        )

        summary = collector.summary()
        assert summary["experiment_name"] == "test-exp"
        assert summary["experiment_description"] == "Test experiment"
        assert summary["backend_type"] == "pytorch"
        assert summary["device"] == "cpu"

    def test_metrics_collector_is_active(self):
        collector = MetricsCollector()
        assert collector.is_active() is False

        collector.record(10.0)
        assert collector.is_active() is True

        with patch("src.server.models.metrics.collector.time.time") as mock_time:
            mock_time.return_value = collector.last_update_time + 5.0

            assert collector.is_active() is True

            mock_time.return_value = collector.last_update_time + 15.0

            collector.recent_latencies.append((collector.last_update_time + 5.0, 10.0))

            assert collector.is_active() is True

    def test_metrics_collector_reset(self):
        collector = MetricsCollector()
        collector.record(10.0)
        collector.record_stage_timings(t_tokenize=5.0)
        collector.reset()

        summary = collector.summary()

        assert summary["query_count"] == 0
        assert "count" not in summary

    def test_metrics_collector_gpu_memory(self):
        collector = MetricsCollector()
        memory = collector.get_gpu_memory_mb()

        assert isinstance(memory, float)
        assert memory >= 0

    def test_metrics_collector_gpu_utilization(self):
        collector = MetricsCollector()
        util = collector.get_gpu_utilization_pct()

        assert isinstance(util, float)
        assert 0 <= util <= 100
