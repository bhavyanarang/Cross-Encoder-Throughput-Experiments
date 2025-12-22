# throughput_optimal

**Timestamp:** 2025-12-22 23:51:34

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `True` (max_batch=128, timeout=15ms)

**Model Type:** Cross-Encoder

**Requests per config:** `300`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 3 | 19200 | 42.88 | 428.3ms | 548.6ms | 626.5ms | 447.7 | 204.6 |
| 64 | 4 | 19200 | 32.92 | 438.8ms | 513.2ms | 555.6ms | 583.3 | 165.0 |
| 96 | 3 | 28800 | 54.09 | 540.0ms | 674.6ms | 722.8ms | 532.4 | 206.3 |
| 96 | 4 | 28800 | 50.64 | 674.6ms | 873.5ms | 989.0ms | 568.7 | 159.1 |
| 128 | 3 | 38400 | 69.29 | 691.7ms | 842.2ms | 913.0ms | 554.2 | 208.9 |
| 128 | 4 | 38400 | 67.37 | 896.7ms | 1006.5ms | 1181.2ms | 570.0 | 162.1 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=64, concurrency=3

**Total:** 19200 pairs in 42.88s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 428.35 |
| Min | 273.44 |
| Max | 696.09 |
| Std Dev | 81.18 |
| P50 | 430.33 |
| P90 | 523.56 |
| P95 | 548.59 |
| P99 | 626.46 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 447.73 |
| Min | 91.94 |
| Max | 234.05 |
| Std Dev | 29.52 |
| P50 | 148.72 |
| P90 | 197.74 |
| P95 | 204.55 |
| P99 | 220.81 |

### Config 2: batch=64, concurrency=4

**Total:** 19200 pairs in 32.92s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 438.82 |
| Min | 359.65 |
| Max | 562.38 |
| Std Dev | 39.52 |
| P50 | 433.40 |
| P90 | 482.64 |
| P95 | 513.24 |
| P99 | 555.60 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 583.31 |
| Min | 113.80 |
| Max | 177.95 |
| Std Dev | 12.62 |
| P50 | 147.67 |
| P90 | 162.67 |
| P95 | 165.05 |
| P99 | 176.28 |

### Config 3: batch=96, concurrency=3

**Total:** 28800 pairs in 54.09s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 540.00 |
| Min | 225.61 |
| Max | 793.79 |
| Std Dev | 70.17 |
| P50 | 523.48 |
| P90 | 644.50 |
| P95 | 674.64 |
| P99 | 722.76 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 532.41 |
| Min | 120.94 |
| Max | 425.51 |
| Std Dev | 25.06 |
| P50 | 183.39 |
| P90 | 201.89 |
| P95 | 206.30 |
| P99 | 216.19 |

### Config 4: batch=96, concurrency=4

**Total:** 28800 pairs in 50.64s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 674.57 |
| Min | 443.94 |
| Max | 1031.16 |
| Std Dev | 76.78 |
| P50 | 653.92 |
| P90 | 752.69 |
| P95 | 873.45 |
| P99 | 989.00 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 568.71 |
| Min | 93.10 |
| Max | 216.24 |
| Std Dev | 14.00 |
| P50 | 146.81 |
| P90 | 156.52 |
| P95 | 159.12 |
| P99 | 166.13 |

### Config 5: batch=128, concurrency=3

**Total:** 38400 pairs in 69.29s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 691.66 |
| Min | 313.71 |
| Max | 946.86 |
| Std Dev | 75.02 |
| P50 | 670.06 |
| P90 | 802.20 |
| P95 | 842.19 |
| P99 | 912.98 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 554.22 |
| Min | 135.18 |
| Max | 408.02 |
| Std Dev | 21.88 |
| P50 | 191.03 |
| P90 | 204.43 |
| P95 | 208.90 |
| P99 | 223.73 |

### Config 6: batch=128, concurrency=4

**Total:** 38400 pairs in 67.37s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 896.65 |
| Min | 303.76 |
| Max | 1347.27 |
| Std Dev | 84.83 |
| P50 | 889.47 |
| P90 | 975.21 |
| P95 | 1006.46 |
| P99 | 1181.24 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 569.97 |
| Min | 95.01 |
| Max | 421.39 |
| Std Dev | 19.56 |
| P50 | 143.91 |
| P90 | 155.34 |
| P95 | 162.08 |
| P99 | 173.37 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 583.31 p/s | batch=64, conc=4 |
| Best Latency | 428.35ms | batch=64, conc=3 |
| Avg Throughput | 542.73 p/s | all configs |
| Avg Latency | 611.67ms | all configs |
