# 14_optimized_production

**Timestamp:** 2025-12-24 05:05:44

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `True` (max_batch=256, timeout=200ms)

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 6400 | 16.92 | 84.6ms | 180.8ms | 268.0ms | 378.2 | 719.6 |
| 48 | 1 | 9600 | 18.50 | 92.5ms | 134.7ms | 165.4ms | 519.0 | 722.6 |
| 64 | 1 | 12800 | 24.87 | 124.3ms | 194.6ms | 318.8ms | 514.7 | 700.8 |
| 96 | 1 | 19200 | 36.52 | 182.6ms | 251.1ms | 365.3ms | 525.7 | 697.6 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 6400 pairs in 16.92s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 84.59 |
| Min | 38.33 |
| Max | 296.73 |
| Std Dev | 48.84 |
| P50 | 67.24 |
| P90 | 133.31 |
| P95 | 180.75 |
| P99 | 268.03 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 378.17 |
| Min | 107.84 |
| Max | 834.75 |
| Std Dev | 174.93 |
| P50 | 475.95 |
| P90 | 669.16 |
| P95 | 719.64 |
| P99 | 794.65 |

### Config 2: batch=48, concurrency=1

**Total:** 9600 pairs in 18.50s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 92.47 |
| Min | 52.19 |
| Max | 167.24 |
| Std Dev | 21.31 |
| P50 | 88.96 |
| P90 | 119.94 |
| P95 | 134.68 |
| P99 | 165.39 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 518.97 |
| Min | 287.02 |
| Max | 919.76 |
| Std Dev | 114.47 |
| P50 | 539.57 |
| P90 | 682.70 |
| P95 | 722.65 |
| P99 | 833.30 |

### Config 3: batch=64, concurrency=1

**Total:** 12800 pairs in 24.87s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 124.31 |
| Min | 82.49 |
| Max | 321.53 |
| Std Dev | 38.14 |
| P50 | 116.39 |
| P90 | 157.83 |
| P95 | 194.65 |
| P99 | 318.79 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 514.71 |
| Min | 199.05 |
| Max | 775.86 |
| Std Dev | 114.75 |
| P50 | 549.88 |
| P90 | 678.70 |
| P95 | 700.84 |
| P99 | 742.44 |

### Config 4: batch=96, concurrency=1

**Total:** 19200 pairs in 36.52s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 182.59 |
| Min | 129.45 |
| Max | 493.19 |
| Std Dev | 44.83 |
| P50 | 171.92 |
| P90 | 226.98 |
| P95 | 251.12 |
| P99 | 365.28 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 525.68 |
| Min | 194.65 |
| Max | 741.63 |
| Std Dev | 98.79 |
| P50 | 558.41 |
| P90 | 673.55 |
| P95 | 697.57 |
| P99 | 729.12 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 525.68 p/s | batch=96, conc=1 |
| Best Latency | 84.59ms | batch=32, conc=1 |
| Avg Throughput | 484.38 p/s | all configs |
| Avg Latency | 120.99ms | all configs |
