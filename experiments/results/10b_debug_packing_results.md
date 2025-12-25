# 10b_debug_packing

_Debug sequence packing with minimal requests_

**Timestamp:** 2025-12-26 02:23:31

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 4 | 1 | 400 | 3.56 | 35.6ms | 52.9ms | 57.4ms | 112.4 | 231.1 |

## Detailed Metrics

### Config 1: batch=4, concurrency=1

**Total:** 400 pairs in 3.56s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 35.58 |
| Min | 12.25 |
| Max | 66.04 |
| Std Dev | 13.86 |
| P50 | 42.20 |
| P90 | 49.65 |
| P95 | 52.94 |
| P99 | 57.41 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 112.38 |
| Min | 60.57 |
| Max | 326.46 |
| Std Dev | 63.56 |
| P50 | 94.79 |
| P90 | 219.54 |
| P95 | 231.05 |
| P99 | 260.22 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 42.2ms (P50) | 188.01 | 94.86 | 326.46 | 50 |
| 42.2-47.2ms (P50-P75) | 90.25 | 84.71 | 94.72 | 25 |
| 47.2-49.7ms (P75-P90) | 82.86 | 80.70 | 84.69 | 15 |
| >= 49.7ms (P90+) | 74.12 | 60.57 | 79.37 | 10 |

**Correlation:** -0.969 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 112.38 p/s | batch=4, conc=1 |
| Best Latency | 35.58ms | batch=4, conc=1 |
| Avg Throughput | 112.38 p/s | all configs |
| Avg Latency | 35.58ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1084.6 | 1071.6 | 1087.6 | 1087.6 | 1087.6 |
| GPU Utilization (%) | 83.9 | 46.2 | 92.7 | 88.7 | 92.4 |
| CPU Usage (%) | 2.2 | 1.7 | 2.7 | 2.2 | 2.7 |
| Tokenization (ms) | 2.6 | 2.2 | 2.8 | 2.6 | 2.8 |
| Inference (ms) | 38.4 | 13.1 | 62.0 | 41.5 | 57.3 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 29.9 | 18.1 | 37.0 | 30.8 | 36.7 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1071.6 | 46.2 | 2.6 | 45.5 | 44 | 2.8 | 43.4 | 0.0 | 26.2 |
| 1 | 1079.6 | 91.9 | 1.8 | 43.3 | 92 | 2.5 | 39.1 | 0.0 | 24.6 |
| 2 | 1087.6 | 92.7 | 1.7 | 41.9 | 96 | 2.8 | 62.0 | 0.0 | 28.7 |
| 3 | 1087.6 | 90.6 | 1.9 | 41.1 | 96 | 2.3 | 39.7 | 0.0 | 35.2 |
| 4 | 1087.6 | 89.3 | 2.1 | 36.3 | 108 | 2.6 | 46.3 | 0.0 | 37.0 |
| 5 | 1087.6 | 87.8 | 2.5 | 30.7 | 128 | 2.2 | 14.9 | 0.0 | 36.2 |
| 6 | 1087.6 | 84.8 | 2.3 | 28.9 | 132 | 2.6 | 13.1 | 0.0 | 18.1 |
| 7 | 1087.6 | 88.1 | 2.7 | 27.8 | 144 | 2.8 | 48.6 | 0.0 | 32.9 |
