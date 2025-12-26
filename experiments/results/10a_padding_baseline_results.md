# 10a_padding_baseline

_Baseline with random ordering (length-aware batching disabled)_

**Timestamp:** 2025-12-26 16:36:38

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=64, timeout=50ms)

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 1 | 32000 | 46.55 | 93.0ms | 133.1ms | 168.0ms | 687.4 | 843.8 |

## Detailed Metrics

### Config 1: batch=64, concurrency=1

**Total:** 32000 pairs in 46.55s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 92.97 |
| Min | 68.21 |
| Max | 250.38 |
| Std Dev | 20.60 |
| P50 | 86.59 |
| P90 | 117.38 |
| P95 | 133.11 |
| P99 | 168.00 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 687.44 |
| Min | 255.61 |
| Max | 938.34 |
| Std Dev | 113.02 |
| P50 | 739.12 |
| P90 | 823.02 |
| P95 | 843.81 |
| P99 | 877.32 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 86.6ms (P50) | 798.22 | 739.75 | 938.34 | 250 |
| 86.6-96.1ms (P50-P75) | 699.46 | 666.38 | 738.48 | 125 |
| 96.1-117.4ms (P75-P90) | 612.94 | 545.28 | 665.55 | 75 |
| >= 117.4ms (P90+) | 462.63 | 255.61 | 545.05 | 50 |

**Correlation:** -0.951 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 687.44 p/s | batch=64, conc=1 |
| Best Latency | 92.97ms | batch=64, conc=1 |
| Avg Throughput | 687.44 p/s | all configs |
| Avg Latency | 92.97ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 2347.3 | 1106.6 | 2734.6 | 2520.6 | 2734.6 |
| GPU Utilization (%) | 70.3 | 33.1 | 86.6 | 70.1 | 78.3 |
| CPU Usage (%) | 1.2 | 0.9 | 1.7 | 1.2 | 1.4 |
| Tokenization (ms) | 23.5 | 19.5 | 74.0 | 22.5 | 27.0 |
| Inference (ms) | 66.4 | 49.7 | 133.1 | 58.9 | 102.7 |
| Queue Wait (ms) | 1.3 | 1.1 | 1.6 | 1.3 | 1.3 |
| Padding Waste (%) | 44.6 | 35.6 | 60.4 | 43.8 | 54.4 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 26.0% |
| Queue Wait | 1.4% |
| Model Inference | 71.5% |
| Other/gRPC | 1.0% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 91.9 | 132.3 | 682.1 | 32320 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/10a_padding_baseline_timeseries.md`
