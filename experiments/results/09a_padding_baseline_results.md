# 09a_padding_baseline

_Baseline padding analysis - random ordering_

**Timestamp:** 2025-12-26 02:22:21

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 3200 | 7.30 | 72.9ms | 107.9ms | 116.5ms | 438.6 | 763.6 |

## Detailed Metrics

### Config 1: batch=32, concurrency=1

**Total:** 3200 pairs in 7.30s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 72.94 |
| Min | 38.73 |
| Max | 125.88 |
| Std Dev | 22.55 |
| P50 | 69.46 |
| P90 | 102.54 |
| P95 | 107.86 |
| P99 | 116.45 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 438.60 |
| Min | 254.22 |
| Max | 826.29 |
| Std Dev | 153.00 |
| P50 | 460.91 |
| P90 | 679.06 |
| P95 | 763.59 |
| P99 | 804.79 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 69.5ms (P50) | 618.35 | 471.08 | 826.29 | 50 |
| 69.5-92.9ms (P50-P75) | 388.26 | 344.89 | 450.74 | 25 |
| 92.9-102.5ms (P75-P90) | 327.54 | 312.19 | 342.55 | 15 |
| >= 102.5ms (P90+) | 289.74 | 254.22 | 311.12 | 10 |

**Correlation:** -0.964 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 438.60 p/s | batch=32, conc=1 |
| Best Latency | 72.94ms | batch=32, conc=1 |
| Avg Throughput | 438.60 p/s | all configs |
| Avg Latency | 72.94ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1250.1 | 1087.6 | 1303.6 | 1283.6 | 1303.6 |
| GPU Utilization (%) | 76.2 | 21.7 | 86.7 | 80.5 | 86.0 |
| CPU Usage (%) | 1.4 | 1.1 | 1.6 | 1.4 | 1.5 |
| Tokenization (ms) | 12.2 | 10.9 | 13.6 | 12.2 | 13.6 |
| Inference (ms) | 51.0 | 28.3 | 83.7 | 42.0 | 82.9 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 39.7 | 29.2 | 55.1 | 39.3 | 52.8 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1087.6 | 21.7 | 1.1 | 66.9 | 128 | 11.4 | 28.5 | 0.0 | 37.1 |
| 1 | 1137.6 | 59.2 | 1.4 | 71.6 | 320 | 11.2 | 82.6 | 0.0 | 39.4 |
| 2 | 1165.6 | 79.5 | 1.2 | 78.8 | 384 | 12.3 | 40.5 | 0.0 | 29.2 |
| 3 | 1195.6 | 86.7 | 1.2 | 79.1 | 416 | 10.9 | 28.3 | 0.0 | 32.9 |
| 4 | 1195.6 | 84.1 | 1.6 | 68.2 | 480 | 11.4 | 74.3 | 0.0 | 39.5 |
| 5 | 1263.6 | 80.3 | 1.1 | 69.8 | 448 | 11.5 | 40.0 | 0.0 | 33.0 |
| 6 | 1263.6 | 80.7 | 1.5 | 70.6 | 448 | 12.1 | 37.6 | 0.0 | 43.5 |
| 7 | 1263.6 | 81.3 | 1.5 | 71.6 | 448 | 13.6 | 43.5 | 0.0 | 39.2 |
| 8 | 1303.6 | 78.3 | 1.3 | 78.7 | 384 | 11.2 | 39.5 | 0.0 | 37.0 |
| 9 | 1303.6 | 81.6 | 1.4 | 75.8 | 416 | 11.5 | 63.5 | 0.0 | 35.4 |
| 10 | 1303.6 | 84.7 | 1.5 | 73.9 | 448 | 12.5 | 36.7 | 0.0 | 34.3 |
| 11 | 1303.6 | 81.4 | 1.4 | 71.3 | 448 | 12.5 | 46.0 | 0.0 | 55.1 |
| 12 | 1303.6 | 77.5 | 1.5 | 65.4 | 480 | 13.1 | 40.1 | 0.0 | 40.8 |
| 13 | 1303.6 | 75.7 | 1.2 | 68.3 | 448 | 13.1 | 48.5 | 0.0 | 41.1 |
| 14 | 1303.6 | 80.1 | 1.4 | 70.7 | 448 | 13.6 | 83.7 | 0.0 | 52.0 |
| 15 | 1303.6 | 85.8 | 1.5 | 70.6 | 480 | 12.8 | 82.3 | 0.0 | 45.5 |
