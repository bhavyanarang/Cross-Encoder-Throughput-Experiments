# 07a_dynamic_batch_baseline

_Baseline with static batching (dynamic batching disabled)_

**Timestamp:** 2026-01-01 21:14:24

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 70.50 | 557.6ms | 578.0ms | 601.8ms | 227.0 | 58.4 |

## Detailed Metrics

### Run 1

**Total:** 16000 pairs in 70.50s

### Latency

| Metric | Value |
|--------|-------|
| Average | 557.57 |
| Min | 57.44 |
| Max | 2035.95 |
| Std Dev | 112.42 |
| P50 | 561.95 |
| P90 | 576.09 |
| P95 | 577.97 |
| P99 | 601.83 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 226.96 |
| Min | 15.72 |
| Max | 557.12 |
| Std Dev | 64.86 |
| P50 | 56.94 |
| P90 | 58.10 |
| P95 | 58.40 |
| P99 | 477.47 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 561.9ms (P50) | 77.53 | 56.94 | 557.12 | 250 |
| 561.9-570.6ms (P50-P75) | 56.55 | 56.09 | 56.94 | 125 |
| 570.6-576.1ms (P75-P90) | 55.82 | 55.55 | 56.08 | 75 |
| >= 576.1ms (P90+) | 53.10 | 15.72 | 55.54 | 50 |

**Correlation:** -0.703 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 226.96 p/s | batch=32, conc=4 |
| Best Latency | 557.57ms | batch=32, conc=4 |
| Avg Throughput | 226.96 p/s | all configs |
| Avg Latency | 557.57ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1219.7 | 1170.6 | 1324.6 | 1214.8 | 1324.6 |
| GPU Utilization (%) | 26.5 | 3.3 | 43.5 | 27.5 | 36.0 |
| CPU Usage (%) | 11.3 | 1.1 | 26.7 | 10.3 | 25.9 |
| Tokenization (ms) | 12.2 | 8.7 | 25.4 | 11.0 | 20.0 |
| Inference (ms) | 36.7 | 24.6 | 67.0 | 32.6 | 63.7 |
| Queue Wait (ms) | 12.3 | 8.8 | 25.6 | 11.1 | 20.3 |
| Padding Waste (%) | 42.1 | 31.0 | 58.0 | 42.1 | 52.4 |

### Stage Timing

| Stage | Percentage |
|-------|------------|
| Tokenization | 2.3% |
| Queue Wait | 2.4% |
| Model Inference | 7.0% |
| Other/gRPC | 0.0% |

### Worker Metrics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 38.7 | 64.1 | 0.0 | 16160 |

Full time-series data is available in: `distribution/07a_dynamic_batch_baseline_timeseries.md`
