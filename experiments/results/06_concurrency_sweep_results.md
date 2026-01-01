# 06_concurrency_sweep_mlx

_Sweep concurrency levels on MPS and MLX backends_

**Timestamp:** 2026-01-01 21:12:40

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 3616 | 60.15 | 531.5ms | 539.5ms | 541.1ms | 60.1 | 61.3 |

## Detailed Metrics

### Run 1

**Total:** 3616 pairs in 60.15s

### Latency

| Metric | Value |
|--------|-------|
| Average | 531.46 |
| Min | 512.92 |
| Max | 544.04 |
| Std Dev | 5.65 |
| P50 | 531.25 |
| P90 | 538.55 |
| P95 | 539.55 |
| P99 | 541.11 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 60.12 |
| Min | 58.82 |
| Max | 62.39 |
| Std Dev | 0.64 |
| P50 | 60.24 |
| P90 | 61.13 |
| P95 | 61.28 |
| P99 | 61.89 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 531.3ms (P50) | 60.73 | 60.24 | 62.39 | 56 |
| 531.3-536.4ms (P50-P75) | 60.01 | 59.68 | 60.24 | 28 |
| 536.4-538.6ms (P75-P90) | 59.54 | 59.42 | 59.66 | 17 |
| >= 538.6ms (P90+) | 59.27 | 58.82 | 59.42 | 12 |

**Correlation:** -1.000 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 60.12 p/s | batch=32, conc=1 |
| Best Latency | 531.46ms | batch=32, conc=1 |
| Avg Throughput | 60.12 p/s | all configs |
| Avg Latency | 531.46ms | all configs |


---

# 06_concurrency_sweep_mlx

_Sweep concurrency levels on MPS and MLX backends_

**Timestamp:** 2026-01-01 21:12:40

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 2 | 16000 | 137.13 | 547.4ms | 556.0ms | 557.9ms | 116.7 | 59.7 |

## Detailed Metrics

### Run 1

**Total:** 16000 pairs in 137.13s

### Latency

| Metric | Value |
|--------|-------|
| Average | 547.39 |
| Min | 528.79 |
| Max | 1037.29 |
| Std Dev | 22.84 |
| P50 | 546.20 |
| P90 | 554.83 |
| P95 | 556.01 |
| P99 | 557.93 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 116.68 |
| Min | 30.85 |
| Max | 60.51 |
| Std Dev | 1.41 |
| P50 | 58.59 |
| P90 | 59.45 |
| P95 | 59.72 |
| P99 | 60.11 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 546.2ms (P50) | 59.14 | 58.59 | 60.51 | 250 |
| 546.2-551.5ms (P50-P75) | 58.30 | 58.03 | 58.58 | 125 |
| 551.5-554.8ms (P75-P90) | 57.84 | 57.68 | 58.02 | 75 |
| >= 554.8ms (P90+) | 56.97 | 30.85 | 57.68 | 50 |

**Correlation:** -0.975 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 116.68 p/s | batch=32, conc=2 |
| Best Latency | 547.39ms | batch=32, conc=2 |
| Avg Throughput | 116.68 p/s | all configs |
| Avg Latency | 547.39ms | all configs |


---

# 06_concurrency_sweep_mlx

_Sweep concurrency levels on MPS and MLX backends_

**Timestamp:** 2026-01-01 21:12:40

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 3 | 16000 | 93.97 | 560.6ms | 571.2ms | 577.2ms | 170.3 | 58.7 |

## Detailed Metrics

### Run 1

**Total:** 16000 pairs in 93.97s

### Latency

| Metric | Value |
|--------|-------|
| Average | 560.65 |
| Min | 536.24 |
| Max | 1039.69 |
| Std Dev | 23.47 |
| P50 | 559.88 |
| P90 | 569.53 |
| P95 | 571.24 |
| P99 | 577.19 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 170.27 |
| Min | 30.78 |
| Max | 59.67 |
| Std Dev | 1.52 |
| P50 | 57.15 |
| P90 | 58.46 |
| P95 | 58.72 |
| P99 | 59.14 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 559.9ms (P50) | 57.93 | 57.16 | 59.67 | 250 |
| 559.9-566.3ms (P50-P75) | 56.81 | 56.50 | 57.15 | 125 |
| 566.3-569.5ms (P75-P90) | 56.34 | 56.19 | 56.50 | 75 |
| >= 569.5ms (P90+) | 55.22 | 30.78 | 56.19 | 50 |

**Correlation:** -0.965 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 170.27 p/s | batch=32, conc=3 |
| Best Latency | 560.65ms | batch=32, conc=3 |
| Avg Throughput | 170.27 p/s | all configs |
| Avg Latency | 560.65ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1155.4 | 1154.6 | 1158.6 | 1154.8 | 1157.6 |
| GPU Utilization (%) | 14.9 | 3.3 | 23.5 | 14.9 | 23.2 |
| CPU Usage (%) | 7.0 | 3.8 | 9.4 | 7.3 | 9.2 |
| Tokenization (ms) | 12.8 | 10.3 | 16.0 | 12.7 | 15.4 |
| Inference (ms) | 35.6 | 27.8 | 42.9 | 34.7 | 42.5 |
| Queue Wait (ms) | 12.9 | 10.6 | 16.1 | 12.8 | 15.5 |
| Padding Waste (%) | 42.3 | 35.7 | 46.7 | 43.6 | 46.6 |

### Stage Timing

| Stage | Percentage |
|-------|------------|
| Tokenization | 2.9% |
| Queue Wait | 3.0% |
| Model Inference | 7.1% |
| Other/gRPC | 0.0% |

### Worker Metrics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 39.0 | 64.2 | 0.0 | 35776 |

Full time-series data is available in: `distribution/06_concurrency_sweep_timeseries.md`
