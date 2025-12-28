# Multi-Model Pool (3x MPS)

_Three MPS model instances with round-robin routing for parallel inference_

**Timestamp:** 2025-12-28 19:37:53

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 16 | 2 | 8000 | 11.24 | 44.9ms | 75.1ms | 152.2ms | 711.7 | 643.3 |
| 16 | 4 | 8000 | 6.50 | 51.8ms | 70.6ms | 92.0ms | 1231.5 | 479.7 |
| 32 | 2 | 16000 | 16.48 | 65.8ms | 91.3ms | 100.2ms | 970.9 | 698.5 |
| 32 | 4 | 16000 | 12.85 | 102.5ms | 146.0ms | 168.5ms | 1244.9 | 483.5 |

## Detailed Metrics

### Run 1

**Total:** 8000 pairs in 11.24s

### Latency

| Metric | Value |
|--------|-------|
| Average | 44.87 |
| Min | 22.13 |
| Max | 217.22 |
| Std Dev | 24.00 |
| P50 | 36.37 |
| P90 | 66.26 |
| P95 | 75.09 |
| P99 | 152.16 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 711.67 |
| Min | 73.66 |
| Max | 722.94 |
| Std Dev | 144.62 |
| P50 | 439.88 |
| P90 | 618.14 |
| P95 | 643.35 |
| P99 | 703.96 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 36.4ms (P50) | 541.63 | 439.88 | 722.94 | 250 |
| 36.4-54.8ms (P50-P75) | 365.02 | 292.17 | 439.88 | 125 |
| 54.8-66.3ms (P75-P90) | 264.51 | 241.55 | 292.15 | 75 |
| >= 66.3ms (P90+) | 188.86 | 73.66 | 240.85 | 50 |

**Correlation:** -0.827 (negative correlation expected: lower latency = higher throughput)

### Run 2

**Total:** 8000 pairs in 6.50s

### Latency

| Metric | Value |
|--------|-------|
| Average | 51.83 |
| Min | 28.45 |
| Max | 121.61 |
| Std Dev | 12.63 |
| P50 | 51.41 |
| P90 | 66.86 |
| P95 | 70.59 |
| P99 | 91.96 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 1231.54 |
| Min | 131.57 |
| Max | 562.38 |
| Std Dev | 77.50 |
| P50 | 311.22 |
| P90 | 443.07 |
| P95 | 479.67 |
| P99 | 529.69 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 51.4ms (P50) | 386.42 | 311.37 | 562.38 | 250 |
| 51.4-58.6ms (P50-P75) | 292.63 | 273.00 | 311.08 | 125 |
| 58.6-66.9ms (P75-P90) | 257.66 | 239.35 | 272.98 | 75 |
| >= 66.9ms (P90+) | 213.45 | 131.57 | 238.79 | 50 |

**Correlation:** -0.936 (negative correlation expected: lower latency = higher throughput)

### Run 3

**Total:** 16000 pairs in 16.48s

### Latency

| Metric | Value |
|--------|-------|
| Average | 65.80 |
| Min | 39.94 |
| Max | 105.95 |
| Std Dev | 14.08 |
| P50 | 63.38 |
| P90 | 85.46 |
| P95 | 91.28 |
| P99 | 100.19 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 970.93 |
| Min | 302.02 |
| Max | 801.25 |
| Std Dev | 107.57 |
| P50 | 504.88 |
| P90 | 659.43 |
| P95 | 698.53 |
| P99 | 771.91 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 63.4ms (P50) | 597.34 | 505.91 | 801.25 | 250 |
| 63.4-75.6ms (P50-P75) | 461.67 | 423.44 | 503.85 | 125 |
| 75.6-85.5ms (P75-P90) | 400.60 | 374.46 | 422.45 | 75 |
| >= 85.5ms (P90+) | 345.22 | 302.02 | 374.16 | 50 |

**Correlation:** -0.971 (negative correlation expected: lower latency = higher throughput)

### Run 4

**Total:** 16000 pairs in 12.85s

### Latency

| Metric | Value |
|--------|-------|
| Average | 102.54 |
| Min | 55.45 |
| Max | 175.62 |
| Std Dev | 24.02 |
| P50 | 101.97 |
| P90 | 132.18 |
| P95 | 145.96 |
| P99 | 168.47 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 1244.89 |
| Min | 182.21 |
| Max | 577.11 |
| Std Dev | 80.49 |
| P50 | 313.82 |
| P90 | 456.25 |
| P95 | 483.48 |
| P99 | 521.16 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 102.0ms (P50) | 393.77 | 313.95 | 577.11 | 250 |
| 102.0-117.6ms (P50-P75) | 291.78 | 272.24 | 313.69 | 125 |
| 117.6-132.2ms (P75-P90) | 257.23 | 242.12 | 272.08 | 75 |
| >= 132.2ms (P90+) | 217.84 | 182.21 | 241.88 | 50 |

**Correlation:** -0.960 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 1244.89 p/s | batch=32, conc=4 |
| Best Latency | 44.87ms | batch=16, conc=2 |
| Avg Throughput | 1039.76 p/s | all configs |
| Avg Latency | 66.26ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1150.5 | 1076.6 | 1210.8 | 1152.8 | 1208.9 |
| GPU Utilization (%) | 98.0 | 12.5 | 100.0 | 100.0 | 100.0 |
| CPU Usage (%) | 37.3 | 1.4 | 51.2 | 37.1 | 49.9 |
| Tokenization (ms) | 9.4 | 4.5 | 58.3 | 9.9 | 13.8 |
| Inference (ms) | 48.7 | 14.6 | 139.1 | 46.3 | 89.1 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 39.4 | 21.8 | 51.3 | 40.0 | 48.6 |

### Stage Timing

| Stage | Percentage |
|-------|------------|
| Tokenization | 12.7% |
| Queue Wait | 0.0% |
| Model Inference | 0.0% |
| Other/gRPC | 0.1% |

### Worker Metrics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 1 | 60.3 | 103.8 | 1903.3 | 96112 |
| 0 | 68.7 | 131.4 | 1551.5 | 78112 |
| 2 | 70.1 | 130.6 | 1546.4 | 76160 |

Full time-series data is available in: `distribution/10_multi_model_pool_timeseries.md`
