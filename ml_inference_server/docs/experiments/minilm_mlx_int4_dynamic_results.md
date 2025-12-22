# cross_encoder_mlx_int4

**Timestamp:** 2025-12-22 23:19:17

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `True` (max_batch=512, timeout=200ms)

**Model Type:** Cross-Encoder

**Requests per config:** `500`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 26.86 | 214.6ms | 297.3ms | 341.7ms | 595.7 | 183.9 |
| 32 | 8 | 16000 | 25.04 | 399.6ms | 512.8ms | 576.5ms | 639.0 | 90.2 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=4

**Total:** 16000 pairs in 26.86s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 214.62 |
| Min | 112.95 |
| Max | 389.46 |
| Std Dev | 40.21 |
| P50 | 200.40 |
| P90 | 271.06 |
| P95 | 297.33 |
| P99 | 341.72 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 595.74 |
| Min | 82.16 |
| Max | 283.32 |
| Std Dev | 25.50 |
| P50 | 159.68 |
| P90 | 178.88 |
| P95 | 183.86 |
| P99 | 205.90 |

### Config 2: batch=32, concurrency=8

**Total:** 16000 pairs in 25.04s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 399.56 |
| Min | 286.66 |
| Max | 654.80 |
| Std Dev | 49.57 |
| P50 | 384.15 |
| P90 | 474.80 |
| P95 | 512.75 |
| P99 | 576.51 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 638.99 |
| Min | 48.87 |
| Max | 111.63 |
| Std Dev | 8.38 |
| P50 | 83.30 |
| P90 | 88.84 |
| P95 | 90.23 |
| P99 | 93.07 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 638.99 p/s | batch=32, conc=8 |
| Best Latency | 214.62ms | batch=32, conc=4 |
| Avg Throughput | 617.37 p/s | all configs |
| Avg Latency | 307.09ms | all configs |
