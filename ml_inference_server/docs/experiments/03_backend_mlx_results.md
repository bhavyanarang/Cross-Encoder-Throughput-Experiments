# 03_backend_mlx

**Timestamp:** 2025-12-23 02:22:44

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 6400 | 10.47 | 52.3ms | 79.0ms | 97.4ms | 611.1 | 861.7 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 6400 pairs in 10.47s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 52.34 |
| Min | 33.29 |
| Max | 146.11 |
| Std Dev | 16.56 |
| P50 | 45.23 |
| P90 | 72.71 |
| P95 | 79.02 |
| P99 | 97.42 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 611.15 |
| Min | 219.02 |
| Max | 961.20 |
| Std Dev | 163.99 |
| P50 | 707.57 |
| P90 | 845.33 |
| P95 | 861.74 |
| P99 | 927.85 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 611.15 p/s | batch=32, conc=1 |
| Best Latency | 52.34ms | batch=32, conc=1 |
| Avg Throughput | 611.15 p/s | all configs |
| Avg Latency | 52.34ms | all configs |
