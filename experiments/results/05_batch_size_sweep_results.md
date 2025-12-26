# 05_batch_size_sweep_mlx

_Sweep batch sizes on MPS and MLX backends_

**Timestamp:** 2025-12-26 16:13:13

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 4000 | 14.53 | 29.0ms | 55.9ms | 63.5ms | 275.2 | 471.5 |

## Detailed Metrics

### Config 1: batch=8, concurrency=1

**Total:** 4000 pairs in 14.53s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 28.98 |
| Min | 13.29 |
| Max | 65.44 |
| Std Dev | 12.58 |
| P50 | 24.06 |
| P90 | 50.97 |
| P95 | 55.92 |
| P99 | 63.50 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 275.20 |
| Min | 122.25 |
| Max | 602.03 |
| Std Dev | 105.80 |
| P50 | 332.55 |
| P90 | 446.66 |
| P95 | 471.45 |
| P99 | 524.38 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 24.1ms (P50) | 405.85 | 332.66 | 602.03 | 250 |
| 24.1-31.6ms (P50-P75) | 293.35 | 253.86 | 332.44 | 125 |
| 31.6-51.0ms (P75-P90) | 190.45 | 156.95 | 252.25 | 75 |
| >= 51.0ms (P90+) | 142.26 | 122.25 | 156.92 | 50 |

**Correlation:** -0.936 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 275.20 p/s | batch=8, conc=1 |
| Best Latency | 28.98ms | batch=8, conc=1 |
| Avg Throughput | 275.20 p/s | all configs |
| Avg Latency | 28.98ms | all configs |


---

# 05_batch_size_sweep_mlx

_Sweep batch sizes on MPS and MLX backends_

**Timestamp:** 2025-12-26 16:13:13

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 16 | 1 | 8000 | 18.67 | 37.3ms | 70.5ms | 85.7ms | 428.6 | 675.3 |

## Detailed Metrics

### Config 1: batch=16, concurrency=1

**Total:** 8000 pairs in 18.67s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 37.29 |
| Min | 21.03 |
| Max | 116.21 |
| Std Dev | 16.16 |
| P50 | 31.21 |
| P90 | 63.60 |
| P95 | 70.49 |
| P99 | 85.71 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 428.57 |
| Min | 137.68 |
| Max | 760.64 |
| Std Dev | 142.79 |
| P50 | 512.73 |
| P90 | 649.84 |
| P95 | 675.32 |
| P99 | 735.72 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 31.2ms (P50) | 599.52 | 512.76 | 760.64 | 250 |
| 31.2-38.3ms (P50-P75) | 472.66 | 418.40 | 512.71 | 125 |
| 38.3-63.6ms (P75-P90) | 315.72 | 251.66 | 415.98 | 75 |
| >= 63.6ms (P90+) | 216.41 | 137.68 | 250.81 | 50 |

**Correlation:** -0.934 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 428.57 p/s | batch=16, conc=1 |
| Best Latency | 37.29ms | batch=16, conc=1 |
| Avg Throughput | 428.57 p/s | all configs |
| Avg Latency | 37.29ms | all configs |


---

# 05_batch_size_sweep_mlx

_Sweep batch sizes on MPS and MLX backends_

**Timestamp:** 2025-12-26 16:13:13

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 16000 | 26.03 | 52.0ms | 87.3ms | 106.1ms | 614.7 | 811.8 |

## Detailed Metrics

### Config 1: batch=32, concurrency=1

**Total:** 16000 pairs in 26.03s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 52.00 |
| Min | 33.74 |
| Max | 149.40 |
| Std Dev | 17.17 |
| P50 | 44.82 |
| P90 | 80.72 |
| P95 | 87.34 |
| P99 | 106.10 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 614.67 |
| Min | 214.19 |
| Max | 948.53 |
| Std Dev | 146.61 |
| P50 | 713.98 |
| P90 | 799.09 |
| P95 | 811.83 |
| P99 | 850.05 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 44.8ms (P50) | 766.22 | 713.98 | 948.53 | 250 |
| 44.8-51.0ms (P50-P75) | 677.76 | 627.76 | 713.97 | 125 |
| 51.0-80.7ms (P75-P90) | 496.33 | 396.47 | 626.25 | 75 |
| >= 80.7ms (P90+) | 350.73 | 214.19 | 395.95 | 50 |

**Correlation:** -0.964 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 614.67 p/s | batch=32, conc=1 |
| Best Latency | 52.00ms | batch=32, conc=1 |
| Avg Throughput | 614.67 p/s | all configs |
| Avg Latency | 52.00ms | all configs |


---

# 05_batch_size_sweep_mlx

_Sweep batch sizes on MPS and MLX backends_

**Timestamp:** 2025-12-26 16:13:13

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 48 | 1 | 24000 | 35.70 | 71.3ms | 112.3ms | 126.6ms | 672.3 | 861.5 |

## Detailed Metrics

### Config 1: batch=48, concurrency=1

**Total:** 24000 pairs in 35.70s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 71.32 |
| Min | 51.13 |
| Max | 174.80 |
| Std Dev | 18.28 |
| P50 | 64.00 |
| P90 | 103.37 |
| P95 | 112.34 |
| P99 | 126.56 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 672.31 |
| Min | 274.60 |
| Max | 938.82 |
| Std Dev | 134.24 |
| P50 | 750.03 |
| P90 | 836.57 |
| P95 | 861.54 |
| P99 | 906.07 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 64.0ms (P50) | 805.44 | 750.46 | 938.82 | 250 |
| 64.0-71.9ms (P50-P75) | 709.02 | 667.85 | 749.59 | 125 |
| 71.9-103.4ms (P75-P90) | 563.83 | 464.40 | 665.06 | 75 |
| >= 103.4ms (P90+) | 419.80 | 274.60 | 464.01 | 50 |

**Correlation:** -0.973 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 672.31 p/s | batch=48, conc=1 |
| Best Latency | 71.32ms | batch=48, conc=1 |
| Avg Throughput | 672.31 p/s | all configs |
| Avg Latency | 71.32ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1190.1 | 1080.6 | 1381.0 | 1176.9 | 1343.8 |
| GPU Utilization (%) | 74.4 | 33.6 | 86.1 | 74.8 | 84.1 |
| CPU Usage (%) | 1.6 | 0.5 | 2.5 | 1.6 | 2.3 |
| Tokenization (ms) | 11.7 | 3.0 | 43.8 | 11.6 | 18.5 |
| Inference (ms) | 41.1 | 13.3 | 109.8 | 40.0 | 81.5 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 40.0 | 12.8 | 57.0 | 40.6 | 51.5 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 21.4% |
| Queue Wait | 0.0% |
| Model Inference | 77.1% |
| Other/gRPC | 1.6% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 46.6 | 91.0 | 536.1 | 52040 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/05_batch_size_sweep_timeseries.md`
