#!/usr/bin/env python3
"""Client for running benchmarks against inference server."""

import argparse
import json
import logging
import os
import signal
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from threading import Lock

import numpy as np
import requests
import yaml

from src.client.grpc_client import InferenceClient
from src.models import BenchmarkState, DashboardMetrics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


class DatasetLoader:
    """Handles loading and caching of test datasets."""

    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or Path(__file__).parent.parent / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load(self, num_samples: int = 1000) -> list:
        """Load MS MARCO query-passage pairs with caching."""
        cache_file = self.cache_dir / f"msmarco_pairs_{num_samples}.json"

        if cache_file.exists():
            logger.info(f"Loading cached pairs from {cache_file}")
            with open(cache_file) as f:
                pairs = json.load(f)
            logger.info(f"Loaded {len(pairs)} cached query-passage pairs")
            return [(p[0], p[1]) for p in pairs]

        return self._download_and_cache(num_samples, cache_file)

    def _download_and_cache(self, num_samples: int, cache_file: Path) -> list:
        """Download dataset from HuggingFace and cache."""
        try:
            from datasets import load_dataset as hf_load_dataset

            logger.info("Downloading MS MARCO dataset (first time only)...")
            dataset = hf_load_dataset("ms_marco", "v1.1", split="train", streaming=True)

            pairs = []
            for i, item in enumerate(dataset):
                if i >= num_samples:
                    break
                query = item["query"]
                passages = item.get("passages", {})
                passage_texts = passages.get("passage_text", [])
                if passage_texts:
                    pairs.append([query, passage_texts[0]])
                else:
                    pairs.append([query, query])

            with open(cache_file, "w") as f:
                json.dump(pairs, f)
            logger.info(f"Cached {len(pairs)} pairs to {cache_file}")
            return [(p[0], p[1]) for p in pairs]

        except ImportError:
            logger.warning("datasets not installed, using synthetic pairs")
            pairs = [
                (f"query {i}", f"document {i} with some text content") for i in range(num_samples)
            ]
            with open(cache_file, "w") as f:
                json.dump([[p[0], p[1]] for p in pairs], f)
            return pairs


class DashboardCollector:
    """Collects metrics from the dashboard during experiments."""

    def __init__(self, dashboard_url: str = "http://localhost:8080"):
        self.dashboard_url = dashboard_url

    def fetch_metrics(self) -> dict:
        """Fetch current metrics from dashboard."""
        try:
            response = requests.get(f"{self.dashboard_url}/metrics", timeout=2)
            return response.json()
        except Exception:
            return {}

    def collect_history(self) -> DashboardMetrics:
        """Collect all history data from dashboard."""
        try:
            data = self.fetch_metrics()
            history = data.get("history", {})
            return DashboardMetrics(
                gpu_memory_mb=history.get("gpu_memory_mb", []),
                gpu_utilization_pct=history.get("gpu_utilization_pct", []),
                cpu_percent=history.get("cpu_percent", []),
                latencies=history.get("latencies", []),
                throughput=history.get("throughput", []),
                tokenize_ms=history.get("tokenize_ms", []),
                inference_ms=history.get("inference_ms", []),
                queue_wait_ms=history.get("queue_wait_ms", []),
                padding_pct=history.get("padding_pct", []),
            )
        except Exception as e:
            logger.warning(f"Failed to collect dashboard metrics: {e}")
            return DashboardMetrics()


class BenchmarkRunner:
    """Runs benchmarks with configurable parameters."""

    def __init__(self, client: InferenceClient, state: BenchmarkState):
        self.client = client
        self.state = state

    def run(
        self,
        pairs: list,
        batch_size: int,
        num_requests: int,
        concurrency: int = 1,
    ) -> dict:
        """Run benchmark with per-request metrics tracking."""
        logger.info(
            f"Starting benchmark: {num_requests} requests, "
            f"concurrency={concurrency}, batch_size={batch_size}"
        )

        batches = self._prepare_batches(pairs, batch_size, num_requests)

        request_latencies = []
        request_throughputs = []
        latency_throughput_pairs = []
        lock = Lock()
        start = time.perf_counter()
        completed = [0]  # Use list to allow mutation in nested function

        def run_batch(batch):
            if self.state.interrupted:
                return None
            _, latency_ms = self.client.infer(batch)
            throughput = batch_size / (latency_ms / 1000)
            with lock:
                request_latencies.append(latency_ms)
                request_throughputs.append(throughput)
                latency_throughput_pairs.append((latency_ms, throughput))
                completed[0] += 1
            return latency_ms

        self._execute_batches(batches, run_batch, concurrency, completed, num_requests)

        elapsed = time.perf_counter() - start

        if len(request_latencies) == 0:
            return {"error": "No requests completed", "interrupted": True}

        return self._compute_results(
            request_latencies,
            request_throughputs,
            latency_throughput_pairs,
            batch_size,
            concurrency,
            elapsed,
        )

    def _prepare_batches(self, pairs: list, batch_size: int, num_requests: int) -> list:
        """Prepare batches of pairs for benchmark."""
        batches = []
        for i in range(num_requests):
            start_idx = (i * batch_size) % len(pairs)
            batch = pairs[start_idx : start_idx + batch_size]
            if len(batch) < batch_size:
                batch = batch + pairs[: batch_size - len(batch)]
            batches.append(batch)
        return batches

    def _execute_batches(
        self,
        batches: list,
        run_batch: Callable,
        concurrency: int,
        completed: list,
        num_requests: int,
    ):
        """Execute batches with specified concurrency."""
        if concurrency == 1:
            for batch in batches:
                if self.state.interrupted:
                    break
                run_batch(batch)
                if completed[0] % 50 == 0:
                    logger.info(f"Progress: {completed[0]}/{num_requests}")
        else:
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = [executor.submit(run_batch, batch) for batch in batches]
                for _f in as_completed(futures):
                    if self.state.interrupted:
                        break

    def _compute_results(
        self,
        latencies: list,
        throughputs: list,
        pairs: list,
        batch_size: int,
        concurrency: int,
        elapsed: float,
    ) -> dict:
        """Compute final benchmark results."""
        lat = np.array(latencies)
        tp = np.array(throughputs)
        total_pairs = len(latencies) * batch_size

        return {
            "batch_size": batch_size,
            "concurrency": concurrency,
            "num_requests": len(latencies),
            "total_pairs": total_pairs,
            "total_time_s": elapsed,
            "latency_avg_ms": float(np.mean(lat)),
            "latency_min_ms": float(np.min(lat)),
            "latency_max_ms": float(np.max(lat)),
            "latency_std_ms": float(np.std(lat)),
            "latency_p50_ms": float(np.percentile(lat, 50)),
            "latency_p90_ms": float(np.percentile(lat, 90)),
            "latency_p95_ms": float(np.percentile(lat, 95)),
            "latency_p99_ms": float(np.percentile(lat, 99)),
            "throughput_avg": total_pairs / elapsed if elapsed > 0 else 0,
            "throughput_min": float(np.min(tp)),
            "throughput_max": float(np.max(tp)),
            "throughput_std": float(np.std(tp)),
            "throughput_p50": float(np.percentile(tp, 50)),
            "throughput_p90": float(np.percentile(tp, 90)),
            "throughput_p95": float(np.percentile(tp, 95)),
            "throughput_p99": float(np.percentile(tp, 99)),
            "latency_throughput_pairs": pairs,
            "interrupted": self.state.interrupted,
        }


class ResultsWriter:
    """Writes experiment results to markdown files."""

    def save(
        self,
        results: list,
        config: dict,
        output_file: str,
        dashboard_metrics: DashboardMetrics = None,
    ):
        """Save experiment results to markdown with detailed metrics."""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        experiment_name = config.get("name", "Experiment")
        description = config.get("description", "")
        model_config = self._get_model_config(config)
        batching = config.get("batching", {})

        with open(output_file, "w") as f:
            self._write_header(f, experiment_name, description, timestamp, model_config, batching)
            self._write_summary_table(f, results)
            self._write_detailed_metrics(f, results)
            self._write_overall_summary(f, results)

            if dashboard_metrics:
                self._write_dashboard_metrics(f, dashboard_metrics)

        logger.info(f"Results saved to {output_file}")

    def _get_model_config(self, config: dict) -> dict:
        """Extract model config from experiment config."""
        if "model" in config:
            return config["model"]
        if "models" in config and config["models"]:
            return config["models"][0]
        if "model_pool" in config and "instances" in config["model_pool"]:
            instances = config["model_pool"]["instances"]
            if instances:
                return instances[0]
        return {}

    def _write_header(
        self,
        f,
        name: str,
        description: str,
        timestamp: str,
        model_config: dict,
        batching: dict,
    ):
        """Write markdown header."""
        f.write(f"# {name}\n\n")
        if description:
            f.write(f"_{description}_\n\n")
        f.write(f"**Timestamp:** {timestamp}\n\n")
        f.write(
            f"**Model:** `{model_config.get('name', 'cross-encoder/ms-marco-MiniLM-L-6-v2')}`\n\n"
        )
        f.write(f"**Backend:** `{model_config.get('backend', 'pytorch')}` | ")
        f.write(f"**Device:** `{model_config.get('device', 'mps')}`\n\n")

        if batching.get("enabled"):
            f.write(f"**Dynamic Batching:** enabled (max_batch={batching.get('max_batch_size')}, ")
            f.write(f"timeout={batching.get('timeout_ms')}ms)\n\n")

    def _write_summary_table(self, f, results: list):
        """Write results summary table."""
        f.write("## Results Summary\n\n")
        f.write(
            "| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |\n"
        )
        f.write(
            "|-------|------|-------|---------|---------|---------|---------|--------|--------|\n"
        )

        for r in results:
            if "error" in r:
                f.write(
                    f"| {r.get('batch_size', '-')} | {r.get('concurrency', '-')} "
                    f"| ERROR | - | - | - | - | - | - |\n"
                )
            else:
                f.write(
                    f"| {r['batch_size']} | {r['concurrency']} | {r['total_pairs']} | "
                    f"{r['total_time_s']:.2f} | {r['latency_avg_ms']:.1f}ms | "
                    f"{r['latency_p95_ms']:.1f}ms | {r['latency_p99_ms']:.1f}ms | "
                    f"{r['throughput_avg']:.1f} | {r['throughput_p95']:.1f} |\n"
                )

    def _write_detailed_metrics(self, f, results: list):
        """Write detailed per-config metrics."""
        f.write("\n## Detailed Metrics\n\n")

        for i, r in enumerate(results, 1):
            if "error" in r:
                f.write(f"### Config {i}: **ERROR**\n\n")
                f.write(f"Error: {r.get('error')}\n\n")
                continue

            f.write(f"### Config {i}: batch={r['batch_size']}, concurrency={r['concurrency']}\n\n")
            f.write(f"**Total:** {r['total_pairs']} pairs in {r['total_time_s']:.2f}s\n\n")

            self._write_latency_table(f, r)
            self._write_throughput_table(f, r)
            self._write_latency_throughput_analysis(f, r)

    def _write_latency_table(self, f, r: dict):
        """Write latency metrics table."""
        f.write("#### Latency (ms)\n")
        f.write("| Metric | Value |\n|--------|-------|\n")
        f.write(f"| Average | {r['latency_avg_ms']:.2f} |\n")
        f.write(f"| Min | {r['latency_min_ms']:.2f} |\n")
        f.write(f"| Max | {r['latency_max_ms']:.2f} |\n")
        f.write(f"| Std Dev | {r['latency_std_ms']:.2f} |\n")
        f.write(f"| P50 | {r['latency_p50_ms']:.2f} |\n")
        f.write(f"| P90 | {r['latency_p90_ms']:.2f} |\n")
        f.write(f"| P95 | {r['latency_p95_ms']:.2f} |\n")
        f.write(f"| P99 | {r['latency_p99_ms']:.2f} |\n\n")

    def _write_throughput_table(self, f, r: dict):
        """Write throughput metrics table."""
        f.write("#### Throughput (pairs/s)\n")
        f.write("| Metric | Value |\n|--------|-------|\n")
        f.write(f"| Average | {r['throughput_avg']:.2f} |\n")
        f.write(f"| Min | {r['throughput_min']:.2f} |\n")
        f.write(f"| Max | {r['throughput_max']:.2f} |\n")
        f.write(f"| Std Dev | {r['throughput_std']:.2f} |\n")
        f.write(f"| P50 | {r['throughput_p50']:.2f} |\n")
        f.write(f"| P90 | {r['throughput_p90']:.2f} |\n")
        f.write(f"| P95 | {r['throughput_p95']:.2f} |\n")
        f.write(f"| P99 | {r['throughput_p99']:.2f} |\n\n")

    def _write_latency_throughput_analysis(self, f, r: dict):
        """Write latency vs throughput analysis."""
        if "latency_throughput_pairs" not in r or not r["latency_throughput_pairs"]:
            return

        pairs = r["latency_throughput_pairs"]
        lat_array = np.array([p[0] for p in pairs])
        tp_array = np.array([p[1] for p in pairs])

        lat_p50 = float(np.percentile(lat_array, 50))
        lat_p75 = float(np.percentile(lat_array, 75))
        lat_p90 = float(np.percentile(lat_array, 90))

        f.write("#### Latency vs Throughput Analysis\n\n")
        f.write("| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |\n")
        f.write("|---------------|----------------|----------------|----------------|-------|\n")

        buckets = [
            (lat_array < lat_p50, f"< {lat_p50:.1f}ms (P50)"),
            (
                (lat_array >= lat_p50) & (lat_array < lat_p75),
                f"{lat_p50:.1f}-{lat_p75:.1f}ms (P50-P75)",
            ),
            (
                (lat_array >= lat_p75) & (lat_array < lat_p90),
                f"{lat_p75:.1f}-{lat_p90:.1f}ms (P75-P90)",
            ),
            (lat_array >= lat_p90, f">= {lat_p90:.1f}ms (P90+)"),
        ]

        for mask, label in buckets:
            if np.any(mask):
                f.write(f"| {label} | {np.mean(tp_array[mask]):.2f} | ")
                f.write(
                    f"{np.min(tp_array[mask]):.2f} | {np.max(tp_array[mask]):.2f} | {np.sum(mask)} |\n"
                )

        correlation = float(np.corrcoef(lat_array, tp_array)[0, 1])
        f.write(
            f"\n**Correlation:** {correlation:.3f} "
            f"(negative correlation expected: lower latency = higher throughput)\n\n"
        )

    def _write_overall_summary(self, f, results: list):
        """Write overall summary statistics."""
        successful = [r for r in results if "error" not in r]
        if not successful:
            return

        best_tp = max(successful, key=lambda x: x["throughput_avg"])
        best_lat = min(successful, key=lambda x: x["latency_avg_ms"])
        avg_tp = sum(r["throughput_avg"] for r in successful) / len(successful)
        avg_lat = sum(r["latency_avg_ms"] for r in successful) / len(successful)

        f.write("## Overall Summary\n\n")
        f.write("| Metric | Value | Config |\n|--------|-------|--------|\n")
        f.write(
            f"| Best Throughput | {best_tp['throughput_avg']:.2f} p/s | "
            f"batch={best_tp['batch_size']}, conc={best_tp['concurrency']} |\n"
        )
        f.write(
            f"| Best Latency | {best_lat['latency_avg_ms']:.2f}ms | "
            f"batch={best_lat['batch_size']}, conc={best_lat['concurrency']} |\n"
        )
        f.write(f"| Avg Throughput | {avg_tp:.2f} p/s | all configs |\n")
        f.write(f"| Avg Latency | {avg_lat:.2f}ms | all configs |\n")

    def _write_dashboard_metrics(self, f, metrics: DashboardMetrics):
        """Write dashboard metrics summary and full time-series data."""
        summary = metrics.get_summary()

        # Summary statistics table
        f.write("\n## Dashboard Metrics Summary\n\n")
        f.write("| Metric | Avg | Min | Max | P50 | P95 |\n")
        f.write("|--------|-----|-----|-----|-----|-----|\n")

        metric_names = {
            "gpu_memory_mb": "GPU Memory (MB)",
            "gpu_utilization_pct": "GPU Utilization (%)",
            "cpu_percent": "CPU Usage (%)",
            "tokenize_ms": "Tokenization (ms)",
            "inference_ms": "Inference (ms)",
            "queue_wait_ms": "Queue Wait (ms)",
            "padding_pct": "Padding Waste (%)",
        }

        for key, display_name in metric_names.items():
            s = summary.get(key, {})
            f.write(f"| {display_name} | {s.get('avg', 0):.1f} | {s.get('min', 0):.1f} | ")
            f.write(f"{s.get('max', 0):.1f} | {s.get('p50', 0):.1f} | {s.get('p95', 0):.1f} |\n")

        # Full time-series data table
        self._write_dashboard_timeseries(f, metrics)

    def _write_dashboard_timeseries(self, f, metrics: DashboardMetrics):
        """Write full time-series data from dashboard."""
        # Get all lists and find the longest one
        data_lists = {
            "GPU Mem (MB)": metrics.gpu_memory_mb,
            "GPU Util (%)": metrics.gpu_utilization_pct,
            "CPU (%)": metrics.cpu_percent,
            "Latency (ms)": metrics.latencies,
            "Throughput": metrics.throughput,
            "Tokenize (ms)": metrics.tokenize_ms,
            "Inference (ms)": metrics.inference_ms,
            "Queue (ms)": metrics.queue_wait_ms,
            "Padding (%)": metrics.padding_pct,
        }

        max_len = max(len(v) for v in data_lists.values()) if data_lists else 0

        if max_len == 0:
            return

        f.write("\n## Dashboard Time-Series Data\n\n")

        # Header
        headers = ["Index"] + list(data_lists.keys())
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("|" + "|".join(["-----"] * len(headers)) + "|\n")

        # Data rows
        for i in range(max_len):
            row = [str(i)]
            for _key, data in data_lists.items():
                if i < len(data):
                    val = data[i]
                    row.append(f"{val:.1f}" if isinstance(val, float) else str(val))
                else:
                    row.append("-")
            f.write("| " + " | ".join(row) + " |\n")


def main():
    parser = argparse.ArgumentParser(description="Inference Benchmark Client")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=50051, help="Server port")
    parser.add_argument("--experiment", "-e", action="store_true", help="Experiment mode")
    parser.add_argument("--config", "-c", help="Experiment config YAML")
    parser.add_argument("--output", "-o", help="Output file for results")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--num-requests", type=int, default=100, help="Number of requests")
    parser.add_argument("--concurrency", type=int, default=1, help="Concurrency level")
    parser.add_argument("--dataset-size", type=int, default=50000, help="Number of test pairs")
    args = parser.parse_args()

    # Setup state and signal handlers
    state = BenchmarkState()
    signal.signal(signal.SIGINT, state.handle_interrupt)
    signal.signal(signal.SIGTERM, state.handle_interrupt)

    # Load config if provided
    config = {}
    if args.config:
        with open(args.config) as f:
            config = yaml.safe_load(f)

        exp = config.get("experiment", config.get("benchmark", {}))
        if "batch_sizes" in exp:
            args.batch_size = exp["batch_sizes"][0] if exp["batch_sizes"] else args.batch_size
        if "benchmark_requests" in exp:
            args.num_requests = exp["benchmark_requests"]
        if "batch_size" in exp:
            args.batch_size = exp["batch_size"]
        if "num_requests" in exp:
            args.num_requests = exp["num_requests"]
        if "concurrency" in exp:
            args.concurrency = exp["concurrency"]

    # Load test pairs
    loader = DatasetLoader()
    pairs = loader.load(args.dataset_size)
    logger.info(f"Loaded {len(pairs)} test pairs")

    # Create client
    client = InferenceClient(args.host, args.port)

    # Warmup
    logger.info("Warming up...")
    for _ in range(5):
        client.infer(pairs[: args.batch_size])

    try:
        runner = BenchmarkRunner(client, state)
        results = [
            runner.run(
                pairs,
                args.batch_size,
                args.num_requests,
                args.concurrency,
            )
        ]

        # Collect dashboard metrics
        dashboard_collector = DashboardCollector()
        dashboard_metrics = dashboard_collector.collect_history()

        # Print summary
        r = results[0]
        if "error" not in r:
            print("\n" + "=" * 80)
            print("BENCHMARK RESULTS")
            print("=" * 80)
            print(f"Total Pairs: {r['total_pairs']} in {r['total_time_s']:.2f}s")
            print("\nLatency (ms):")
            print(f"  Average: {r['latency_avg_ms']:.2f}")
            print(
                f"  P50: {r['latency_p50_ms']:.2f} | P95: {r['latency_p95_ms']:.2f} | "
                f"P99: {r['latency_p99_ms']:.2f}"
            )
            print("\nThroughput (pairs/s):")
            print(f"  Average: {r['throughput_avg']:.2f}")
            print(
                f"  P50: {r['throughput_p50']:.2f} | P95: {r['throughput_p95']:.2f} | "
                f"P99: {r['throughput_p99']:.2f}"
            )
            print("=" * 80 + "\n")

        # Save results
        if args.output:
            writer = ResultsWriter()
            writer.save(results, config, args.output, dashboard_metrics)

    finally:
        client.close()


if __name__ == "__main__":
    main()
