# Pipeline Mode Baseline

_Baseline experiment with decoupled tokenization and inference pipeline_

**Timestamp:** 2025-12-29 01:02:05

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `pytorch` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 2 | 16000 | 29.47 | 117.6ms | 169.0ms | 209.8ms | 542.9 | 346.6 |
| 64 | 2 | 27328 | 54.02 | 245.6ms | 308.3ms | 329.8ms | 505.9 | 312.2 |

## Detailed Metrics

### Run 1

**Total:** 16000 pairs in 29.47s

### Latency

| Metric | Value |
|--------|-------|
| Average | 117.61 |
| Min | 67.59 |
| Max | 314.21 |
| Std Dev | 26.69 |
| P50 | 110.54 |
| P90 | 151.15 |
| P95 | 168.95 |
| P99 | 209.81 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 542.91 |
| Min | 101.84 |
| Max | 473.44 |
| Std Dev | 49.19 |
| P50 | 289.48 |
| P90 | 334.92 |
| P95 | 346.59 |
| P99 | 382.78 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 110.5ms (P50) | 320.08 | 289.49 | 473.44 | 250 |
| 110.5-125.5ms (P50-P75) | 273.01 | 254.97 | 289.48 | 125 |
| 125.5-151.1ms (P75-P90) | 239.94 | 211.74 | 254.78 | 75 |
| >= 151.1ms (P90+) | 182.66 | 101.84 | 211.48 | 50 |

**Correlation:** -0.939 (negative correlation expected: lower latency = higher throughput)

### Run 2

**Total:** 27328 pairs in 54.02s

### Latency

| Metric | Value |
|--------|-------|
| Average | 245.63 |
| Min | 184.10 |
| Max | 346.24 |
| Std Dev | 29.93 |
| P50 | 240.10 |
| P90 | 287.44 |
| P95 | 308.33 |
| P99 | 329.83 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 505.91 |
| Min | 184.84 |
| Max | 347.64 |
| Std Dev | 30.34 |
| P50 | 266.55 |
| P90 | 300.21 |
| P95 | 312.25 |
| P99 | 332.47 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 240.1ms (P50) | 288.18 | 266.61 | 347.64 | 213 |
| 240.1-260.5ms (P50-P75) | 256.41 | 245.71 | 266.55 | 107 |
| 260.5-287.4ms (P75-P90) | 235.76 | 223.29 | 245.61 | 64 |
| >= 287.4ms (P90+) | 207.18 | 184.84 | 221.72 | 43 |

**Correlation:** -0.987 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 542.91 p/s | batch=32, conc=2 |
| Best Latency | 117.61ms | batch=32, conc=2 |
| Avg Throughput | 524.41 p/s | all configs |
| Avg Latency | 181.62ms | all configs |

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

Full time-series data is available in: `distribution/20_pipeline_baseline_timeseries.md`
