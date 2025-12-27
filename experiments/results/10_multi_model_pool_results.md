# Multi-Model Pool (2x MPS)

_Two MPS model instances with round-robin routing for parallel inference_

**Timestamp:** 2025-12-28 02:34:32

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 16 | 2 | 8000 | 11.73 | 46.7ms | 79.3ms | 93.3ms | 681.8 | 604.7 |
| 16 | 4 | 8000 | 10.91 | 87.0ms | 114.7ms | 135.4ms | 733.2 | 264.4 |
| 32 | 2 | 16000 | 24.96 | 99.7ms | 145.3ms | 172.3ms | 641.0 | 504.1 |
| 32 | 4 | 16000 | 26.27 | 209.6ms | 284.3ms | 318.7ms | 609.1 | 237.5 |

## Detailed Metrics

### Config 1: batch=16, concurrency=2

**Total:** 8000 pairs in 11.73s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 46.75 |
| Min | 21.40 |
| Max | 118.56 |
| Std Dev | 17.05 |
| P50 | 42.03 |
| P90 | 70.76 |
| P95 | 79.29 |
| P99 | 93.34 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 681.78 |
| Min | 134.96 |
| Max | 747.81 |
| Std Dev | 128.72 |
| P50 | 380.65 |
| P90 | 563.83 |
| P95 | 604.67 |
| P99 | 675.89 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 42.0ms (P50) | 493.75 | 381.00 | 747.81 | 250 |
| 42.0-57.9ms (P50-P75) | 326.97 | 276.53 | 380.30 | 125 |
| 57.9-70.8ms (P75-P90) | 251.16 | 226.19 | 275.60 | 75 |
| >= 70.8ms (P90+) | 197.81 | 134.96 | 225.38 | 50 |

**Correlation:** -0.933 (negative correlation expected: lower latency = higher throughput)

### Config 2: batch=16, concurrency=4

**Total:** 8000 pairs in 10.91s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 87.00 |
| Min | 47.47 |
| Max | 209.63 |
| Std Dev | 17.55 |
| P50 | 86.63 |
| P90 | 105.72 |
| P95 | 114.73 |
| P99 | 135.45 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 733.24 |
| Min | 76.32 |
| Max | 337.08 |
| Std Dev | 37.56 |
| P50 | 184.70 |
| P90 | 244.84 |
| P95 | 264.38 |
| P99 | 295.39 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 86.6ms (P50) | 219.49 | 184.88 | 337.08 | 250 |
| 86.6-97.1ms (P50-P75) | 175.65 | 164.75 | 184.52 | 125 |
| 97.1-105.7ms (P75-P90) | 158.87 | 151.36 | 164.63 | 75 |
| >= 105.7ms (P90+) | 135.62 | 76.32 | 151.24 | 50 |

**Correlation:** -0.941 (negative correlation expected: lower latency = higher throughput)

### Config 3: batch=32, concurrency=2

**Total:** 16000 pairs in 24.96s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 99.71 |
| Min | 39.88 |
| Max | 311.12 |
| Std Dev | 27.04 |
| P50 | 97.10 |
| P90 | 132.58 |
| P95 | 145.29 |
| P99 | 172.27 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 641.02 |
| Min | 102.85 |
| Max | 802.32 |
| Std Dev | 90.24 |
| P50 | 329.56 |
| P90 | 464.05 |
| P95 | 504.11 |
| P99 | 613.94 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 97.1ms (P50) | 409.50 | 329.60 | 802.32 | 250 |
| 97.1-112.4ms (P50-P75) | 309.54 | 284.66 | 329.52 | 125 |
| 112.4-132.6ms (P75-P90) | 264.67 | 241.47 | 284.44 | 75 |
| >= 132.6ms (P90+) | 211.81 | 102.85 | 240.50 | 50 |

**Correlation:** -0.902 (negative correlation expected: lower latency = higher throughput)

### Config 4: batch=32, concurrency=4

**Total:** 16000 pairs in 26.27s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 209.57 |
| Min | 95.09 |
| Max | 368.36 |
| Std Dev | 43.04 |
| P50 | 208.33 |
| P90 | 260.33 |
| P95 | 284.28 |
| P99 | 318.74 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 609.14 |
| Min | 86.87 |
| Max | 336.53 |
| Std Dev | 36.72 |
| P50 | 153.60 |
| P90 | 201.33 |
| P95 | 237.47 |
| P99 | 271.83 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 208.3ms (P50) | 185.92 | 153.65 | 336.53 | 250 |
| 208.3-232.7ms (P50-P75) | 144.53 | 137.54 | 153.55 | 125 |
| 232.7-260.3ms (P75-P90) | 131.11 | 122.94 | 137.53 | 75 |
| >= 260.3ms (P90+) | 110.57 | 86.87 | 122.75 | 50 |

**Correlation:** -0.944 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 733.24 p/s | batch=16, conc=4 |
| Best Latency | 46.75ms | batch=16, conc=2 |
| Avg Throughput | 666.29 p/s | all configs |
| Avg Latency | 110.75ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1196.9 | 1076.6 | 1298.8 | 1186.8 | 1254.8 |
| GPU Utilization (%) | 98.7 | 23.8 | 100.0 | 100.0 | 100.0 |
| CPU Usage (%) | 2.6 | 0.8 | 5.4 | 2.4 | 3.8 |
| Tokenization (ms) | 12.1 | 5.6 | 26.2 | 12.9 | 21.8 |
| Inference (ms) | 69.5 | 16.8 | 188.7 | 72.9 | 123.7 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 39.9 | 25.6 | 57.0 | 40.0 | 50.4 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 10.5% |
| Queue Wait | 0.0% |
| Model Inference | 55.6% |
| Other/gRPC | 0.5% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 1 | 109.4 | 235.6 | 316.7 | 24128 |
| 0 | 110.1 | 236.6 | 314.9 | 23952 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/10_multi_model_pool_timeseries.md`
