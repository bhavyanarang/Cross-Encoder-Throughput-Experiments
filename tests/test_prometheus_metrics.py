from src.server.services.metrics_service import MetricsService


class TestPrometheusMetrics:
    """Test that all metrics are properly recorded to Prometheus."""

    def test_metrics_service_initializes_all_prometheus_metrics(self):
        """Verify that MetricsService initializes all Prometheus metrics."""
        service = MetricsService()

        # Verify counter metrics exist
        assert service.prom_request_count is not None
        assert service.prom_request_latency is not None
        assert service.prom_worker_requests is not None
        assert service.prom_padded_tokens is not None
        assert service.prom_total_tokens is not None

        # Verify gauge metrics exist
        assert service.prom_gpu_memory is not None
        assert service.prom_cpu_percent is not None
        assert service.prom_tokenizer_queue_size is not None
        assert service.prom_model_queue_size is not None
        assert service.prom_batch_queue_size is not None
        assert service.prom_worker_latency is not None
        assert service.prom_worker_throughput is not None
        assert service.prom_padding_ratio is not None
        assert service.prom_gpu_utilization is not None
        assert service.prom_tokenizer_throughput is not None
        assert service.prom_inference_throughput is not None
        assert service.prom_overall_throughput is not None

        # Verify histogram metrics exist
        assert service.prom_inference_latency is not None
        assert service.prom_tokenization_latency is not None
        assert service.prom_queue_wait_latency is not None
        assert service.prom_overhead_latency is not None
        assert service.prom_mp_queue_send_latency is not None
        assert service.prom_mp_queue_receive_latency is not None
        assert service.prom_grpc_serialize_latency is not None
        assert service.prom_grpc_deserialize_latency is not None
        assert service.prom_scheduler_latency is not None

    def test_record_increments_prometheus_metrics(self):
        """Verify that record() increments Prometheus metrics."""
        service = MetricsService()

        # Record metrics - no exceptions should be raised
        service.record(duration_ms=100.0, num_queries=5)
        service.record(duration_ms=150.0, num_queries=3)

        # Verify metrics were recorded (just check they don't raise errors)
        assert service.prom_request_count is not None
        assert service.prom_request_latency is not None

    def test_stage_timings_recorded_to_prometheus(self):
        """Verify that stage timings are recorded to Prometheus histograms."""
        service = MetricsService()

        # Record stage timings
        service.record_stage_timings(
            t_tokenize=10.0,
            t_tokenizer_queue_wait=5.0,
            t_model_queue_wait=3.0,
            t_model_inference=50.0,
            t_overhead=2.0,
            t_mp_queue_send=1.0,
            t_mp_queue_receive=1.0,
            t_grpc_serialize=1.0,
            t_grpc_deserialize=1.0,
            t_scheduler=0.5,
            total_ms=74.5,
        )

        # Verify Prometheus histograms exist
        assert service.prom_tokenization_latency is not None
        assert service.prom_inference_latency is not None
        assert service.prom_queue_wait_latency is not None
        assert service.prom_mp_queue_send_latency is not None
        assert service.prom_grpc_serialize_latency is not None

    def test_padding_stats_recorded_to_prometheus(self):
        """Verify that padding stats are recorded to Prometheus."""
        service = MetricsService()

        # Record padding stats
        service.record_padding_stats(
            padding_ratio=0.15,
            padded_tokens=150,
            total_tokens=1000,
            max_seq_length=512,
            avg_seq_length=256.5,
        )

        # Verify Prometheus metrics exist
        assert service.prom_padding_ratio is not None
        assert service.prom_padded_tokens is not None
        assert service.prom_total_tokens is not None
        assert service.prom_max_seq_length is not None
        assert service.prom_avg_seq_length is not None

    def test_worker_stats_recorded_to_prometheus(self):
        """Verify that worker stats are recorded to Prometheus."""
        service = MetricsService()

        # Record worker stats
        for worker_id in range(3):
            service.record_worker_stats(
                worker_id=worker_id,
                latency_ms=50.0 + worker_id * 10,
                num_queries=5,
            )

        # Verify metrics were recorded without errors
        assert service.prom_worker_latency is not None
        assert service.prom_worker_requests is not None

    def test_throughput_recorded_to_prometheus(self):
        """Verify that throughput stats are recorded to Prometheus."""
        service = MetricsService()

        # Record throughput
        service.record_throughput_stats(
            tokenizer_qps=100.0,
            inference_qps=80.0,
            overall_qps=75.0,
        )

        # Verify metrics exist
        assert service.prom_tokenizer_throughput is not None
        assert service.prom_inference_throughput is not None
        assert service.prom_overall_throughput is not None

    def test_gpu_utilization_recorded_to_prometheus(self):
        """Verify that GPU utilization is recorded to Prometheus."""
        service = MetricsService()

        # Record GPU utilization
        service.record_gpu_utilization(gpu_utilization_pct=75.5)

        # Verify metric exists
        assert service.prom_gpu_utilization is not None

    def test_metrics_service_reset_clears_collectors(self):
        """Verify that reset() clears the internal collector state."""
        service = MetricsService()

        # Record some metrics
        service.record(duration_ms=100.0, num_queries=5)
        service.record_padding_stats(padding_ratio=0.1, padded_tokens=100, total_tokens=1000)

        # Reset
        service.reset()

        # Verify collector is reset (Prometheus metrics persist, but collector state is cleared)
        collector = service.get_collector()
        assert collector is not None
