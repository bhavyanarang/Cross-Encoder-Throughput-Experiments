# 09_dynamic_batch_max_batch_sweep_mlx_batch256

_Dynamic batching max batch size sweep across backends and batch sizes_

**Timestamp:** 2025-12-26 16:34:13

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mlx` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=256, timeout=50ms)

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 23.82 | 190.0ms | 258.9ms | 306.4ms | 671.6 | 202.5 |

## Detailed Metrics

### Config 1: batch=32, concurrency=4

**Total:** 16000 pairs in 23.82s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 189.99 |
| Min | 107.40 |
| Max | 463.69 |
| Std Dev | 36.94 |
| P50 | 180.74 |
| P90 | 227.66 |
| P95 | 258.88 |
| P99 | 306.39 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 671.63 |
| Min | 69.01 |
| Max | 297.94 |
| Std Dev | 25.21 |
| P50 | 177.05 |
| P90 | 200.29 |
| P95 | 202.53 |
| P99 | 213.39 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 180.7ms (P50) | 190.60 | 177.11 | 297.94 | 250 |
| 180.7-198.4ms (P50-P75) | 169.71 | 161.29 | 177.00 | 125 |
| 198.4-227.7ms (P75-P90) | 153.02 | 140.63 | 161.14 | 75 |
| >= 227.7ms (P90+) | 122.38 | 69.01 | 139.88 | 50 |

**Correlation:** -0.916 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 671.63 p/s | batch=32, conc=4 |
| Best Latency | 189.99ms | batch=32, conc=4 |
| Avg Throughput | 671.63 p/s | all configs |
| Avg Latency | 189.99ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 3541.3 | 1228.6 | 4310.6 | 3784.6 | 4310.6 |
| GPU Utilization (%) | 98.8 | 40.1 | 100.0 | 100.0 | 100.0 |
| CPU Usage (%) | 1.9 | 0.9 | 4.5 | 1.8 | 2.3 |
| Tokenization (ms) | 46.8 | 20.9 | 103.3 | 45.6 | 60.4 |
| Inference (ms) | 141.0 | 80.5 | 401.2 | 131.3 | 182.3 |
| Queue Wait (ms) | 1.3 | 1.1 | 2.5 | 1.3 | 1.8 |
| Padding Waste (%) | 48.0 | 36.7 | 74.8 | 47.7 | 56.3 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 24.9% |
| Queue Wait | 1.0% |
| Model Inference | 73.3% |
| Other/gRPC | 0.7% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 187.0 | 255.7 | 659.2 | 16160 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/09_dynamic_batch_max_batch_sweep_timeseries.md`
