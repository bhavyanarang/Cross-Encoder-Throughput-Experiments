# Multi-Model Pool (2x MPS) + Batching

_Two MPS model instances with round-robin routing and dynamic batching enabled_

**Timestamp:** 2026-01-01 22:35:25

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=8, timeout=100.0ms)

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 8 | 32000 | 52.68 | 795.3ms | 1222.2ms | 1676.9ms | 607.5 | 90.4 |

## Detailed Metrics

### Run 1

**Total:** 32000 pairs in 52.68s

### Latency

| Metric | Value |
|--------|-------|
| Average | 795.30 |
| Min | 148.44 |
| Max | 3557.05 |
| Std Dev | 265.09 |
| P50 | 718.06 |
| P90 | 1212.96 |
| P95 | 1222.18 |
| P99 | 1676.91 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 607.48 |
| Min | 17.99 |
| Max | 431.16 |
| Std Dev | 29.15 |
| P50 | 89.13 |
| P90 | 90.20 |
| P95 | 90.44 |
| P99 | 284.16 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 718.1ms (P50) | 95.26 | 89.13 | 431.16 | 250 |
| 718.1-729.4ms (P50-P75) | 88.54 | 87.75 | 89.13 | 125 |
| 729.4-1213.0ms (P75-P90) | 78.30 | 52.77 | 87.74 | 75 |
| >= 1213.0ms (P90+) | 49.10 | 17.99 | 52.70 | 50 |

**Correlation:** -0.612 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 607.48 p/s | batch=64, conc=8 |
| Best Latency | 795.30ms | batch=64, conc=8 |
| Avg Throughput | 607.48 p/s | all configs |
| Avg Latency | 795.30ms | all configs |

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

Full time-series data is available in: `distribution/10a_multi_model_pool_batching_timeseries.md`
