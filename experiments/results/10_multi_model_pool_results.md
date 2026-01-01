# Multi-Model Pool (2x MPS)

_Two MPS model instances with round-robin routing for parallel inference_

**Timestamp:** 2026-01-01 20:04:10

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 128 | 4 | 37760 | 61.56 | 824.1ms | 1222.2ms | 1246.5ms | 613.4 | 183.0 |

## Detailed Metrics

### Run 1

**Total:** 37760 pairs in 61.56s

### Latency

| Metric | Value |
|--------|-------|
| Average | 824.10 |
| Min | 201.17 |
| Max | 1566.25 |
| Std Dev | 225.48 |
| P50 | 709.02 |
| P90 | 1214.77 |
| P95 | 1222.19 |
| P99 | 1246.48 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 613.37 |
| Min | 81.72 |
| Max | 636.27 |
| Std Dev | 56.23 |
| P50 | 180.53 |
| P90 | 182.55 |
| P95 | 182.98 |
| P99 | 209.72 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 709.0ms (P50) | 190.81 | 180.57 | 636.27 | 147 |
| 709.0-758.3ms (P50-P75) | 178.60 | 169.90 | 180.53 | 74 |
| 758.3-1214.8ms (P75-P90) | 112.57 | 105.38 | 167.70 | 44 |
| >= 1214.8ms (P90+) | 103.72 | 81.72 | 105.37 | 30 |

**Correlation:** -0.774 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 613.37 p/s | batch=128, conc=4 |
| Best Latency | 824.10ms | batch=128, conc=4 |
| Avg Throughput | 613.37 p/s | all configs |
| Avg Latency | 824.10ms | all configs |

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

Full time-series data is available in: `distribution/10_multi_model_pool_timeseries.md`
