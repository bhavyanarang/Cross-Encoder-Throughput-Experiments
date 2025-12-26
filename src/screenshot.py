#!/usr/bin/env python3
"""Generate static HTML dashboard from timeseries data."""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).parent / "frontend"
TEMPLATES_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR / "static"


def parse_timeseries_markdown(markdown_path: Path) -> dict:
    """Parse timeseries markdown file and extract data."""
    with open(markdown_path) as f:
        content = f.read()

    # Extract experiment name
    exp_match = re.search(r"\*\*Experiment:\*\* (.+)", content)
    experiment_name = exp_match.group(1).strip() if exp_match else "Unknown Experiment"

    # Find the table
    lines = content.split("\n")
    table_start = None
    headers = None

    for i, line in enumerate(lines):
        if line.startswith("| Index |"):
            headers = [h.strip() for h in line.split("|")[1:-1]]
            table_start = i + 2  # Skip header and separator
            break

    if not headers or table_start is None:
        raise ValueError("Could not find timeseries table in markdown file")

    # Parse data rows
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

    # Convert to arrays, filtering None values
    max_len = max(len(v) for v in data.values() if v)
    timestamps = [float(i) for i in range(max_len)]

    return {
        "experiment_name": experiment_name,
        "timestamps": timestamps,
        "gpu_memory_mb": [v for v in data.get("GPU Mem (MB)", []) if v is not None],
        "gpu_utilization_pct": [v for v in data.get("GPU Util (%)", []) if v is not None],
        "cpu_percent": [v for v in data.get("CPU (%)", []) if v is not None],
        "latencies": [v for v in data.get("Latency (ms)", []) if v is not None],
        "throughput": [v for v in data.get("Throughput", []) if v is not None],
        "tokenize_ms": [v for v in data.get("Tokenize (ms)", []) if v is not None],
        "inference_ms": [v for v in data.get("Inference (ms)", []) if v is not None],
        "queue_wait_ms": [v for v in data.get("Queue (ms)", []) if v is not None],
        "padding_pct": [v for v in data.get("Padding (%)", []) if v is not None],
    }


def compute_summary_stats(timeseries_data: dict) -> dict:
    """Compute summary statistics from timeseries data."""

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

    latencies = timeseries_data.get("latencies", [])
    if not latencies:
        return {}

    # Compute stage breakdown percentages
    tokenize_total = sum(timeseries_data.get("tokenize_ms", []))
    queue_total = sum(timeseries_data.get("queue_wait_ms", []))
    inference_total = sum(timeseries_data.get("inference_ms", []))
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
        "query_count": len(latencies),  # Approximate
        "instant_latency_ms": latencies[-1] if latencies else 0,
        "avg_ms": stats(latencies)["avg"],
        "p50_ms": stats(latencies)["p50"],
        "p95_ms": stats(latencies)["p95"],
        "p99_ms": float(np.percentile(np.array(latencies), 99)) if latencies else 0,
        "throughput_qps": timeseries_data.get("throughput", [0])[-1]
        if timeseries_data.get("throughput")
        else 0,
        "avg_throughput_qps": stats(timeseries_data.get("throughput", []))["avg"],
        "cpu_percent": stats(timeseries_data.get("cpu_percent", []))["avg"],
        "gpu_memory_mb": stats(timeseries_data.get("gpu_memory_mb", []))["avg"],
        "gpu_utilization_pct": stats(timeseries_data.get("gpu_utilization_pct", []))["avg"],
        "last_tokenize_ms": timeseries_data.get("tokenize_ms", [0])[-1]
        if timeseries_data.get("tokenize_ms")
        else 0,
        "last_inference_ms": timeseries_data.get("inference_ms", [0])[-1]
        if timeseries_data.get("inference_ms")
        else 0,
        "last_queue_wait_ms": timeseries_data.get("queue_wait_ms", [0])[-1]
        if timeseries_data.get("queue_wait_ms")
        else 0,
        "stage_breakdown": {
            "tokenize": stats(timeseries_data.get("tokenize_ms", [])),
            "queue_wait": stats(timeseries_data.get("queue_wait_ms", [])),
            "model_inference": stats(timeseries_data.get("inference_ms", [])),
        },
        "stage_percentages": {
            "tokenize_pct": round(tokenize_pct, 1),
            "queue_wait_pct": round(queue_pct, 1),
            "inference_pct": round(inference_pct, 1),
            "other_pct": round(other_pct, 1),
        },
        "queue_wait_analysis": {
            "avg_ms": stats(timeseries_data.get("queue_wait_ms", []))["avg"],
            "p95_ms": stats(timeseries_data.get("queue_wait_ms", []))["p95"],
        },
        "padding_analysis": {
            "last_padding_pct": timeseries_data.get("padding_pct", [0])[-1]
            if timeseries_data.get("padding_pct")
            else 0,
            "avg_padding_pct": stats(timeseries_data.get("padding_pct", []))["avg"],
        },
    }


def generate_static_dashboard(
    timeseries_path: Path,
    output_path: Path,
    experiment_config: dict | None = None,
) -> bool:
    """Generate static HTML dashboard from timeseries data."""
    try:
        # Parse timeseries data
        timeseries_data = parse_timeseries_markdown(timeseries_path)

        # Compute summary statistics
        summary = compute_summary_stats(timeseries_data)

        # Build metrics response structure
        metrics_data = {
            "experiment_name": timeseries_data["experiment_name"],
            "experiment_description": experiment_config.get("description", "")
            if experiment_config
            else "",
            "backend_type": experiment_config.get("model", {}).get("backend", "pytorch")
            if experiment_config
            else "pytorch",
            "device": experiment_config.get("model", {}).get("device", "cpu")
            if experiment_config
            else "cpu",
            "is_running": False,  # Static dashboard is always not running
            **summary,
            "history": {
                "timestamps": timeseries_data["timestamps"],
                "latencies": timeseries_data["latencies"],
                "throughput": timeseries_data["throughput"],
                "queries": list(range(len(timeseries_data["latencies"]))),
                "cpu_percent": timeseries_data["cpu_percent"],
                "gpu_memory_mb": timeseries_data["gpu_memory_mb"],
                "gpu_utilization_pct": timeseries_data["gpu_utilization_pct"],
                "queue_wait_ms": timeseries_data["queue_wait_ms"],
                "tokenize_ms": timeseries_data["tokenize_ms"],
                "inference_ms": timeseries_data["inference_ms"],
                "padding_pct": timeseries_data["padding_pct"],
            },
            "worker_stats": [],  # Empty for now, can be enhanced later
        }

        # Read HTML template
        html_template = (TEMPLATES_DIR / "index.html").read_text()

        # Read CSS
        css_content = (STATIC_DIR / "css" / "styles.css").read_text()

        # Read JS files
        charts_js = (STATIC_DIR / "js" / "charts.js").read_text()
        main_js = (STATIC_DIR / "js" / "main.js").read_text()

        # Modify main.js to use embedded data instead of polling
        # Replace the fetchAndUpdate function and init function
        modified_main_js = main_js.replace(
            "// Fetch metrics and update dashboard\nasync function fetchAndUpdate() {",
            "// Fetch metrics from embedded data\nasync function fetchAndUpdate() {",
        )
        modified_main_js = modified_main_js.replace(
            "        const response = await fetch('/metrics');\n        const data = await response.json();",
            "        // Use embedded data instead of fetching\n        const data = window.embeddedMetricsData;",
        )
        modified_main_js = modified_main_js.replace(
            "// Initialize dashboard\nfunction init() {\n    window.DashboardCharts.init();\n    fetchAndUpdate();\n    setInterval(fetchAndUpdate, 500);\n}",
            "// Initialize dashboard\nfunction init() {\n    window.DashboardCharts.init();\n    fetchAndUpdate();\n    // No polling for static dashboard\n}",
        )

        # Replace Chart.js CDN link with embedded version or keep CDN
        # For now, keep CDN link in template

        # Extract body content from template (everything between <body> and <!-- Scripts -->)
        body_match = re.search(r"<body>(.*?)<!-- Scripts -->", html_template, re.DOTALL)
        if body_match:
            body_content = body_match.group(1)
        else:
            # Fallback: extract everything between body tags, excluding scripts
            body_match = re.search(r"<body>(.*?)</body>", html_template, re.DOTALL)
            if body_match:
                body_content = body_match.group(1)
                # Remove script tags
                body_content = re.sub(
                    r"<script[^>]*>.*?</script>", "", body_content, flags=re.DOTALL
                )
            else:
                body_content = ""

        # Generate static HTML
        static_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metrics_data["experiment_name"]} - Static Dashboard</title>
    <style>
{css_content}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
</head>
<body>
    {body_content}

    <!-- Embedded Metrics Data -->
    <script>
        window.embeddedMetricsData = {json.dumps(metrics_data, indent=2)};
    </script>

    <!-- Charts JS -->
    <script>
{charts_js}
    </script>

    <!-- Main JS (modified) -->
    <script>
{modified_main_js}
    </script>
</body>
</html>"""

        # Write output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(static_html)

        logger.info(f"Generated static dashboard: {output_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to generate static dashboard: {e}", exc_info=True)
        return False


def find_timeseries_file(experiment_name: str, distribution_dir: Path) -> Path | None:
    """Find timeseries markdown file for an experiment."""
    # Try different naming patterns
    patterns = [
        f"{experiment_name}_timeseries.md",
        f"{experiment_name.replace('_results', '')}_timeseries.md",
    ]

    for pattern in patterns:
        path = distribution_dir / pattern
        if path.exists():
            return path

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate static HTML dashboard from timeseries data"
    )
    parser.add_argument("--timeseries", "-t", type=Path, help="Path to timeseries markdown file")
    parser.add_argument(
        "--experiment", "-e", help="Experiment name (to find timeseries file in distribution/)"
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

    # Determine timeseries file path
    if args.timeseries:
        timeseries_path = args.timeseries
    elif args.experiment:
        timeseries_path = find_timeseries_file(args.experiment, args.distribution_dir)
        if not timeseries_path:
            logger.error(f"Could not find timeseries file for experiment: {args.experiment}")
            sys.exit(1)
    else:
        logger.error("Must provide either --timeseries or --experiment")
        sys.exit(1)

    if not timeseries_path.exists():
        logger.error(f"Timeseries file not found: {timeseries_path}")
        sys.exit(1)

    success = generate_static_dashboard(timeseries_path, args.output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
