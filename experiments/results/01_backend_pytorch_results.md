# 01_backend_pytorch

_PyTorch backend baseline on MPS with FP16_

**Timestamp:** 2025-12-26 02:16:55

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `pytorch` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 3200 | 7.00 | 70.0ms | 139.4ms | 168.7ms | 457.1 | 787.0 |

## Detailed Metrics

### Config 1: batch=32, concurrency=1

**Total:** 3200 pairs in 7.00s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 69.98 |
| Min | 37.73 |
| Max | 181.26 |
| Std Dev | 30.28 |
| P50 | 68.20 |
| P90 | 104.40 |
| P95 | 139.39 |
| P99 | 168.71 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 457.11 |
| Min | 176.54 |
| Max | 848.20 |
| Std Dev | 176.93 |
| P50 | 469.22 |
| P90 | 779.38 |
| P95 | 787.03 |
| P99 | 818.84 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 68.2ms (P50) | 678.14 | 470.43 | 848.20 | 50 |
| 68.2-78.6ms (P50-P75) | 436.87 | 407.29 | 468.00 | 25 |
| 78.6-104.4ms (P75-P90) | 363.51 | 306.91 | 406.38 | 15 |
| >= 104.4ms (P90+) | 233.45 | 176.54 | 303.01 | 10 |

**Correlation:** -0.900 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 457.11 p/s | batch=32, conc=1 |
| Best Latency | 69.98ms | batch=32, conc=1 |
| Avg Throughput | 457.11 p/s | all configs |
| Avg Latency | 69.98ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1269.0 | 1195.6 | 1303.6 | 1283.6 | 1303.6 |
| GPU Utilization (%) | 72.8 | 62.4 | 83.1 | 73.8 | 81.1 |
| CPU Usage (%) | 1.8 | 1.0 | 7.9 | 1.4 | 3.9 |
| Tokenization (ms) | 30.1 | 10.7 | 130.1 | 12.8 | 98.4 |
| Inference (ms) | 61.2 | 29.8 | 86.9 | 63.9 | 84.0 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 43.6 | 30.7 | 52.0 | 44.0 | 51.5 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1195.6 | 80.0 | 1.1 | 65.9 | 480 | 12.8 | 62.4 | 0.0 | 44.6 |
| 1 | 1195.6 | 83.1 | 7.9 | 68.0 | 480 | 12.9 | 31.5 | 0.0 | 44.1 |
| 2 | 1195.6 | 71.9 | 1.5 | 57.5 | 512 | 10.7 | 57.1 | 0.0 | 41.6 |
| 3 | 1263.6 | 77.2 | 1.4 | 64.7 | 480 | 12.3 | 74.7 | 0.0 | 30.7 |
| 4 | 1263.6 | 78.0 | 1.6 | 66.1 | 480 | 12.3 | 29.8 | 0.0 | 43.5 |
| 5 | 1263.6 | 75.1 | 1.2 | 65.4 | 480 | 39.5 | 40.7 | 0.0 | 39.2 |
| 6 | 1263.6 | 72.5 | 1.0 | 92.5 | 320 | 45.5 | 86.9 | 0.0 | 51.2 |
| 7 | 1303.6 | 73.4 | 1.3 | 99.9 | 320 | 15.1 | 76.3 | 0.0 | 50.1 |
| 8 | 1303.6 | 76.7 | 1.7 | 81.0 | 416 | 13.8 | 68.1 | 0.0 | 47.6 |
| 9 | 1303.6 | 62.5 | 1.2 | 78.3 | 384 | 130.1 | 42.7 | 0.0 | 41.6 |
| 10 | 1303.6 | 63.2 | 1.5 | 68.3 | 448 | 11.1 | 60.6 | 0.0 | 34.5 |
| 11 | 1303.6 | 62.4 | 1.5 | 53.5 | 512 | 81.3 | 82.4 | 0.0 | 44.0 |
| 12 | 1303.6 | 68.7 | 1.5 | 61.1 | 512 | 11.8 | 65.3 | 0.0 | 52.0 |
| 13 | 1303.6 | 74.1 | 1.4 | 66.8 | 480 | 12.2 | 79.0 | 0.0 | 45.5 |
