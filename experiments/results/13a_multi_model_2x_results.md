# 13a_multi_model_2x

_Two model instances in pool for parallel processing_

**Timestamp:** 2025-12-27 01:37:44

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `pytorch` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 25.39 | 202.5ms | 272.4ms | 310.8ms | 630.1 | 214.8 |

## Detailed Metrics

### Config 1: batch=32, concurrency=4

**Total:** 16000 pairs in 25.39s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 202.47 |
| Min | 55.71 |
| Max | 387.52 |
| Std Dev | 38.78 |
| P50 | 199.25 |
| P90 | 250.09 |
| P95 | 272.45 |
| P99 | 310.83 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 630.15 |
| Min | 82.58 |
| Max | 574.38 |
| Std Dev | 35.95 |
| P50 | 160.61 |
| P90 | 201.83 |
| P95 | 214.82 |
| P99 | 247.12 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 199.2ms (P50) | 188.51 | 160.62 | 574.38 | 250 |
| 199.2-223.8ms (P50-P75) | 152.00 | 142.98 | 160.59 | 125 |
| 223.8-250.1ms (P75-P90) | 136.14 | 128.01 | 142.98 | 75 |
| >= 250.1ms (P90+) | 115.28 | 82.58 | 127.48 | 50 |

**Correlation:** -0.894 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 630.15 p/s | batch=32, conc=4 |
| Best Latency | 202.47ms | batch=32, conc=4 |
| Avg Throughput | 630.15 p/s | all configs |
| Avg Latency | 202.47ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 1229.8 | 1110.6 | 1330.6 | 1212.6 | 1330.6 |
| GPU Utilization (%) | 98.6 | 39.6 | 100.0 | 100.0 | 100.0 |
| CPU Usage (%) | 1.9 | 1.1 | 4.2 | 1.9 | 2.3 |
| Tokenization (ms) | 14.9 | 11.9 | 25.0 | 13.5 | 22.7 |
| Inference (ms) | 81.2 | 44.4 | 172.0 | 79.2 | 112.4 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 41.8 | 29.1 | 58.2 | 41.7 | 49.0 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 7.6% |
| Queue Wait | 0.0% |
| Model Inference | 42.6% |
| Other/gRPC | 49.8% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 1 | 198.6 | 266.4 | 312.7 | 8192 |
| 0 | 202.1 | 276.2 | 305.8 | 7968 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/13a_multi_model_2x_timeseries.md`
