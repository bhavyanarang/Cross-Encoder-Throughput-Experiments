# 09b_padding_length_aware

_Length-aware batching - sorted by token length_

**Timestamp:** 2025-12-26 02:22:45

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 3200 | 7.06 | 70.6ms | 97.1ms | 105.4ms | 453.2 | 753.5 |

## Detailed Metrics

### Config 1: batch=32, concurrency=1

**Total:** 3200 pairs in 7.06s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 70.59 |
| Min | 39.81 |
| Max | 228.77 |
| Std Dev | 24.98 |
| P50 | 69.96 |
| P90 | 95.08 |
| P95 | 97.06 |
| P99 | 105.38 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 453.18 |
| Min | 139.88 |
| Max | 803.81 |
| Std Dev | 150.16 |
| P50 | 457.61 |
| P90 | 698.28 |
| P95 | 753.49 |
| P99 | 790.54 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 70.0ms (P50) | 635.34 | 466.94 | 803.81 | 50 |
| 70.0-87.9ms (P50-P75) | 396.55 | 364.77 | 448.29 | 25 |
| 87.9-95.1ms (P75-P90) | 352.97 | 336.60 | 362.47 | 15 |
| >= 95.1ms (P90+) | 307.26 | 139.88 | 336.05 | 10 |

**Correlation:** -0.887 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 453.18 p/s | batch=32, conc=1 |
| Best Latency | 70.59ms | batch=32, conc=1 |
| Avg Throughput | 453.18 p/s | all configs |
| Avg Latency | 70.59ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1258.3 | 1137.6 | 1303.6 | 1263.6 | 1303.6 |
| GPU Utilization (%) | 79.1 | 47.5 | 95.4 | 81.9 | 88.8 |
| CPU Usage (%) | 1.3 | 1.0 | 1.7 | 1.3 | 1.7 |
| Tokenization (ms) | 12.0 | 10.5 | 13.6 | 11.8 | 13.4 |
| Inference (ms) | 59.8 | 34.4 | 87.8 | 62.5 | 85.9 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 42.1 | 31.9 | 52.7 | 41.6 | 52.2 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1137.6 | 47.5 | 1.7 | 65.7 | 288 | 11.8 | 83.8 | 0.0 | 40.8 |
| 1 | 1165.6 | 84.1 | 1.2 | 73.0 | 448 | 12.0 | 69.8 | 0.0 | 39.3 |
| 2 | 1195.6 | 82.5 | 1.3 | 81.5 | 384 | 10.5 | 62.5 | 0.0 | 32.0 |
| 3 | 1195.6 | 82.2 | 1.6 | 67.5 | 480 | 11.4 | 64.1 | 0.0 | 41.6 |
| 4 | 1263.6 | 78.1 | 1.0 | 68.5 | 448 | 13.6 | 85.1 | 0.0 | 44.2 |
| 5 | 1263.6 | 84.8 | 1.4 | 68.9 | 480 | 10.8 | 36.1 | 0.0 | 36.4 |
| 6 | 1263.6 | 83.4 | 1.2 | 68.0 | 480 | 12.5 | 42.3 | 0.0 | 31.9 |
| 7 | 1263.6 | 68.9 | 1.0 | 75.6 | 352 | 11.6 | 41.2 | 0.0 | 32.7 |
| 8 | 1303.6 | 80.9 | 1.3 | 86.4 | 352 | 13.3 | 87.8 | 0.0 | 50.1 |
| 9 | 1303.6 | 95.4 | 1.3 | 81.0 | 448 | 12.6 | 45.9 | 0.0 | 48.3 |
| 10 | 1303.6 | 86.0 | 1.3 | 70.2 | 480 | 13.4 | 81.4 | 0.0 | 52.0 |
| 11 | 1303.6 | 77.5 | 1.7 | 60.9 | 512 | 11.6 | 43.3 | 0.0 | 52.7 |
| 12 | 1303.6 | 74.0 | 1.3 | 56.0 | 544 | 11.0 | 34.4 | 0.0 | 46.0 |
| 13 | 1303.6 | 78.9 | 1.4 | 62.0 | 512 | 11.4 | 38.5 | 0.0 | 37.6 |
| 14 | 1303.6 | 81.9 | 1.5 | 63.7 | 512 | 12.7 | 81.2 | 0.0 | 45.5 |
