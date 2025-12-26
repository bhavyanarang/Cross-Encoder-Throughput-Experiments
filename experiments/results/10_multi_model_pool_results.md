# Multi-Model Pool (2x MPS)

_Two MPS model instances with round-robin routing for parallel inference_

**Timestamp:** 2025-12-26 16:35:28

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 16 | 2 | 8000 | 10.08 | 40.2ms | 69.5ms | 80.0ms | 793.4 | 669.1 |
| 16 | 4 | 8000 | 8.26 | 65.8ms | 93.4ms | 105.4ms | 968.8 | 317.3 |
| 32 | 2 | 16000 | 16.70 | 66.7ms | 98.7ms | 126.6ms | 958.2 | 746.2 |
| 32 | 4 | 16000 | 15.82 | 126.1ms | 169.5ms | 206.0ms | 1011.6 | 323.3 |

## Detailed Metrics

### Config 1: batch=16, concurrency=2

**Total:** 8000 pairs in 10.08s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 40.24 |
| Min | 21.31 |
| Max | 86.82 |
| Std Dev | 15.81 |
| P50 | 33.53 |
| P90 | 65.56 |
| P95 | 69.54 |
| P99 | 79.98 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 793.41 |
| Min | 184.30 |
| Max | 750.71 |
| Std Dev | 146.29 |
| P50 | 477.25 |
| P90 | 638.39 |
| P95 | 669.06 |
| P99 | 724.98 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 33.5ms (P50) | 574.58 | 478.09 | 750.71 | 250 |
| 33.5-54.6ms (P50-P75) | 410.75 | 292.90 | 476.40 | 125 |
| 54.6-65.6ms (P75-P90) | 267.55 | 244.17 | 292.62 | 75 |
| >= 65.6ms (P90+) | 224.79 | 184.30 | 242.94 | 50 |

**Correlation:** -0.957 (negative correlation expected: lower latency = higher throughput)

### Config 2: batch=16, concurrency=4

**Total:** 8000 pairs in 8.26s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 65.83 |
| Min | 44.00 |
| Max | 139.96 |
| Std Dev | 12.91 |
| P50 | 63.75 |
| P90 | 83.35 |
| P95 | 93.44 |
| P99 | 105.35 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 968.79 |
| Min | 114.32 |
| Max | 363.62 |
| Std Dev | 41.79 |
| P50 | 250.98 |
| P90 | 302.12 |
| P95 | 317.28 |
| P99 | 347.89 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 63.7ms (P50) | 282.64 | 251.21 | 363.62 | 250 |
| 63.7-69.6ms (P50-P75) | 240.27 | 230.04 | 250.75 | 125 |
| 69.6-83.3ms (P75-P90) | 217.51 | 192.16 | 230.01 | 75 |
| >= 83.3ms (P90+) | 168.86 | 114.32 | 190.22 | 50 |

**Correlation:** -0.958 (negative correlation expected: lower latency = higher throughput)

### Config 3: batch=32, concurrency=2

**Total:** 16000 pairs in 16.70s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 66.65 |
| Min | 37.88 |
| Max | 206.16 |
| Std Dev | 19.91 |
| P50 | 61.92 |
| P90 | 91.17 |
| P95 | 98.68 |
| P99 | 126.59 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 958.23 |
| Min | 155.22 |
| Max | 844.84 |
| Std Dev | 127.52 |
| P50 | 516.78 |
| P90 | 691.72 |
| P95 | 746.23 |
| P99 | 792.85 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 61.9ms (P50) | 617.73 | 516.81 | 844.84 | 250 |
| 61.9-76.5ms (P50-P75) | 471.13 | 418.44 | 516.75 | 125 |
| 76.5-91.2ms (P75-P90) | 382.66 | 351.03 | 417.79 | 75 |
| >= 91.2ms (P90+) | 308.22 | 155.22 | 350.54 | 50 |

**Correlation:** -0.913 (negative correlation expected: lower latency = higher throughput)

### Config 4: batch=32, concurrency=4

**Total:** 16000 pairs in 15.82s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 126.09 |
| Min | 77.55 |
| Max | 240.06 |
| Std Dev | 21.27 |
| P50 | 122.20 |
| P90 | 149.30 |
| P95 | 169.49 |
| P99 | 206.01 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 1011.55 |
| Min | 133.30 |
| Max | 412.66 |
| Std Dev | 37.82 |
| P50 | 261.87 |
| P90 | 301.21 |
| P95 | 323.31 |
| P99 | 356.47 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 122.2ms (P50) | 287.26 | 261.88 | 412.66 | 250 |
| 122.2-132.4ms (P50-P75) | 252.75 | 241.71 | 261.85 | 125 |
| 132.4-149.3ms (P75-P90) | 230.32 | 214.39 | 241.31 | 75 |
| >= 149.3ms (P90+) | 185.46 | 133.30 | 213.81 | 50 |

**Correlation:** -0.959 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 1011.55 p/s | batch=32, conc=4 |
| Best Latency | 40.24ms | batch=16, conc=2 |
| Avg Throughput | 933.00 p/s | all configs |
| Avg Latency | 74.70ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1206.7 | 1076.6 | 1308.8 | 1186.7 | 1268.8 |
| GPU Utilization (%) | 98.7 | 31.8 | 100.0 | 100.0 | 100.0 |
| CPU Usage (%) | 2.7 | 1.1 | 4.0 | 2.5 | 3.8 |
| Tokenization (ms) | 10.7 | 5.4 | 56.3 | 11.4 | 13.9 |
| Inference (ms) | 42.6 | 16.1 | 88.2 | 43.3 | 69.6 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 39.6 | 24.2 | 57.0 | 39.5 | 49.9 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 12.9% |
| Queue Wait | 0.0% |
| Model Inference | 54.5% |
| Other/gRPC | 32.6% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 74.0 | 134.2 | 450.3 | 23904 |
| 1 | 73.6 | 136.5 | 456.4 | 24176 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/10_multi_model_pool_timeseries.md`
