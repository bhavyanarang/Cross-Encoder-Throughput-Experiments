#!/usr/bin/env python3
"""
Extract latency and throughput data from all distribution markdown files.
"""

import csv
from collections import defaultdict
from pathlib import Path


def extract_metrics_from_md(md_content):
    """Extract latency and throughput data from markdown table."""
    lines = md_content.strip().split("\n")

    # Find the header line
    header_idx = -1
    for i, line in enumerate(lines):
        if "|" in line and "Latency" in line and "Throughput" in line:
            header_idx = i
            break

    if header_idx == -1:
        return []

    # Parse header
    header_line = lines[header_idx]
    headers = [h.strip() for h in header_line.split("|")[1:-1]]

    # Find latency and throughput column indices
    latency_idx = -1
    throughput_idx = -1
    for i, h in enumerate(headers):
        if "latency" in h.lower():
            latency_idx = i
        if "throughput" in h.lower():
            throughput_idx = i

    if latency_idx == -1 or throughput_idx == -1:
        return []

    # Extract data rows
    data = []
    for i in range(header_idx + 2, len(lines)):
        line = lines[i].strip()
        if not line or line.startswith("|"):
            continue

        try:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) > max(latency_idx, throughput_idx):
                latency_str = cells[latency_idx].replace(" (ms)", "").strip()
                throughput_str = cells[throughput_idx].strip()

                latency = float(latency_str)
                throughput = float(throughput_str)

                data.append({"latency_ms": latency, "throughput": throughput})
        except (ValueError, IndexError):
            continue

    return data


def main():
    dist_dir = Path("experiments/distribution")

    # Collect all metrics
    all_metrics = []

    # Process all markdown files
    md_files = sorted(dist_dir.glob("*_timeseries.md"))
    print(f"Found {len(md_files)} distribution files")

    for md_file in md_files:
        experiment_name = md_file.stem.replace("_timeseries", "")

        with open(md_file) as f:
            content = f.read()

        metrics = extract_metrics_from_md(content)

        for idx, metric in enumerate(metrics):
            all_metrics.append(
                {
                    "experiment": experiment_name,
                    "index": idx,
                    "latency_ms": metric["latency_ms"],
                    "throughput": metric["throughput"],
                }
            )

        print(f"  {experiment_name}: {len(metrics)} data points")

    print(f"\nTotal data points collected: {len(all_metrics)}")

    # Save to CSV
    output_file = "experiments/all_metrics_distribution.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["experiment", "index", "latency_ms", "throughput"])
        writer.writeheader()
        writer.writerows(all_metrics)

    print(f"✓ Saved to {output_file}")

    # Print summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    # By experiment
    by_exp = defaultdict(list)
    for m in all_metrics:
        by_exp[m["experiment"]].append({"latency": m["latency_ms"], "throughput": m["throughput"]})

    for exp in sorted(by_exp.keys()):
        latencies = [m["latency"] for m in by_exp[exp]]
        throughputs = [m["throughput"] for m in by_exp[exp]]

        avg_lat = sum(latencies) / len(latencies)
        min_lat = min(latencies)
        max_lat = max(latencies)
        avg_tp = sum(throughputs) / len(throughputs)
        min_tp = min(throughputs)
        max_tp = max(throughputs)

        print(f"\n{exp}:")
        print(f"  Latency (ms):  avg={avg_lat:.2f}, min={min_lat:.2f}, max={max_lat:.2f}")
        print(f"  Throughput:    avg={avg_tp:.1f}, min={min_tp:.0f}, max={max_tp:.0f}")

    # Overall stats
    all_latencies = [m["latency_ms"] for m in all_metrics]
    all_throughputs = [m["throughput"] for m in all_metrics]

    print(f"\n{'OVERALL STATISTICS':}")
    print(f"  Total experiments: {len(by_exp)}")
    print(f"  Total data points: {len(all_metrics)}")
    print(
        f"  Latency (ms):  avg={sum(all_latencies) / len(all_latencies):.2f}, min={min(all_latencies):.2f}, max={max(all_latencies):.2f}"
    )
    print(
        f"  Throughput:    avg={sum(all_throughputs) / len(all_throughputs):.1f}, min={min(all_throughputs):.0f}, max={max(all_throughputs):.0f}"
    )


if __name__ == "__main__":
    main()
