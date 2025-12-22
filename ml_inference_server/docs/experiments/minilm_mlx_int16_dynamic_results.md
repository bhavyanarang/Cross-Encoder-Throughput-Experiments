# cross_encoder_mlx_int16_dynamic

**Timestamp:** 2025-12-23 00:07:13

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `True` (max_batch=96, timeout=15ms)

**Model Type:** Cross-Encoder

**Requests per config:** `500`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 3 | 32000 | 75.68 | 453.8ms | 568.3ms | 641.5ms | 422.8 | 183.0 |
| 96 | 3 | 48000 | 86.86 | 520.6ms | 605.4ms | 678.0ms | 552.6 | 210.2 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=64, concurrency=3

**Total:** 32000 pairs in 75.68s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 453.77 |
| Min | 186.15 |
| Max | 687.76 |
| Std Dev | 69.87 |
| P50 | 450.78 |
| P90 | 539.63 |
| P95 | 568.27 |
| P99 | 641.51 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 422.82 |
| Min | 93.06 |
| Max | 343.81 |
| Std Dev | 23.85 |
| P50 | 141.98 |
| P90 | 173.64 |
| P95 | 182.97 |
| P99 | 205.97 |

### Config 2: batch=96, concurrency=3

**Total:** 48000 pairs in 86.86s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 520.63 |
| Min | 351.57 |
| Max | 832.11 |
| Std Dev | 48.96 |
| P50 | 515.80 |
| P90 | 577.08 |
| P95 | 605.43 |
| P99 | 678.00 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 552.64 |
| Min | 115.37 |
| Max | 273.06 |
| Std Dev | 16.31 |
| P50 | 186.12 |
| P90 | 205.79 |
| P95 | 210.22 |
| P99 | 216.36 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 552.64 p/s | batch=96, conc=3 |
| Best Latency | 453.77ms | batch=64, conc=3 |
| Avg Throughput | 487.73 p/s | all configs |
| Avg Latency | 487.20ms | all configs |
