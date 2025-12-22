# 02_backend_mps

**Timestamp:** 2025-12-23 04:19:51

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 6400 | 10.54 | 52.7ms | 81.4ms | 94.6ms | 607.3 | 863.9 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 6400 pairs in 10.54s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 52.67 |
| Min | 33.34 |
| Max | 112.09 |
| Std Dev | 16.37 |
| P50 | 45.00 |
| P90 | 77.53 |
| P95 | 81.38 |
| P99 | 94.63 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 607.35 |
| Min | 285.47 |
| Max | 959.78 |
| Std Dev | 169.21 |
| P50 | 711.19 |
| P90 | 850.49 |
| P95 | 863.88 |
| P99 | 932.38 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 607.35 p/s | batch=32, conc=1 |
| Best Latency | 52.67ms | batch=32, conc=1 |
| Avg Throughput | 607.35 p/s | all configs |
| Avg Latency | 52.67ms | all configs |
