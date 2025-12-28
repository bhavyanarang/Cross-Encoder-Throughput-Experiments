from src.server.models.metrics_dto import LatencyStats, PaddingStats, StageStats, ThroughputStats


class TestLatencyStats:
    def test_latency_stats_defaults(self):
        stats = LatencyStats()
        assert stats.count == 0
        assert stats.avg_ms == 0.0
        assert stats.min_ms == 0.0
        assert stats.max_ms == 0.0
        assert stats.p50_ms == 0.0
        assert stats.p95_ms == 0.0
        assert stats.p99_ms == 0.0

    def test_latency_stats_custom(self):
        stats = LatencyStats(
            count=100,
            avg_ms=50.5,
            min_ms=10.0,
            max_ms=200.0,
            p50_ms=45.0,
            p95_ms=150.0,
            p99_ms=180.0,
        )
        assert stats.count == 100
        assert stats.avg_ms == 50.5
        assert stats.min_ms == 10.0
        assert stats.max_ms == 200.0
        assert stats.p50_ms == 45.0
        assert stats.p95_ms == 150.0
        assert stats.p99_ms == 180.0


class TestThroughputStats:
    def test_throughput_stats_defaults(self):
        stats = ThroughputStats()
        assert stats.instant_qps == 0.0
        assert stats.avg_qps == 0.0
        assert stats.total_queries == 0
        assert stats.total_requests == 0

    def test_throughput_stats_custom(self):
        stats = ThroughputStats(
            instant_qps=100.5,
            avg_qps=95.2,
            total_queries=1000,
            total_requests=100,
        )
        assert stats.instant_qps == 100.5
        assert stats.avg_qps == 95.2
        assert stats.total_queries == 1000
        assert stats.total_requests == 100


class TestPaddingStats:
    def test_padding_stats_defaults(self):
        stats = PaddingStats()
        assert stats.avg_padding_pct == 0.0
        assert stats.p50_padding_pct == 0.0
        assert stats.p95_padding_pct == 0.0
        assert stats.total_wasted_pct == 0.0

    def test_padding_stats_custom(self):
        stats = PaddingStats(
            avg_padding_pct=25.5,
            p50_padding_pct=20.0,
            p95_padding_pct=50.0,
            total_wasted_pct=15.0,
        )
        assert stats.avg_padding_pct == 25.5
        assert stats.p50_padding_pct == 20.0
        assert stats.p95_padding_pct == 50.0
        assert stats.total_wasted_pct == 15.0


class TestStageStats:
    def test_stage_stats_defaults(self):
        stats = StageStats()
        assert stats.p50_ms == 0.0
        assert stats.p95_ms == 0.0
        assert stats.avg_ms == 0.0
        assert stats.count == 0

    def test_stage_stats_custom(self):
        stats = StageStats(
            p50_ms=10.5,
            p95_ms=25.0,
            avg_ms=12.3,
            count=50,
        )
        assert stats.p50_ms == 10.5
        assert stats.p95_ms == 25.0
        assert stats.avg_ms == 12.3
        assert stats.count == 50
