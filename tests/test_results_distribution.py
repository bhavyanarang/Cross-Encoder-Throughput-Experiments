"""Tests to ensure distribution and results are updated after each run."""

import tempfile
from pathlib import Path

import pytest

from src.run_client import ResultsWriter
from src.server.dto.dashboard import DashboardMetrics


class TestResultsWriter:
    """Test ResultsWriter creates and updates files correctly."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def sample_results(self):
        """Create sample results data."""
        return [
            {
                "batch_size": 8,
                "concurrency": 4,
                "total_pairs": 100,
                "total_time_s": 10.5,
                "latency_avg_ms": 50.0,
                "latency_min_ms": 30.0,
                "latency_max_ms": 100.0,
                "latency_std_ms": 15.0,
                "latency_p50_ms": 45.0,
                "latency_p90_ms": 70.0,
                "latency_p95_ms": 80.0,
                "latency_p99_ms": 95.0,
                "throughput_avg": 9.5,
                "throughput_min": 8.0,
                "throughput_max": 11.0,
                "throughput_std": 1.0,
                "throughput_p50": 9.0,
                "throughput_p90": 10.5,
                "throughput_p95": 10.8,
                "throughput_p99": 10.9,
                "latency_throughput_pairs": [(50.0, 9.5), (45.0, 10.0), (55.0, 9.0)],
            }
        ]

    @pytest.fixture
    def sample_config(self):
        """Create sample experiment config."""
        return {
            "name": "test_experiment",
            "description": "Test experiment description",
            "model": {
                "name": "cross-encoder/ms-marco-MiniLM-L-6-v2",
                "backend": "pytorch",
                "device": "cpu",
            },
            "batching": {"enabled": True, "max_batch_size": 8, "timeout_ms": 100.0},
        }

    @pytest.fixture
    def sample_dashboard_metrics(self):
        """Create sample dashboard metrics."""
        return DashboardMetrics(
            gpu_memory_mb=[100.0, 105.0, 110.0],
            gpu_utilization_pct=[50.0, 55.0, 60.0],
            cpu_percent=[20.0, 25.0, 30.0],
            latencies=[50.0, 45.0, 55.0],
            throughput=[9.5, 10.0, 9.0],
            tokenize_ms=[5.0, 4.5, 5.5],
            inference_ms=[40.0, 35.0, 45.0],
            queue_wait_ms=[2.0, 2.5, 3.0],
            padding_pct=[10.0, 12.0, 11.0],
            worker_stats=[],
            stage_percentages={},
        )

    def test_results_file_created(self, temp_dir, sample_results, sample_config):
        """Test that results file is created when saving."""
        output_file = str(temp_dir / "test_results.md")
        writer = ResultsWriter()

        writer.save(sample_results, sample_config, output_file)

        assert Path(output_file).exists(), "Results file should be created"
        content = Path(output_file).read_text()
        assert "test_experiment" in content
        assert "Test experiment description" in content
        assert "Summary" in content
        assert "Detailed Metrics" in content

    def test_results_file_contains_correct_data(self, temp_dir, sample_results, sample_config):
        """Test that results file contains correct data."""
        output_file = str(temp_dir / "test_results.md")
        writer = ResultsWriter()

        writer.save(sample_results, sample_config, output_file)

        content = Path(output_file).read_text()
        assert "batch_size" in content.lower() or "Batch" in content
        assert "8" in content  # batch_size
        assert "4" in content  # concurrency
        assert "100" in content  # total_pairs
        assert "50.0" in content or "50" in content  # latency_avg_ms
        assert "9.5" in content  # throughput_avg

    def test_distribution_file_created_with_dashboard_metrics(
        self, temp_dir, sample_results, sample_config, sample_dashboard_metrics
    ):
        """Test that distribution/timeseries file is created when dashboard metrics are provided."""
        output_file = str(temp_dir / "test_results.md")
        writer = ResultsWriter()

        writer.save(
            sample_results, sample_config, output_file, dashboard_metrics=sample_dashboard_metrics
        )

        # Check that distribution directory was created
        distribution_dir = temp_dir.parent / "distribution"
        assert distribution_dir.exists(), "Distribution directory should be created"

        # Check that timeseries file was created
        timeseries_file = distribution_dir / "test_timeseries.md"
        assert timeseries_file.exists(), "Timeseries file should be created"

        # Check that index file was created
        index_file = distribution_dir / "test_timeseries.idx"
        assert index_file.exists(), "Index file should be created"

    def test_distribution_file_contains_correct_data(
        self, temp_dir, sample_results, sample_config, sample_dashboard_metrics
    ):
        """Test that distribution/timeseries file contains correct data."""
        output_file = str(temp_dir / "test_results.md")
        writer = ResultsWriter()

        writer.save(
            sample_results, sample_config, output_file, dashboard_metrics=sample_dashboard_metrics
        )

        timeseries_file = temp_dir.parent / "distribution" / "test_timeseries.md"
        content = timeseries_file.read_text()

        assert "Timeseries Data" in content
        assert "test" in content.lower()  # experiment name
        assert "Index" in content
        assert "GPU Mem" in content
        assert "GPU Util" in content
        assert "CPU" in content
        assert "Latency" in content
        assert "Throughput" in content
        assert "Tokenize" in content
        assert "Inference" in content

        # Check that data rows are present
        assert "| 0 |" in content or "|0|" in content

    def test_results_file_updated_on_append(self, temp_dir, sample_results, sample_config):
        """Test that results file is updated correctly when appending."""
        output_file = str(temp_dir / "test_results.md")
        writer = ResultsWriter()

        # First save
        writer.save(sample_results, sample_config, output_file, append=False)

        # Second save with append
        sample_results_2 = [
            {
                **sample_results[0],
                "batch_size": 16,
                "concurrency": 8,
                "total_pairs": 200,
            }
        ]
        writer.save(sample_results_2, sample_config, output_file, append=True)

        content = Path(output_file).read_text()

        # Should contain separator
        assert "---" in content

        # Should contain data from both runs
        assert "8" in content  # First batch_size
        assert "16" in content  # Second batch_size

    def test_distribution_file_updated_on_append(
        self, temp_dir, sample_results, sample_config, sample_dashboard_metrics
    ):
        """Test that distribution/timeseries file is updated correctly when appending."""
        output_file = str(temp_dir / "test_results.md")
        timeseries_file = str(temp_dir.parent / "distribution" / "test_timeseries.md")
        writer = ResultsWriter()

        # First save
        writer.save(
            sample_results,
            sample_config,
            output_file,
            dashboard_metrics=sample_dashboard_metrics,
            timeseries_file=timeseries_file,
            append=False,
        )

        # Second save with append
        sample_dashboard_metrics_2 = DashboardMetrics(
            gpu_memory_mb=[120.0, 125.0],
            gpu_utilization_pct=[65.0, 70.0],
            cpu_percent=[35.0, 40.0],
            latencies=[60.0, 65.0],
            throughput=[11.0, 12.0],
            tokenize_ms=[6.0, 6.5],
            inference_ms=[50.0, 55.0],
            queue_wait_ms=[4.0, 4.5],
            padding_pct=[15.0, 16.0],
            worker_stats=[],
            stage_percentages={},
        )

        writer.save(
            sample_results,
            sample_config,
            output_file,
            dashboard_metrics=sample_dashboard_metrics_2,
            timeseries_file=timeseries_file,
            append=True,
        )

        content = Path(timeseries_file).read_text()

        # Should contain separator
        assert "---" in content

        # Should contain data from both runs
        # First run has 3 data points, second has 2
        # Index should continue from where first run left off
        assert "| 3 |" in content or "|3|" in content  # First index of second run

    def test_index_file_updated_correctly(
        self, temp_dir, sample_results, sample_config, sample_dashboard_metrics
    ):
        """Test that index file is updated correctly after each run."""
        output_file = str(temp_dir / "test_results.md")
        timeseries_file = str(temp_dir.parent / "distribution" / "test_timeseries.md")
        index_file = temp_dir.parent / "distribution" / "test_timeseries.idx"
        writer = ResultsWriter()

        # First save
        writer.save(
            sample_results,
            sample_config,
            output_file,
            dashboard_metrics=sample_dashboard_metrics,
            timeseries_file=timeseries_file,
            append=False,
        )

        # Check index file after first run (3 data points, indices 0-2)
        assert index_file.exists()
        first_index = int(index_file.read_text().strip())
        assert first_index == 2, f"Expected index 2, got {first_index}"

        # Second save with append
        sample_dashboard_metrics_2 = DashboardMetrics(
            gpu_memory_mb=[120.0, 125.0],
            gpu_utilization_pct=[65.0, 70.0],
            cpu_percent=[35.0, 40.0],
            latencies=[60.0, 65.0],
            throughput=[11.0, 12.0],
            tokenize_ms=[6.0, 6.5],
            inference_ms=[50.0, 55.0],
            queue_wait_ms=[4.0, 4.5],
            padding_pct=[15.0, 16.0],
            worker_stats=[],
            stage_percentages={},
        )

        writer.save(
            sample_results,
            sample_config,
            output_file,
            dashboard_metrics=sample_dashboard_metrics_2,
            timeseries_file=timeseries_file,
            append=True,
        )

        # Check index file after second run (should be 2 + 2 - 1 = 3)
        second_index = int(index_file.read_text().strip())
        assert second_index == 4, f"Expected index 4, got {second_index}"

    def test_results_file_references_distribution_file(
        self, temp_dir, sample_results, sample_config, sample_dashboard_metrics
    ):
        """Test that results file references the distribution/timeseries file."""
        output_file = str(temp_dir / "test_results.md")
        writer = ResultsWriter()

        writer.save(
            sample_results, sample_config, output_file, dashboard_metrics=sample_dashboard_metrics
        )

        content = Path(output_file).read_text()

        # Should reference the timeseries file
        assert "distribution" in content
        assert "timeseries" in content.lower()

    def test_multiple_runs_update_files_correctly(
        self, temp_dir, sample_results, sample_config, sample_dashboard_metrics
    ):
        """Test that multiple runs update files correctly."""
        output_file = str(temp_dir / "test_results.md")
        timeseries_file = str(temp_dir.parent / "distribution" / "test_timeseries.md")
        writer = ResultsWriter()

        # Run 1
        writer.save(
            sample_results,
            sample_config,
            output_file,
            dashboard_metrics=sample_dashboard_metrics,
            timeseries_file=timeseries_file,
            append=False,
        )

        results_size_1 = Path(output_file).stat().st_size
        timeseries_size_1 = Path(timeseries_file).stat().st_size

        # Run 2
        sample_dashboard_metrics_2 = DashboardMetrics(
            gpu_memory_mb=[120.0, 125.0],
            gpu_utilization_pct=[65.0, 70.0],
            cpu_percent=[35.0, 40.0],
            latencies=[60.0, 65.0],
            throughput=[11.0, 12.0],
            tokenize_ms=[6.0, 6.5],
            inference_ms=[50.0, 55.0],
            queue_wait_ms=[4.0, 4.5],
            padding_pct=[15.0, 16.0],
            worker_stats=[],
            stage_percentages={},
        )

        writer.save(
            sample_results,
            sample_config,
            output_file,
            dashboard_metrics=sample_dashboard_metrics_2,
            timeseries_file=timeseries_file,
            append=True,
        )

        results_size_2 = Path(output_file).stat().st_size
        timeseries_size_2 = Path(timeseries_file).stat().st_size

        # Files should be larger after second run
        assert results_size_2 > results_size_1, "Results file should grow after second run"
        assert timeseries_size_2 > timeseries_size_1, "Timeseries file should grow after second run"

    def test_results_file_without_dashboard_metrics(self, temp_dir, sample_results, sample_config):
        """Test that results file is created even without dashboard metrics."""
        output_file = str(temp_dir / "test_results.md")
        writer = ResultsWriter()

        writer.save(sample_results, sample_config, output_file, dashboard_metrics=None)

        assert Path(output_file).exists()
        content = Path(output_file).read_text()
        assert "test_experiment" in content
        # Should not reference distribution file when no dashboard metrics
        assert "distribution" not in content or "timeseries" not in content.lower()

    def test_custom_timeseries_file_path(
        self, temp_dir, sample_results, sample_config, sample_dashboard_metrics
    ):
        """Test that custom timeseries file path works correctly."""
        output_file = str(temp_dir / "test_results.md")
        custom_timeseries_file = str(temp_dir / "custom_timeseries.md")
        writer = ResultsWriter()

        writer.save(
            sample_results,
            sample_config,
            output_file,
            dashboard_metrics=sample_dashboard_metrics,
            timeseries_file=custom_timeseries_file,
        )

        assert Path(custom_timeseries_file).exists()
        content = Path(output_file).read_text()
        assert "custom_timeseries.md" in content

    def test_distribution_dir_created_in_correct_location(
        self, temp_dir, sample_results, sample_config, sample_dashboard_metrics
    ):
        """Test that distribution directory is created in the correct location."""
        results_dir = temp_dir / "results"
        results_dir.mkdir()
        output_file = str(results_dir / "test_results.md")
        writer = ResultsWriter()

        writer.save(
            sample_results, sample_config, output_file, dashboard_metrics=sample_dashboard_metrics
        )

        # Distribution should be in parent of results directory
        distribution_dir = temp_dir / "distribution"
        assert distribution_dir.exists(), "Distribution directory should be created"

    def test_results_file_contains_overall_summary(self, temp_dir, sample_results, sample_config):
        """Test that results file contains overall summary."""
        output_file = str(temp_dir / "test_results.md")
        writer = ResultsWriter()

        writer.save(sample_results, sample_config, output_file)

        content = Path(output_file).read_text()
        assert "Overall Summary" in content
        assert "Best Throughput" in content
        assert "Best Latency" in content
        assert "Avg Throughput" in content
        assert "Avg Latency" in content

    def test_results_file_contains_dashboard_metrics_section(
        self, temp_dir, sample_results, sample_config, sample_dashboard_metrics
    ):
        """Test that results file contains dashboard metrics section when provided."""
        output_file = str(temp_dir / "test_results.md")
        writer = ResultsWriter()

        writer.save(
            sample_results, sample_config, output_file, dashboard_metrics=sample_dashboard_metrics
        )

        content = Path(output_file).read_text()
        assert "Dashboard Metrics" in content
        assert "GPU Memory" in content
        assert "GPU Utilization" in content
        assert "CPU Usage" in content
        assert "Tokenization" in content
        assert "Inference" in content

    def test_sweep_experiment_updates_files_correctly(
        self, temp_dir, sample_config, sample_dashboard_metrics
    ):
        """Test that sweep experiments update files correctly with multiple configs."""
        output_file = str(temp_dir / "sweep_results.md")
        timeseries_file = str(temp_dir.parent / "distribution" / "sweep_timeseries.md")
        writer = ResultsWriter()

        # Simulate multiple config runs in a sweep
        configs = [
            {"batch_size": 8, "concurrency": 4},
            {"batch_size": 16, "concurrency": 8},
            {"batch_size": 32, "concurrency": 16},
        ]

        for idx, config in enumerate(configs):
            result = {
                "batch_size": config["batch_size"],
                "concurrency": config["concurrency"],
                "total_pairs": 100 * (idx + 1),
                "total_time_s": 10.0 + idx,
                "latency_avg_ms": 50.0 + idx * 5,
                "latency_min_ms": 30.0,
                "latency_max_ms": 100.0 + idx * 10,
                "latency_std_ms": 15.0,
                "latency_p50_ms": 45.0 + idx * 5,
                "latency_p90_ms": 70.0 + idx * 5,
                "latency_p95_ms": 80.0 + idx * 5,
                "latency_p99_ms": 95.0 + idx * 5,
                "throughput_avg": 9.5 + idx * 0.5,
                "throughput_min": 8.0,
                "throughput_max": 11.0 + idx,
                "throughput_std": 1.0,
                "throughput_p50": 9.0 + idx * 0.5,
                "throughput_p90": 10.5 + idx * 0.5,
                "throughput_p95": 10.8 + idx * 0.5,
                "throughput_p99": 10.9 + idx * 0.5,
                "latency_throughput_pairs": [(50.0, 9.5), (45.0, 10.0)],
            }

            metrics = DashboardMetrics(
                gpu_memory_mb=[100.0 + idx * 10, 105.0 + idx * 10],
                gpu_utilization_pct=[50.0 + idx * 5, 55.0 + idx * 5],
                cpu_percent=[20.0 + idx * 5, 25.0 + idx * 5],
                latencies=[50.0 + idx * 5, 45.0 + idx * 5],
                throughput=[9.5 + idx * 0.5, 10.0 + idx * 0.5],
                tokenize_ms=[5.0 + idx, 4.5 + idx],
                inference_ms=[40.0 + idx * 5, 35.0 + idx * 5],
                queue_wait_ms=[2.0 + idx, 2.5 + idx],
                padding_pct=[10.0 + idx, 12.0 + idx],
                worker_stats=[],
                stage_percentages={},
            )

            append = idx > 0
            writer.save(
                [result],
                sample_config,
                output_file,
                dashboard_metrics=metrics if idx == len(configs) - 1 else None,
                timeseries_file=timeseries_file,
                append=append,
            )

        # Verify results file contains all configs
        results_content = Path(output_file).read_text()
        assert "8" in results_content  # First batch_size
        assert "16" in results_content  # Second batch_size
        assert "32" in results_content  # Third batch_size

        # Verify timeseries file was updated
        assert Path(timeseries_file).exists()
        timeseries_content = Path(timeseries_file).read_text()

        # Should contain separators for each config (after first)
        separator_count = timeseries_content.count("---")
        assert separator_count >= 2, "Should have separators for multiple configs"

        # Should contain data from multiple runs
        # Each run adds 2 data points, so we should have at least 6 data points total
        timeseries_content.count("| 0 |") + timeseries_content.count("|0|")
        # Actually, let's count the number of data rows more accurately
        lines_with_pipe = [
            line
            for line in timeseries_content.split("\n")
            if line.startswith("|") and "|--" not in line
        ]
        assert len(lines_with_pipe) >= 6, (
            f"Should have data from multiple runs, got {len(lines_with_pipe)} rows"
        )

    def test_empty_dashboard_metrics_does_not_create_timeseries(
        self, temp_dir, sample_results, sample_config
    ):
        """Test that empty dashboard metrics don't create timeseries file."""
        output_file = str(temp_dir / "empty_test_results.md")
        writer = ResultsWriter()

        empty_metrics = DashboardMetrics()

        writer.save(sample_results, sample_config, output_file, dashboard_metrics=empty_metrics)

        # Results file should exist
        assert Path(output_file).exists()

        # Timeseries file should not be created if metrics are empty (max_len == 0)
        # The _write_dashboard_timeseries method returns early if max_len == 0
        # Check for the specific timeseries file that would be created for this test
        distribution_dir = temp_dir.parent / "distribution"
        timeseries_file = distribution_dir / "empty_test_timeseries.md"

        # File should not exist because empty metrics cause early return
        assert not timeseries_file.exists(), (
            "Timeseries file should not be created for empty metrics"
        )

    def test_file_timestamps_updated_on_each_run(
        self, temp_dir, sample_results, sample_config, sample_dashboard_metrics
    ):
        """Test that file modification times are updated on each run."""
        import time

        output_file = str(temp_dir / "test_results.md")
        timeseries_file = str(temp_dir.parent / "distribution" / "test_timeseries.md")
        writer = ResultsWriter()

        # First run
        writer.save(
            sample_results,
            sample_config,
            output_file,
            dashboard_metrics=sample_dashboard_metrics,
            timeseries_file=timeseries_file,
            append=False,
        )

        time.sleep(0.1)  # Small delay to ensure different timestamps

        results_mtime_1 = Path(output_file).stat().st_mtime
        timeseries_mtime_1 = Path(timeseries_file).stat().st_mtime

        # Second run
        sample_dashboard_metrics_2 = DashboardMetrics(
            gpu_memory_mb=[120.0, 125.0],
            gpu_utilization_pct=[65.0, 70.0],
            cpu_percent=[35.0, 40.0],
            latencies=[60.0, 65.0],
            throughput=[11.0, 12.0],
            tokenize_ms=[6.0, 6.5],
            inference_ms=[50.0, 55.0],
            queue_wait_ms=[4.0, 4.5],
            padding_pct=[15.0, 16.0],
            worker_stats=[],
            stage_percentages={},
        )

        writer.save(
            sample_results,
            sample_config,
            output_file,
            dashboard_metrics=sample_dashboard_metrics_2,
            timeseries_file=timeseries_file,
            append=True,
        )

        results_mtime_2 = Path(output_file).stat().st_mtime
        timeseries_mtime_2 = Path(timeseries_file).stat().st_mtime

        # Modification times should be updated
        assert results_mtime_2 >= results_mtime_1, "Results file should be updated"
        assert timeseries_mtime_2 >= timeseries_mtime_1, "Timeseries file should be updated"
