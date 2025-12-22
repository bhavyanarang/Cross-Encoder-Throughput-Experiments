# 01_backend_pytorch

**Timestamp:** 2025-12-23 01:33:36

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `pytorch`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 6400 | 12.35 | 61.7ms | 91.7ms | 128.7ms | 518.2 | 711.6 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 6400 pairs in 12.35s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 61.73 |
| Min | 41.54 |
| Max | 155.48 |
| Std Dev | 18.99 |
| P50 | 53.12 |
| P90 | 84.81 |
| P95 | 91.68 |
| P99 | 128.70 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 518.23 |
| Min | 205.82 |
| Max | 770.38 |
| Std Dev | 132.58 |
| P50 | 602.43 |
| P90 | 703.11 |
| P95 | 711.63 |
| P99 | 765.05 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 518.23 p/s | batch=32, conc=1 |
| Best Latency | 61.73ms | batch=32, conc=1 |
| Avg Throughput | 518.23 p/s | all configs |
| Avg Latency | 61.73ms | all configs |
