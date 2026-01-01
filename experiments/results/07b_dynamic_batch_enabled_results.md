# 07b_dynamic_batch_enabled

_Dynamic batching enabled with max_batch=96, timeout=50ms_

**Timestamp:** 2026-01-01 21:16:08

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=96, timeout=50.0ms)

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 70.35 | 556.6ms | 578.8ms | 596.0ms | 227.4 | 58.4 |

## Detailed Metrics

### Run 1

**Total:** 16000 pairs in 70.35s

### Latency

| Metric | Value |
|--------|-------|
| Average | 556.59 |
| Min | 57.92 |
| Max | 2026.06 |
| Std Dev | 112.01 |
| P50 | 560.80 |
| P90 | 574.71 |
| P95 | 578.84 |
| P99 | 595.97 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 227.44 |
| Min | 15.79 |
| Max | 552.50 |
| Std Dev | 65.11 |
| P50 | 57.06 |
| P90 | 58.13 |
| P95 | 58.36 |
| P99 | 506.73 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 560.8ms (P50) | 77.74 | 57.07 | 552.50 | 250 |
| 560.8-568.6ms (P50-P75) | 56.72 | 56.28 | 57.05 | 125 |
| 568.6-574.7ms (P75-P90) | 55.97 | 55.68 | 56.27 | 75 |
| >= 574.7ms (P90+) | 53.07 | 15.79 | 55.68 | 50 |

**Correlation:** -0.707 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 227.44 p/s | batch=32, conc=4 |
| Best Latency | 556.59ms | batch=32, conc=4 |
| Avg Throughput | 227.44 p/s | all configs |
| Avg Latency | 556.59ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1219.1 | 1058.4 | 1324.6 | 1214.6 | 1324.6 |
| GPU Utilization (%) | 26.8 | 0.0 | 41.8 | 28.4 | 38.9 |
| CPU Usage (%) | 10.8 | 0.5 | 32.1 | 8.4 | 26.9 |
| Tokenization (ms) | 11.9 | 0.0 | 23.0 | 11.1 | 18.8 |
| Inference (ms) | 37.7 | 0.0 | 114.6 | 32.5 | 63.6 |
| Queue Wait (ms) | 12.0 | 0.0 | 23.5 | 11.3 | 19.0 |
| Padding Waste (%) | 41.0 | 0.0 | 55.1 | 41.1 | 52.3 |

### Stage Timing

| Stage | Percentage |
|-------|------------|
| Tokenization | 2.3% |
| Queue Wait | 2.4% |
| Model Inference | 7.0% |
| Other/gRPC | 0.0% |

### Worker Metrics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 39.1 | 65.8 | 0.0 | 16160 |

Full time-series data is available in: `distribution/07b_dynamic_batch_enabled_timeseries.md`
