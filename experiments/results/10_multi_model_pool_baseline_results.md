# Multi-Model Pool Baseline (2x MPS, No Tokenizer Pool)

_Two MPS model instances with round-robin routing - baseline without tokenizer pool_

**Timestamp:** 2025-12-28 01:36:27

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 16 | 2 | 8000 | 12.03 | 48.0ms | 84.9ms | 105.9ms | 665.1 | 620.4 |
| 16 | 4 | 8000 | 10.92 | 87.1ms | 114.3ms | 129.5ms | 732.3 | 251.9 |
| 32 | 2 | 16000 | 24.28 | 97.1ms | 134.1ms | 162.0ms | 658.9 | 509.6 |
| 32 | 4 | 16000 | 25.37 | 202.3ms | 259.3ms | 283.7ms | 630.7 | 234.7 |
| 48 | 2 | 13632 | 63.88 | 163.6ms | 232.9ms | 284.7ms | 213.4 | 446.5 |

## Detailed Metrics

### Config 1: batch=16, concurrency=2

**Total:** 8000 pairs in 12.03s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 48.00 |
| Min | 21.96 |
| Max | 157.34 |
| Std Dev | 20.40 |
| P50 | 40.87 |
| P90 | 76.45 |
| P95 | 84.91 |
| P99 | 105.88 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 665.08 |
| Min | 101.69 |
| Max | 728.73 |
| Std Dev | 142.36 |
| P50 | 391.49 |
| P90 | 585.41 |
| P95 | 620.40 |
| P99 | 695.73 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 40.9ms (P50) | 510.99 | 392.22 | 728.73 | 250 |
| 40.9-62.5ms (P50-P75) | 322.18 | 256.17 | 390.76 | 125 |
| 62.5-76.4ms (P75-P90) | 232.74 | 209.44 | 254.87 | 75 |
| >= 76.4ms (P90+) | 181.68 | 101.69 | 208.09 | 50 |

**Correlation:** -0.922 (negative correlation expected: lower latency = higher throughput)

### Config 2: batch=16, concurrency=4

**Total:** 8000 pairs in 10.92s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 87.09 |
| Min | 53.10 |
| Max | 145.09 |
| Std Dev | 15.73 |
| P50 | 87.29 |
| P90 | 107.18 |
| P95 | 114.32 |
| P99 | 129.48 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 732.33 |
| Min | 110.28 |
| Max | 301.34 |
| Std Dev | 34.38 |
| P50 | 183.29 |
| P90 | 237.53 |
| P95 | 251.87 |
| P99 | 276.66 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 87.3ms (P50) | 217.15 | 183.32 | 301.34 | 250 |
| 87.3-97.3ms (P50-P75) | 174.65 | 164.47 | 183.27 | 125 |
| 97.3-107.2ms (P75-P90) | 158.65 | 149.29 | 164.36 | 75 |
| >= 107.2ms (P90+) | 137.10 | 110.28 | 149.19 | 50 |

**Correlation:** -0.972 (negative correlation expected: lower latency = higher throughput)

### Config 3: batch=32, concurrency=2

**Total:** 16000 pairs in 24.28s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 97.09 |
| Min | 41.76 |
| Max | 239.02 |
| Std Dev | 23.12 |
| P50 | 95.34 |
| P90 | 124.47 |
| P95 | 134.10 |
| P99 | 162.02 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 658.87 |
| Min | 133.88 |
| Max | 766.23 |
| Std Dev | 87.96 |
| P50 | 335.65 |
| P90 | 450.02 |
| P95 | 509.60 |
| P99 | 640.65 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 95.3ms (P50) | 411.69 | 335.65 | 766.23 | 250 |
| 95.3-108.7ms (P50-P75) | 316.89 | 294.64 | 335.65 | 125 |
| 108.7-124.5ms (P75-P90) | 272.41 | 257.13 | 293.63 | 75 |
| >= 124.5ms (P90+) | 229.11 | 133.88 | 256.80 | 50 |

**Correlation:** -0.919 (negative correlation expected: lower latency = higher throughput)

### Config 4: batch=32, concurrency=4

**Total:** 16000 pairs in 25.37s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 202.30 |
| Min | 90.74 |
| Max | 311.04 |
| Std Dev | 35.29 |
| P50 | 203.03 |
| P90 | 245.02 |
| P95 | 259.34 |
| P99 | 283.74 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 630.68 |
| Min | 102.88 |
| Max | 352.67 |
| Std Dev | 34.43 |
| P50 | 157.61 |
| P90 | 199.21 |
| P95 | 234.67 |
| P99 | 296.73 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 203.0ms (P50) | 186.86 | 157.63 | 352.67 | 250 |
| 203.0-224.3ms (P50-P75) | 150.97 | 142.68 | 157.60 | 125 |
| 224.3-245.0ms (P75-P90) | 136.98 | 130.63 | 142.64 | 75 |
| >= 245.0ms (P90+) | 121.68 | 102.88 | 130.34 | 50 |

**Correlation:** -0.949 (negative correlation expected: lower latency = higher throughput)

### Config 5: batch=48, concurrency=2

**Total:** 13632 pairs in 63.88s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 163.64 |
| Min | 61.18 |
| Max | 339.65 |
| Std Dev | 38.15 |
| P50 | 160.57 |
| P90 | 206.71 |
| P95 | 232.86 |
| P99 | 284.66 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 213.42 |
| Min | 141.32 |
| Max | 784.53 |
| Std Dev | 75.83 |
| P50 | 298.94 |
| P90 | 393.44 |
| P95 | 446.54 |
| P99 | 507.87 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 160.6ms (P50) | 363.84 | 299.62 | 784.53 | 142 |
| 160.6-182.4ms (P50-P75) | 281.64 | 263.43 | 298.27 | 71 |
| 182.4-206.7ms (P75-P90) | 248.20 | 233.76 | 262.41 | 42 |
| >= 206.7ms (P90+) | 200.92 | 141.32 | 231.55 | 29 |

**Correlation:** -0.918 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 732.33 p/s | batch=16, conc=4 |
| Best Latency | 48.00ms | batch=16, conc=2 |
| Avg Throughput | 580.07 p/s | all configs |
| Avg Latency | 119.62ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| GPU Utilization (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| CPU Usage (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Tokenization (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Inference (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/10_multi_model_pool_baseline_timeseries.md`
