# Multi-Model Pool (2x MPS)

_Two MPS model instances with round-robin routing for parallel inference_

**Timestamp:** 2025-12-26 02:23:11

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 16 | 1 | 1600 | 6.83 | 68.3ms | 119.6ms | 194.7ms | 234.1 | 540.2 |

## Detailed Metrics

### Config 1: batch=16, concurrency=1

**Total:** 1600 pairs in 6.83s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 68.32 |
| Min | 26.16 |
| Max | 239.88 |
| Std Dev | 34.87 |
| P50 | 66.94 |
| P90 | 99.19 |
| P95 | 119.57 |
| P99 | 194.67 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 234.13 |
| Min | 66.70 |
| Max | 611.53 |
| Std Dev | 126.93 |
| P50 | 239.02 |
| P90 | 498.51 |
| P95 | 540.20 |
| P99 | 583.58 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 66.9ms (P50) | 376.83 | 239.59 | 611.53 | 50 |
| 66.9-75.5ms (P50-P75) | 225.88 | 211.86 | 238.45 | 25 |
| 75.5-99.2ms (P75-P90) | 193.59 | 161.45 | 211.63 | 15 |
| >= 99.2ms (P90+) | 117.49 | 66.70 | 159.94 | 10 |

**Correlation:** -0.795 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 234.13 p/s | batch=16, conc=1 |
| Best Latency | 68.32ms | batch=16, conc=1 |
| Avg Throughput | 234.13 p/s | all configs |
| Avg Latency | 68.32ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1106.5 | 1077.6 | 1127.6 | 1111.6 | 1127.6 |
| GPU Utilization (%) | 81.1 | 40.1 | 91.6 | 82.6 | 90.5 |
| CPU Usage (%) | 1.3 | 0.8 | 1.7 | 1.3 | 1.6 |
| Tokenization (ms) | 6.6 | 6.2 | 7.1 | 6.5 | 7.1 |
| Inference (ms) | 56.0 | 17.6 | 163.8 | 54.7 | 97.9 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 37.1 | 27.1 | 48.3 | 36.5 | 47.6 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1077.6 | 40.1 | 1.2 | 74.7 | 96 | 7.0 | 17.6 | 0.0 | 31.4 |
| 1 | 1103.6 | 82.6 | 1.3 | 71.2 | 208 | 6.3 | 55.5 | 0.0 | 47.3 |
| 2 | 1103.6 | 84.6 | 1.1 | 67.8 | 224 | 6.7 | 69.7 | 0.0 | 42.8 |
| 3 | 1103.6 | 81.6 | 1.4 | 58.2 | 256 | 6.8 | 67.0 | 0.0 | 34.1 |
| 4 | 1127.6 | 87.0 | 1.5 | 55.5 | 288 | 6.3 | 63.3 | 0.0 | 34.4 |
| 5 | 1111.6 | 90.1 | 1.4 | 57.2 | 288 | 6.5 | 40.2 | 0.0 | 38.9 |
| 6 | 1111.6 | 80.8 | 1.3 | 54.8 | 272 | 6.5 | 54.7 | 0.0 | 29.0 |
| 7 | 1111.6 | 80.7 | 1.3 | 61.4 | 240 | 6.3 | 35.0 | 0.0 | 48.3 |
| 8 | 1127.6 | 82.3 | 0.8 | 83.4 | 176 | 7.1 | 68.3 | 0.0 | 27.1 |
| 9 | 1097.6 | 88.7 | 1.5 | 94.1 | 176 | 6.5 | 45.8 | 0.0 | 42.4 |
| 10 | 1093.6 | 79.6 | 1.2 | 78.7 | 208 | 7.0 | 23.7 | 0.0 | 36.5 |
| 11 | 1093.6 | 76.5 | 1.1 | 104.7 | 144 | 6.9 | 163.8 | 0.0 | 35.2 |
| 12 | 1111.6 | 91.6 | 1.5 | 94.0 | 176 | 6.5 | 67.5 | 0.0 | 38.3 |
| 13 | 1111.6 | 86.4 | 1.2 | 65.0 | 240 | 6.6 | 42.9 | 0.0 | 39.7 |
| 14 | 1111.6 | 84.1 | 1.7 | 56.9 | 272 | 6.2 | 25.2 | 0.0 | 30.5 |
