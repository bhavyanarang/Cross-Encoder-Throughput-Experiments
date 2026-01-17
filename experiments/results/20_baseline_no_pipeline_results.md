# Baseline Without Pipeline

_Baseline experiment with sequential tokenization and inference (no pipeline)_

**Timestamp:** 2025-12-28 23:42:26

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `pytorch` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 29.52 | 235.3ms | 309.2ms | 389.3ms | 542.0 | 167.2 |
| 32 | 8 | 3744 | 39.50 | 450.1ms | 620.9ms | 644.9ms | 94.8 | 115.8 |

## Detailed Metrics

### Run 1

**Total:** 16000 pairs in 29.52s

### Latency

| Metric | Value |
|--------|-------|
| Average | 235.31 |
| Min | 61.77 |
| Max | 411.36 |
| Std Dev | 41.10 |
| P50 | 225.94 |
| P90 | 284.90 |
| P95 | 309.16 |
| P99 | 389.35 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 541.97 |
| Min | 77.79 |
| Max | 518.06 |
| Std Dev | 26.78 |
| P50 | 141.63 |
| P90 | 162.35 |
| P95 | 167.22 |
| P99 | 177.81 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 225.9ms (P50) | 157.01 | 141.73 | 518.06 | 250 |
| 225.9-254.8ms (P50-P75) | 134.23 | 125.61 | 141.53 | 125 |
| 254.8-284.9ms (P75-P90) | 119.84 | 112.36 | 125.55 | 75 |
| >= 284.9ms (P90+) | 99.56 | 77.79 | 111.95 | 50 |

**Correlation:** -0.856 (negative correlation expected: lower latency = higher throughput)

### Run 2

**Total:** 3744 pairs in 39.50s

### Latency

| Metric | Value |
|--------|-------|
| Average | 450.08 |
| Min | 83.28 |
| Max | 653.03 |
| Std Dev | 120.96 |
| P50 | 452.05 |
| P90 | 606.74 |
| P95 | 620.86 |
| P99 | 644.95 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 94.78 |
| Min | 49.00 |
| Max | 384.25 |
| Std Dev | 41.67 |
| P50 | 70.79 |
| P90 | 109.49 |
| P95 | 115.78 |
| P99 | 262.19 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 452.1ms (P50) | 100.59 | 70.92 | 384.25 | 58 |
| 452.1-558.6ms (P50-P75) | 66.84 | 57.66 | 70.79 | 29 |
| 558.6-606.7ms (P75-P90) | 54.84 | 52.94 | 57.28 | 18 |
| >= 606.7ms (P90+) | 51.16 | 49.00 | 52.45 | 12 |

**Correlation:** -0.805 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 541.97 p/s | batch=32, conc=4 |
| Best Latency | 235.31ms | batch=32, conc=4 |
| Avg Throughput | 318.37 p/s | all configs |
| Avg Latency | 342.69ms | all configs |

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

Full time-series data is available in: `distribution/20_baseline_no_pipeline_timeseries.md`
