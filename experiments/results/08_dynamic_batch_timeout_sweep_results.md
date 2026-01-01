# 08_dynamic_batch_timeout_sweep_mps_10ms

_Dynamic batching timeout sweep across backends and timeout values_

**Timestamp:** 2026-01-01 21:18:55

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=96, timeout=10ms)

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 12256 | 54.42 | 560.1ms | 578.0ms | 597.0ms | 225.2 | 58.3 |

## Detailed Metrics

### Run 1

**Total:** 12256 pairs in 54.42s

### Latency

| Metric | Value |
|--------|-------|
| Average | 560.13 |
| Min | 48.22 |
| Max | 2026.03 |
| Std Dev | 115.40 |
| P50 | 559.46 |
| P90 | 574.12 |
| P95 | 578.03 |
| P99 | 597.00 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 225.22 |
| Min | 15.79 |
| Max | 663.62 |
| Std Dev | 64.51 |
| P50 | 57.20 |
| P90 | 58.15 |
| P95 | 58.27 |
| P99 | 489.28 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 559.5ms (P50) | 75.11 | 57.21 | 663.62 | 191 |
| 559.5-568.1ms (P50-P75) | 56.79 | 56.33 | 57.20 | 96 |
| 568.1-574.1ms (P75-P90) | 56.06 | 55.74 | 56.32 | 57 |
| >= 574.1ms (P90+) | 52.61 | 15.79 | 55.74 | 39 |

**Correlation:** -0.622 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 225.22 p/s | batch=32, conc=4 |
| Best Latency | 560.13ms | batch=32, conc=4 |
| Avg Throughput | 225.22 p/s | all configs |
| Avg Latency | 560.13ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1226.8 | 1058.4 | 1324.6 | 1214.8 | 1324.6 |
| GPU Utilization (%) | 27.9 | 0.0 | 62.3 | 29.1 | 42.3 |
| CPU Usage (%) | 10.7 | 0.6 | 30.4 | 8.9 | 24.4 |
| Tokenization (ms) | 11.3 | 0.0 | 22.4 | 10.8 | 14.3 |
| Inference (ms) | 36.0 | 0.0 | 68.2 | 31.7 | 61.8 |
| Queue Wait (ms) | 11.8 | 0.0 | 40.9 | 10.9 | 15.1 |
| Padding Waste (%) | 40.9 | 0.0 | 58.3 | 41.2 | 52.7 |

### Stage Timing

| Stage | Percentage |
|-------|------------|
| Tokenization | 2.3% |
| Queue Wait | 2.3% |
| Model Inference | 7.4% |
| Other/gRPC | 0.0% |

### Worker Metrics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 41.1 | 68.0 | 0.0 | 12416 |
