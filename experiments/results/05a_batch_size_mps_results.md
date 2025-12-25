# 05a_batch_size_mps

_Sweep batch sizes on MPS backend_

**Timestamp:** 2025-12-26 02:18:47

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 800 | 4.84 | 48.4ms | 102.2ms | 178.8ms | 165.3 | 392.8 |

## Detailed Metrics

### Config 1: batch=8, concurrency=1

**Total:** 800 pairs in 4.84s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 48.39 |
| Min | 15.36 |
| Max | 193.34 |
| Std Dev | 31.58 |
| P50 | 46.66 |
| P90 | 69.42 |
| P95 | 102.21 |
| P99 | 178.80 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 165.27 |
| Min | 41.38 |
| Max | 520.88 |
| Std Dev | 109.02 |
| P50 | 171.52 |
| P90 | 360.59 |
| P95 | 392.83 |
| P99 | 493.43 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 46.7ms (P50) | 314.54 | 175.02 | 520.88 | 50 |
| 46.7-58.8ms (P50-P75) | 147.50 | 136.50 | 168.03 | 25 |
| 58.8-69.4ms (P75-P90) | 128.37 | 115.75 | 134.95 | 15 |
| >= 69.4ms (P90+) | 75.11 | 41.38 | 110.76 | 10 |

**Correlation:** -0.781 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 165.27 p/s | batch=8, conc=1 |
| Best Latency | 48.39ms | batch=8, conc=1 |
| Avg Throughput | 165.27 p/s | all configs |
| Avg Latency | 48.39ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1088.0 | 1081.6 | 1089.6 | 1089.6 | 1089.6 |
| GPU Utilization (%) | 78.3 | 33.2 | 89.7 | 82.7 | 89.1 |
| CPU Usage (%) | 2.2 | 1.6 | 6.1 | 1.8 | 4.3 |
| Tokenization (ms) | 4.7 | 3.8 | 8.7 | 4.4 | 6.9 |
| Inference (ms) | 44.9 | 15.4 | 108.4 | 37.7 | 97.1 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 31.7 | 15.9 | 41.6 | 34.0 | 40.5 |

## Dashboard Time-Series Data

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1081.6 | 33.2 | 1.7 | 42.1 | 72 | 3.8 | 46.8 | 0.0 | 25.9 |
| 1 | 1081.6 | 79.1 | 1.6 | 52.0 | 136 | 8.7 | 108.4 | 0.0 | 38.4 |
| 2 | 1089.6 | 89.7 | 1.7 | 58.2 | 136 | 4.4 | 51.8 | 0.0 | 35.0 |
| 3 | 1089.6 | 88.3 | 1.9 | 51.8 | 152 | 4.1 | 52.7 | 0.0 | 41.6 |
| 4 | 1089.6 | 86.7 | 2.0 | 40.2 | 200 | 4.4 | 28.6 | 0.0 | 39.2 |
| 5 | 1089.6 | 83.1 | 2.2 | 37.0 | 216 | 4.5 | 16.8 | 0.0 | 15.9 |
| 6 | 1089.6 | 82.2 | 2.0 | 35.5 | 216 | 4.6 | 23.1 | 0.0 | 37.8 |
| 7 | 1089.6 | 79.7 | 1.6 | 43.2 | 168 | 4.0 | 15.4 | 0.0 | 23.4 |
| 8 | 1089.6 | 76.0 | 1.7 | 60.8 | 120 | 4.0 | 83.2 | 0.0 | 33.0 |
| 9 | 1089.6 | 85.4 | 6.1 | 70.5 | 120 | 4.6 | 22.5 | 0.0 | 26.4 |
