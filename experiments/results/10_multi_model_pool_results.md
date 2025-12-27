# Multi-Model Pool (2x MPS)

_Two MPS model instances with round-robin routing for parallel inference_

**Timestamp:** 2025-12-28 03:55:14

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 16 | 2 | 8000 | 12.44 | 49.6ms | 84.3ms | 96.9ms | 643.0 | 547.7 |
| 16 | 4 | 6880 | 10.02 | 86.9ms | 120.6ms | 136.9ms | 686.8 | 255.6 |

## Detailed Metrics

### Config 1: batch=16, concurrency=2

**Total:** 8000 pairs in 12.44s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 49.65 |
| Min | 25.67 |
| Max | 141.32 |
| Std Dev | 19.29 |
| P50 | 42.44 |
| P90 | 78.23 |
| P95 | 84.29 |
| P99 | 96.90 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 643.01 |
| Min | 113.22 |
| Max | 623.28 |
| Std Dev | 120.41 |
| P50 | 377.04 |
| P90 | 521.14 |
| P95 | 547.65 |
| P99 | 598.13 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 42.4ms (P50) | 470.96 | 377.12 | 623.28 | 250 |
| 42.4-63.5ms (P50-P75) | 312.40 | 252.10 | 376.95 | 125 |
| 63.5-78.2ms (P75-P90) | 228.07 | 204.63 | 251.68 | 75 |
| >= 78.2ms (P90+) | 184.23 | 113.22 | 203.67 | 50 |

**Correlation:** -0.939 (negative correlation expected: lower latency = higher throughput)

### Config 2: batch=16, concurrency=4

**Total:** 6880 pairs in 10.02s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 86.93 |
| Min | 46.71 |
| Max | 162.17 |
| Std Dev | 17.91 |
| P50 | 85.08 |
| P90 | 110.03 |
| P95 | 120.65 |
| P99 | 136.87 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 686.80 |
| Min | 98.66 |
| Max | 342.56 |
| Std Dev | 39.30 |
| P50 | 188.06 |
| P90 | 241.23 |
| P95 | 255.64 |
| P99 | 306.25 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 85.1ms (P50) | 222.05 | 188.16 | 342.56 | 215 |
| 85.1-96.4ms (P50-P75) | 176.74 | 166.07 | 187.96 | 107 |
| 96.4-110.0ms (P75-P90) | 157.19 | 145.45 | 165.99 | 65 |
| >= 110.0ms (P90+) | 130.13 | 98.66 | 145.14 | 43 |

**Correlation:** -0.955 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 686.80 p/s | batch=16, conc=4 |
| Best Latency | 49.65ms | batch=16, conc=2 |
| Avg Throughput | 664.90 p/s | all configs |
| Avg Latency | 68.29ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| GPU Utilization (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| CPU Usage (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Tokenization (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Inference (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/10_multi_model_pool_timeseries.md`
