# Multi-Model Pool (2x MPS)

_Two MPS model instances with round-robin routing for parallel inference_

**Timestamp:** 2026-01-01 05:48:22

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=4, timeout=100.0ms)

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 4 | 13632 | 60.75 | 1133.1ms | 1190.9ms | 1637.7ms | 224.4 | 57.8 |

## Detailed Metrics

### Run 1

**Total:** 13632 pairs in 60.75s

### Latency

| Metric | Value |
|--------|-------|
| Average | 1133.07 |
| Min | 533.06 |
| Max | 1639.60 |
| Std Dev | 83.92 |
| P50 | 1118.65 |
| P90 | 1175.36 |
| P95 | 1190.87 |
| P99 | 1637.72 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 224.38 |
| Min | 39.03 |
| Max | 120.06 |
| Std Dev | 5.09 |
| P50 | 57.21 |
| P90 | 57.75 |
| P95 | 57.83 |
| P99 | 58.01 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 1118.6ms (P50) | 58.15 | 57.21 | 120.06 | 106 |
| 1118.6-1130.3ms (P50-P75) | 56.93 | 56.64 | 57.21 | 53 |
| 1130.3-1175.4ms (P75-P90) | 56.11 | 54.49 | 56.62 | 32 |
| >= 1175.4ms (P90+) | 51.09 | 39.03 | 54.44 | 22 |

**Correlation:** -0.870 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 224.38 p/s | batch=64, conc=4 |
| Best Latency | 1133.07ms | batch=64, conc=4 |
| Avg Throughput | 224.38 p/s | all configs |
| Avg Latency | 1133.07ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 3745.9 | 1058.4 | 5422.6 | 3642.6 | 5341.9 |
| GPU Utilization (%) | 74.7 | 0.0 | 100.0 | 82.1 | 100.0 |
| CPU Usage (%) | 11.8 | 0.3 | 45.9 | 10.7 | 38.1 |
| Tokenization (ms) | 55.5 | 0.0 | 159.0 | 39.9 | 98.5 |
| Inference (ms) | 184.5 | 0.0 | 508.1 | 124.7 | 372.9 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 46.7 | 0.0 | 74.9 | 46.8 | 57.6 |

### Stage Timing

| Stage | Percentage |
|-------|------------|
| Tokenization | 6.4% |
| Queue Wait | 0.0% |
| Model Inference | 20.7% |
| Other/gRPC | 0.0% |

### Worker Metrics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 185.5 | 372.9 | 0.0 | 13952 |

Full time-series data is available in: `distribution/10_multi_model_pool_timeseries.md`
