# cross_encoder_mps_fp16

**Timestamp:** 2025-12-22 23:41:44

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `True` (max_batch=64, timeout=200ms)

**Model Type:** Cross-Encoder

**Requests per config:** `500`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 42.77 | 341.7ms | 439.8ms | 476.2ms | 374.1 | 131.3 |
| 32 | 8 | 16000 | 35.20 | 561.1ms | 719.5ms | 748.3ms | 454.6 | 75.5 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=4

**Total:** 16000 pairs in 42.77s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 341.66 |
| Min | 165.14 |
| Max | 540.12 |
| Std Dev | 56.13 |
| P50 | 341.34 |
| P90 | 407.36 |
| P95 | 439.84 |
| P99 | 476.18 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 374.10 |
| Min | 59.25 |
| Max | 193.77 |
| Std Dev | 17.81 |
| P50 | 93.75 |
| P90 | 117.18 |
| P95 | 131.34 |
| P99 | 160.21 |

### Config 2: batch=32, concurrency=8

**Total:** 16000 pairs in 35.20s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 561.09 |
| Min | 393.63 |
| Max | 770.74 |
| Std Dev | 102.98 |
| P50 | 587.11 |
| P90 | 699.12 |
| P95 | 719.51 |
| P99 | 748.34 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 454.55 |
| Min | 41.52 |
| Max | 81.29 |
| Std Dev | 11.08 |
| P50 | 54.50 |
| P90 | 73.71 |
| P95 | 75.46 |
| P99 | 78.12 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 454.55 p/s | batch=32, conc=8 |
| Best Latency | 341.66ms | batch=32, conc=4 |
| Avg Throughput | 414.32 p/s | all configs |
| Avg Latency | 451.38ms | all configs |
