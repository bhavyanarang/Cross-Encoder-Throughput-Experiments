# Multi-Model Pool (2x MPS) + Batching

_Two MPS model instances with round-robin routing and dynamic batching enabled_

**Timestamp:** 2026-01-01 22:37:28

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=32, timeout=100.0ms)

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 32 | 32000 | 61.39 | 3426.1ms | 5310.1ms | 13794.2ms | 521.2 | 25.5 |

## Detailed Metrics

### Run 1

**Total:** 32000 pairs in 61.39s

### Latency

| Metric | Value |
|--------|-------|
| Average | 3426.06 |
| Min | 107.23 |
| Max | 15673.17 |
| Std Dev | 1884.83 |
| P50 | 2962.42 |
| P90 | 3540.38 |
| P95 | 5310.14 |
| P99 | 13794.15 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 521.24 |
| Min | 4.08 |
| Max | 596.82 |
| Std Dev | 32.23 |
| P50 | 21.60 |
| P90 | 22.28 |
| P95 | 25.50 |
| P99 | 66.47 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 2962.4ms (P50) | 29.53 | 21.60 | 596.82 | 250 |
| 2962.4-3402.0ms (P50-P75) | 19.61 | 18.81 | 21.60 | 125 |
| 3402.0-3540.4ms (P75-P90) | 18.46 | 18.08 | 18.81 | 75 |
| >= 3540.4ms (P90+) | 11.80 | 4.08 | 18.07 | 50 |

**Correlation:** -0.279 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 521.24 p/s | batch=64, conc=32 |
| Best Latency | 3426.06ms | batch=64, conc=32 |
| Avg Throughput | 521.24 p/s | all configs |
| Avg Latency | 3426.06ms | all configs |

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

Full time-series data is available in: `distribution/10a_multi_model_pool_batching_tokenizer_pool_2_timeseries.md`
