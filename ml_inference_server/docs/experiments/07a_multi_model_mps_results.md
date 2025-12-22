# 07a_multi_model_mps

**Timestamp:** 2025-12-23 01:01:58

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `100`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 3200 | 7.13 | 283.7ms | 357.9ms | 381.3ms | 448.7 | 153.9 |
| 32 | 8 | 3200 | 4.89 | 384.3ms | 447.1ms | 453.0ms | 654.6 | 92.0 |
| 32 | 16 | 3200 | 5.06 | 777.8ms | 990.0ms | 1007.6ms | 632.5 | 65.6 |
| 32 | 24 | 3200 | 5.25 | 1160.5ms | 1495.3ms | 1514.5ms | 609.6 | 61.5 |
| 64 | 4 | 6400 | 9.00 | 359.7ms | 407.0ms | 445.4ms | 711.3 | 194.7 |
| 64 | 8 | 6400 | 9.91 | 780.5ms | 880.4ms | 968.7ms | 645.5 | 94.5 |
| 64 | 16 | 6400 | 9.12 | 1404.2ms | 1856.5ms | 1876.2ms | 701.9 | 70.5 |
| 64 | 24 | 6400 | 9.68 | 2128.0ms | 2918.0ms | 3054.9ms | 660.8 | 68.9 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=4

**Total:** 3200 pairs in 7.13s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 283.68 |
| Min | 130.55 |
| Max | 392.34 |
| Std Dev | 50.12 |
| P50 | 290.00 |
| P90 | 348.54 |
| P95 | 357.90 |
| P99 | 381.35 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 448.66 |
| Min | 81.56 |
| Max | 245.12 |
| Std Dev | 24.59 |
| P50 | 110.34 |
| P90 | 147.54 |
| P95 | 153.88 |
| P99 | 176.38 |

### Config 2: batch=32, concurrency=8

**Total:** 3200 pairs in 4.89s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 384.29 |
| Min | 186.15 |
| Max | 456.79 |
| Std Dev | 42.64 |
| P50 | 386.56 |
| P90 | 424.26 |
| P95 | 447.11 |
| P99 | 453.04 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 654.58 |
| Min | 70.05 |
| Max | 171.90 |
| Std Dev | 14.16 |
| P50 | 82.78 |
| P90 | 89.51 |
| P95 | 91.99 |
| P99 | 150.77 |

### Config 3: batch=32, concurrency=16

**Total:** 3200 pairs in 5.06s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 777.83 |
| Min | 454.13 |
| Max | 1009.72 |
| Std Dev | 187.17 |
| P50 | 875.41 |
| P90 | 975.37 |
| P95 | 989.96 |
| P99 | 1007.60 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 632.49 |
| Min | 31.69 |
| Max | 70.46 |
| Std Dev | 11.95 |
| P50 | 36.55 |
| P90 | 63.74 |
| P95 | 65.61 |
| P99 | 70.34 |

### Config 4: batch=32, concurrency=24

**Total:** 3200 pairs in 5.25s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1160.45 |
| Min | 416.33 |
| Max | 1515.55 |
| Std Dev | 270.91 |
| P50 | 1158.89 |
| P90 | 1487.36 |
| P95 | 1495.31 |
| P99 | 1514.54 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 609.57 |
| Min | 21.11 |
| Max | 76.86 |
| Std Dev | 11.72 |
| P50 | 27.61 |
| P90 | 39.93 |
| P95 | 61.49 |
| P99 | 66.32 |

### Config 5: batch=64, concurrency=4

**Total:** 6400 pairs in 9.00s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 359.72 |
| Min | 316.56 |
| Max | 457.29 |
| Std Dev | 24.85 |
| P50 | 357.64 |
| P90 | 394.35 |
| P95 | 406.99 |
| P99 | 445.42 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 711.32 |
| Min | 139.95 |
| Max | 202.17 |
| Std Dev | 11.47 |
| P50 | 178.95 |
| P90 | 190.80 |
| P95 | 194.67 |
| P99 | 199.53 |

### Config 6: batch=64, concurrency=8

**Total:** 6400 pairs in 9.91s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 780.49 |
| Min | 331.78 |
| Max | 973.20 |
| Std Dev | 84.85 |
| P50 | 784.37 |
| P90 | 846.39 |
| P95 | 880.40 |
| P99 | 968.70 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 645.49 |
| Min | 65.76 |
| Max | 192.90 |
| Std Dev | 13.81 |
| P50 | 81.60 |
| P90 | 89.48 |
| P95 | 94.45 |
| P99 | 119.03 |

### Config 7: batch=64, concurrency=16

**Total:** 6400 pairs in 9.12s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1404.16 |
| Min | 893.08 |
| Max | 1876.63 |
| Std Dev | 411.88 |
| P50 | 1714.70 |
| P90 | 1834.22 |
| P95 | 1856.52 |
| P99 | 1876.18 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 701.85 |
| Min | 34.10 |
| Max | 71.66 |
| Std Dev | 15.47 |
| P50 | 37.32 |
| P90 | 69.50 |
| P95 | 70.50 |
| P99 | 71.45 |

### Config 8: batch=64, concurrency=24

**Total:** 6400 pairs in 9.68s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 2127.97 |
| Min | 877.22 |
| Max | 3124.15 |
| Std Dev | 557.83 |
| P50 | 1998.37 |
| P90 | 2783.38 |
| P95 | 2918.03 |
| P99 | 3054.91 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 660.82 |
| Min | 20.49 |
| Max | 72.96 |
| Std Dev | 12.82 |
| P50 | 32.03 |
| P90 | 39.78 |
| P95 | 68.90 |
| P99 | 69.70 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 711.32 p/s | batch=64, conc=4 |
| Best Latency | 283.68ms | batch=32, conc=4 |
| Avg Throughput | 633.10 p/s | all configs |
| Avg Latency | 909.82ms | all configs |
