#!/usr/bin/env python3

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
from tqdm import tqdm

from src.client.grpc_client import InferenceClient
from src.server.dto import BenchmarkState, DashboardMetrics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


class DatasetLoader:
    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or Path(__file__).parent.parent / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load(self, num_samples: int = 1000) -> list:
        cache_file = self.cache_dir / f"msmarco_pairs_{num_samples}.json"

        if cache_file.exists():
            logger.info(f"Loading cached pairs from {cache_file}")
            with open(cache_file) as f:
                pairs = json.load(f)
            logger.info(f"Loaded {len(pairs)} cached query-passage pairs")
            return [(p[0], p[1]) for p in pairs]

        return self._download_and_cache(num_samples, cache_file)

    def _download_and_cache(self, num_samples: int, cache_file: Path) -> list:
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
    def __init__(self, dashboard_url: str = "http://localhost:8080"):
        self.dashboard_url = dashboard_url

    def fetch_metrics(self) -> dict:
        try:
            response = requests.get(f"{self.dashboard_url}/metrics", timeout=2)
            return response.json()
        except Exception:
            return {}

    def collect_history(self) -> DashboardMetrics:
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
                worker_stats=data.get("worker_stats", []),
                stage_percentages=data.get("stage_percentages", {}),
            )
        except Exception as e:
            logger.warning(f"Failed to collect dashboard metrics: {e}")
            return DashboardMetrics()


class BenchmarkRunner:
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
        completed = [0]

        def run_batch(batch):
            if self.state.interrupted:
                return None

            elapsed = time.perf_counter() - start
            if elapsed > 60.0:
                logger.info(
                    f"Reached 1-minute timeout, stopping benchmark (completed {completed[0]}/{num_requests} requests)"
                )
                return None
            _, latency_ms = self.client.infer(batch)
            throughput = batch_size / (latency_ms / 1000)
            with lock:
                request_latencies.append(latency_ms)
                request_throughputs.append(throughput)
                latency_throughput_pairs.append((latency_ms, throughput))
                completed[0] += 1
            return latency_ms

        self._execute_batches(batches, run_batch, concurrency, completed, num_requests, start)

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
        start_time: float = None,
    ):
        if start_time is None:
            start_time = time.perf_counter()

        pbar = tqdm(total=num_requests, desc="Benchmarking", unit="req", ncols=80, leave=False)
        last_completed = 0

        try:
            if concurrency == 1:
                for batch in batches:
                    if self.state.interrupted:
                        break

                    if time.perf_counter() - start_time > 60.0:
                        break
                    run_batch(batch)

                    current = completed[0]
                    if current > last_completed:
                        pbar.update(current - last_completed)
                        last_completed = current
            else:
                with ThreadPoolExecutor(max_workers=concurrency) as executor:
                    futures = [executor.submit(run_batch, batch) for batch in batches]
                    for _f in as_completed(futures):
                        if self.state.interrupted:
                            break

                        if time.perf_counter() - start_time > 60.0:
                            break

                        current = completed[0]
                        if current > last_completed:
                            pbar.update(current - last_completed)
                            last_completed = current
        finally:
            final = completed[0]
            if final > last_completed:
                pbar.update(final - last_completed)
            pbar.close()

    def _compute_results(
        self,
        latencies: list,
        throughputs: list,
        pairs: list,
        batch_size: int,
        concurrency: int,
        elapsed: float,
    ) -> dict:
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
    def save(
        self,
        results: list,
        config: dict,
        output_file: str,
        dashboard_metrics: DashboardMetrics = None,
        append: bool = False,
        timeseries_file: str = None,
    ):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        experiment_name = config.get("name", "Experiment")
        description = config.get("description", "")
        model_config = self._get_model_config(config)
        batching = config.get("batching", {})

        output_path = Path(output_file)
        distribution_dir = output_path.parent.parent / "distribution"
        distribution_dir.mkdir(exist_ok=True)
        experiment_basename = output_path.stem.replace("_results", "")

        mode = "a" if append else "w"

        with open(output_file, mode) as f:
            if append:
                f.write("\n\n---\n\n")

            self._write_header(f, experiment_name, description, timestamp, model_config, batching)
            self._write_summary_table(f, results)
            self._write_detailed_metrics(f, results)
            self._write_overall_summary(f, results)

            if dashboard_metrics:
                result = None
                if results and len(results) > 0:
                    result = results[0]

                self._write_dashboard_metrics(
                    f,
                    dashboard_metrics,
                    distribution_dir,
                    experiment_basename,
                    timeseries_file=timeseries_file,
                    append=append,
                    config=config,
                    result=result,
                )

        logger.info(f"Results {'appended to' if append else 'saved to'} {output_file}")

    def _get_model_config(self, config: dict) -> dict:
        if "model" in config:
            return config["model"]
        if "dto" in config and config["dto"]:
            return config["dto"][0]
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
        f.write("## Summary\n\n")
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
        f.write("\n## Detailed Metrics\n\n")

        for i, r in enumerate(results, 1):
            if "error" in r:
                f.write(f"### Run {i}\n\n")
                f.write(f"Error: {r.get('error')}\n\n")
                continue

            f.write(f"### Run {i}\n\n")
            f.write(f"**Total:** {r['total_pairs']} pairs in {r['total_time_s']:.2f}s\n\n")

            self._write_latency_table(f, r)
            self._write_throughput_table(f, r)
            self._write_latency_throughput_analysis(f, r)

    def _write_latency_table(self, f, r: dict):
        f.write("### Latency\n\n")
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
        f.write("### Throughput\n\n")
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
        if "latency_throughput_pairs" not in r or not r["latency_throughput_pairs"]:
            return

        pairs = r["latency_throughput_pairs"]
        lat_array = np.array([p[0] for p in pairs])
        tp_array = np.array([p[1] for p in pairs])

        lat_p50 = float(np.percentile(lat_array, 50))
        lat_p75 = float(np.percentile(lat_array, 75))
        lat_p90 = float(np.percentile(lat_array, 90))

        f.write("### Latency vs Throughput Analysis\n\n")
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

    def _write_dashboard_metrics(
        self,
        f,
        metrics: DashboardMetrics,
        distribution_dir: Path,
        experiment_basename: str,
        timeseries_file: str = None,
        append: bool = False,
        config: dict = None,
        result: dict = None,
    ):
        summary = metrics.get_summary()

        f.write("\n## Dashboard Metrics\n\n")
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

        self._write_stage_breakdown(f, metrics)

        self._write_worker_stats(f, metrics)

        sweep_config = self._extract_sweep_config(config, result)

        if timeseries_file:
            ts_path = Path(timeseries_file)
            ts_path.parent.mkdir(exist_ok=True)
            self._write_dashboard_timeseries(ts_path, metrics, append=append, config=sweep_config)
            f.write(f"\nFull time-series data is available in: `distribution/{ts_path.name}`\n")
        else:
            ts_path = distribution_dir / f"{experiment_basename}_timeseries.md"
            self._write_dashboard_timeseries(ts_path, metrics, append=False, config=sweep_config)
            f.write(
                f"\nFull time-series data is available in: `distribution/{experiment_basename}_timeseries.md`\n"
            )

    def _extract_sweep_config(self, config: dict, result: dict) -> dict:
        sweep_config = {}

        if result:
            if "batch_size" in result:
                sweep_config["batch_size"] = result["batch_size"]
            if "concurrency" in result:
                sweep_config["concurrency"] = result["concurrency"]

        if config:
            model_config = self._get_model_config(config)
            if model_config:
                if "backend" in model_config:
                    sweep_config["backend"] = model_config["backend"]
                if "device" in model_config:
                    sweep_config["device"] = model_config["device"]
                if "name" in model_config:
                    sweep_config["model"] = model_config["name"]

            batching = config.get("batching", {})
            if batching.get("enabled"):
                sweep_config["batching_enabled"] = True
                if "max_batch_size" in batching:
                    sweep_config["max_batch_size"] = batching["max_batch_size"]
                if "timeout_ms" in batching:
                    sweep_config["timeout_ms"] = batching["timeout_ms"]

        return sweep_config

    def _write_stage_breakdown(self, f, metrics: DashboardMetrics):
        stage_pct = metrics.stage_percentages
        if not stage_pct:
            return

        f.write("\n### Stage Timing\n\n")
        f.write("| Stage | Percentage |\n")
        f.write("|-------|------------|\n")
        f.write(f"| Tokenization | {stage_pct.get('tokenize_pct', 0):.1f}% |\n")
        f.write(f"| Queue Wait | {stage_pct.get('queue_wait_pct', 0):.1f}% |\n")
        f.write(f"| Model Inference | {stage_pct.get('inference_pct', 0):.1f}% |\n")
        f.write(f"| Other/gRPC | {stage_pct.get('other_pct', 0):.1f}% |\n")

    def _write_worker_stats(self, f, metrics: DashboardMetrics):
        worker_stats = metrics.worker_stats
        if not worker_stats:
            return

        f.write("\n### Worker Metrics\n\n")
        f.write(
            "| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |\n"
        )
        f.write("|-----------|------------------|------------------|------------------|--------|\n")

        for ws in worker_stats:
            f.write(f"| {ws.get('worker_id', '-')} | ")
            f.write(f"{ws.get('avg_ms', 0):.1f} | ")
            f.write(f"{ws.get('p95_ms', 0):.1f} | ")
            f.write(f"{ws.get('throughput_qps', 0):.1f} | ")
            f.write(f"{ws.get('query_count', 0)} |\n")

    def _write_dashboard_timeseries(
        self,
        output_file: Path,
        metrics: DashboardMetrics,
        append: bool = False,
        config: dict = None,
    ):
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

        index_file = output_file.with_suffix(".idx")
        file_exists = output_file.exists() and output_file.stat().st_size > 0

        start_idx = 0
        if append and file_exists:
            try:
                if index_file.exists():
                    with open(index_file) as f:
                        start_idx = int(f.read().strip()) + 1
                else:
                    with open(output_file, "rb") as f:
                        f.seek(0, 2)
                        file_size = f.tell()

                        read_size = min(500, file_size)
                        f.seek(-read_size, 2)
                        last_chunk = f.read(read_size).decode("utf-8", errors="ignore")
                        last_line = last_chunk.rstrip().split("\n")[-1]

                        if last_line.startswith("| ") and "|--" not in last_line:
                            parts = last_line.split("|")
                            if len(parts) > 1:
                                try:
                                    start_idx = int(parts[1].strip()) + 1
                                except ValueError:
                                    start_idx = 0
            except Exception:
                start_idx = 0

        mode = "a" if append else "w"
        with open(output_file, mode) as f:
            if not append or not file_exists:
                f.write("# Timeseries Data\n\n")
                f.write(f"**Experiment:** {output_file.stem.replace('_timeseries', '')}\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                headers = ["Index"] + list(data_lists.keys())
                f.write("| " + " | ".join(headers) + " |\n")
                f.write("|" + "|".join(["-----"] * len(headers)) + "|\n")
            else:
                f.write("\n---\n\n")
                if config:
                    f.write("### Configuration\n\n")

                    key_order = [
                        "batch_size",
                        "concurrency",
                        "backend",
                        "device",
                        "model",
                        "batching_enabled",
                        "max_batch_size",
                        "timeout_ms",
                    ]

                    config_items = []
                    for key in key_order:
                        if key in config:
                            val = config[key]

                            if isinstance(val, bool):
                                display_val = "Yes" if val else "No"
                            else:
                                display_val = str(val)
                            config_items.append(f"{key}: {display_val}")

                    if config_items:
                        f.write("**Parameters:** " + " | ".join(config_items) + "\n\n")

                f.write("**Data rows:**\n\n")
                headers = ["Index"] + list(data_lists.keys())
                f.write("| " + " | ".join(headers) + " |\n")
                f.write("|" + "|".join(["-----"] * len(headers)) + "|\n")

            buffer = []
            for i in range(max_len):
                row = [str(start_idx + i)]
                for _key, data in data_lists.items():
                    if i < len(data):
                        val = data[i]
                        row.append(f"{val:.1f}" if isinstance(val, float) else str(val))
                    else:
                        row.append("-")
                buffer.append("| " + " | ".join(row) + " |\n")

                if len(buffer) >= 1000:
                    f.writelines(buffer)
                    buffer.clear()

            if buffer:
                f.writelines(buffer)

        try:
            with open(index_file, "w") as f:
                f.write(str(start_idx + max_len - 1))
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Inference Benchmark Client")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=50051, help="Server port")
    parser.add_argument("--experiment", "-e", action="store_true", help="Experiment mode")
    parser.add_argument("--config", "-c", help="Experiment config YAML")
    parser.add_argument("--output", "-o", help="Output file for results")
    parser.add_argument(
        "--timeseries-file", help="Separate file for timeseries data (for sweep consolidation)"
    )
    parser.add_argument(
        "--append", action="store_true", help="Append to output file instead of overwriting"
    )
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--num-requests", type=int, default=100, help="Number of requests")
    parser.add_argument("--concurrency", type=int, default=1, help="Concurrency level")
    parser.add_argument("--dataset-size", type=int, default=50000, help="Number of test pairs")
    args = parser.parse_args()

    state = BenchmarkState()
    signal.signal(signal.SIGINT, state.handle_interrupt)
    signal.signal(signal.SIGTERM, state.handle_interrupt)

    config = {}
    if args.config:
        base_config_path = Path(__file__).parent.parent / "experiments" / "base_config.yaml"
        base_config = {}
        if base_config_path.exists():
            with open(base_config_path) as f:
                base_config = yaml.safe_load(f) or {}

        with open(args.config) as f:
            exp_config = yaml.safe_load(f) or {}

        def deep_merge(base, override):
            result = base.copy()
            for key, value in override.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result

        config = deep_merge(base_config, exp_config)

        exp = config.get("experiment", config.get("benchmark", {}))
        if "benchmark_requests" in exp:
            args.num_requests = exp["benchmark_requests"]
        if "num_requests" in exp:
            args.num_requests = exp["num_requests"]

    loader = DatasetLoader()
    pairs = loader.load(args.dataset_size)
    logger.info(f"Loaded {len(pairs)} test pairs")

    client = InferenceClient(args.host, args.port)

    exp = config.get("experiment", config.get("benchmark", {})) if config else {}
    batch_sizes = exp.get("batch_sizes", [args.batch_size])
    concurrency_levels = exp.get("concurrency_levels", [args.concurrency])

    if "batch_size" in exp and "batch_sizes" not in exp:
        batch_sizes = [exp["batch_size"]]
    if "concurrency" in exp and "concurrency_levels" not in exp:
        concurrency_levels = [exp["concurrency"]]

    total_combinations = len(batch_sizes) * len(concurrency_levels)
    logger.info(
        f"Running {total_combinations} configuration(s): {len(batch_sizes)} batch size(s) × {len(concurrency_levels)} concurrency level(s)"
    )

    logger.info("Warming up...")
    warmup_batch_size = batch_sizes[0] if batch_sizes else args.batch_size
    for _ in range(5):
        client.infer(pairs[:warmup_batch_size])

    try:
        runner = BenchmarkRunner(client, state)
        results = []

        config_num = 0
        for batch_size in batch_sizes:
            for concurrency in concurrency_levels:
                if state.interrupted:
                    logger.warning("Experiment interrupted, stopping...")
                    break

                config_num += 1
                logger.info(f"\n{'=' * 60}")
                logger.info(
                    f"Config {config_num}/{total_combinations}: batch_size={batch_size}, concurrency={concurrency}"
                )
                logger.info(f"Requests per config: {args.num_requests} (fixed for all configs)")
                logger.info(f"{'=' * 60}")

                try:
                    requests.post("http://localhost:8080/reset", timeout=2)
                except Exception:
                    pass

                result = runner.run(
                    pairs,
                    batch_size,
                    args.num_requests,
                    concurrency,
                )
                result["batch_size"] = batch_size
                result["concurrency"] = concurrency
                results.append(result)

                if "error" not in result:
                    logger.info(
                        f"✓ Completed: {result['total_pairs']} pairs in {result['total_time_s']:.2f}s"
                    )
                    logger.info(
                        f"  Throughput: {result['throughput_avg']:.1f} p/s, Latency: {result['latency_avg_ms']:.1f}ms"
                    )
                else:
                    logger.error(f"✗ Failed: {result.get('error', 'Unknown error')}")

                time.sleep(0.5)

            if state.interrupted:
                break

        dashboard_collector = DashboardCollector()
        dashboard_metrics = dashboard_collector.collect_history()

        successful = [r for r in results if "error" not in r]
        if successful:
            print("\n" + "=" * 80)
            print("EXPERIMENT SUMMARY")
            print("=" * 80)
            print(f"Total configurations tested: {len(results)}")
            print(f"Successful: {len(successful)}")
            print(f"Failed: {len(results) - len(successful)}")

            if successful:
                if len(successful) == 1:
                    r = successful[0]
                    print("\n" + "-" * 80)
                    print(f"CONFIGURATION: batch={r['batch_size']}, concurrency={r['concurrency']}")
                    print("-" * 80)

                    print("\nPER-REQUEST THROUGHPUT STATISTICS (pairs/s)")
                    print("-" * 80)
                    print(f"  Average: {r['throughput_avg']:.1f}")
                    print(f"  Min:     {r['throughput_min']:.1f}")
                    print(f"  Max:     {r['throughput_max']:.1f}")
                    print(f"  Std Dev: {r['throughput_std']:.1f}")
                    print(f"  P50:     {r['throughput_p50']:.1f}")
                    print(f"  P95:     {r['throughput_p95']:.1f}")

                    print("\nPER-REQUEST LATENCY STATISTICS (ms)")
                    print("-" * 80)
                    print(f"  Average: {r['latency_avg_ms']:.1f}")
                    print(f"  Min:     {r['latency_min_ms']:.1f}")
                    print(f"  Max:     {r['latency_max_ms']:.1f}")
                    print(f"  Std Dev: {r['latency_std_ms']:.1f}")
                    print(f"  P50:     {r['latency_p50_ms']:.1f}")
                    print(f"  P95:     {r['latency_p95_ms']:.1f}")
                    print(f"  P99:     {r['latency_p99_ms']:.1f}")
                else:
                    all_throughputs = [r["throughput_avg"] for r in successful]
                    all_latencies = [r["latency_avg_ms"] for r in successful]

                    best_tp = max(successful, key=lambda x: x["throughput_avg"])
                    worst_tp = min(successful, key=lambda x: x["throughput_avg"])
                    best_lat = min(successful, key=lambda x: x["latency_avg_ms"])
                    worst_lat = max(successful, key=lambda x: x["latency_avg_ms"])

                    avg_tp = sum(all_throughputs) / len(all_throughputs)
                    avg_lat = sum(all_latencies) / len(all_latencies)

                    tp_sorted = sorted(all_throughputs)
                    lat_sorted = sorted(all_latencies)
                    tp_p50 = tp_sorted[len(tp_sorted) // 2]
                    tp_p95 = (
                        tp_sorted[int(len(tp_sorted) * 0.95)]
                        if len(tp_sorted) > 1
                        else tp_sorted[0]
                    )
                    lat_p50 = lat_sorted[len(lat_sorted) // 2]
                    lat_p95 = (
                        lat_sorted[int(len(lat_sorted) * 0.95)]
                        if len(lat_sorted) > 1
                        else lat_sorted[0]
                    )

                    print("\n" + "-" * 80)
                    print("PER-CONFIGURATION THROUGHPUT STATISTICS (pairs/s)")
                    print("-" * 80)
                    print(f"  Average: {avg_tp:.1f}")
                    print(
                        f"  Min:     {worst_tp['throughput_avg']:.1f} (batch={worst_tp['batch_size']}, conc={worst_tp['concurrency']})"
                    )
                    print(
                        f"  Max:     {best_tp['throughput_avg']:.1f} (batch={best_tp['batch_size']}, conc={best_tp['concurrency']})"
                    )
                    print(f"  P50:     {tp_p50:.1f}")
                    print(f"  P95:     {tp_p95:.1f}")

                    print("\n" + "-" * 80)
                    print("PER-CONFIGURATION LATENCY STATISTICS (ms)")
                    print("-" * 80)
                    print(f"  Average: {avg_lat:.1f}")
                    print(
                        f"  Min:     {best_lat['latency_avg_ms']:.1f} (batch={best_lat['batch_size']}, conc={best_lat['concurrency']})"
                    )
                    print(
                        f"  Max:     {worst_lat['latency_avg_ms']:.1f} (batch={worst_lat['batch_size']}, conc={worst_lat['concurrency']})"
                    )
                    print(f"  P50:     {lat_p50:.1f}")
                    print(f"  P95:     {lat_p95:.1f}")

                print("\n" + "-" * 80)
                print("PER-CONFIGURATION RESULTS")
                print("-" * 80)
                print(
                    f"{'Batch':<8} {'Conc':<6} {'Throughput':<12} {'Latency':<10} {'Pairs':<8} {'Time(s)':<10}"
                )
                print("-" * 80)
                for r in sorted(successful, key=lambda x: (x["batch_size"], x["concurrency"])):
                    print(
                        f"{r['batch_size']:<8} {r['concurrency']:<6} "
                        f"{r['throughput_avg']:<12.1f} {r['latency_avg_ms']:<10.1f} "
                        f"{r['total_pairs']:<8} {r['total_time_s']:<10.2f}"
                    )
                print("=" * 80 + "\n")

        if args.output:
            writer = ResultsWriter()

            for idx, result in enumerate(results):
                if args.timeseries_file and idx == 0:
                    writer.save(
                        [result],
                        config,
                        args.output,
                        dashboard_metrics if idx == len(results) - 1 else None,
                        append=False,
                        timeseries_file=args.timeseries_file,
                    )
                elif args.timeseries_file:
                    writer.save(
                        [result],
                        config,
                        args.output,
                        dashboard_metrics if idx == len(results) - 1 else None,
                        append=True,
                        timeseries_file=args.timeseries_file,
                    )
                elif idx == 0:
                    writer.save(
                        results,
                        config,
                        args.output,
                        dashboard_metrics,
                        append=False,
                        timeseries_file=args.timeseries_file,
                    )
                    break

    finally:
        client.close()


if __name__ == "__main__":
    main()
