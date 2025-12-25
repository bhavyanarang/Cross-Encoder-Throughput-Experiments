# 02_backend_mps

_MPS backend with FP16 optimization_

**Timestamp:** 2025-12-26 02:17:21

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 3200 | 6.01 | 60.1ms | 85.9ms | 106.8ms | 532.5 | 794.8 |

## Detailed Metrics

### Config 1: batch=32, concurrency=1

**Total:** 3200 pairs in 6.01s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 60.07 |
| Min | 38.13 |
| Max | 131.99 |
| Std Dev | 17.89 |
| P50 | 59.96 |
| P90 | 79.19 |
| P95 | 85.93 |
| P99 | 106.81 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 532.51 |
| Min | 242.45 |
| Max | 839.18 |
| Std Dev | 159.52 |
| P50 | 536.31 |
| P90 | 783.34 |
| P95 | 794.84 |
| P99 | 836.05 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 60.0ms (P50) | 728.94 | 573.62 | 839.18 | 50 |
| 60.0-73.5ms (P50-P75) | 459.50 | 435.63 | 499.00 | 25 |
| 73.5-79.2ms (P75-P90) | 423.02 | 404.11 | 435.63 | 15 |
| >= 79.2ms (P90+) | 356.20 | 242.45 | 404.01 | 10 |

**Correlation:** -0.963 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 532.51 p/s | batch=32, conc=1 |
| Best Latency | 60.07ms | batch=32, conc=1 |
| Avg Throughput | 532.51 p/s | all configs |
| Avg Latency | 60.07ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1252.4 | 1111.6 | 1303.6 | 1263.6 | 1303.6 |
| GPU Utilization (%) | 73.3 | 30.7 | 82.1 | 76.5 | 81.6 |
| CPU Usage (%) | 1.5 | 1.3 | 1.6 | 1.5 | 1.6 |
| Tokenization (ms) | 11.6 | 10.3 | 13.0 | 11.5 | 12.9 |
| Inference (ms) | 45.9 | 25.2 | 92.7 | 36.6 | 75.0 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 40.9 | 32.7 | 47.1 | 41.9 | 46.8 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1111.6 | 30.7 | 1.3 | 56.2 | 224 | 10.3 | 56.2 | 0.0 | 40.2 |
| 1 | 1165.6 | 71.8 | 1.5 | 63.6 | 448 | 11.2 | 60.7 | 0.0 | 41.9 |
| 2 | 1195.6 | 82.1 | 1.6 | 67.0 | 480 | 11.5 | 25.2 | 0.0 | 32.9 |
| 3 | 1195.6 | 76.8 | 1.6 | 57.5 | 544 | 11.4 | 55.9 | 0.0 | 39.5 |
| 4 | 1263.6 | 77.6 | 1.3 | 58.2 | 544 | 11.4 | 32.5 | 0.0 | 47.1 |
| 5 | 1263.6 | 76.2 | 1.5 | 60.1 | 512 | 11.8 | 56.0 | 0.0 | 42.0 |
| 6 | 1263.6 | 76.9 | 1.4 | 57.6 | 544 | 11.0 | 27.2 | 0.0 | 32.7 |
| 7 | 1303.6 | 81.3 | 1.5 | 63.2 | 512 | 12.1 | 29.7 | 0.0 | 40.5 |
| 8 | 1303.6 | 76.7 | 1.4 | 60.5 | 512 | 13.0 | 33.8 | 0.0 | 34.3 |
| 9 | 1303.6 | 75.7 | 1.6 | 54.6 | 576 | 11.1 | 27.6 | 0.0 | 44.7 |
| 10 | 1303.6 | 76.5 | 1.6 | 53.5 | 608 | 11.7 | 92.7 | 0.0 | 44.0 |
| 11 | 1303.6 | 73.7 | 1.5 | 57.0 | 544 | 11.8 | 36.6 | 0.0 | 46.6 |
| 12 | 1303.6 | 76.5 | 1.5 | 58.6 | 544 | 12.8 | 63.2 | 0.0 | 45.5 |
