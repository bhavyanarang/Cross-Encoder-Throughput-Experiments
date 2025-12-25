# 10b_packing_enabled

_Sequential packing (no padding, block-diagonal attention)_

**Timestamp:** 2025-12-26 02:23:56

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 3200 | 7.15 | 71.4ms | 104.6ms | 127.3ms | 447.7 | 773.9 |

## Detailed Metrics

### Config 1: batch=32, concurrency=1

**Total:** 3200 pairs in 7.15s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 71.45 |
| Min | 39.51 |
| Max | 148.70 |
| Std Dev | 23.54 |
| P50 | 70.46 |
| P90 | 102.15 |
| P95 | 104.65 |
| P99 | 127.27 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 447.75 |
| Min | 215.20 |
| Max | 809.95 |
| Std Dev | 161.16 |
| P50 | 454.26 |
| P90 | 719.90 |
| P95 | 773.87 |
| P99 | 807.84 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 70.5ms (P50) | 643.90 | 460.76 | 809.95 | 50 |
| 70.5-92.9ms (P50-P75) | 392.50 | 344.91 | 447.75 | 25 |
| 92.9-102.1ms (P75-P90) | 331.35 | 313.45 | 343.07 | 15 |
| >= 102.1ms (P90+) | 290.82 | 215.20 | 311.69 | 10 |

**Correlation:** -0.960 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 447.75 p/s | batch=32, conc=1 |
| Best Latency | 71.45ms | batch=32, conc=1 |
| Avg Throughput | 447.75 p/s | all configs |
| Avg Latency | 71.45ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1254.1 | 1111.6 | 1303.6 | 1263.6 | 1303.6 |
| GPU Utilization (%) | 77.7 | 36.3 | 88.9 | 79.7 | 88.1 |
| CPU Usage (%) | 1.4 | 1.1 | 1.6 | 1.4 | 1.6 |
| Tokenization (ms) | 12.4 | 11.0 | 20.9 | 11.5 | 15.4 |
| Inference (ms) | 66.8 | 28.0 | 108.3 | 74.6 | 94.5 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 40.0 | 32.2 | 45.8 | 40.4 | 45.6 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1111.6 | 36.3 | 1.5 | 66.0 | 224 | 20.9 | 85.3 | 0.0 | 40.2 |
| 1 | 1165.6 | 74.8 | 1.3 | 75.8 | 384 | 11.1 | 79.9 | 0.0 | 45.8 |
| 2 | 1195.6 | 85.1 | 1.4 | 83.4 | 384 | 11.0 | 83.1 | 0.0 | 40.4 |
| 3 | 1195.6 | 87.1 | 1.5 | 74.8 | 448 | 11.4 | 28.0 | 0.0 | 39.1 |
| 4 | 1227.6 | 74.6 | 1.4 | 66.0 | 448 | 12.6 | 78.8 | 0.0 | 42.1 |
| 5 | 1263.6 | 79.7 | 1.6 | 65.9 | 480 | 11.3 | 32.7 | 0.0 | 42.3 |
| 6 | 1263.6 | 80.5 | 1.4 | 70.3 | 448 | 12.4 | 88.5 | 0.0 | 42.0 |
| 7 | 1263.6 | 73.8 | 1.1 | 80.7 | 352 | 12.6 | 108.3 | 0.0 | 39.2 |
| 8 | 1303.6 | 87.8 | 1.3 | 88.6 | 384 | 12.2 | 57.8 | 0.0 | 32.2 |
| 9 | 1303.6 | 88.9 | 1.2 | 77.9 | 448 | 11.8 | 46.0 | 0.0 | 36.0 |
| 10 | 1303.6 | 83.5 | 1.3 | 68.4 | 480 | 11.0 | 41.6 | 0.0 | 41.6 |
| 11 | 1303.6 | 77.6 | 1.6 | 61.0 | 512 | 11.4 | 72.7 | 0.0 | 34.5 |
| 12 | 1303.6 | 75.3 | 1.5 | 56.7 | 544 | 11.5 | 74.6 | 0.0 | 44.0 |
| 13 | 1303.6 | 77.3 | 1.4 | 60.5 | 512 | 11.1 | 36.6 | 0.0 | 34.9 |
| 14 | 1303.6 | 82.6 | 1.3 | 67.5 | 480 | 13.1 | 87.4 | 0.0 | 45.5 |
