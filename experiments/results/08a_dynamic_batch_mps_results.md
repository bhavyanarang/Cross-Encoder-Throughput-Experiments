# 08a_dynamic_batch_mps

_Dynamic batching with MPS backend_

**Timestamp:** 2025-12-26 02:21:32

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=96, timeout=20ms)

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 800 | 7.13 | 71.3ms | 108.5ms | 315.6ms | 112.2 | 212.1 |

## Detailed Metrics

### Config 1: batch=8, concurrency=1

**Total:** 800 pairs in 7.13s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 71.31 |
| Min | 34.05 |
| Max | 372.61 |
| Std Dev | 50.51 |
| P50 | 67.90 |
| P90 | 82.88 |
| P95 | 108.45 |
| P99 | 315.63 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 112.16 |
| Min | 21.47 |
| Max | 234.95 |
| Std Dev | 46.31 |
| P50 | 117.83 |
| P90 | 203.60 |
| P95 | 212.11 |
| P99 | 218.53 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 67.9ms (P50) | 173.26 | 117.87 | 234.95 | 50 |
| 67.9-74.6ms (P50-P75) | 112.52 | 107.19 | 117.79 | 25 |
| 74.6-82.9ms (P75-P90) | 103.10 | 96.86 | 107.18 | 15 |
| >= 82.9ms (P90+) | 60.50 | 21.47 | 93.64 | 10 |

**Correlation:** -0.735 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 112.16 p/s | batch=8, conc=1 |
| Best Latency | 71.31ms | batch=8, conc=1 |
| Avg Throughput | 112.16 p/s | all configs |
| Avg Latency | 71.31ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1088.9 | 1081.6 | 1089.6 | 1089.6 | 1089.6 |
| GPU Utilization (%) | 53.0 | 16.7 | 75.4 | 56.2 | 69.8 |
| CPU Usage (%) | 22.7 | 2.2 | 36.4 | 28.2 | 34.5 |
| Tokenization (ms) | 5.7 | 3.9 | 17.4 | 4.2 | 11.8 |
| Inference (ms) | 51.1 | 16.2 | 168.2 | 45.1 | 116.4 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1081.6 | 16.7 | 10.4 | 54.6 | 40 | 4.9 | 20.9 | 0.0 | 0.0 |
| 1 | 1089.6 | 64.1 | 28.2 | 70.1 | 112 | 4.3 | 45.1 | 0.0 | 0.0 |
| 2 | 1089.6 | 58.4 | 31.3 | 63.0 | 120 | 4.2 | 64.6 | 0.0 | 0.0 |
| 3 | 1089.6 | 53.7 | 36.4 | 54.0 | 144 | 4.0 | 49.0 | 0.0 | 0.0 |
| 4 | 1089.6 | 53.3 | 32.5 | 55.6 | 136 | 4.1 | 16.2 | 0.0 | 0.0 |
| 5 | 1089.6 | 42.6 | 10.9 | 144.0 | 40 | 6.2 | 41.3 | 0.0 | 0.0 |
| 6 | 1089.6 | 57.0 | 2.2 | 199.5 | 40 | 17.4 | 168.2 | 0.0 | 0.0 |
| 7 | 1089.6 | 75.4 | 8.5 | 161.1 | 56 | 4.9 | 55.7 | 0.0 | 0.0 |
| 8 | 1089.6 | 49.3 | 31.4 | 79.8 | 96 | 4.2 | 60.7 | 0.0 | 0.0 |
| 9 | 1089.6 | 56.2 | 31.7 | 59.0 | 136 | 3.9 | 19.7 | 0.0 | 0.0 |
| 10 | 1089.6 | 56.6 | 26.2 | 61.2 | 128 | 4.1 | 20.5 | 0.0 | 0.0 |
