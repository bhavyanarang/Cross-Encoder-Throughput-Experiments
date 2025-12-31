# Multi-Model Pool (2x MPS)

_Two MPS model instances with round-robin routing for parallel inference_

**Timestamp:** 2025-12-28 23:16:07

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 2 | 16000 | 24.20 | 96.6ms | 140.9ms | 175.5ms | 661.1 | 535.6 |
| 64 | 2 | 19072 | 30.53 | 198.7ms | 284.3ms | 301.4ms | 624.7 | 496.0 |

## Detailed Metrics

### Run 1

**Total:** 16000 pairs in 24.20s

### Latency

| Metric | Value |
|--------|-------|
| Average | 96.61 |
| Min | 45.38 |
| Max | 232.59 |
| Std Dev | 26.33 |
| P50 | 91.58 |
| P90 | 129.14 |
| P95 | 140.89 |
| P99 | 175.53 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 661.10 |
| Min | 137.58 |
| Max | 705.10 |
| Std Dev | 92.41 |
| P50 | 349.43 |
| P90 | 484.52 |
| P95 | 535.64 |
| P99 | 589.78 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 91.6ms (P50) | 427.07 | 349.93 | 705.10 | 250 |
| 91.6-111.8ms (P50-P75) | 318.29 | 286.24 | 348.93 | 125 |
| 111.8-129.1ms (P75-P90) | 265.44 | 247.93 | 285.99 | 75 |
| >= 129.1ms (P90+) | 217.70 | 137.58 | 246.68 | 50 |

**Correlation:** -0.931 (negative correlation expected: lower latency = higher throughput)

### Run 2

**Total:** 19072 pairs in 30.53s

### Latency

| Metric | Value |
|--------|-------|
| Average | 198.65 |
| Min | 105.23 |
| Max | 320.80 |
| Std Dev | 44.04 |
| P50 | 197.76 |
| P90 | 260.62 |
| P95 | 284.29 |
| P99 | 301.38 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 624.67 |
| Min | 199.50 |
| Max | 608.18 |
| Std Dev | 79.84 |
| P50 | 323.62 |
| P90 | 445.02 |
| P95 | 496.00 |
| P99 | 564.14 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 197.8ms (P50) | 400.73 | 324.01 | 608.18 | 149 |
| 197.8-225.8ms (P50-P75) | 303.25 | 283.84 | 323.23 | 74 |
| 225.8-260.6ms (P75-P90) | 269.02 | 246.13 | 283.29 | 45 |
| >= 260.6ms (P90+) | 226.75 | 199.50 | 244.27 | 30 |

**Correlation:** -0.958 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 661.10 p/s | batch=32, conc=2 |
| Best Latency | 96.61ms | batch=32, conc=2 |
| Avg Throughput | 642.89 p/s | all configs |
| Avg Latency | 147.63ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| GPU Utilization (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| CPU Usage (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Tokenization (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Inference (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

Full time-series data is available in: `distribution/10_multi_model_pool_timeseries.md`
