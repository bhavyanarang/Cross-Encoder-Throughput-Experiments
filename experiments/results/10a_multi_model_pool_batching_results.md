# Multi-Model Pool (2x MPS) + Batching

_Two MPS model instances with round-robin routing and dynamic batching enabled_

**Timestamp:** 2026-01-02 00:33:50

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=8, timeout=100.0ms)

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 8 | 72320 | 63.79 | 439.0ms | 567.6ms | 600.0ms | 1133.8 | 1401.9 |

## Detailed Metrics

### Run 1

**Total:** 72320 pairs in 63.79s

### Latency

| Metric | Value |
|--------|-------|
| Average | 439.05 |
| Min | 36.48 |
| Max | 4034.47 |
| Std Dev | 286.89 |
| P50 | 551.80 |
| P90 | 564.97 |
| P95 | 567.59 |
| P99 | 600.03 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 1133.78 |
| Min | 15.86 |
| Max | 1754.29 |
| Std Dev | 514.85 |
| P50 | 115.98 |
| P90 | 1322.63 |
| P95 | 1401.93 |
| P99 | 1572.30 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 551.8ms (P50) | 711.82 | 115.98 | 1754.29 | 565 |
| 551.8-559.3ms (P50-P75) | 115.24 | 114.44 | 115.98 | 282 |
| 559.3-565.0ms (P75-P90) | 113.88 | 113.28 | 114.43 | 170 |
| >= 565.0ms (P90+) | 106.69 | 15.86 | 113.26 | 113 |

**Correlation:** -0.793 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 1133.78 p/s | batch=64, conc=8 |
| Best Latency | 439.05ms | batch=64, conc=8 |
| Avg Throughput | 1133.78 p/s | all configs |
| Avg Latency | 439.05ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1077.4 | 1058.4 | 1114.6 | 1074.6 | 1106.6 |
| GPU Utilization (%) | 20.4 | 0.0 | 42.1 | 24.2 | 29.0 |
| CPU Usage (%) | 4.0 | 1.1 | 8.6 | 3.7 | 7.1 |
| Tokenization (ms) | 5.6 | 0.0 | 35.0 | 4.9 | 7.0 |
| Inference (ms) | 15.3 | 0.0 | 165.9 | 10.8 | 21.1 |
| Queue Wait (ms) | 7.5 | 0.0 | 161.9 | 5.7 | 8.2 |
| Padding Waste (%) | 7.0 | 0.0 | 38.8 | 7.1 | 21.3 |

### Stage Timing

| Stage | Percentage |
|-------|------------|
| Tokenization | 1.1% |
| Queue Wait | 1.3% |
| Model Inference | 2.9% |
| Other/gRPC | 0.0% |

### Worker Metrics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 12.8 | 20.8 | 0.0 | 72640 |

Full time-series data is available in: `distribution/10a_multi_model_pool_batching_timeseries.md`
