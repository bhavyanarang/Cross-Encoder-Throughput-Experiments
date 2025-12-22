# 02_backend_mps

**Timestamp:** 2025-12-23 01:35:04

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 6400 | 12.20 | 61.0ms | 90.0ms | 133.4ms | 524.8 | 724.8 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 6400 pairs in 12.20s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 60.96 |
| Min | 39.79 |
| Max | 160.57 |
| Std Dev | 18.80 |
| P50 | 52.33 |
| P90 | 85.48 |
| P95 | 89.98 |
| P99 | 133.35 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 524.79 |
| Min | 199.29 |
| Max | 804.24 |
| Std Dev | 134.53 |
| P50 | 611.46 |
| P90 | 714.02 |
| P95 | 724.76 |
| P99 | 779.83 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 524.79 p/s | batch=32, conc=1 |
| Best Latency | 60.96ms | batch=32, conc=1 |
| Avg Throughput | 524.79 p/s | all configs |
| Avg Latency | 60.96ms | all configs |
