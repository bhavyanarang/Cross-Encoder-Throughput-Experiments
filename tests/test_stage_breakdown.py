import pytest

from src.server.services.metrics_service import MetricsService


class TestStageBreakdownPercentages:
    def test_stage_percentages_sum_to_100_with_all_stages(self):
        service = MetricsService()
        service.get_collector()

        for _i in range(10):
            service.record_stage_timings(
                t_tokenize=10.0,
                t_tokenizer_queue_wait=10.0,
                t_model_queue_wait=10.0,
                t_model_inference=50.0,
                t_overhead=5.0,
                t_mp_queue_send=5.0,
                t_mp_queue_receive=5.0,
                t_grpc_serialize=2.5,
                t_grpc_deserialize=2.5,
                t_scheduler=0.0,
                total_ms=100.0,
            )
            service.record(duration_ms=100.0)

        summary = service.get_summary()
        stage_pct = summary["stage_percentages"]

        total_pct = (
            stage_pct.get("tokenize_pct", 0)
            + stage_pct.get("tokenizer_queue_wait_pct", 0)
            + stage_pct.get("model_queue_wait_pct", 0)
            + stage_pct.get("inference_pct", 0)
            + stage_pct.get("overhead_pct", 0)
            + stage_pct.get("mp_queue_send_pct", 0)
            + stage_pct.get("mp_queue_receive_pct", 0)
            + stage_pct.get("grpc_serialize_pct", 0)
            + stage_pct.get("grpc_deserialize_pct", 0)
            + stage_pct.get("scheduler_pct", 0)
            + stage_pct.get("pipeline_overhead_pct", 0)
            + stage_pct.get("other_pct", 0)
        )

        assert abs(total_pct - 100.0) < 1.0, (
            f"Stage percentages sum to {total_pct}%, expected ~100%"
        )

    def test_stage_percentages_sum_to_100_with_partial_stages(self):
        service = MetricsService()
        for _i in range(5):
            service.record_stage_timings(
                t_tokenize=20.0,
                t_model_inference=70.0,
                t_tokenizer_queue_wait=5.0,
                t_model_queue_wait=5.0,
                total_ms=100.0,
            )
            service.record(duration_ms=100.0)

        summary = service.get_summary()
        stage_pct = summary["stage_percentages"]

        total_pct = (
            stage_pct.get("tokenize_pct", 0)
            + stage_pct.get("tokenizer_queue_wait_pct", 0)
            + stage_pct.get("model_queue_wait_pct", 0)
            + stage_pct.get("inference_pct", 0)
            + stage_pct.get("overhead_pct", 0)
            + stage_pct.get("mp_queue_send_pct", 0)
            + stage_pct.get("mp_queue_receive_pct", 0)
            + stage_pct.get("grpc_serialize_pct", 0)
            + stage_pct.get("grpc_deserialize_pct", 0)
            + stage_pct.get("scheduler_pct", 0)
            + stage_pct.get("pipeline_overhead_pct", 0)
            + stage_pct.get("other_pct", 0)
        )

        assert abs(total_pct - 100.0) < 1.0, (
            f"Stage percentages sum to {total_pct}%, expected ~100%"
        )

    def test_stage_percentages_sum_to_100_with_rounding(self):
        service = MetricsService()
        for _i in range(100):
            service.record_stage_timings(
                t_tokenize=7.777,
                t_tokenizer_queue_wait=21.666,
                t_model_queue_wait=21.667,
                t_model_inference=22.222,
                t_overhead=0.111,
                t_mp_queue_send=5.555,
                t_mp_queue_receive=10.0,
                t_grpc_serialize=3.333,
                t_grpc_deserialize=3.333,
                t_scheduler=4.336,
                total_ms=100.0,
            )
            service.record(duration_ms=100.0)

        summary = service.get_summary()
        stage_pct = summary["stage_percentages"]

        total_pct = (
            stage_pct.get("tokenize_pct", 0)
            + stage_pct.get("tokenizer_queue_wait_pct", 0)
            + stage_pct.get("model_queue_wait_pct", 0)
            + stage_pct.get("inference_pct", 0)
            + stage_pct.get("overhead_pct", 0)
            + stage_pct.get("mp_queue_send_pct", 0)
            + stage_pct.get("mp_queue_receive_pct", 0)
            + stage_pct.get("grpc_serialize_pct", 0)
            + stage_pct.get("grpc_deserialize_pct", 0)
            + stage_pct.get("scheduler_pct", 0)
            + stage_pct.get("pipeline_overhead_pct", 0)
            + stage_pct.get("other_pct", 0)
        )

        assert abs(total_pct - 100.0) < 1.0, (
            f"Stage percentages sum to {total_pct}%, expected ~100%"
        )

    def test_stage_percentages_individual_values_correct(self):
        service = MetricsService()
        for _i in range(10):
            service.record_stage_timings(
                t_tokenize=10.0,
                t_tokenizer_queue_wait=10.0,
                t_model_queue_wait=10.0,
                t_model_inference=50.0,
                t_overhead=20.0,
                total_ms=100.0,
            )
            service.record(duration_ms=100.0)

        summary = service.get_summary()
        stage_pct = summary["stage_percentages"]

        assert abs(stage_pct["tokenize_pct"] - 10.0) < 1.0, "Tokenize should be ~10%"
        queue_wait_total = stage_pct.get("tokenizer_queue_wait_pct", 0) + stage_pct.get(
            "model_queue_wait_pct", 0
        )
        assert abs(queue_wait_total - 20.0) < 1.0, "Queue wait should be ~20%"
        assert abs(stage_pct["inference_pct"] - 50.0) < 1.0, "Inference should be ~50%"
        assert abs(stage_pct["overhead_pct"] - 20.0) < 1.0, "Overhead should be ~20%"

        total_pct = (
            stage_pct.get("tokenize_pct", 0)
            + stage_pct.get("tokenizer_queue_wait_pct", 0)
            + stage_pct.get("model_queue_wait_pct", 0)
            + stage_pct.get("inference_pct", 0)
            + stage_pct.get("overhead_pct", 0)
            + stage_pct.get("mp_queue_send_pct", 0)
            + stage_pct.get("mp_queue_receive_pct", 0)
            + stage_pct.get("grpc_serialize_pct", 0)
            + stage_pct.get("grpc_deserialize_pct", 0)
            + stage_pct.get("scheduler_pct", 0)
            + stage_pct.get("pipeline_overhead_pct", 0)
            + stage_pct.get("other_pct", 0)
        )
        assert abs(total_pct - 100.0) < 1.0, f"Total should be ~100%, got {total_pct}%"

    def test_other_pct_calculated_correctly(self):
        service = MetricsService()
        for _i in range(5):
            service.record_stage_timings(
                t_tokenize=10.0,
                t_tokenizer_queue_wait=10.0,
                t_model_queue_wait=10.0,
                t_model_inference=40.0,
                total_ms=100.0,
            )
            service.record(duration_ms=100.0)

        summary = service.get_summary()
        stage_pct = summary["stage_percentages"]

        named_total = (
            stage_pct.get("tokenize_pct", 0)
            + stage_pct.get("tokenizer_queue_wait_pct", 0)
            + stage_pct.get("model_queue_wait_pct", 0)
            + stage_pct.get("inference_pct", 0)
        )

        total_with_other = (
            named_total + stage_pct.get("other_pct", 0) + stage_pct.get("pipeline_overhead_pct", 0)
        )
        assert abs(total_with_other - 100.0) < 1.0, (
            f"Total with other: {total_with_other}%, expected ~100%"
        )

    def test_stage_percentages_no_data(self):
        service = MetricsService()
        summary = service.get_summary()

        assert "stage_percentages" in summary
        stage_pct = summary["stage_percentages"]
        assert isinstance(stage_pct, dict)

    def test_stage_percentages_single_dominant_stage(self):
        service = MetricsService()
        for _i in range(10):
            service.record_stage_timings(
                t_model_inference=95.0,
                t_tokenize=5.0,
                total_ms=100.0,
            )
            service.record(duration_ms=100.0)

        summary = service.get_summary()
        stage_pct = summary["stage_percentages"]

        assert abs(stage_pct["inference_pct"] - 95.0) < 1.0, "Inference should be ~95%"
        assert abs(stage_pct["tokenize_pct"] - 5.0) < 1.0, "Tokenize should be ~5%"

        total_pct = (
            stage_pct.get("tokenize_pct", 0)
            + stage_pct.get("tokenizer_queue_wait_pct", 0)
            + stage_pct.get("model_queue_wait_pct", 0)
            + stage_pct.get("inference_pct", 0)
            + stage_pct.get("overhead_pct", 0)
            + stage_pct.get("mp_queue_send_pct", 0)
            + stage_pct.get("mp_queue_receive_pct", 0)
            + stage_pct.get("grpc_serialize_pct", 0)
            + stage_pct.get("grpc_deserialize_pct", 0)
            + stage_pct.get("scheduler_pct", 0)
            + stage_pct.get("pipeline_overhead_pct", 0)
            + stage_pct.get("other_pct", 0)
        )
        assert abs(total_pct - 100.0) < 1.0, f"Total should be ~100%, got {total_pct}%"

    def test_frontend_display_compatibility(self):
        service = MetricsService()
        for _i in range(20):
            service.record_stage_timings(
                t_tokenize=10.0,
                t_tokenizer_queue_wait=50.0,
                t_model_queue_wait=50.0,
                t_model_inference=300.0,
                t_overhead=10.0,
                t_mp_queue_send=5.0,
                t_mp_queue_receive=50.0,
                total_ms=475.0,
            )
            service.record(duration_ms=475.0)

        summary = service.get_summary()
        stage_pct = summary["stage_percentages"]

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

        sorted_comps = sorted(
            [(name, pct) for name, pct in components if pct > 0],
            key=lambda x: x[1],
            reverse=True,
        )
        top3 = sorted_comps[:3]
        rest = sorted_comps[3:]

        other_from_rest = sum(pct for _, pct in rest if _ != "other")
        display_total = sum(pct for _, pct in top3) + other_from_rest

        if display_total > 0:
            scale_factor = 100.0 / display_total
            normalized_total = display_total * scale_factor
            assert abs(normalized_total - 100.0) < 0.01, (
                f"Normalized total should be 100%, got {normalized_total}%"
            )


class TestStageBreakdownEdgeCases:
    def test_zero_average_latency_handling(self):
        service = MetricsService()
        service.record_stage_timings(
            t_tokenize=0.0,
            t_tokenizer_queue_wait=0.0,
            t_model_queue_wait=0.0,
            t_model_inference=0.0,
            total_ms=0.0,
        )
        service.record(duration_ms=0.0)

        summary = service.get_summary()

        stage_pct = summary.get("stage_percentages", {})
        if stage_pct:
            total = sum(v for k, v in stage_pct.items() if k.endswith("_pct"))
            assert total >= 0, "Percentages should be non-negative"

    def test_very_small_stage_values(self):
        service = MetricsService()
        for _i in range(10):
            service.record_stage_timings(
                t_tokenize=0.001,
                t_tokenizer_queue_wait=0.0005,
                t_model_queue_wait=0.0005,
                t_model_inference=99.996,
                total_ms=99.998,
            )
            service.record(duration_ms=99.998)

        summary = service.get_summary()
        stage_pct = summary["stage_percentages"]

        total_pct = sum(v for k, v in stage_pct.items() if k.endswith("_pct"))
        assert abs(total_pct - 100.0) < 0.1, f"Total should be ~100%, got {total_pct}%"

    def test_stage_values_much_larger_than_total_latency(self):
        service = MetricsService()
        for _i in range(5):
            service.record_stage_timings(
                t_tokenize=10.0,
                t_model_inference=30.0,
                total_ms=100.0,
            )
            service.record(duration_ms=100.0)

        summary = service.get_summary()
        stage_pct = summary["stage_percentages"]

        total_pct = (
            stage_pct.get("tokenize_pct", 0)
            + stage_pct.get("tokenizer_queue_wait_pct", 0)
            + stage_pct.get("model_queue_wait_pct", 0)
            + stage_pct.get("inference_pct", 0)
            + stage_pct.get("overhead_pct", 0)
            + stage_pct.get("mp_queue_send_pct", 0)
            + stage_pct.get("mp_queue_receive_pct", 0)
            + stage_pct.get("grpc_serialize_pct", 0)
            + stage_pct.get("grpc_deserialize_pct", 0)
            + stage_pct.get("scheduler_pct", 0)
            + stage_pct.get("pipeline_overhead_pct", 0)
            + stage_pct.get("other_pct", 0)
        )
        assert abs(total_pct - 100.0) < 1.0, f"Total should be ~100%, got {total_pct}%"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
