# 03_backend_mlx

_MLX backend with 16-bit quantization_

**Timestamp:** 2025-12-26 02:17:44

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 3200 | 6.15 | 61.5ms | 86.6ms | 105.1ms | 520.1 | 804.3 |

## Detailed Metrics

### Config 1: batch=32, concurrency=1

**Total:** 3200 pairs in 6.15s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 61.51 |
| Min | 38.11 |
| Max | 145.51 |
| Std Dev | 19.20 |
| P50 | 66.87 |
| P90 | 81.98 |
| P95 | 86.65 |
| P99 | 105.07 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 520.09 |
| Min | 219.91 |
| Max | 839.70 |
| Std Dev | 167.59 |
| P50 | 478.53 |
| P90 | 790.49 |
| P95 | 804.32 |
| P99 | 828.61 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 66.9ms (P50) | 724.99 | 479.95 | 839.70 | 50 |
| 66.9-75.5ms (P50-P75) | 447.00 | 424.70 | 477.10 | 25 |
| 75.5-82.0ms (P75-P90) | 407.92 | 391.07 | 422.03 | 15 |
| >= 82.0ms (P90+) | 348.65 | 219.91 | 383.86 | 10 |

**Correlation:** -0.956 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 520.09 p/s | batch=32, conc=1 |
| Best Latency | 61.51ms | batch=32, conc=1 |
| Avg Throughput | 520.09 p/s | all configs |
| Avg Latency | 61.51ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1259.9 | 1137.6 | 1303.6 | 1303.6 | 1303.6 |
| GPU Utilization (%) | 74.9 | 43.7 | 83.3 | 77.1 | 82.3 |
| CPU Usage (%) | 1.5 | 1.3 | 1.7 | 1.6 | 1.7 |
| Tokenization (ms) | 11.6 | 10.8 | 12.7 | 11.5 | 12.5 |
| Inference (ms) | 52.3 | 27.4 | 72.2 | 54.8 | 70.4 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 42.1 | 34.5 | 56.0 | 41.6 | 52.1 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1137.6 | 43.7 | 1.7 | 60.8 | 288 | 11.6 | 72.2 | 0.0 | 40.8 |
| 1 | 1165.6 | 83.3 | 1.5 | 64.4 | 512 | 11.6 | 54.8 | 0.0 | 36.5 |
| 2 | 1195.6 | 80.1 | 1.6 | 66.1 | 480 | 10.8 | 54.3 | 0.0 | 39.4 |
| 3 | 1227.6 | 77.8 | 1.7 | 58.4 | 544 | 12.3 | 61.4 | 0.0 | 42.1 |
| 4 | 1263.6 | 75.4 | 1.7 | 56.9 | 544 | 11.1 | 28.3 | 0.0 | 42.3 |
| 5 | 1263.6 | 77.1 | 1.4 | 60.8 | 512 | 11.4 | 61.3 | 0.0 | 49.5 |
| 6 | 1303.6 | 76.1 | 1.6 | 60.0 | 512 | 12.1 | 67.9 | 0.0 | 56.0 |
| 7 | 1303.6 | 77.0 | 1.3 | 60.6 | 512 | 11.4 | 54.6 | 0.0 | 35.4 |
| 8 | 1303.6 | 78.3 | 1.5 | 61.8 | 512 | 10.9 | 27.4 | 0.0 | 41.6 |
| 9 | 1303.6 | 80.0 | 1.6 | 57.2 | 576 | 11.5 | 63.0 | 0.0 | 34.5 |
| 10 | 1303.6 | 73.4 | 1.3 | 58.7 | 544 | 11.2 | 28.6 | 0.0 | 36.8 |
| 11 | 1303.6 | 70.2 | 1.7 | 60.0 | 512 | 11.9 | 36.7 | 0.0 | 46.6 |
| 12 | 1303.6 | 81.7 | 1.4 | 58.4 | 576 | 12.7 | 69.2 | 0.0 | 45.5 |
