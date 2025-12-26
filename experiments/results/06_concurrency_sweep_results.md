# 06_concurrency_sweep_mlx

_Sweep concurrency levels on MPS and MLX backends_

**Timestamp:** 2025-12-26 16:16:17

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 16000 | 25.63 | 51.2ms | 81.0ms | 99.3ms | 624.2 | 810.3 |

## Detailed Metrics

### Config 1: batch=32, concurrency=1

**Total:** 16000 pairs in 25.63s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 51.16 |
| Min | 35.97 |
| Max | 159.87 |
| Std Dev | 15.14 |
| P50 | 45.25 |
| P90 | 74.10 |
| P95 | 81.04 |
| P99 | 99.29 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 624.20 |
| Min | 200.16 |
| Max | 889.63 |
| Std Dev | 136.34 |
| P50 | 707.26 |
| P90 | 793.25 |
| P95 | 810.26 |
| P99 | 860.51 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 45.2ms (P50) | 764.04 | 707.28 | 889.63 | 250 |
| 45.2-51.5ms (P50-P75) | 671.59 | 621.98 | 707.23 | 125 |
| 51.5-74.1ms (P75-P90) | 509.02 | 432.61 | 621.60 | 75 |
| >= 74.1ms (P90+) | 377.23 | 200.16 | 425.28 | 50 |

**Correlation:** -0.956 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 624.20 p/s | batch=32, conc=1 |
| Best Latency | 51.16ms | batch=32, conc=1 |
| Avg Throughput | 624.20 p/s | all configs |
| Avg Latency | 51.16ms | all configs |


---

# 06_concurrency_sweep_mlx

_Sweep concurrency levels on MPS and MLX backends_

**Timestamp:** 2025-12-26 16:16:17

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 2 | 16000 | 22.43 | 89.6ms | 102.5ms | 135.8ms | 713.4 | 406.4 |

## Detailed Metrics

### Config 1: batch=32, concurrency=2

**Total:** 16000 pairs in 22.43s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 89.58 |
| Min | 64.20 |
| Max | 181.21 |
| Std Dev | 10.34 |
| P50 | 87.73 |
| P90 | 98.26 |
| P95 | 102.54 |
| P99 | 135.84 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 713.41 |
| Min | 176.59 |
| Max | 498.47 |
| Std Dev | 32.98 |
| P50 | 364.74 |
| P90 | 394.27 |
| P95 | 406.37 |
| P99 | 423.23 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 87.7ms (P50) | 385.00 | 364.82 | 498.47 | 250 |
| 87.7-93.3ms (P50-P75) | 353.85 | 343.11 | 364.67 | 125 |
| 93.3-98.3ms (P75-P90) | 334.90 | 325.73 | 342.84 | 75 |
| >= 98.3ms (P90+) | 296.93 | 176.59 | 325.08 | 50 |

**Correlation:** -0.959 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 713.41 p/s | batch=32, conc=2 |
| Best Latency | 89.58ms | batch=32, conc=2 |
| Avg Throughput | 713.41 p/s | all configs |
| Avg Latency | 89.58ms | all configs |


---

# 06_concurrency_sweep_mlx

_Sweep concurrency levels on MPS and MLX backends_

**Timestamp:** 2025-12-26 16:16:17

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 3 | 16000 | 22.43 | 134.3ms | 153.1ms | 190.4ms | 713.2 | 264.9 |

## Detailed Metrics

### Config 1: batch=32, concurrency=3

**Total:** 16000 pairs in 22.43s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 134.27 |
| Min | 62.82 |
| Max | 229.45 |
| Std Dev | 14.04 |
| P50 | 132.11 |
| P90 | 146.02 |
| P95 | 153.08 |
| P99 | 190.42 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 713.21 |
| Min | 139.46 |
| Max | 509.43 |
| Std Dev | 23.25 |
| P50 | 242.23 |
| P90 | 261.33 |
| P95 | 264.92 |
| P99 | 273.61 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 132.1ms (P50) | 255.22 | 242.25 | 509.43 | 250 |
| 132.1-138.7ms (P50-P75) | 237.01 | 230.64 | 242.21 | 125 |
| 138.7-146.0ms (P75-P90) | 225.54 | 219.19 | 230.60 | 75 |
| >= 146.0ms (P90+) | 198.97 | 139.46 | 218.80 | 50 |

**Correlation:** -0.931 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 713.21 p/s | batch=32, conc=3 |
| Best Latency | 134.27ms | batch=32, conc=3 |
| Avg Throughput | 713.21 p/s | all configs |
| Avg Latency | 134.27ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1360.8 | 1110.6 | 1380.8 | 1380.8 | 1380.8 |
| GPU Utilization (%) | 70.8 | 29.9 | 84.8 | 71.5 | 76.3 |
| CPU Usage (%) | 1.8 | 0.7 | 2.4 | 1.8 | 2.2 |
| Tokenization (ms) | 12.2 | 10.2 | 31.6 | 12.0 | 13.7 |
| Inference (ms) | 35.0 | 23.4 | 77.6 | 31.2 | 60.3 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 41.5 | 25.6 | 58.0 | 40.8 | 52.4 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 13.5% |
| Queue Wait | 0.0% |
| Model Inference | 37.3% |
| Other/gRPC | 49.2% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 90.7 | 142.3 | 667.0 | 48160 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/06_concurrency_sweep_timeseries.md`
