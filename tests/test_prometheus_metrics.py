from src.server.services.metrics_service import MetricsService


class TestPrometheusMetrics:
    def test_metrics_service_initializes_all_prometheus_metrics(self):
        service = MetricsService()

        assert service.prom_request_count is not None
        assert service.prom_request_latency is not None
        assert service.prom_worker_requests is not None
        assert service.prom_padded_tokens is not None
        assert service.prom_total_tokens is not None

        assert service.prom_gpu_memory is not None
        assert service.prom_cpu_percent is not None
        assert service.prom_tokenizer_queue_size is not None
        assert service.prom_model_queue_size is not None
        assert service.prom_batch_queue_size is not None
        assert service.prom_worker_latency is not None
        assert service.prom_padding_ratio is not None

        assert service.prom_inference_latency is not None
        assert service.prom_tokenization_latency is not None
        assert service.prom_queue_wait_latency is not None

    def test_record_increments_prometheus_metrics(self):
        service = MetricsService()
        service.record(duration_ms=100.0, num_queries=5)
        service.record(duration_ms=150.0, num_queries=3)
        assert service.prom_request_count is not None
        assert service.prom_request_latency is not None

    def test_stage_timings_recorded_to_prometheus(self):
        service = MetricsService()
        service.record_stage_timings(
            t_tokenize=10.0,
            t_tokenizer_queue_wait=5.0,
            t_model_queue_wait=3.0,
            t_model_inference=50.0,
            t_overhead=2.0,
        )
        assert service.prom_tokenization_latency is not None
        assert service.prom_inference_latency is not None
        assert service.prom_queue_wait_latency is not None

    def test_padding_stats_recorded_to_prometheus(self):
        service = MetricsService()
        service.record_padding_stats(
            padding_ratio=0.15,
            padded_tokens=150,
            total_tokens=1000,
            max_seq_length=512,
            avg_seq_length=256.5,
        )
        assert service.prom_padding_ratio is not None
        assert service.prom_padded_tokens is not None
        assert service.prom_total_tokens is not None
        assert service.prom_max_seq_length is not None
        assert service.prom_avg_seq_length is not None

    def test_worker_stats_recorded_to_prometheus(self):
        service = MetricsService()
        for worker_id in range(3):
            service.record_worker_stats(
                worker_id=worker_id, latency_ms=50.0 + worker_id * 10, num_queries=5
            )
        assert service.prom_worker_latency is not None
        assert service.prom_worker_requests is not None
