# 08_dynamic_batch_timeout_sweep_mlx_200ms

_Dynamic batching timeout sweep across backends and timeout values_

**Timestamp:** 2025-12-26 16:26:43

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=96, timeout=200ms)

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 23.86 | 190.4ms | 263.9ms | 414.2ms | 670.6 | 209.1 |

## Detailed Metrics

### Config 1: batch=32, concurrency=4

**Total:** 16000 pairs in 23.86s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 190.45 |
| Min | 102.92 |
| Max | 436.46 |
| Std Dev | 39.72 |
| P50 | 180.68 |
| P90 | 237.98 |
| P95 | 263.94 |
| P99 | 414.19 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 670.56 |
| Min | 73.32 |
| Max | 310.93 |
| Std Dev | 27.15 |
| P50 | 177.11 |
| P90 | 203.17 |
| P95 | 209.06 |
| P99 | 228.29 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 180.7ms (P50) | 193.19 | 177.13 | 310.93 | 250 |
| 180.7-201.7ms (P50-P75) | 169.17 | 158.72 | 177.10 | 125 |
| 201.7-238.0ms (P75-P90) | 150.74 | 134.49 | 158.57 | 75 |
| >= 238.0ms (P90+) | 118.13 | 73.32 | 134.27 | 50 |

**Correlation:** -0.933 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 670.56 p/s | batch=32, conc=4 |
| Best Latency | 190.45ms | batch=32, conc=4 |
| Avg Throughput | 670.56 p/s | all configs |
| Avg Latency | 190.45ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 3326.0 | 1086.6 | 4096.6 | 3630.6 | 4096.6 |
| GPU Utilization (%) | 97.5 | 13.0 | 100.0 | 100.0 | 100.0 |
| CPU Usage (%) | 1.7 | 0.7 | 2.3 | 1.7 | 2.2 |
| Tokenization (ms) | 45.2 | 11.3 | 67.3 | 44.4 | 57.8 |
| Inference (ms) | 136.9 | 27.0 | 371.0 | 125.8 | 186.7 |
| Queue Wait (ms) | 7.0 | 1.1 | 165.8 | 1.3 | 2.2 |
| Padding Waste (%) | 48.9 | 37.1 | 74.2 | 47.8 | 57.3 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 24.6% |
| Queue Wait | 2.0% |
| Model Inference | 72.7% |
| Other/gRPC | 0.7% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 187.4 | 260.2 | 658.1 | 16160 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/08_dynamic_batch_timeout_sweep_timeseries.md`
