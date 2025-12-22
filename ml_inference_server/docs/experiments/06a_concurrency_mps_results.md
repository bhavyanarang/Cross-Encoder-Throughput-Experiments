# 06a_concurrency_mps

**Timestamp:** 2025-12-23 02:59:11

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 96 | 1 | 14400 | 20.19 | 134.6ms | 176.7ms | 255.1ms | 713.3 | 917.6 |
| 96 | 2 | 14400 | 18.72 | 248.8ms | 298.9ms | 350.2ms | 769.3 | 445.1 |
| 96 | 3 | 14400 | 18.54 | 368.7ms | 429.1ms | 447.3ms | 776.5 | 287.8 |
| 96 | 4 | 14400 | 18.65 | 493.1ms | 554.0ms | 605.5ms | 771.9 | 213.7 |
| 96 | 6 | 14400 | 18.71 | 737.3ms | 825.8ms | 857.1ms | 769.7 | 139.5 |
| 96 | 8 | 14400 | 18.49 | 965.0ms | 1065.9ms | 1109.1ms | 778.6 | 106.5 |
| 96 | 12 | 14400 | 18.83 | 1453.0ms | 1658.7ms | 1699.7ms | 764.6 | 100.1 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=96, concurrency=1

**Total:** 14400 pairs in 20.19s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 134.55 |
| Min | 100.89 |
| Max | 455.17 |
| Std Dev | 36.53 |
| P50 | 128.18 |
| P90 | 159.04 |
| P95 | 176.68 |
| P99 | 255.06 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 713.29 |
| Min | 210.91 |
| Max | 951.57 |
| Std Dev | 121.76 |
| P50 | 748.93 |
| P90 | 886.33 |
| P95 | 917.64 |
| P99 | 939.89 |

### Config 2: batch=96, concurrency=2

**Total:** 14400 pairs in 18.72s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 248.81 |
| Min | 106.52 |
| Max | 400.36 |
| Std Dev | 29.99 |
| P50 | 245.62 |
| P90 | 273.53 |
| P95 | 298.90 |
| P99 | 350.16 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 769.29 |
| Min | 239.78 |
| Max | 901.25 |
| Std Dev | 55.88 |
| P50 | 390.84 |
| P90 | 436.35 |
| P95 | 445.14 |
| P99 | 456.05 |

### Config 3: batch=96, concurrency=3

**Total:** 14400 pairs in 18.54s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 368.68 |
| Min | 108.53 |
| Max | 455.53 |
| Std Dev | 36.57 |
| P50 | 366.89 |
| P90 | 405.51 |
| P95 | 429.14 |
| P99 | 447.32 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 776.52 |
| Min | 210.74 |
| Max | 884.53 |
| Std Dev | 55.54 |
| P50 | 261.66 |
| P90 | 282.74 |
| P95 | 287.79 |
| P99 | 363.55 |

### Config 4: batch=96, concurrency=4

**Total:** 14400 pairs in 18.65s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 493.10 |
| Min | 106.30 |
| Max | 617.10 |
| Std Dev | 52.24 |
| P50 | 489.92 |
| P90 | 540.67 |
| P95 | 554.01 |
| P99 | 605.51 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 771.94 |
| Min | 155.57 |
| Max | 903.12 |
| Std Dev | 62.32 |
| P50 | 195.95 |
| P90 | 210.13 |
| P95 | 213.69 |
| P99 | 357.95 |

### Config 5: batch=96, concurrency=6

**Total:** 14400 pairs in 18.71s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 737.31 |
| Min | 106.09 |
| Max | 872.85 |
| Std Dev | 89.88 |
| P50 | 745.13 |
| P90 | 808.65 |
| P95 | 825.83 |
| P99 | 857.11 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 769.66 |
| Min | 109.98 |
| Max | 904.85 |
| Std Dev | 69.50 |
| P50 | 128.84 |
| P90 | 137.60 |
| P95 | 139.53 |
| P99 | 362.01 |

### Config 6: batch=96, concurrency=8

**Total:** 14400 pairs in 18.49s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 964.98 |
| Min | 105.20 |
| Max | 1113.08 |
| Std Dev | 132.70 |
| P50 | 990.33 |
| P90 | 1052.92 |
| P95 | 1065.89 |
| P99 | 1109.06 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 778.59 |
| Min | 86.25 |
| Max | 912.51 |
| Std Dev | 73.96 |
| P50 | 96.94 |
| P90 | 104.12 |
| P95 | 106.50 |
| P99 | 361.70 |

### Config 7: batch=96, concurrency=12

**Total:** 14400 pairs in 18.83s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1452.99 |
| Min | 106.22 |
| Max | 1726.23 |
| Std Dev | 248.02 |
| P50 | 1514.14 |
| P90 | 1602.71 |
| P95 | 1658.68 |
| P99 | 1699.73 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 764.64 |
| Min | 55.61 |
| Max | 903.79 |
| Std Dev | 77.77 |
| P50 | 63.40 |
| P90 | 68.58 |
| P95 | 100.14 |
| P99 | 356.35 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 778.59 p/s | batch=96, conc=8 |
| Best Latency | 134.55ms | batch=96, conc=1 |
| Avg Throughput | 763.42 p/s | all configs |
| Avg Latency | 628.63ms | all configs |
