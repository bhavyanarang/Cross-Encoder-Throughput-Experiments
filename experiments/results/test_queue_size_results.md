# test_queue_size

_High batch size and concurrency to test queue size tracking_

**Timestamp:** 2026-01-01 04:12:03

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 128 | 32 | 39936 | 95.03 | 6454.4ms | 7771.3ms | 8293.9ms | 420.2 | 30.6 |

## Detailed Metrics

### Run 1

**Total:** 39936 pairs in 95.03s

### Latency

| Metric | Value |
|--------|-------|
| Average | 6454.44 |
| Min | 333.34 |
| Max | 9230.20 |
| Std Dev | 1163.53 |
| P50 | 6689.94 |
| P90 | 7273.81 |
| P95 | 7771.30 |
| P99 | 8293.86 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 420.25 |
| Min | 13.87 |
| Max | 383.99 |
| Std Dev | 24.62 |
| P50 | 19.13 |
| P90 | 20.73 |
| P95 | 30.60 |
| P99 | 124.33 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 6689.9ms (P50) | 27.59 | 19.13 | 383.99 | 156 |
| 6689.9-6807.4ms (P50-P75) | 19.08 | 18.80 | 19.13 | 78 |
| 6807.4-7273.8ms (P75-P90) | 18.02 | 17.60 | 18.80 | 46 |
| >= 7273.8ms (P90+) | 16.50 | 13.87 | 17.60 | 32 |

**Correlation:** -0.694 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 420.25 p/s | batch=128, conc=32 |
| Best Latency | 6454.44ms | batch=128, conc=32 |
| Avg Throughput | 420.25 p/s | all configs |
| Avg Latency | 6454.44ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| GPU Utilization (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| CPU Usage (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Tokenization (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Inference (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

Full time-series data is available in: `distribution/test_queue_size_timeseries.md`
