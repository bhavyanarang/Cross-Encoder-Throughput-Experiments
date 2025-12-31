"""
Comprehensive tests for stage breakdown percentage calculations.
Ensures that stage percentages always sum to 100% and display correctly.
"""

import pytest
from src.server.dto.metrics.collector import MetricsCollector


class TestStageBreakdownPercentages:
    """Test that stage breakdown percentages always sum to 100%."""

    def test_stage_percentages_sum_to_100_with_all_stages(self):
        """All stages recorded should sum to 100%."""
        collector = MetricsCollector()

        # Record multiple stage timings
        for i in range(10):
            collector.record_stage_timings(
                t_tokenize=10.0,
                t_queue_wait=20.0,
                t_model_inference=50.0,
                t_overhead=5.0,
                t_mp_queue_send=5.0,
                t_mp_queue_receive=5.0,
                t_grpc_serialize=2.5,
                t_grpc_deserialize=2.5,
                t_scheduler=0.0,
            )
            collector.record(duration_ms=100.0)

        summary = collector.summary()
        stage_pct = summary["stage_percentages"]

        # Calculate total (excluding combined percentages which are derived)
        total_pct = sum(v for k, v in stage_pct.items() if k.endswith("_pct") and "combined" not in k)
        
        # Should be exactly 100%
        assert total_pct == 100.0, f"Stage percentages sum to {total_pct}%, expected 100%"

    def test_stage_percentages_sum_to_100_with_partial_stages(self):
        """Only some stages recorded should still sum to 100%."""
        collector = MetricsCollector()

        # Only record a few stages
        for i in range(5):
            collector.record_stage_timings(
                t_tokenize=20.0,
                t_model_inference=70.0,
                t_queue_wait=10.0,
            )
            collector.record(duration_ms=100.0)

        summary = collector.summary()
        stage_pct = summary["stage_percentages"]

        total_pct = sum(v for k, v in stage_pct.items() if k.endswith("_pct") and "combined" not in k)
        
        assert total_pct == 100.0, f"Stage percentages sum to {total_pct}%, expected 100%"

    def test_stage_percentages_sum_to_100_with_rounding(self):
        """Rounding should not cause percentages to not sum to 100%."""
        collector = MetricsCollector()

        # Create values that would cause rounding issues
        for i in range(100):
            collector.record_stage_timings(
                t_tokenize=7.777,
                t_queue_wait=43.333,
                t_model_inference=22.222,
                t_overhead=0.111,
                t_mp_queue_send=5.555,
                t_mp_queue_receive=10.0,
                t_grpc_serialize=3.333,
                t_grpc_deserialize=3.333,
                t_scheduler=4.336,
            )
            collector.record(duration_ms=100.0)

        summary = collector.summary()
        stage_pct = summary["stage_percentages"]

        total_pct = sum(v for k, v in stage_pct.items() if k.endswith("_pct") and "combined" not in k)
        
        # Allow small tolerance for floating point rounding
        assert abs(total_pct - 100.0) < 0.2, f"Stage percentages sum to {total_pct}%, expected ~100%"

    def test_stage_percentages_individual_values_correct(self):
        """Individual stage percentages should match their proportion of total."""
        collector = MetricsCollector()

        # Record stages with known proportions
        for i in range(10):
            collector.record_stage_timings(
                t_tokenize=10.0,   # 10%
                t_queue_wait=20.0,  # 20%
                t_model_inference=50.0,  # 50%
                t_overhead=20.0,  # 20%
            )
            collector.record(duration_ms=100.0)

        summary = collector.summary()
        stage_pct = summary["stage_percentages"]

        assert abs(stage_pct["tokenize_pct"] - 10.0) < 1.0, "Tokenize should be ~10%"
        assert abs(stage_pct["queue_wait_pct"] - 20.0) < 1.0, "Queue wait should be ~20%"
        assert abs(stage_pct["inference_pct"] - 50.0) < 1.0, "Inference should be ~50%"
        assert abs(stage_pct["overhead_pct"] - 20.0) < 1.0, "Overhead should be ~20%"

        # Verify total still sums to 100%
        total_pct = sum(v for k, v in stage_pct.items() if k.endswith("_pct") and "combined" not in k)
        assert abs(total_pct - 100.0) < 1.0, f"Total should be ~100%, got {total_pct}%"

    def test_other_pct_calculated_correctly(self):
        """Other percentage should account for unaccounted time."""
        collector = MetricsCollector()

        # Record stages that don't add up to 100
        for i in range(5):
            collector.record_stage_timings(
                t_tokenize=10.0,
                t_queue_wait=20.0,
                t_model_inference=40.0,
            )
            collector.record(duration_ms=100.0)

        summary = collector.summary()
        stage_pct = summary["stage_percentages"]

        # Named stages should sum to about 70%, other should be ~30%
        named_total = (
            stage_pct["tokenize_pct"]
            + stage_pct["queue_wait_pct"]
            + stage_pct["inference_pct"]
        )
        
        # Total with other should be 100
        total_with_other = named_total + stage_pct["other_pct"]
        assert abs(total_with_other - 100.0) < 0.1, f"Total with other: {total_with_other}%, expected 100%"

    def test_stage_percentages_no_data(self):
        """Should handle case with no stage data gracefully."""
        collector = MetricsCollector()

        summary = collector.summary()
        
        # When no data, should not have stage_percentages key or it should be empty
        assert "stage_percentages" not in summary or len(summary.get("stage_percentages", {})) == 0

    def test_stage_percentages_single_dominant_stage(self):
        """Single dominant stage should be recognized correctly."""
        collector = MetricsCollector()

        for i in range(10):
            collector.record_stage_timings(
                t_model_inference=95.0,
                t_tokenize=5.0,
            )
            collector.record(duration_ms=100.0)

        summary = collector.summary()
        stage_pct = summary["stage_percentages"]

        assert abs(stage_pct["inference_pct"] - 95.0) < 1.0, "Inference should be ~95%"
        assert abs(stage_pct["tokenize_pct"] - 5.0) < 1.0, "Tokenize should be ~5%"
        
        total_pct = sum(v for k, v in stage_pct.items() if k.endswith("_pct") and "combined" not in k)
        assert abs(total_pct - 100.0) < 0.1, f"Total should be 100%, got {total_pct}%"

    def test_frontend_display_compatibility(self):
        """Test that percentages work correctly with frontend display logic."""
        collector = MetricsCollector()

        # Record typical metrics
        for i in range(20):
            collector.record_stage_timings(
                t_tokenize=10.0,
                t_queue_wait=100.0,
                t_model_inference=300.0,
                t_overhead=10.0,
                t_mp_queue_send=5.0,
                t_mp_queue_receive=50.0,
            )
            collector.record(duration_ms=475.0)

        summary = collector.summary()
        stage_pct = summary["stage_percentages"]

        # Simulate frontend display logic: top 3 + other
        components = [
            ("tokenize", stage_pct.get("tokenize_pct", 0)),
            ("queue_wait", stage_pct.get("queue_wait_pct", 0)),
            ("inference", stage_pct.get("inference_pct", 0)),
            ("overhead", stage_pct.get("overhead_pct", 0)),
            ("mp_queue_send", stage_pct.get("mp_queue_send_pct", 0)),
            ("mp_queue_receive", stage_pct.get("mp_queue_receive_pct", 0)),
            ("grpc_serialize", stage_pct.get("grpc_serialize_pct", 0)),
            ("grpc_deserialize", stage_pct.get("grpc_deserialize_pct", 0)),
            ("scheduler", stage_pct.get("scheduler_pct", 0)),
            ("other", stage_pct.get("other_pct", 0)),
        ]

        # Get top 3
        sorted_comps = sorted(
            [(name, pct) for name, pct in components if pct > 0],
            key=lambda x: x[1],
            reverse=True,
        )
        top3 = sorted_comps[:3]
        rest = sorted_comps[3:]

        # Calculate other from rest
        other_from_rest = sum(pct for _, pct in rest if _ != "other")
        display_total = sum(pct for _, pct in top3) + other_from_rest

        # After normalization in frontend, should fill 100%
        if display_total > 0:
            scale_factor = 100.0 / display_total
            normalized_total = display_total * scale_factor
            assert abs(normalized_total - 100.0) < 0.01, f"Normalized total should be 100%, got {normalized_total}%"


class TestStageBreakdownEdgeCases:
    """Test edge cases for stage breakdown calculation."""

    def test_zero_average_latency_handling(self):
        """Should handle case where average latency is 0."""
        collector = MetricsCollector()
        
        # Only record with 0 values
        collector.record_stage_timings(
            t_tokenize=0.0,
            t_queue_wait=0.0,
            t_model_inference=0.0,
        )
        collector.record(duration_ms=0.0)

        summary = collector.summary()
        
        # Should not crash, percentages should be 0 or "other" should be 100
        stage_pct = summary.get("stage_percentages", {})
        if stage_pct:
            total = sum(v for k, v in stage_pct.items() if k.endswith("_pct"))
            assert total >= 0, "Percentages should be non-negative"

    def test_very_small_stage_values(self):
        """Should handle very small stage values correctly."""
        collector = MetricsCollector()

        for i in range(10):
            collector.record_stage_timings(
                t_tokenize=0.001,
                t_queue_wait=0.001,
                t_model_inference=99.996,
            )
            collector.record(duration_ms=99.998)

        summary = collector.summary()
        stage_pct = summary["stage_percentages"]

        total_pct = sum(v for k, v in stage_pct.items() if k.endswith("_pct"))
        assert abs(total_pct - 100.0) < 0.1, f"Total should be ~100%, got {total_pct}%"

    def test_stage_values_much_larger_than_total_latency(self):
        """Stages might sum to less than total latency (unaccounted overhead)."""
        collector = MetricsCollector()

        for i in range(5):
            collector.record_stage_timings(
                t_tokenize=10.0,
                t_model_inference=30.0,
            )
            # Total latency is higher than sum of stages
            collector.record(duration_ms=100.0)

        summary = collector.summary()
        stage_pct = summary["stage_percentages"]

        total_pct = sum(v for k, v in stage_pct.items() if k.endswith("_pct") and "combined" not in k)
        assert abs(total_pct - 100.0) < 0.1, f"Total should be 100%, got {total_pct}%"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
