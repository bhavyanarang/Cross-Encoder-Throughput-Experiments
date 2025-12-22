# 05a_batch_size_mps

**Timestamp:** 2025-12-23 00:47:58

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 1200 | 5.96 | 39.7ms | 71.2ms | 125.9ms | 201.3 | 441.5 |
| 16 | 1 | 2400 | 7.28 | 48.5ms | 79.0ms | 85.6ms | 329.7 | 586.7 |
| 32 | 1 | 4800 | 9.66 | 64.4ms | 94.8ms | 106.9ms | 497.1 | 727.8 |
| 48 | 1 | 7200 | 11.48 | 76.5ms | 100.6ms | 110.6ms | 627.4 | 731.2 |
| 64 | 1 | 9600 | 13.97 | 93.1ms | 106.6ms | 119.0ms | 687.4 | 774.0 |
| 96 | 1 | 14400 | 20.33 | 135.5ms | 153.9ms | 180.5ms | 708.2 | 783.0 |
| 128 | 1 | 19200 | 26.48 | 176.5ms | 200.6ms | 215.0ms | 725.1 | 791.2 |
| 192 | 1 | 28800 | 39.02 | 260.1ms | 275.8ms | 318.8ms | 738.1 | 796.3 |
| 256 | 1 | 38400 | 51.34 | 342.2ms | 364.4ms | 393.9ms | 748.0 | 796.1 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=8, concurrency=1

**Total:** 1200 pairs in 5.96s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 39.74 |
| Min | 16.62 |
| Max | 135.83 |
| Std Dev | 21.73 |
| P50 | 30.71 |
| P90 | 58.91 |
| P95 | 71.23 |
| P99 | 125.93 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 201.25 |
| Min | 58.90 |
| Max | 481.39 |
| Std Dev | 111.69 |
| P50 | 260.56 |
| P90 | 406.73 |
| P95 | 441.46 |
| P99 | 467.59 |

### Config 2: batch=16, concurrency=1

**Total:** 2400 pairs in 7.28s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 48.52 |
| Min | 23.78 |
| Max | 92.41 |
| Std Dev | 18.10 |
| P50 | 40.01 |
| P90 | 74.05 |
| P95 | 79.04 |
| P99 | 85.56 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 329.70 |
| Min | 173.14 |
| Max | 672.73 |
| Std Dev | 131.30 |
| P50 | 399.93 |
| P90 | 543.12 |
| P95 | 586.73 |
| P99 | 615.30 |

### Config 3: batch=32, concurrency=1

**Total:** 4800 pairs in 9.66s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 64.36 |
| Min | 41.29 |
| Max | 119.62 |
| Std Dev | 18.81 |
| P50 | 54.44 |
| P90 | 90.39 |
| P95 | 94.78 |
| P99 | 106.95 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 497.07 |
| Min | 267.52 |
| Max | 774.93 |
| Std Dev | 143.40 |
| P50 | 587.79 |
| P90 | 705.07 |
| P95 | 727.77 |
| P99 | 771.54 |

### Config 4: batch=48, concurrency=1

**Total:** 7200 pairs in 11.48s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 76.49 |
| Min | 62.77 |
| Max | 111.41 |
| Std Dev | 10.48 |
| P50 | 73.46 |
| P90 | 90.46 |
| P95 | 100.62 |
| P99 | 110.60 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 627.38 |
| Min | 430.83 |
| Max | 764.69 |
| Std Dev | 74.08 |
| P50 | 653.41 |
| P90 | 722.20 |
| P95 | 731.21 |
| P99 | 753.30 |

### Config 5: batch=64, concurrency=1

**Total:** 9600 pairs in 13.97s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 93.09 |
| Min | 79.36 |
| Max | 152.60 |
| Std Dev | 9.16 |
| P50 | 91.47 |
| P90 | 104.12 |
| P95 | 106.63 |
| P99 | 118.98 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 687.39 |
| Min | 419.39 |
| Max | 806.45 |
| Std Dev | 59.03 |
| P50 | 699.69 |
| P90 | 760.42 |
| P95 | 774.04 |
| P99 | 791.80 |

### Config 6: batch=96, concurrency=1

**Total:** 14400 pairs in 20.33s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 135.53 |
| Min | 115.40 |
| Max | 185.32 |
| Std Dev | 11.51 |
| P50 | 133.76 |
| P90 | 149.04 |
| P95 | 153.88 |
| P99 | 180.52 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 708.19 |
| Min | 518.02 |
| Max | 831.88 |
| Std Dev | 54.96 |
| P50 | 717.73 |
| P90 | 774.70 |
| P95 | 782.98 |
| P99 | 802.98 |

### Config 7: batch=128, concurrency=1

**Total:** 19200 pairs in 26.48s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 176.49 |
| Min | 155.93 |
| Max | 232.89 |
| Std Dev | 12.10 |
| P50 | 174.84 |
| P90 | 189.31 |
| P95 | 200.62 |
| P99 | 215.01 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 725.14 |
| Min | 549.62 |
| Max | 820.87 |
| Std Dev | 46.73 |
| P50 | 732.11 |
| P90 | 781.98 |
| P95 | 791.22 |
| P99 | 814.75 |

### Config 8: batch=192, concurrency=1

**Total:** 28800 pairs in 39.02s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 260.09 |
| Min | 235.82 |
| Max | 419.24 |
| Std Dev | 18.10 |
| P50 | 258.26 |
| P90 | 272.63 |
| P95 | 275.85 |
| P99 | 318.82 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 738.12 |
| Min | 457.97 |
| Max | 814.19 |
| Std Dev | 41.28 |
| P50 | 743.44 |
| P90 | 787.28 |
| P95 | 796.32 |
| P99 | 810.12 |

### Config 9: batch=256, concurrency=1

**Total:** 38400 pairs in 51.34s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 342.20 |
| Min | 313.31 |
| Max | 430.54 |
| Std Dev | 15.53 |
| P50 | 341.62 |
| P90 | 358.17 |
| P95 | 364.41 |
| P99 | 393.91 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 748.01 |
| Min | 594.61 |
| Max | 817.08 |
| Std Dev | 32.05 |
| P50 | 749.37 |
| P90 | 788.63 |
| P95 | 796.09 |
| P99 | 804.86 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 748.01 p/s | batch=256, conc=1 |
| Best Latency | 39.74ms | batch=8, conc=1 |
| Avg Throughput | 584.70 p/s | all configs |
| Avg Latency | 137.39ms | all configs |
