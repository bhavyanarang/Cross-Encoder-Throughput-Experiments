# stress_queue_test

_Stress test to force queue buildup - high concurrency, single worker bottleneck_

**Timestamp:** 2026-01-01 04:21:20

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 128 | 64 | 22144 | 69.61 | 12113.2ms | 16045.8ms | 16080.4ms | 318.1 | 57.3 |

## Detailed Metrics

### Run 1

**Total:** 22144 pairs in 69.61s

### Latency

| Metric | Value |
|--------|-------|
| Average | 12113.18 |
| Min | 201.10 |
| Max | 16082.61 |
| Std Dev | 4425.52 |
| P50 | 13866.69 |
| P90 | 15686.26 |
| P95 | 16045.78 |
| P99 | 16080.39 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 318.12 |
| Min | 7.96 |
| Max | 636.51 |
| Std Dev | 59.25 |
| P50 | 9.23 |
| P90 | 31.92 |
| P95 | 57.26 |
| P99 | 289.13 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 13866.7ms (P50) | 35.45 | 9.23 | 636.51 | 86 |
| 13866.7-15278.0ms (P50-P75) | 8.73 | 8.43 | 9.23 | 43 |
| 15278.0-15686.3ms (P75-P90) | 8.23 | 8.16 | 8.38 | 26 |
| >= 15686.3ms (P90+) | 8.03 | 7.96 | 8.16 | 18 |

**Correlation:** -0.522 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 318.12 p/s | batch=128, conc=64 |
| Best Latency | 12113.18ms | batch=128, conc=64 |
| Avg Throughput | 318.12 p/s | all configs |
| Avg Latency | 12113.18ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1190.9 | 0.4 | 4368.6 | 0.4 | 3988.6 |
| GPU Utilization (%) | 31.9 | 0.0 | 100.0 | 0.0 | 100.0 |
| CPU Usage (%) | 11.7 | 0.1 | 85.5 | 0.7 | 45.1 |
| Tokenization (ms) | 53.5 | 0.0 | 60.4 | 56.2 | 56.2 |
| Inference (ms) | 291.8 | 0.0 | 348.1 | 348.1 | 348.1 |
| Queue Wait (ms) | 63.1 | 0.0 | 489.1 | 56.5 | 59.0 |
| Padding Waste (%) | 53.0 | 0.0 | 74.2 | 57.4 | 57.4 |

### Stage Timing

| Stage | Percentage |
|-------|------------|
| Tokenization | 2.4% |
| Queue Wait | 3.1% |
| Model Inference | 10.3% |
| Other/gRPC | 0.0% |

Full time-series data is available in: `distribution/stress_queue_test_timeseries.md`
