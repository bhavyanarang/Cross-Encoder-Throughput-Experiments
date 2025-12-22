# 02_backend_mps

**Timestamp:** 2025-12-23 02:52:30

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 6400 | 10.66 | 53.3ms | 83.8ms | 107.6ms | 600.4 | 858.5 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 6400 pairs in 10.66s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 53.28 |
| Min | 34.17 |
| Max | 120.84 |
| Std Dev | 16.75 |
| P50 | 45.49 |
| P90 | 74.86 |
| P95 | 83.80 |
| P99 | 107.60 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 600.39 |
| Min | 264.82 |
| Max | 936.46 |
| Std Dev | 168.30 |
| P50 | 703.42 |
| P90 | 847.55 |
| P95 | 858.46 |
| P99 | 918.51 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 600.39 p/s | batch=32, conc=1 |
| Best Latency | 53.28ms | batch=32, conc=1 |
| Avg Throughput | 600.39 p/s | all configs |
| Avg Latency | 53.28ms | all configs |
