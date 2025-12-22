# 10b_debug_packing

**Timestamp:** 2025-12-23 03:44:43

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `5`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 4 | 1 | 20 | 0.33 | 66.8ms | 141.8ms | 160.5ms | 59.8 | 108.1 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=4, concurrency=1

**Total:** 20 pairs in 0.33s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 66.85 |
| Min | 36.51 |
| Max | 165.14 |
| Std Dev | 49.33 |
| P50 | 44.86 |
| P90 | 118.55 |
| P95 | 141.85 |
| P99 | 160.48 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 59.83 |
| Min | 24.22 |
| Max | 109.57 |
| Std Dev | 30.22 |
| P50 | 89.17 |
| P90 | 106.71 |
| P95 | 108.14 |
| P99 | 109.28 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 59.83 p/s | batch=4, conc=1 |
| Best Latency | 66.85ms | batch=4, conc=1 |
| Avg Throughput | 59.83 p/s | all configs |
| Avg Latency | 66.85ms | all configs |
