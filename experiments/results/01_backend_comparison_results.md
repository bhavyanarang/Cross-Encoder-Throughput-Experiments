# 01_backend_comparison_compiled

_Compare all backends (pytorch, mps, mlx, compiled)_

**Timestamp:** 2026-01-01 20:52:38

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `compiled` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 3648 | 60.12 | 526.7ms | 533.4ms | 535.0ms | 60.7 | 61.6 |

## Detailed Metrics

### Run 1

**Total:** 3648 pairs in 60.12s

### Latency

| Metric | Value |
|--------|-------|
| Average | 526.70 |
| Min | 513.15 |
| Max | 535.20 |
| Std Dev | 4.64 |
| P50 | 526.42 |
| P90 | 532.51 |
| P95 | 533.40 |
| P99 | 535.05 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 60.68 |
| Min | 59.79 |
| Max | 62.36 |
| Std Dev | 0.54 |
| P50 | 60.79 |
| P90 | 61.39 |
| P95 | 61.64 |
| P99 | 62.04 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 526.4ms (P50) | 61.20 | 60.80 | 62.36 | 57 |
| 526.4-531.0ms (P50-P75) | 60.57 | 60.27 | 60.77 | 28 |
| 531.0-532.5ms (P75-P90) | 60.17 | 60.10 | 60.26 | 17 |
| >= 532.5ms (P90+) | 59.97 | 59.79 | 60.09 | 12 |

**Correlation:** -1.000 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 60.68 p/s | batch=32, conc=1 |
| Best Latency | 526.70ms | batch=32, conc=1 |
| Avg Throughput | 60.68 p/s | all configs |
| Avg Latency | 526.70ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1152.6 | 1150.6 | 1154.6 | 1152.6 | 1154.4 |
| GPU Utilization (%) | 6.6 | 4.5 | 8.7 | 6.6 | 8.5 |
| CPU Usage (%) | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| Tokenization (ms) | 18.4 | 17.2 | 19.7 | 18.4 | 19.5 |
| Inference (ms) | 42.2 | 39.8 | 44.7 | 42.2 | 44.5 |
| Queue Wait (ms) | 18.6 | 17.3 | 19.8 | 18.6 | 19.7 |
| Padding Waste (%) | 41.2 | 39.1 | 43.4 | 41.2 | 43.2 |

### Stage Timing

| Stage | Percentage |
|-------|------------|
| Tokenization | 3.5% |
| Queue Wait | 3.6% |
| Model Inference | 10.1% |
| Other/gRPC | 0.0% |

### Worker Metrics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 53.2 | 72.8 | 0.0 | 3808 |

Full time-series data is available in: `distribution/01_backend_comparison_timeseries.md`
