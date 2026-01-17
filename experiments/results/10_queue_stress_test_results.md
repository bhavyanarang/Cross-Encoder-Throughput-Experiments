# Queue Stress Test

_High concurrency with single tokenizer worker to observe queue growth_

**Timestamp:** 2026-01-01 05:11:04

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 256 | 16 | 22016 | 52.30 | 7930.2ms | 9492.0ms | 10078.2ms | 420.9 | 85.0 |

## Detailed Metrics

### Run 1

**Total:** 22016 pairs in 52.30s

### Latency

| Metric | Value |
|--------|-------|
| Average | 7930.16 |
| Min | 658.53 |
| Max | 10134.26 |
| Std Dev | 1953.43 |
| P50 | 8452.81 |
| P90 | 9362.65 |
| P95 | 9492.03 |
| P99 | 10078.22 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 420.94 |
| Min | 25.26 |
| Max | 388.74 |
| Std Dev | 46.01 |
| P50 | 30.29 |
| P90 | 50.41 |
| P95 | 84.98 |
| P99 | 243.98 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 8452.8ms (P50) | 53.85 | 30.30 | 388.74 | 43 |
| 8452.8-8818.1ms (P50-P75) | 29.51 | 29.12 | 30.27 | 21 |
| 8818.1-9362.6ms (P75-P90) | 28.22 | 27.41 | 29.00 | 13 |
| >= 9362.6ms (P90+) | 26.49 | 25.26 | 27.28 | 9 |

**Correlation:** -0.784 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 420.94 p/s | batch=256, conc=16 |
| Best Latency | 7930.16ms | batch=256, conc=16 |
| Avg Throughput | 420.94 p/s | all configs |
| Avg Latency | 7930.16ms | all configs |

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

Full time-series data is available in: `distribution/10_queue_stress_test_timeseries.md`
