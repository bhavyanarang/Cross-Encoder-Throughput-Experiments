# 06b_concurrency_mlx

**Timestamp:** 2025-12-23 00:59:40

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 96 | 1 | 14400 | 21.50 | 143.3ms | 190.0ms | 219.5ms | 669.9 | 788.7 |
| 96 | 2 | 14400 | 19.23 | 256.3ms | 277.0ms | 346.8ms | 748.8 | 405.5 |
| 96 | 3 | 14400 | 20.58 | 411.3ms | 455.8ms | 464.7ms | 699.7 | 260.3 |
| 96 | 4 | 14400 | 20.23 | 536.2ms | 612.1ms | 633.8ms | 711.8 | 199.9 |
| 96 | 6 | 14400 | 20.56 | 821.0ms | 936.6ms | 1184.2ms | 700.5 | 130.8 |
| 96 | 8 | 14400 | 19.97 | 1054.3ms | 1168.8ms | 1202.2ms | 721.2 | 99.0 |
| 96 | 12 | 14400 | 21.21 | 1678.7ms | 2720.1ms | 2786.4ms | 679.0 | 73.0 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=96, concurrency=1

**Total:** 14400 pairs in 21.50s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 143.28 |
| Min | 114.10 |
| Max | 258.34 |
| Std Dev | 22.71 |
| P50 | 136.53 |
| P90 | 170.95 |
| P95 | 189.97 |
| P99 | 219.51 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 669.85 |
| Min | 371.60 |
| Max | 841.39 |
| Std Dev | 88.61 |
| P50 | 703.14 |
| P90 | 778.47 |
| P95 | 788.70 |
| P99 | 824.46 |

### Config 2: batch=96, concurrency=2

**Total:** 14400 pairs in 19.23s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 256.35 |
| Min | 231.65 |
| Max | 400.61 |
| Std Dev | 20.40 |
| P50 | 253.72 |
| P90 | 271.32 |
| P95 | 277.03 |
| P99 | 346.79 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 748.81 |
| Min | 239.63 |
| Max | 414.42 |
| Std Dev | 23.26 |
| P50 | 378.36 |
| P90 | 399.30 |
| P95 | 405.45 |
| P99 | 411.59 |

### Config 3: batch=96, concurrency=3

**Total:** 14400 pairs in 20.58s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 411.30 |
| Min | 339.42 |
| Max | 469.69 |
| Std Dev | 27.62 |
| P50 | 412.23 |
| P90 | 445.72 |
| P95 | 455.76 |
| P99 | 464.71 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 699.66 |
| Min | 204.39 |
| Max | 282.83 |
| Std Dev | 16.21 |
| P50 | 232.88 |
| P90 | 256.07 |
| P95 | 260.31 |
| P99 | 279.86 |

### Config 4: batch=96, concurrency=4

**Total:** 14400 pairs in 20.23s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 536.21 |
| Min | 243.61 |
| Max | 645.42 |
| Std Dev | 56.89 |
| P50 | 536.14 |
| P90 | 605.20 |
| P95 | 612.14 |
| P99 | 633.82 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 711.77 |
| Min | 148.74 |
| Max | 394.07 |
| Std Dev | 28.70 |
| P50 | 179.06 |
| P90 | 197.38 |
| P95 | 199.94 |
| P99 | 304.67 |

### Config 5: batch=96, concurrency=6

**Total:** 14400 pairs in 20.56s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 821.04 |
| Min | 652.24 |
| Max | 1196.67 |
| Std Dev | 85.16 |
| P50 | 807.17 |
| P90 | 881.58 |
| P95 | 936.57 |
| P99 | 1184.20 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 700.52 |
| Min | 80.22 |
| Max | 147.18 |
| Std Dev | 10.13 |
| P50 | 118.93 |
| P90 | 127.90 |
| P95 | 130.75 |
| P99 | 139.17 |

### Config 6: batch=96, concurrency=8

**Total:** 14400 pairs in 19.97s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1054.32 |
| Min | 745.56 |
| Max | 1221.55 |
| Std Dev | 73.31 |
| P50 | 1060.38 |
| P90 | 1131.08 |
| P95 | 1168.79 |
| P99 | 1202.19 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 721.23 |
| Min | 78.59 |
| Max | 128.76 |
| Std Dev | 7.50 |
| P50 | 90.53 |
| P90 | 96.70 |
| P95 | 98.97 |
| P99 | 124.21 |

### Config 7: batch=96, concurrency=12

**Total:** 14400 pairs in 21.21s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1678.70 |
| Min | 1134.19 |
| Max | 2896.58 |
| Std Dev | 466.24 |
| P50 | 1471.01 |
| P90 | 2592.50 |
| P95 | 2720.14 |
| P99 | 2786.38 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 679.01 |
| Min | 33.14 |
| Max | 84.64 |
| Std Dev | 12.22 |
| P50 | 65.26 |
| P90 | 69.80 |
| P95 | 72.97 |
| P99 | 77.06 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 748.81 p/s | batch=96, conc=2 |
| Best Latency | 143.28ms | batch=96, conc=1 |
| Avg Throughput | 704.41 p/s | all configs |
| Avg Latency | 700.17ms | all configs |
