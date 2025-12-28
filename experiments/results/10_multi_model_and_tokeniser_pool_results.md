# Multi-Model Pool (2x MPS)

_Two MPS model instances with round-robin routing for parallel inference_

**Timestamp:** 2025-12-28 13:30:02

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 16 | 2 | 8000 | 9.49 | 37.7ms | 62.4ms | 70.9ms | 843.2 | 729.9 |
| 16 | 4 | 8000 | 7.09 | 56.6ms | 77.0ms | 99.0ms | 1127.6 | 365.7 |
| 32 | 2 | 16000 | 15.76 | 62.9ms | 95.3ms | 112.3ms | 1015.1 | 793.3 |
| 32 | 4 | 16000 | 13.42 | 107.0ms | 131.8ms | 160.5ms | 1192.4 | 369.5 |

## Detailed Metrics

### Config 1: batch=16, concurrency=2

**Total:** 8000 pairs in 9.49s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 37.71 |
| Min | 19.15 |
| Max | 85.86 |
| Std Dev | 13.88 |
| P50 | 32.48 |
| P90 | 58.36 |
| P95 | 62.36 |
| P99 | 70.89 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 843.19 |
| Min | 186.34 |
| Max | 835.49 |
| Std Dev | 155.73 |
| P50 | 492.59 |
| P90 | 685.97 |
| P95 | 729.93 |
| P99 | 807.38 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 32.5ms (P50) | 608.83 | 492.79 | 835.49 | 250 |
| 32.5-50.4ms (P50-P75) | 420.95 | 317.78 | 492.40 | 125 |
| 50.4-58.4ms (P75-P90) | 293.06 | 274.14 | 317.72 | 75 |
| >= 58.4ms (P90+) | 251.40 | 186.34 | 274.13 | 50 |

**Correlation:** -0.951 (negative correlation expected: lower latency = higher throughput)

### Config 2: batch=16, concurrency=4

**Total:** 8000 pairs in 7.09s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 56.59 |
| Min | 34.50 |
| Max | 117.94 |
| Std Dev | 10.57 |
| P50 | 55.14 |
| P90 | 64.98 |
| P95 | 76.99 |
| P99 | 99.03 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 1127.57 |
| Min | 135.66 |
| Max | 463.74 |
| Std Dev | 45.62 |
| P50 | 290.19 |
| P90 | 344.63 |
| P95 | 365.74 |
| P99 | 406.31 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 55.1ms (P50) | 324.02 | 290.19 | 463.74 | 250 |
| 55.1-60.0ms (P50-P75) | 278.82 | 266.78 | 290.19 | 125 |
| 60.0-65.0ms (P75-P90) | 258.45 | 246.24 | 266.76 | 75 |
| >= 65.0ms (P90+) | 203.43 | 135.66 | 246.09 | 50 |

**Correlation:** -0.947 (negative correlation expected: lower latency = higher throughput)

### Config 3: batch=32, concurrency=2

**Total:** 16000 pairs in 15.76s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 62.94 |
| Min | 34.31 |
| Max | 137.97 |
| Std Dev | 17.09 |
| P50 | 59.95 |
| P90 | 87.59 |
| P95 | 95.26 |
| P99 | 112.31 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 1015.07 |
| Min | 231.93 |
| Max | 932.76 |
| Std Dev | 137.84 |
| P50 | 533.81 |
| P90 | 733.31 |
| P95 | 793.34 |
| P99 | 862.92 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 59.9ms (P50) | 656.15 | 533.82 | 932.76 | 250 |
| 59.9-73.4ms (P50-P75) | 490.49 | 436.30 | 533.81 | 125 |
| 73.4-87.6ms (P75-P90) | 402.37 | 365.39 | 436.14 | 75 |
| >= 87.6ms (P90+) | 329.95 | 231.93 | 364.88 | 50 |

**Correlation:** -0.951 (negative correlation expected: lower latency = higher throughput)

### Config 4: batch=32, concurrency=4

**Total:** 16000 pairs in 13.42s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 106.99 |
| Min | 71.08 |
| Max | 195.97 |
| Std Dev | 15.01 |
| P50 | 104.92 |
| P90 | 124.86 |
| P95 | 131.82 |
| P99 | 160.51 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 1192.44 |
| Min | 163.29 |
| Max | 450.18 |
| Std Dev | 38.92 |
| P50 | 304.99 |
| P90 | 351.38 |
| P95 | 369.49 |
| P99 | 404.42 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 104.9ms (P50) | 333.71 | 305.00 | 450.18 | 250 |
| 104.9-113.1ms (P50-P75) | 294.35 | 282.98 | 304.99 | 125 |
| 113.1-124.9ms (P75-P90) | 271.97 | 256.32 | 282.69 | 75 |
| >= 124.9ms (P90+) | 231.55 | 163.29 | 255.98 | 50 |

**Correlation:** -0.972 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 1192.44 p/s | batch=32, conc=4 |
| Best Latency | 37.71ms | batch=16, conc=2 |
| Avg Throughput | 1044.57 p/s | all configs |
| Avg Latency | 66.06ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1191.7 | 1088.6 | 1294.8 | 1182.8 | 1294.8 |
| GPU Utilization (%) | 98.8 | 51.4 | 100.0 | 100.0 | 100.0 |
| CPU Usage (%) | 55.6 | 3.2 | 73.1 | 55.7 | 70.4 |
| Tokenization (ms) | 5.1 | 2.2 | 14.8 | 5.2 | 9.2 |
| Inference (ms) | 40.8 | 14.7 | 89.6 | 43.9 | 64.8 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 40.7 | 26.2 | 58.2 | 40.2 | 51.2 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 7.7% |
| Queue Wait | 0.0% |
| Model Inference | 62.1% |
| Other/gRPC | 0.0% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 1 | 65.9 | 115.1 | 500.3 | 24048 |
| 0 | 65.0 | 114.9 | 501.5 | 24032 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/10_multi_model_pool_timeseries.md`
