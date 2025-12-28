# Multi-Model Pool (2x MPS)

_Two MPS model instances with round-robin routing for parallel inference_

**Timestamp:** 2025-12-28 04:06:51

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 16 | 2 | 8000 | 12.52 | 49.2ms | 83.6ms | 107.1ms | 638.8 | 623.1 |
| 16 | 4 | 8000 | 10.04 | 80.1ms | 107.9ms | 126.0ms | 796.7 | 300.6 |
| 32 | 2 | 3136 | 5.73 | 96.4ms | 136.6ms | 163.9ms | 547.1 | 687.6 |

## Detailed Metrics

### Config 1: batch=16, concurrency=2

**Total:** 8000 pairs in 12.52s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 49.22 |
| Min | 20.94 |
| Max | 184.57 |
| Std Dev | 20.18 |
| P50 | 44.83 |
| P90 | 73.02 |
| P95 | 83.60 |
| P99 | 107.12 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 638.79 |
| Min | 86.69 |
| Max | 764.19 |
| Std Dev | 130.12 |
| P50 | 356.88 |
| P90 | 559.51 |
| P95 | 623.10 |
| P99 | 692.60 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 44.8ms (P50) | 476.57 | 357.11 | 764.19 | 250 |
| 44.8-59.2ms (P50-P75) | 313.28 | 270.36 | 356.64 | 125 |
| 59.2-73.0ms (P75-P90) | 245.49 | 219.16 | 269.21 | 75 |
| >= 73.0ms (P90+) | 181.81 | 86.69 | 218.79 | 50 |

**Correlation:** -0.872 (negative correlation expected: lower latency = higher throughput)

### Config 2: batch=16, concurrency=4

**Total:** 8000 pairs in 10.04s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 80.07 |
| Min | 38.21 |
| Max | 188.40 |
| Std Dev | 16.29 |
| P50 | 79.90 |
| P90 | 97.63 |
| P95 | 107.85 |
| P99 | 125.99 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 796.67 |
| Min | 84.92 |
| Max | 418.73 |
| Std Dev | 44.19 |
| P50 | 200.24 |
| P90 | 270.81 |
| P95 | 300.63 |
| P99 | 341.37 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 79.9ms (P50) | 239.28 | 200.39 | 418.73 | 250 |
| 79.9-87.5ms (P50-P75) | 192.14 | 182.81 | 200.10 | 125 |
| 87.5-97.6ms (P75-P90) | 173.97 | 163.90 | 182.63 | 75 |
| >= 97.6ms (P90+) | 144.64 | 84.92 | 163.79 | 50 |

**Correlation:** -0.935 (negative correlation expected: lower latency = higher throughput)

### Config 3: batch=32, concurrency=2

**Total:** 3136 pairs in 5.73s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 96.37 |
| Min | 37.51 |
| Max | 197.36 |
| Std Dev | 27.16 |
| P50 | 96.00 |
| P90 | 128.34 |
| P95 | 136.63 |
| P99 | 163.89 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 547.10 |
| Min | 162.14 |
| Max | 853.08 |
| Std Dev | 128.48 |
| P50 | 333.32 |
| P90 | 521.49 |
| P95 | 687.60 |
| P99 | 817.56 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 96.0ms (P50) | 447.91 | 333.92 | 853.08 | 49 |
| 96.0-112.2ms (P50-P75) | 313.56 | 285.41 | 332.73 | 24 |
| 112.2-128.3ms (P75-P90) | 267.71 | 249.56 | 285.00 | 15 |
| >= 128.3ms (P90+) | 222.38 | 162.14 | 248.82 | 10 |

**Correlation:** -0.894 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 796.67 p/s | batch=16, conc=4 |
| Best Latency | 49.22ms | batch=16, conc=2 |
| Avg Throughput | 660.85 p/s | all configs |
| Avg Latency | 75.22ms | all configs |

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
