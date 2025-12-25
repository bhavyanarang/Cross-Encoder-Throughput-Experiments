# 05b_batch_size_mlx

_Sweep batch sizes on MLX backend_

**Timestamp:** 2025-12-26 02:19:09

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 800 | 4.89 | 48.9ms | 104.8ms | 207.7ms | 163.5 | 433.5 |

## Detailed Metrics

### Config 1: batch=8, concurrency=1

**Total:** 800 pairs in 4.89s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 48.92 |
| Min | 16.06 |
| Max | 213.83 |
| Std Dev | 34.96 |
| P50 | 49.95 |
| P90 | 66.90 |
| P95 | 104.81 |
| P99 | 207.69 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 163.46 |
| Min | 37.41 |
| Max | 498.26 |
| Std Dev | 117.68 |
| P50 | 160.18 |
| P90 | 384.97 |
| P95 | 433.51 |
| P99 | 473.79 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 49.9ms (P50) | 322.33 | 161.57 | 498.26 | 50 |
| 49.9-57.4ms (P50-P75) | 149.80 | 139.37 | 158.80 | 25 |
| 57.4-66.9ms (P75-P90) | 131.92 | 120.47 | 138.90 | 15 |
| >= 66.9ms (P90+) | 74.32 | 37.41 | 112.14 | 10 |

**Correlation:** -0.741 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 163.46 p/s | batch=8, conc=1 |
| Best Latency | 48.92ms | batch=8, conc=1 |
| Avg Throughput | 163.46 p/s | all configs |
| Avg Latency | 48.92ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1088.3 | 1081.6 | 1089.6 | 1089.6 | 1089.6 |
| GPU Utilization (%) | 74.3 | 22.5 | 96.8 | 81.1 | 94.8 |
| CPU Usage (%) | 1.7 | 1.6 | 1.9 | 1.8 | 1.9 |
| Tokenization (ms) | 4.3 | 3.2 | 4.7 | 4.4 | 4.7 |
| Inference (ms) | 40.8 | 21.2 | 56.4 | 47.1 | 55.1 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 30.7 | 22.1 | 40.6 | 30.2 | 39.5 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1081.6 | 22.5 | 1.8 | 38.4 | 56 | 4.5 | 51.3 | 0.0 | 36.0 |
| 1 | 1089.6 | 88.9 | 1.6 | 51.8 | 152 | 3.2 | 44.9 | 0.0 | 24.8 |
| 2 | 1089.6 | 83.2 | 1.8 | 37.1 | 208 | 4.2 | 49.3 | 0.0 | 34.1 |
| 3 | 1089.6 | 75.6 | 1.6 | 49.6 | 152 | 4.7 | 21.8 | 0.0 | 40.6 |
| 4 | 1089.6 | 79.0 | 1.7 | 48.0 | 160 | 4.6 | 56.4 | 0.0 | 22.1 |
| 5 | 1089.6 | 96.8 | 1.9 | 55.5 | 168 | 4.4 | 21.2 | 0.0 | 26.4 |
