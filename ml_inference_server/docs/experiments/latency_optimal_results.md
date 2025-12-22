# latency_optimal

**Timestamp:** 2025-12-22 23:55:21

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `True` (max_batch=32, timeout=5ms)

**Model Type:** Cross-Encoder

**Requests per config:** `300`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 2400 | 10.49 | 35.0ms | 65.0ms | 73.1ms | 228.8 | 431.2 |
| 8 | 2 | 2400 | 6.85 | 45.6ms | 58.0ms | 63.6ms | 350.6 | 220.3 |
| 8 | 3 | 2400 | 7.79 | 77.7ms | 117.7ms | 171.2ms | 308.3 | 141.7 |
| 16 | 1 | 4800 | 13.89 | 46.3ms | 76.2ms | 84.9ms | 345.6 | 529.6 |
| 16 | 2 | 4800 | 9.01 | 60.0ms | 75.5ms | 94.7ms | 532.9 | 320.3 |
| 16 | 3 | 4800 | 9.42 | 94.1ms | 131.9ms | 143.1ms | 509.3 | 216.4 |
| 24 | 1 | 7200 | 15.80 | 52.6ms | 88.7ms | 101.0ms | 455.7 | 643.7 |
| 24 | 2 | 7200 | 16.13 | 107.4ms | 136.7ms | 149.8ms | 446.4 | 304.5 |
| 24 | 3 | 7200 | 16.42 | 163.9ms | 224.8ms | 251.9ms | 438.4 | 223.0 |
| 32 | 1 | 9600 | 17.84 | 59.5ms | 91.8ms | 117.5ms | 538.1 | 708.5 |
| 32 | 2 | 9600 | 19.73 | 131.4ms | 166.6ms | 183.0ms | 486.5 | 322.5 |
| 32 | 3 | 9600 | 22.01 | 219.8ms | 285.3ms | 318.1ms | 436.2 | 210.5 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=8, concurrency=1

**Total:** 2400 pairs in 10.49s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 34.96 |
| Min | 16.08 |
| Max | 121.32 |
| Std Dev | 17.04 |
| P50 | 27.01 |
| P90 | 61.13 |
| P95 | 65.05 |
| P99 | 73.07 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 228.81 |
| Min | 65.94 |
| Max | 497.58 |
| Std Dev | 106.17 |
| P50 | 296.20 |
| P90 | 411.83 |
| P95 | 431.22 |
| P99 | 457.92 |

### Config 2: batch=8, concurrency=2

**Total:** 2400 pairs in 6.85s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 45.60 |
| Min | 26.96 |
| Max | 68.13 |
| Std Dev | 6.81 |
| P50 | 44.38 |
| P90 | 54.89 |
| P95 | 58.03 |
| P99 | 63.56 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 350.61 |
| Min | 117.43 |
| Max | 296.73 |
| Std Dev | 26.31 |
| P50 | 180.27 |
| P90 | 211.28 |
| P95 | 220.29 |
| P99 | 246.78 |

### Config 3: batch=8, concurrency=3

**Total:** 2400 pairs in 7.79s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 77.69 |
| Min | 31.61 |
| Max | 218.24 |
| Std Dev | 21.91 |
| P50 | 73.19 |
| P90 | 95.59 |
| P95 | 117.65 |
| P99 | 171.22 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 308.25 |
| Min | 36.66 |
| Max | 253.05 |
| Std Dev | 22.97 |
| P50 | 109.31 |
| P90 | 134.13 |
| P95 | 141.69 |
| P99 | 158.92 |

### Config 4: batch=16, concurrency=1

**Total:** 4800 pairs in 13.89s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 46.29 |
| Min | 25.74 |
| Max | 102.49 |
| Std Dev | 15.45 |
| P50 | 40.04 |
| P90 | 71.05 |
| P95 | 76.22 |
| P99 | 84.94 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 345.61 |
| Min | 156.12 |
| Max | 621.63 |
| Std Dev | 105.38 |
| P50 | 399.57 |
| P90 | 506.98 |
| P95 | 529.65 |
| P99 | 575.48 |

### Config 5: batch=16, concurrency=2

**Total:** 4800 pairs in 9.01s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 59.99 |
| Min | 32.05 |
| Max | 143.74 |
| Std Dev | 10.59 |
| P50 | 58.20 |
| P90 | 70.19 |
| P95 | 75.49 |
| P99 | 94.68 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 532.93 |
| Min | 111.31 |
| Max | 499.15 |
| Std Dev | 38.96 |
| P50 | 274.90 |
| P90 | 313.09 |
| P95 | 320.31 |
| P99 | 337.75 |

### Config 6: batch=16, concurrency=3

**Total:** 4800 pairs in 9.42s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 94.07 |
| Min | 30.02 |
| Max | 153.06 |
| Std Dev | 18.34 |
| P50 | 90.49 |
| P90 | 120.02 |
| P95 | 131.93 |
| P99 | 143.10 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 509.32 |
| Min | 104.54 |
| Max | 532.99 |
| Std Dev | 45.19 |
| P50 | 176.82 |
| P90 | 207.62 |
| P95 | 216.36 |
| P99 | 444.25 |

### Config 7: batch=24, concurrency=1

**Total:** 7200 pairs in 15.80s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 52.65 |
| Min | 31.77 |
| Max | 170.31 |
| Std Dev | 17.79 |
| P50 | 45.62 |
| P90 | 79.37 |
| P95 | 88.66 |
| P99 | 101.00 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 455.73 |
| Min | 140.92 |
| Max | 755.51 |
| Std Dev | 121.00 |
| P50 | 526.08 |
| P90 | 624.88 |
| P95 | 643.67 |
| P99 | 679.67 |

### Config 8: batch=24, concurrency=2

**Total:** 7200 pairs in 16.13s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 107.43 |
| Min | 63.10 |
| Max | 156.12 |
| Std Dev | 17.76 |
| P50 | 108.57 |
| P90 | 130.50 |
| P95 | 136.67 |
| P99 | 149.75 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 446.41 |
| Min | 153.73 |
| Max | 380.37 |
| Std Dev | 40.46 |
| P50 | 221.06 |
| P90 | 284.67 |
| P95 | 304.53 |
| P99 | 351.55 |

### Config 9: batch=24, concurrency=3

**Total:** 7200 pairs in 16.42s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 163.92 |
| Min | 95.60 |
| Max | 261.22 |
| Std Dev | 37.35 |
| P50 | 171.74 |
| P90 | 206.47 |
| P95 | 224.81 |
| P99 | 251.88 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 438.37 |
| Min | 91.88 |
| Max | 251.05 |
| Std Dev | 37.83 |
| P50 | 139.74 |
| P90 | 210.84 |
| P95 | 222.98 |
| P99 | 230.79 |

### Config 10: batch=32, concurrency=1

**Total:** 9600 pairs in 17.84s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 59.46 |
| Min | 41.90 |
| Max | 140.73 |
| Std Dev | 15.54 |
| P50 | 53.77 |
| P90 | 80.36 |
| P95 | 91.76 |
| P99 | 117.46 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 538.08 |
| Min | 227.38 |
| Max | 763.75 |
| Std Dev | 113.56 |
| P50 | 595.09 |
| P90 | 694.22 |
| P95 | 708.51 |
| P99 | 746.62 |

### Config 11: batch=32, concurrency=2

**Total:** 9600 pairs in 19.73s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 131.40 |
| Min | 83.40 |
| Max | 211.41 |
| Std Dev | 22.33 |
| P50 | 129.81 |
| P90 | 160.90 |
| P95 | 166.62 |
| P99 | 183.01 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 486.51 |
| Min | 151.37 |
| Max | 383.71 |
| Std Dev | 43.09 |
| P50 | 246.51 |
| P90 | 307.59 |
| P95 | 322.52 |
| P99 | 350.05 |

### Config 12: batch=32, concurrency=3

**Total:** 9600 pairs in 22.01s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 219.76 |
| Min | 78.75 |
| Max | 327.78 |
| Std Dev | 41.34 |
| P50 | 219.80 |
| P90 | 270.97 |
| P95 | 285.32 |
| P99 | 318.14 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 436.15 |
| Min | 97.63 |
| Max | 406.37 |
| Std Dev | 33.27 |
| P50 | 145.58 |
| P90 | 190.20 |
| P95 | 210.52 |
| P99 | 238.34 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 538.08 p/s | batch=32, conc=1 |
| Best Latency | 34.96ms | batch=8, conc=1 |
| Avg Throughput | 423.07 p/s | all configs |
| Avg Latency | 91.10ms | all configs |
