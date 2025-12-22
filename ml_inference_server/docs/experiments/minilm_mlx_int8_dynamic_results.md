# cross_encoder_mlx_int8

**Timestamp:** 2025-12-22 23:17:10

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `True` (max_batch=512, timeout=200ms)

**Model Type:** Cross-Encoder

**Requests per config:** `500`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 28.97 | 231.6ms | 311.4ms | 377.0ms | 552.2 | 176.4 |
| 32 | 8 | 16000 | 25.07 | 400.2ms | 498.9ms | 554.9ms | 638.3 | 92.0 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=4

**Total:** 16000 pairs in 28.97s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 231.56 |
| Min | 120.07 |
| Max | 424.62 |
| Std Dev | 45.51 |
| P50 | 221.38 |
| P90 | 293.04 |
| P95 | 311.44 |
| P99 | 377.03 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 552.20 |
| Min | 75.36 |
| Max | 266.51 |
| Std Dev | 25.65 |
| P50 | 144.55 |
| P90 | 172.70 |
| P95 | 176.45 |
| P99 | 183.84 |

### Config 2: batch=32, concurrency=8

**Total:** 16000 pairs in 25.07s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 400.19 |
| Min | 329.64 |
| Max | 572.20 |
| Std Dev | 45.55 |
| P50 | 390.46 |
| P90 | 461.73 |
| P95 | 498.91 |
| P99 | 554.90 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 638.34 |
| Min | 55.92 |
| Max | 97.07 |
| Std Dev | 8.27 |
| P50 | 81.95 |
| P90 | 91.23 |
| P95 | 92.02 |
| P99 | 93.77 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 638.34 p/s | batch=32, conc=8 |
| Best Latency | 231.56ms | batch=32, conc=4 |
| Avg Throughput | 595.27 p/s | all configs |
| Avg Latency | 315.87ms | all configs |
