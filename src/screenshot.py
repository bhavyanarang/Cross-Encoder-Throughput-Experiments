#!/usr/bin/env python3

import argparse
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)


def parse_timeseries_markdown(markdown_path: Path) -> dict:
    with open(markdown_path) as f:
        content = f.read()

    exp_match = re.search(r"\*\*Experiment:\*\* (.+)", content)
    experiment_name = exp_match.group(1).strip() if exp_match else "Unknown Experiment"

    lines = content.split("\n")
    table_start = None
    headers = None

    for i, line in enumerate(lines):
        if line.startswith("| Index |"):
            headers = [h.strip() for h in line.split("|")[1:-1]]
            table_start = i + 2

    if not headers or table_start is None:
        raise ValueError("Could not find timeseries table in markdown file")

    data = {h: [] for h in headers}
    for line in lines[table_start:]:
        if not line.strip() or not line.startswith("|"):
            break
        values = [v.strip() for v in line.split("|")[1:-1]]
        if len(values) != len(headers):
            continue
        for header, value in zip(headers, values, strict=False):
            if value == "-":
                data[header].append(None)
            else:
                try:
                    data[header].append(float(value))
                except ValueError:
                    data[header].append(value)

    max_len = max((len(v) for v in data.values()), default=0)
    timestamps = [float(i) for i in range(max_len)]

    def pick(*names: str) -> list:
        for name in names:
            if name in data:
                return data[name]
        return []

    return {
        "experiment_name": experiment_name,
        "timestamps": timestamps,
        "gpu_memory_mb": pick("GPU Mem (MB)"),
        "gpu_utilization_pct": pick("GPU Util (%)"),
        "cpu_percent": pick("CPU (%)"),
        "latencies": pick("Latency (ms)"),
        "throughput": pick("Throughput"),
        "tokenize_ms": pick("Tokenize (ms)"),
        "inference_ms": pick("Inference (ms)"),
        "queue_wait_ms": pick("Queue Wait (ms)", "Queue (ms)"),
        "tokenizer_queue_wait_ms": pick("Tokenizer Queue Wait (ms)"),
        "model_queue_wait_ms": pick("Model Queue Wait (ms)"),
        "tokenizer_queue_size": pick("Tokenizer Queue Size", "Tokenizer Queue"),
        "model_queue_size": pick("Model Queue Size", "Model Queue"),
        "batch_queue_size": pick("Batch Queue Size"),
        "padding_pct": pick("Padding (%)"),
    }


def compute_summary_stats(timeseries_data: dict) -> dict:
    def stats(arr):
        if not arr:
            return {"avg": 0, "min": 0, "max": 0, "p50": 0, "p95": 0, "count": 0}
        a = np.array(arr)
        return {
            "avg": float(np.mean(a)),
            "min": float(np.min(a)),
            "max": float(np.max(a)),
            "p50": float(np.percentile(a, 50)),
            "p95": float(np.percentile(a, 95)),
            "count": len(a),
        }

    latencies = [v for v in timeseries_data.get("latencies", []) if isinstance(v, (int, float))]
    if not latencies:
        return {}

    tokenize_total = sum(
        v for v in timeseries_data.get("tokenize_ms", []) if isinstance(v, (int, float))
    )
    queue_total = sum(
        v for v in timeseries_data.get("queue_wait_ms", []) if isinstance(v, (int, float))
    )
    inference_total = sum(
        v for v in timeseries_data.get("inference_ms", []) if isinstance(v, (int, float))
    )
    total_latency = sum(latencies)

    if total_latency > 0:
        tokenize_pct = (tokenize_total / total_latency) * 100
        queue_pct = (queue_total / total_latency) * 100
        inference_pct = (inference_total / total_latency) * 100
        other_pct = 100 - tokenize_pct - queue_pct - inference_pct
    else:
        tokenize_pct = queue_pct = inference_pct = other_pct = 0

    return {
        "count": len(latencies),
        "query_count": len(latencies),
        "instant_latency_ms": latencies[-1] if latencies else 0,
        "avg_ms": stats(latencies)["avg"],
        "p50_ms": stats(latencies)["p50"],
        "p95_ms": stats(latencies)["p95"],
        "p99_ms": float(np.percentile(np.array(latencies), 99)) if latencies else 0,
        "throughput_qps": (timeseries_data.get("throughput", []) or [0])[-1],
        "avg_throughput_qps": stats(
            [v for v in timeseries_data.get("throughput", []) if isinstance(v, (int, float))]
        )["avg"],
        "cpu_percent": stats(
            [v for v in timeseries_data.get("cpu_percent", []) if isinstance(v, (int, float))]
        )["avg"],
        "gpu_memory_mb": stats(
            [v for v in timeseries_data.get("gpu_memory_mb", []) if isinstance(v, (int, float))]
        )["avg"],
        "gpu_utilization_pct": stats(
            [
                v
                for v in timeseries_data.get("gpu_utilization_pct", [])
                if isinstance(v, (int, float))
            ]
        )["avg"],
        "last_tokenize_ms": (timeseries_data.get("tokenize_ms", []) or [0])[-1],
        "last_inference_ms": (timeseries_data.get("inference_ms", []) or [0])[-1],
        "last_queue_wait_ms": (timeseries_data.get("queue_wait_ms", []) or [0])[-1],
        "stage_breakdown": {
            "tokenize": stats(
                [v for v in timeseries_data.get("tokenize_ms", []) if isinstance(v, (int, float))]
            ),
            "queue_wait": stats(
                [v for v in timeseries_data.get("queue_wait_ms", []) if isinstance(v, (int, float))]
            ),
            "model_inference": stats(
                [v for v in timeseries_data.get("inference_ms", []) if isinstance(v, (int, float))]
            ),
        },
        "stage_percentages": {
            "tokenize_pct": round(tokenize_pct, 1),
            "queue_wait_pct": round(queue_pct, 1),
            "inference_pct": round(inference_pct, 1),
            "other_pct": round(other_pct, 1),
        },
        "queue_wait_analysis": {
            "avg_ms": stats(
                [v for v in timeseries_data.get("queue_wait_ms", []) if isinstance(v, (int, float))]
            )["avg"],
            "p95_ms": stats(
                [v for v in timeseries_data.get("queue_wait_ms", []) if isinstance(v, (int, float))]
            )["p95"],
        },
        "padding_analysis": {
            "last_padding_pct": (timeseries_data.get("padding_pct", []) or [0])[-1],
            "avg_padding_pct": stats(
                [v for v in timeseries_data.get("padding_pct", []) if isinstance(v, (int, float))]
            )["avg"],
        },
    }


def generate_static_dashboard(
    timeseries_path: Path,
    output_path: Path,
    experiment_config: dict | None = None,
) -> bool:
    try:
        timeseries_data = parse_timeseries_markdown(timeseries_path)

        summary = compute_summary_stats(timeseries_data)

        experiment_name = timeseries_data.get("experiment_name", "experiment")
        description = experiment_config.get("description", "") if experiment_config else ""
        backend = (
            experiment_config.get("model", {}).get("backend", "pytorch")
            if experiment_config
            else "pytorch"
        )
        device = (
            experiment_config.get("model", {}).get("device", "cpu") if experiment_config else "cpu"
        )
        static_html = _build_html(
            experiment_name=experiment_name,
            description=description,
            backend=backend,
            device=device,
            summary=summary,
            timeseries=timeseries_data,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.suffix.lower() == ".png":
            _render_png(static_html, output_path)
        else:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(static_html)
        logger.info(f"Generated static dashboard: {output_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to generate static dashboard: {e}", exc_info=True)
        return False


def _build_html(
    experiment_name: str,
    description: str,
    backend: str,
    device: str,
    summary: dict,
    timeseries: dict,
) -> str:
    rows = []
    timestamps = timeseries.get("timestamps", [])
    max_rows = 120
    start_idx = max(0, len(timestamps) - max_rows)
    for idx in range(start_idx, len(timestamps)):
        rows.append(
            "<tr>"
            f"<td>{idx}</td>"
            f"<td>{_fmt(timeseries.get('gpu_memory_mb', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('gpu_utilization_pct', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('cpu_percent', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('latencies', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('throughput', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('tokenize_ms', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('inference_ms', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('queue_wait_ms', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('tokenizer_queue_wait_ms', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('model_queue_wait_ms', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('tokenizer_queue_size', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('model_queue_size', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('batch_queue_size', []), idx)}</td>"
            f"<td>{_fmt(timeseries.get('padding_pct', []), idx)}</td>"
            "</tr>"
        )
    summary_rows = [
        ("Requests", summary.get("query_count", 0)),
        ("Latency P50 (ms)", round(summary.get("p50_ms", 0), 2)),
        ("Latency P95 (ms)", round(summary.get("p95_ms", 0), 2)),
        ("Throughput (qps)", round(summary.get("throughput_qps", 0), 2)),
        ("Avg Throughput (qps)", round(summary.get("avg_throughput_qps", 0), 2)),
        ("CPU (%)", round(summary.get("cpu_percent", 0), 2)),
        ("GPU Mem (MB)", round(summary.get("gpu_memory_mb", 0), 2)),
        ("GPU Util (%)", round(summary.get("gpu_utilization_pct", 0), 2)),
        ("Padding (%)", round(summary.get("padding_analysis", {}).get("avg_padding_pct", 0), 2)),
    ]
    summary_html = "".join(
        f"<tr><td>{label}</td><td>{value}</td></tr>" for label, value in summary_rows
    )
    description_html = f"<p>{description}</p>" if description else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{experiment_name} Snapshot</title>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 24px; color: #111; }}
    h1 {{ margin-bottom: 4px; }}
    .meta {{ color: #444; margin-bottom: 16px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ border: 1px solid #ddd; padding: 6px 8px; text-align: right; }}
    th {{ background: #f3f4f6; text-align: center; }}
    td:first-child, th:first-child {{ text-align: left; }}
    .section {{ margin-top: 24px; }}
  </style>
</head>
<body>
  <h1>{experiment_name}</h1>
  <div class="meta">Backend: {backend} | Device: {device}</div>
  {description_html}
  <div class="section">
    <h2>Summary</h2>
    <table>
      <thead>
        <tr><th>Metric</th><th>Value</th></tr>
      </thead>
      <tbody>
        {summary_html}
      </tbody>
    </table>
  </div>
  <div class="section">
    <h2>Timeseries (last {min(len(timestamps), max_rows)} samples)</h2>
    <table>
      <thead>
        <tr>
          <th>Index</th>
          <th>GPU Mem (MB)</th>
          <th>GPU Util (%)</th>
          <th>CPU (%)</th>
          <th>Latency (ms)</th>
          <th>Throughput</th>
          <th>Tokenize (ms)</th>
          <th>Inference (ms)</th>
          <th>Queue Wait (ms)</th>
          <th>Tokenizer Queue Wait (ms)</th>
          <th>Model Queue Wait (ms)</th>
          <th>Tokenizer Queue Size</th>
          <th>Model Queue Size</th>
          <th>Batch Queue Size</th>
          <th>Padding (%)</th>
        </tr>
      </thead>
      <tbody>
        {"".join(rows)}
      </tbody>
    </table>
  </div>
</body>
</html>"""


def _fmt(series: list, idx: int) -> str:
    if idx >= len(series):
        return "-"
    value = series[idx]
    if value is None:
        return "-"
    if isinstance(value, str):
        return value
    try:
        numeric = float(value)
    except Exception:
        return "-"
    if abs(numeric) >= 100 or numeric.is_integer():
        return f"{numeric:.0f}"
    if abs(numeric) >= 10:
        return f"{numeric:.1f}"
    return f"{numeric:.2f}"


def _render_png(html: str, output_path: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        executable_path = p.chromium.executable_path
        if executable_path and not Path(executable_path).exists():
            fallback = executable_path.replace("mac-x64", "mac-arm64")
            if Path(fallback).exists():
                executable_path = fallback
        browser = p.chromium.launch(executable_path=executable_path)
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=str(output_path), full_page=True)
        browser.close()


def find_timeseries_file(experiment_name: str, distribution_dir: Path) -> Path | None:
    patterns = [
        f"{experiment_name}_timeseries.md",
        f"{experiment_name.replace('_results', '')}_timeseries.md",
    ]

    for pattern in patterns:
        path = distribution_dir / pattern
        if path.exists():
            return path

    return None


def create_dummy_timeseries(path: Path, experiment_name: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write("# Timeseries Data\n\n")
        f.write(f"**Experiment:** {experiment_name}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        headers = [
            "Index",
            "GPU Mem (MB)",
            "GPU Util (%)",
            "CPU (%)",
            "Latency (ms)",
            "Throughput",
            "Tokenize (ms)",
            "Inference (ms)",
            "Queue Wait (ms)",
            "Tokenizer Queue Wait (ms)",
            "Model Queue Wait (ms)",
            "Tokenizer Queue Size",
            "Model Queue Size",
            "Batch Queue Size",
            "Padding (%)",
        ]
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("|" + "|".join(["-----"] * len(headers)) + "|\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate static HTML dashboard from timeseries data"
    )
    parser.add_argument("--timeseries", "-t", type=Path, help="Path to timeseries markdown file")
    parser.add_argument(
        "--experiment",
        "-e",
        help="Experiment name (to find timeseries file in distribution/)",
    )
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output HTML file path")
    parser.add_argument(
        "--distribution-dir",
        "-d",
        type=Path,
        default=Path("experiments/distribution"),
        help="Directory containing timeseries files",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    if args.timeseries:
        timeseries_path = args.timeseries
    elif args.experiment:
        timeseries_path = find_timeseries_file(args.experiment, args.distribution_dir)
        if not timeseries_path:
            logger.warning(
                f"Could not find timeseries file for experiment: {args.experiment}. Creating dummy file."
            )
            timeseries_path = args.distribution_dir / f"{args.experiment}_timeseries.md"
            create_dummy_timeseries(timeseries_path, args.experiment)
    else:
        logger.error("Must provide either --timeseries or --experiment")
        sys.exit(1)

    if not timeseries_path.exists():
        logger.warning(f"Timeseries file not found: {timeseries_path}. Creating dummy file.")
        experiment_name = (
            args.experiment if args.experiment else timeseries_path.stem.replace("_timeseries", "")
        )
        create_dummy_timeseries(timeseries_path, experiment_name)

    success = generate_static_dashboard(timeseries_path, args.output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
