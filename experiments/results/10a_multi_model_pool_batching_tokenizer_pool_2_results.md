# Multi-Model Pool (2x MPS) + Batching

_Two MPS model instances with round-robin routing and dynamic batching enabled_

**Timestamp:** 2026-01-02 00:36:32

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=32, timeout=100.0ms)

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 32 | 243392 | 75.64 | 570.6ms | 669.2ms | 792.6ms | 3218.0 | 444.7 |

## Detailed Metrics

### Run 1

**Total:** 243392 pairs in 75.64s

### Latency

| Metric | Value |
|--------|-------|
| Average | 570.58 |
| Min | 65.35 |
| Max | 15640.64 |
| Std Dev | 863.53 |
| P50 | 651.31 |
| P90 | 664.92 |
| P95 | 669.21 |
| P99 | 792.58 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 3217.96 |
| Min | 4.09 |
| Max | 979.35 |
| Std Dev | 152.01 |
| P50 | 98.26 |
| P90 | 437.54 |
| P95 | 444.66 |
| P99 | 457.84 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 651.3ms (P50) | 294.97 | 98.26 | 979.35 | 1901 |
| 651.3-657.3ms (P50-P75) | 97.78 | 97.36 | 98.26 | 951 |
| 657.3-664.9ms (P75-P90) | 96.94 | 96.26 | 97.36 | 570 |
| >= 664.9ms (P90+) | 86.95 | 4.09 | 96.25 | 381 |

**Correlation:** -0.361 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 3217.96 p/s | batch=64, conc=32 |
| Best Latency | 570.58ms | batch=64, conc=32 |
| Avg Throughput | 3217.96 p/s | all configs |
| Avg Latency | 570.58ms | all configs |

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
