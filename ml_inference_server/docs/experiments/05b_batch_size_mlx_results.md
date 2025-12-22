# 05b_batch_size_mlx

**Timestamp:** 2025-12-23 00:52:00

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 1200 | 5.69 | 37.9ms | 65.0ms | 101.0ms | 210.9 | 433.7 |
| 16 | 1 | 2400 | 7.03 | 46.8ms | 75.4ms | 84.7ms | 341.5 | 596.5 |
| 32 | 1 | 4800 | 9.78 | 65.2ms | 98.7ms | 116.1ms | 490.6 | 719.8 |
| 48 | 1 | 7200 | 11.57 | 77.1ms | 99.1ms | 108.1ms | 622.5 | 730.8 |
| 64 | 1 | 9600 | 13.82 | 92.1ms | 105.0ms | 112.7ms | 694.5 | 775.0 |
| 96 | 1 | 14400 | 20.33 | 135.5ms | 153.9ms | 208.7ms | 708.2 | 791.1 |
| 128 | 1 | 19200 | 27.23 | 181.5ms | 213.9ms | 255.7ms | 705.2 | 795.4 |
| 192 | 1 | 28800 | 39.04 | 260.2ms | 278.0ms | 303.6ms | 737.8 | 794.8 |
| 256 | 1 | 38400 | 51.57 | 343.7ms | 367.8ms | 392.2ms | 744.7 | 796.0 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=8, concurrency=1

**Total:** 1200 pairs in 5.69s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 37.92 |
| Min | 13.40 |
| Max | 116.87 |
| Std Dev | 18.57 |
| P50 | 31.01 |
| P90 | 56.86 |
| P95 | 64.97 |
| P99 | 101.00 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 210.91 |
| Min | 68.45 |
| Max | 596.97 |
| Std Dev | 112.33 |
| P50 | 258.01 |
| P90 | 405.97 |
| P95 | 433.75 |
| P99 | 489.62 |

### Config 2: batch=16, concurrency=1

**Total:** 2400 pairs in 7.03s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 46.84 |
| Min | 24.15 |
| Max | 87.94 |
| Std Dev | 17.26 |
| P50 | 39.42 |
| P90 | 70.66 |
| P95 | 75.40 |
| P99 | 84.66 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 341.53 |
| Min | 181.95 |
| Max | 662.66 |
| Std Dev | 135.02 |
| P50 | 405.92 |
| P90 | 560.02 |
| P95 | 596.52 |
| P99 | 647.54 |

### Config 3: batch=32, concurrency=1

**Total:** 4800 pairs in 9.78s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 65.22 |
| Min | 40.90 |
| Max | 133.45 |
| Std Dev | 20.13 |
| P50 | 54.77 |
| P90 | 93.94 |
| P95 | 98.71 |
| P99 | 116.10 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 490.56 |
| Min | 239.80 |
| Max | 782.44 |
| Std Dev | 146.34 |
| P50 | 584.38 |
| P90 | 705.73 |
| P95 | 719.76 |
| P99 | 769.30 |

### Config 4: batch=48, concurrency=1

**Total:** 7200 pairs in 11.57s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 77.09 |
| Min | 63.22 |
| Max | 115.64 |
| Std Dev | 10.25 |
| P50 | 73.77 |
| P90 | 91.80 |
| P95 | 99.05 |
| P99 | 108.11 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 622.53 |
| Min | 415.09 |
| Max | 759.25 |
| Std Dev | 73.36 |
| P50 | 650.70 |
| P90 | 713.72 |
| P95 | 730.77 |
| P99 | 753.57 |

### Config 5: batch=64, concurrency=1

**Total:** 9600 pairs in 13.82s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 92.13 |
| Min | 79.62 |
| Max | 117.78 |
| Std Dev | 7.20 |
| P50 | 90.65 |
| P90 | 102.18 |
| P95 | 104.97 |
| P99 | 112.73 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 694.55 |
| Min | 543.41 |
| Max | 803.85 |
| Std Dev | 51.99 |
| P50 | 706.00 |
| P90 | 764.09 |
| P95 | 775.05 |
| P99 | 786.55 |

### Config 6: batch=96, concurrency=1

**Total:** 14400 pairs in 20.33s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 135.54 |
| Min | 116.31 |
| Max | 214.60 |
| Std Dev | 14.19 |
| P50 | 133.08 |
| P90 | 148.17 |
| P95 | 153.86 |
| P99 | 208.67 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 708.16 |
| Min | 447.35 |
| Max | 825.40 |
| Std Dev | 60.73 |
| P50 | 721.37 |
| P90 | 778.53 |
| P95 | 791.12 |
| P99 | 803.53 |

### Config 7: batch=128, concurrency=1

**Total:** 19200 pairs in 27.23s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 181.49 |
| Min | 153.75 |
| Max | 264.63 |
| Std Dev | 17.95 |
| P50 | 177.70 |
| P90 | 199.72 |
| P95 | 213.86 |
| P99 | 255.75 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 705.15 |
| Min | 483.69 |
| Max | 832.53 |
| Std Dev | 61.11 |
| P50 | 720.30 |
| P90 | 781.19 |
| P95 | 795.38 |
| P99 | 808.76 |

### Config 8: batch=192, concurrency=1

**Total:** 28800 pairs in 39.04s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 260.20 |
| Min | 234.66 |
| Max | 329.97 |
| Std Dev | 13.39 |
| P50 | 259.54 |
| P90 | 273.93 |
| P95 | 277.99 |
| P99 | 303.62 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 737.78 |
| Min | 581.87 |
| Max | 818.20 |
| Std Dev | 36.29 |
| P50 | 739.77 |
| P90 | 787.86 |
| P95 | 794.78 |
| P99 | 809.64 |

### Config 9: batch=256, concurrency=1

**Total:** 38400 pairs in 51.57s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 343.72 |
| Min | 316.22 |
| Max | 429.45 |
| Std Dev | 15.99 |
| P50 | 343.47 |
| P90 | 361.03 |
| P95 | 367.78 |
| P99 | 392.17 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 744.69 |
| Min | 596.12 |
| Max | 809.56 |
| Std Dev | 33.00 |
| P50 | 745.34 |
| P90 | 787.83 |
| P95 | 795.96 |
| P99 | 805.68 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 744.69 p/s | batch=256, conc=1 |
| Best Latency | 37.92ms | batch=8, conc=1 |
| Avg Throughput | 583.98 p/s | all configs |
| Avg Latency | 137.79ms | all configs |
