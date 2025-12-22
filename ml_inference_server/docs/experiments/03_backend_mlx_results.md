# 03_backend_mlx

**Timestamp:** 2025-12-23 01:36:13

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 6400 | 12.09 | 60.4ms | 88.1ms | 114.9ms | 529.3 | 721.0 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 6400 pairs in 12.09s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 60.45 |
| Min | 41.06 |
| Max | 146.79 |
| Std Dev | 17.48 |
| P50 | 52.82 |
| P90 | 84.07 |
| P95 | 88.11 |
| P99 | 114.88 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 529.26 |
| Min | 218.00 |
| Max | 779.29 |
| Std Dev | 130.95 |
| P50 | 605.87 |
| P90 | 709.56 |
| P95 | 721.03 |
| P99 | 762.89 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 529.26 p/s | batch=32, conc=1 |
| Best Latency | 60.45ms | batch=32, conc=1 |
| Avg Throughput | 529.26 p/s | all configs |
| Avg Latency | 60.45ms | all configs |
