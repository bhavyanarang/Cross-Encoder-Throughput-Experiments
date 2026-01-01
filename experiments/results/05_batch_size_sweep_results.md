# 05_batch_size_sweep_mlx

_Sweep batch sizes on MPS and MLX backends_

**Timestamp:** 2026-01-01 21:01:48

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 928 | 60.09 | 517.3ms | 522.2ms | 523.2ms | 15.4 | 15.7 |

## Detailed Metrics

### Run 1

**Total:** 928 pairs in 60.09s

### Latency

| Metric | Value |
|--------|-------|
| Average | 517.29 |
| Min | 507.23 |
| Max | 523.79 |
| Std Dev | 4.06 |
| P50 | 518.69 |
| P90 | 521.43 |
| P95 | 522.22 |
| P99 | 523.20 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 15.44 |
| Min | 15.27 |
| Max | 15.77 |
| Std Dev | 0.12 |
| P50 | 15.42 |
| P90 | 15.67 |
| P95 | 15.70 |
| P99 | 15.76 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 518.7ms (P50) | 15.56 | 15.42 | 15.77 | 58 |
| 518.7-520.3ms (P50-P75) | 15.40 | 15.38 | 15.42 | 29 |
| 520.3-521.4ms (P75-P90) | 15.36 | 15.34 | 15.37 | 17 |
| >= 521.4ms (P90+) | 15.32 | 15.27 | 15.34 | 12 |

**Correlation:** -1.000 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 15.44 p/s | batch=8, conc=1 |
| Best Latency | 517.29ms | batch=8, conc=1 |
| Avg Throughput | 15.44 p/s | all configs |
| Avg Latency | 517.29ms | all configs |


---

# 05_batch_size_sweep_mlx

_Sweep batch sizes on MPS and MLX backends_

**Timestamp:** 2026-01-01 21:01:48

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 16 | 1 | 1840 | 60.22 | 523.1ms | 529.1ms | 530.7ms | 30.6 | 30.9 |

## Detailed Metrics

### Run 1

**Total:** 1840 pairs in 60.22s

### Latency

| Metric | Value |
|--------|-------|
| Average | 523.15 |
| Min | 511.06 |
| Max | 530.77 |
| Std Dev | 3.79 |
| P50 | 523.20 |
| P90 | 528.28 |
| P95 | 529.08 |
| P99 | 530.69 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 30.55 |
| Min | 30.14 |
| Max | 31.31 |
| Std Dev | 0.22 |
| P50 | 30.58 |
| P90 | 30.87 |
| P95 | 30.93 |
| P99 | 31.06 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 523.2ms (P50) | 30.76 | 30.58 | 31.31 | 57 |
| 523.2-525.9ms (P50-P75) | 30.52 | 30.43 | 30.58 | 29 |
| 525.9-528.3ms (P75-P90) | 30.35 | 30.29 | 30.42 | 17 |
| >= 528.3ms (P90+) | 30.23 | 30.14 | 30.28 | 12 |

**Correlation:** -1.000 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 30.55 p/s | batch=16, conc=1 |
| Best Latency | 523.15ms | batch=16, conc=1 |
| Avg Throughput | 30.55 p/s | all configs |
| Avg Latency | 523.15ms | all configs |


---

# 05_batch_size_sweep_mlx

_Sweep batch sizes on MPS and MLX backends_

**Timestamp:** 2026-01-01 21:01:48

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 3616 | 60.17 | 532.0ms | 538.9ms | 540.6ms | 60.1 | 61.0 |

## Detailed Metrics

### Run 1

**Total:** 3616 pairs in 60.17s

### Latency

| Metric | Value |
|--------|-------|
| Average | 531.95 |
| Min | 515.84 |
| Max | 540.98 |
| Std Dev | 4.65 |
| P50 | 531.11 |
| P90 | 537.98 |
| P95 | 538.86 |
| P99 | 540.63 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 60.10 |
| Min | 59.15 |
| Max | 62.04 |
| Std Dev | 0.53 |
| P50 | 60.25 |
| P90 | 60.81 |
| P95 | 60.99 |
| P99 | 61.22 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 531.1ms (P50) | 60.59 | 60.25 | 62.04 | 56 |
| 531.1-536.2ms (P50-P75) | 60.01 | 59.70 | 60.25 | 28 |
| 536.2-538.0ms (P75-P90) | 59.59 | 59.49 | 59.68 | 17 |
| >= 538.0ms (P90+) | 59.34 | 59.15 | 59.48 | 12 |

**Correlation:** -1.000 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 60.10 p/s | batch=32, conc=1 |
| Best Latency | 531.95ms | batch=32, conc=1 |
| Avg Throughput | 60.10 p/s | all configs |
| Avg Latency | 531.95ms | all configs |


---

# 05_batch_size_sweep_mlx

_Sweep batch sizes on MPS and MLX backends_

**Timestamp:** 2026-01-01 21:01:48

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 48 | 1 | 5376 | 60.36 | 538.4ms | 545.9ms | 549.5ms | 89.1 | 90.6 |

## Detailed Metrics

### Run 1

**Total:** 5376 pairs in 60.36s

### Latency

| Metric | Value |
|--------|-------|
| Average | 538.43 |
| Min | 524.47 |
| Max | 550.80 |
| Std Dev | 5.33 |
| P50 | 538.84 |
| P90 | 545.10 |
| P95 | 545.85 |
| P99 | 549.49 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 89.07 |
| Min | 87.15 |
| Max | 91.52 |
| Std Dev | 0.88 |
| P50 | 89.08 |
| P90 | 90.39 |
| P95 | 90.60 |
| P99 | 91.08 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 538.8ms (P50) | 89.87 | 89.09 | 91.52 | 56 |
| 538.8-542.2ms (P50-P75) | 88.83 | 88.53 | 89.07 | 28 |
| 542.2-545.1ms (P75-P90) | 88.26 | 88.06 | 88.51 | 16 |
| >= 545.1ms (P90+) | 87.80 | 87.15 | 88.06 | 12 |

**Correlation:** -1.000 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 89.07 p/s | batch=48, conc=1 |
| Best Latency | 538.43ms | batch=48, conc=1 |
| Avg Throughput | 89.07 p/s | all configs |
| Avg Latency | 538.43ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1148.4 | 1088.6 | 1178.9 | 1162.8 | 1178.9 |
| GPU Utilization (%) | 9.9 | 4.9 | 13.6 | 10.4 | 13.5 |
| CPU Usage (%) | 3.7 | 1.7 | 5.6 | 3.7 | 5.5 |
| Tokenization (ms) | 14.3 | 6.6 | 22.4 | 11.4 | 22.2 |
| Inference (ms) | 50.9 | 40.0 | 62.9 | 49.5 | 60.9 |
| Queue Wait (ms) | 14.4 | 6.8 | 22.5 | 11.5 | 22.3 |
| Padding Waste (%) | 38.3 | 36.4 | 41.1 | 37.2 | 41.0 |

### Stage Timing

| Stage | Percentage |
|-------|------------|
| Tokenization | 3.0% |
| Queue Wait | 3.0% |
| Model Inference | 9.8% |
| Other/gRPC | 0.0% |

### Worker Metrics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 51.7 | 83.5 | 0.0 | 11800 |

Full time-series data is available in: `distribution/05_batch_size_sweep_timeseries.md`
