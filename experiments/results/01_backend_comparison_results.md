# 01_backend_comparison_compiled

_Compare all backends (pytorch, mps, mlx, compiled)_

**Timestamp:** 2025-12-26 16:09:15

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `compiled` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 13792 | 60.05 | 139.2ms | 165.2ms | 194.1ms | 229.7 | 281.4 |

## Detailed Metrics

### Config 1: batch=32, concurrency=1

**Total:** 13792 pairs in 60.05s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 139.17 |
| Min | 106.41 |
| Max | 1442.90 |
| Std Dev | 86.45 |
| P50 | 128.30 |
| P90 | 155.35 |
| P95 | 165.20 |
| P99 | 194.10 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 229.66 |
| Min | 22.18 |
| Max | 300.73 |
| Std Dev | 31.63 |
| P50 | 249.42 |
| P90 | 276.03 |
| P95 | 281.45 |
| P99 | 291.86 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 128.3ms (P50) | 265.29 | 249.52 | 300.73 | 215 |
| 128.3-140.8ms (P50-P75) | 238.46 | 227.62 | 249.42 | 108 |
| 140.8-155.3ms (P75-P90) | 218.48 | 206.41 | 227.02 | 64 |
| >= 155.3ms (P90+) | 180.15 | 22.18 | 205.99 | 44 |

**Correlation:** -0.661 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 229.66 p/s | batch=32, conc=1 |
| Best Latency | 139.17ms | batch=32, conc=1 |
| Avg Throughput | 229.66 p/s | all configs |
| Avg Latency | 139.17ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1220.9 | 1084.6 | 1322.6 | 1212.6 | 1322.6 |
| GPU Utilization (%) | 90.2 | 75.0 | 100.0 | 90.2 | 100.0 |
| CPU Usage (%) | 3.2 | 0.8 | 63.1 | 1.0 | 18.3 |
| Tokenization (ms) | 11.9 | 10.2 | 19.8 | 11.6 | 13.5 |
| Inference (ms) | 142.9 | 95.9 | 1427.6 | 117.4 | 163.2 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 41.8 | 26.3 | 72.5 | 41.7 | 52.4 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 8.5% |
| Queue Wait | 0.0% |
| Model Inference | 90.8% |
| Other/gRPC | 0.8% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 141.3 | 164.9 | 228.5 | 13952 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/01_backend_comparison_timeseries.md`
