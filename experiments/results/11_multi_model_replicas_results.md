# Multi-Model Replicas (3x MPS)

_3 model replicas with first-idle routing for max throughput_

**Timestamp:** 2025-12-26 16:41:03

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 14.52 | 115.7ms | 185.8ms | 242.5ms | 1102.1 | 476.0 |
| 32 | 8 | 16000 | 13.32 | 211.6ms | 264.0ms | 283.4ms | 1200.8 | 184.3 |
| 32 | 12 | 16000 | 13.75 | 325.6ms | 401.0ms | 487.4ms | 1163.3 | 117.1 |
| 64 | 4 | 32000 | 29.01 | 231.6ms | 329.6ms | 414.8ms | 1103.1 | 433.2 |
| 64 | 8 | 32000 | 28.49 | 453.2ms | 572.8ms | 628.6ms | 1123.4 | 175.5 |
| 64 | 12 | 32000 | 28.84 | 685.9ms | 820.0ms | 893.6ms | 1109.4 | 113.3 |
| 128 | 4 | 12544 | 39.77 | 489.0ms | 668.9ms | 805.2ms | 315.4 | 367.4 |

## Detailed Metrics

### Config 1: batch=32, concurrency=4

**Total:** 16000 pairs in 14.52s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 115.73 |
| Min | 42.03 |
| Max | 274.58 |
| Std Dev | 35.46 |
| P50 | 111.28 |
| P90 | 158.51 |
| P95 | 185.75 |
| P99 | 242.50 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 1102.08 |
| Min | 116.54 |
| Max | 761.28 |
| Std Dev | 92.88 |
| P50 | 287.56 |
| P90 | 410.91 |
| P95 | 476.04 |
| P99 | 589.93 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 111.3ms (P50) | 368.41 | 287.88 | 761.28 | 250 |
| 111.3-131.3ms (P50-P75) | 267.37 | 244.26 | 287.25 | 125 |
| 131.3-158.5ms (P75-P90) | 224.31 | 201.88 | 241.91 | 75 |
| >= 158.5ms (P90+) | 170.55 | 116.54 | 201.81 | 50 |

**Correlation:** -0.887 (negative correlation expected: lower latency = higher throughput)

### Config 2: batch=32, concurrency=8

**Total:** 16000 pairs in 13.32s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 211.63 |
| Min | 83.18 |
| Max | 355.93 |
| Std Dev | 29.45 |
| P50 | 207.88 |
| P90 | 249.85 |
| P95 | 264.03 |
| P99 | 283.41 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 1200.80 |
| Min | 89.91 |
| Max | 384.70 |
| Std Dev | 23.54 |
| P50 | 153.94 |
| P90 | 178.17 |
| P95 | 184.30 |
| P99 | 203.08 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 207.9ms (P50) | 170.69 | 153.97 | 384.70 | 250 |
| 207.9-228.5ms (P50-P75) | 147.50 | 140.08 | 153.90 | 125 |
| 228.5-249.8ms (P75-P90) | 134.03 | 128.10 | 140.06 | 75 |
| >= 249.8ms (P90+) | 119.48 | 89.91 | 127.90 | 50 |

**Correlation:** -0.936 (negative correlation expected: lower latency = higher throughput)

### Config 3: batch=32, concurrency=12

**Total:** 16000 pairs in 13.75s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 325.59 |
| Min | 85.85 |
| Max | 632.50 |
| Std Dev | 48.38 |
| P50 | 321.13 |
| P90 | 374.94 |
| P95 | 401.03 |
| P99 | 487.36 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 1163.27 |
| Min | 50.59 |
| Max | 372.73 |
| Std Dev | 21.72 |
| P50 | 99.65 |
| P90 | 113.69 |
| P95 | 117.08 |
| P99 | 154.08 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 321.1ms (P50) | 111.37 | 99.69 | 372.73 | 250 |
| 321.1-345.5ms (P50-P75) | 96.52 | 92.64 | 99.61 | 125 |
| 345.5-374.9ms (P75-P90) | 89.21 | 85.35 | 92.59 | 75 |
| >= 374.9ms (P90+) | 77.06 | 50.59 | 85.34 | 50 |

**Correlation:** -0.812 (negative correlation expected: lower latency = higher throughput)

### Config 4: batch=64, concurrency=4

**Total:** 32000 pairs in 29.01s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 231.55 |
| Min | 92.71 |
| Max | 560.24 |
| Std Dev | 58.74 |
| P50 | 224.38 |
| P90 | 298.24 |
| P95 | 329.58 |
| P99 | 414.83 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 1103.12 |
| Min | 114.24 |
| Max | 690.34 |
| Std Dev | 73.97 |
| P50 | 285.22 |
| P90 | 395.93 |
| P95 | 433.20 |
| P99 | 512.02 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 224.4ms (P50) | 349.48 | 285.40 | 690.34 | 250 |
| 224.4-262.5ms (P50-P75) | 263.22 | 243.94 | 285.04 | 125 |
| 262.5-298.2ms (P75-P90) | 230.00 | 214.86 | 243.42 | 75 |
| >= 298.2ms (P90+) | 186.47 | 114.24 | 212.20 | 50 |

**Correlation:** -0.922 (negative correlation expected: lower latency = higher throughput)

### Config 5: batch=64, concurrency=8

**Total:** 32000 pairs in 28.49s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 453.20 |
| Min | 148.52 |
| Max | 858.70 |
| Std Dev | 70.43 |
| P50 | 442.97 |
| P90 | 542.04 |
| P95 | 572.78 |
| P99 | 628.58 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 1123.35 |
| Min | 74.53 |
| Max | 430.93 |
| Std Dev | 24.91 |
| P50 | 144.48 |
| P90 | 169.28 |
| P95 | 175.51 |
| P99 | 189.89 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 443.0ms (P50) | 161.90 | 144.55 | 430.93 | 250 |
| 443.0-493.5ms (P50-P75) | 137.11 | 129.77 | 144.41 | 125 |
| 493.5-542.0ms (P75-P90) | 123.99 | 118.08 | 129.39 | 75 |
| >= 542.0ms (P90+) | 109.16 | 74.53 | 118.01 | 50 |

**Correlation:** -0.910 (negative correlation expected: lower latency = higher throughput)

### Config 6: batch=64, concurrency=12

**Total:** 32000 pairs in 28.84s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 685.88 |
| Min | 165.79 |
| Max | 1035.44 |
| Std Dev | 89.03 |
| P50 | 681.89 |
| P90 | 790.22 |
| P95 | 820.02 |
| P99 | 893.62 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 1109.43 |
| Min | 61.81 |
| Max | 386.03 |
| Std Dev | 21.91 |
| P50 | 93.86 |
| P90 | 108.62 |
| P95 | 113.26 |
| P99 | 156.57 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 681.9ms (P50) | 105.59 | 93.86 | 386.03 | 250 |
| 681.9-736.8ms (P50-P75) | 90.41 | 86.87 | 93.85 | 125 |
| 736.8-790.2ms (P75-P90) | 83.99 | 81.01 | 86.83 | 75 |
| >= 790.2ms (P90+) | 76.86 | 61.81 | 80.82 | 50 |

**Correlation:** -0.835 (negative correlation expected: lower latency = higher throughput)

### Config 7: batch=128, concurrency=4

**Total:** 12544 pairs in 39.77s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 489.02 |
| Min | 292.77 |
| Max | 884.76 |
| Std Dev | 111.37 |
| P50 | 465.72 |
| P90 | 614.56 |
| P95 | 668.92 |
| P99 | 805.20 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 315.39 |
| Min | 144.67 |
| Max | 437.20 |
| Std Dev | 58.90 |
| P50 | 274.85 |
| P90 | 355.18 |
| P95 | 367.42 |
| P99 | 401.91 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 465.7ms (P50) | 323.23 | 276.25 | 437.20 | 49 |
| 465.7-559.7ms (P50-P75) | 248.98 | 228.75 | 273.45 | 24 |
| 559.7-614.6ms (P75-P90) | 218.54 | 209.01 | 228.68 | 15 |
| >= 614.6ms (P90+) | 182.17 | 144.67 | 206.59 | 10 |

**Correlation:** -0.961 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 1200.80 p/s | batch=32, conc=8 |
| Best Latency | 115.73ms | batch=32, conc=4 |
| Avg Throughput | 1016.78 p/s | all configs |
| Avg Latency | 358.94ms | all configs |

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

Full time-series data is available in: `distribution/11_multi_model_replicas_timeseries.md`
