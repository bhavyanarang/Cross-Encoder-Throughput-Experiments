# 14_optimized_production

_Production-optimized config: MLX + Length-Aware Batching_

**Timestamp:** 2025-12-27 01:42:26

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `pytorch` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=256, timeout=200ms)

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 16000 | 28.33 | 56.6ms | 90.3ms | 103.4ms | 564.7 | 702.2 |
| 48 | 1 | 24000 | 37.36 | 74.6ms | 99.2ms | 127.7ms | 642.4 | 766.3 |
| 64 | 1 | 32000 | 48.84 | 97.6ms | 114.9ms | 138.4ms | 655.2 | 767.9 |
| 96 | 1 | 40800 | 60.04 | 141.1ms | 175.3ms | 192.1ms | 679.6 | 741.7 |

## Detailed Metrics

### Config 1: batch=32, concurrency=1

**Total:** 16000 pairs in 28.33s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 56.57 |
| Min | 39.72 |
| Max | 156.58 |
| Std Dev | 14.49 |
| P50 | 51.42 |
| P90 | 81.66 |
| P95 | 90.33 |
| P99 | 103.39 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 564.67 |
| Min | 204.37 |
| Max | 805.59 |
| Std Dev | 105.67 |
| P50 | 622.34 |
| P90 | 687.27 |
| P95 | 702.16 |
| P99 | 735.39 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 51.4ms (P50) | 665.97 | 622.35 | 805.59 | 250 |
| 51.4-57.0ms (P50-P75) | 597.43 | 562.01 | 622.33 | 125 |
| 57.0-81.7ms (P75-P90) | 498.77 | 392.16 | 561.14 | 75 |
| >= 81.7ms (P90+) | 346.63 | 204.37 | 389.37 | 50 |

**Correlation:** -0.966 (negative correlation expected: lower latency = higher throughput)

### Config 2: batch=48, concurrency=1

**Total:** 24000 pairs in 37.36s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 74.64 |
| Min | 56.22 |
| Max | 205.73 |
| Std Dev | 15.27 |
| P50 | 70.17 |
| P90 | 92.81 |
| P95 | 99.25 |
| P99 | 127.74 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 642.36 |
| Min | 233.32 |
| Max | 853.79 |
| Std Dev | 91.42 |
| P50 | 684.07 |
| P90 | 750.86 |
| P95 | 766.31 |
| P99 | 783.66 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 70.2ms (P50) | 722.71 | 684.19 | 853.79 | 250 |
| 70.2-74.6ms (P50-P75) | 666.41 | 643.90 | 683.96 | 125 |
| 74.6-92.8ms (P75-P90) | 582.04 | 517.34 | 643.67 | 75 |
| >= 92.8ms (P90+) | 454.36 | 233.32 | 515.65 | 50 |

**Correlation:** -0.941 (negative correlation expected: lower latency = higher throughput)

### Config 3: batch=64, concurrency=1

**Total:** 32000 pairs in 48.84s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 97.57 |
| Min | 78.61 |
| Max | 200.61 |
| Std Dev | 11.21 |
| P50 | 96.13 |
| P90 | 108.75 |
| P95 | 114.94 |
| P99 | 138.37 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 655.21 |
| Min | 319.02 |
| Max | 814.10 |
| Std Dev | 65.51 |
| P50 | 665.77 |
| P90 | 730.17 |
| P95 | 767.92 |
| P99 | 806.56 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 96.1ms (P50) | 713.12 | 665.92 | 814.10 | 250 |
| 96.1-102.5ms (P50-P75) | 645.82 | 624.21 | 665.62 | 125 |
| 102.5-108.8ms (P75-P90) | 608.44 | 588.52 | 624.16 | 75 |
| >= 108.8ms (P90+) | 539.21 | 319.02 | 588.31 | 50 |

**Correlation:** -0.967 (negative correlation expected: lower latency = higher throughput)

### Config 4: batch=96, concurrency=1

**Total:** 40800 pairs in 60.04s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 141.09 |
| Min | 116.35 |
| Max | 242.39 |
| Std Dev | 14.28 |
| P50 | 136.31 |
| P90 | 154.59 |
| P95 | 175.28 |
| P99 | 192.08 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 679.60 |
| Min | 396.06 |
| Max | 825.09 |
| Std Dev | 57.37 |
| P50 | 704.28 |
| P90 | 730.56 |
| P95 | 741.73 |
| P99 | 803.97 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 136.3ms (P50) | 724.65 | 704.41 | 825.09 | 212 |
| 136.3-144.4ms (P50-P75) | 687.41 | 665.58 | 704.28 | 106 |
| 144.4-154.6ms (P75-P90) | 644.61 | 621.01 | 664.96 | 64 |
| >= 154.6ms (P90+) | 555.03 | 396.06 | 621.01 | 43 |

**Correlation:** -0.984 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 679.60 p/s | batch=96, conc=1 |
| Best Latency | 56.57ms | batch=32, conc=1 |
| Avg Throughput | 635.46 p/s | all configs |
| Avg Latency | 92.47ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1132.0 | 1100.6 | 1228.6 | 1134.6 | 1194.6 |
| GPU Utilization (%) | 69.9 | 30.8 | 84.0 | 70.0 | 77.0 |
| CPU Usage (%) | 1.4 | 0.7 | 10.7 | 1.3 | 1.6 |
| Tokenization (ms) | 26.1 | 11.6 | 74.1 | 24.6 | 38.1 |
| Inference (ms) | 71.8 | 30.6 | 148.0 | 70.6 | 110.4 |
| Queue Wait (ms) | 1.3 | 1.1 | 1.4 | 1.3 | 1.3 |
| Padding Waste (%) | 40.3 | 28.1 | 47.8 | 40.6 | 45.0 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 26.3% |
| Queue Wait | 1.5% |
| Model Inference | 71.3% |
| Other/gRPC | 1.0% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 89.4 | 145.3 | 318.8 | 56416 |
| 1 | 89.9 | 146.7 | 319.8 | 56544 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/14_optimized_production_timeseries.md`
