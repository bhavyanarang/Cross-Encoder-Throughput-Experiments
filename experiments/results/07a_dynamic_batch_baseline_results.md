# 07a_dynamic_batch_baseline

_Baseline with static batching (dynamic batching disabled)_

**Timestamp:** 2025-12-26 16:17:03

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 24.72 | 197.1ms | 263.4ms | 289.8ms | 647.2 | 195.5 |

## Detailed Metrics

### Config 1: batch=32, concurrency=4

**Total:** 16000 pairs in 24.72s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 197.06 |
| Min | 42.62 |
| Max | 307.43 |
| Std Dev | 31.93 |
| P50 | 186.38 |
| P90 | 241.23 |
| P95 | 263.36 |
| P99 | 289.80 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 647.23 |
| Min | 104.09 |
| Max | 750.76 |
| Std Dev | 35.15 |
| P50 | 171.70 |
| P90 | 191.09 |
| P95 | 195.54 |
| P99 | 203.07 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 186.4ms (P50) | 187.31 | 172.03 | 750.76 | 250 |
| 186.4-214.5ms (P50-P75) | 159.61 | 149.22 | 171.36 | 125 |
| 214.5-241.2ms (P75-P90) | 142.38 | 132.70 | 148.94 | 75 |
| >= 241.2ms (P90+) | 120.32 | 104.09 | 132.21 | 50 |

**Correlation:** -0.801 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 647.23 p/s | batch=32, conc=4 |
| Best Latency | 197.06ms | batch=32, conc=4 |
| Avg Throughput | 647.23 p/s | all configs |
| Avg Latency | 197.06ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1311.8 | 1112.6 | 1356.8 | 1356.6 | 1356.8 |
| GPU Utilization (%) | 72.6 | 24.4 | 82.1 | 73.2 | 80.3 |
| CPU Usage (%) | 1.8 | 0.6 | 2.1 | 1.8 | 2.0 |
| Tokenization (ms) | 12.3 | 10.7 | 17.1 | 12.2 | 13.7 |
| Inference (ms) | 39.9 | 25.3 | 109.4 | 32.7 | 66.3 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 43.6 | 29.3 | 72.5 | 42.9 | 54.9 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 6.2% |
| Queue Wait | 0.0% |
| Model Inference | 18.9% |
| Other/gRPC | 74.9% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 194.8 | 261.3 | 636.1 | 16160 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/07a_dynamic_batch_baseline_timeseries.md`
