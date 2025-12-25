# 08b_dynamic_batch_mlx

_Dynamic batching with MLX backend_

**Timestamp:** 2025-12-26 02:21:54

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=96, timeout=20ms)

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 800 | 6.07 | 60.7ms | 79.7ms | 87.1ms | 131.8 | 197.8 |

## Detailed Metrics

### Config 1: batch=8, concurrency=1

**Total:** 800 pairs in 6.07s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 60.70 |
| Min | 35.09 |
| Max | 145.59 |
| Std Dev | 16.67 |
| P50 | 64.74 |
| P90 | 77.19 |
| P95 | 79.70 |
| P99 | 87.09 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 131.75 |
| Min | 54.95 |
| Max | 228.00 |
| Std Dev | 36.97 |
| P50 | 123.57 |
| P90 | 190.62 |
| P95 | 197.76 |
| P99 | 222.42 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 64.7ms (P50) | 174.00 | 123.75 | 228.00 | 50 |
| 64.7-72.5ms (P50-P75) | 115.38 | 110.47 | 123.40 | 25 |
| 72.5-77.2ms (P75-P90) | 106.81 | 103.75 | 110.12 | 15 |
| >= 77.2ms (P90+) | 94.95 | 54.95 | 102.74 | 10 |

**Correlation:** -0.943 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 131.75 p/s | batch=8, conc=1 |
| Best Latency | 60.70ms | batch=8, conc=1 |
| Avg Throughput | 131.75 p/s | all configs |
| Avg Latency | 60.70ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1087.9 | 1081.6 | 1089.6 | 1089.6 | 1089.6 |
| GPU Utilization (%) | 52.5 | 9.7 | 67.1 | 57.2 | 63.2 |
| CPU Usage (%) | 31.9 | 8.0 | 41.2 | 33.4 | 39.2 |
| Tokenization (ms) | 5.9 | 3.2 | 33.0 | 3.8 | 14.4 |
| Inference (ms) | 37.6 | 13.7 | 64.2 | 41.8 | 56.2 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1081.6 | 9.7 | 8.0 | 114.7 | 8 | 4.3 | 13.7 | 0.0 | 0.0 |
| 1 | 1081.6 | 36.9 | 36.9 | 60.4 | 80 | 3.6 | 40.0 | 0.0 | 0.0 |
| 2 | 1081.6 | 61.1 | 29.2 | 62.3 | 128 | 4.1 | 51.9 | 0.0 | 0.0 |
| 3 | 1089.6 | 67.1 | 26.9 | 72.0 | 112 | 4.2 | 42.1 | 0.0 | 0.0 |
| 4 | 1089.6 | 60.7 | 32.5 | 64.5 | 120 | 3.7 | 24.1 | 0.0 | 0.0 |
| 5 | 1089.6 | 59.0 | 34.3 | 60.8 | 128 | 3.6 | 42.0 | 0.0 | 0.0 |
| 6 | 1089.6 | 57.7 | 38.2 | 58.0 | 136 | 4.0 | 22.3 | 0.0 | 0.0 |
| 7 | 1089.6 | 57.8 | 32.1 | 58.0 | 136 | 3.7 | 48.0 | 0.0 | 0.0 |
| 8 | 1089.6 | 56.1 | 41.2 | 57.0 | 136 | 3.6 | 41.5 | 0.0 | 0.0 |
| 9 | 1089.6 | 50.0 | 28.7 | 56.8 | 136 | 33.0 | 64.2 | 0.0 | 0.0 |
| 10 | 1089.6 | 51.0 | 36.8 | 59.7 | 128 | 3.7 | 43.1 | 0.0 | 0.0 |
| 11 | 1089.6 | 56.7 | 37.6 | 55.8 | 144 | 3.2 | 48.5 | 0.0 | 0.0 |
| 12 | 1089.6 | 53.8 | 36.9 | 54.0 | 144 | 3.8 | 22.9 | 0.0 | 0.0 |
| 13 | 1089.6 | 57.6 | 27.8 | 56.1 | 144 | 3.9 | 21.9 | 0.0 | 0.0 |
