# 08b_dynamic_batch_mlx

**Timestamp:** 2025-12-23 01:13:41

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `True` (max_batch=96, timeout=20ms)

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 2 | 1600 | 5.71 | 57.1ms | 92.1ms | 119.7ms | 280.3 | 272.9 |
| 8 | 4 | 1600 | 3.85 | 76.7ms | 97.7ms | 105.2ms | 416.1 | 139.1 |
| 8 | 8 | 1600 | 3.26 | 130.0ms | 155.2ms | 161.6ms | 490.8 | 71.5 |
| 16 | 2 | 3200 | 7.34 | 73.3ms | 109.3ms | 133.2ms | 436.1 | 338.6 |
| 16 | 4 | 3200 | 6.26 | 125.0ms | 172.4ms | 189.6ms | 511.0 | 171.0 |
| 16 | 8 | 3200 | 6.04 | 240.4ms | 300.3ms | 325.5ms | 529.5 | 80.9 |
| 32 | 2 | 6400 | 11.18 | 111.6ms | 157.3ms | 185.9ms | 572.3 | 383.6 |
| 32 | 4 | 6400 | 13.53 | 269.9ms | 355.4ms | 384.7ms | 473.0 | 182.5 |
| 32 | 8 | 6400 | 9.74 | 388.4ms | 413.5ms | 453.2ms | 657.4 | 90.5 |
| 64 | 2 | 12800 | 18.08 | 180.8ms | 212.3ms | 248.4ms | 707.8 | 394.5 |
| 64 | 4 | 12800 | 18.42 | 368.1ms | 425.8ms | 432.9ms | 694.7 | 195.3 |
| 64 | 8 | 12800 | 20.18 | 805.0ms | 1003.4ms | 1048.2ms | 634.2 | 92.3 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=8, concurrency=2

**Total:** 1600 pairs in 5.71s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 57.06 |
| Min | 26.22 |
| Max | 139.07 |
| Std Dev | 22.64 |
| P50 | 55.73 |
| P90 | 88.28 |
| P95 | 92.15 |
| P99 | 119.69 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 280.31 |
| Min | 57.53 |
| Max | 305.05 |
| Std Dev | 62.95 |
| P50 | 143.55 |
| P90 | 248.38 |
| P95 | 272.89 |
| P99 | 300.96 |

### Config 2: batch=8, concurrency=4

**Total:** 1600 pairs in 3.85s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 76.72 |
| Min | 52.79 |
| Max | 121.37 |
| Std Dev | 12.94 |
| P50 | 76.07 |
| P90 | 93.45 |
| P95 | 97.74 |
| P99 | 105.21 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 416.11 |
| Min | 65.91 |
| Max | 151.55 |
| Std Dev | 18.04 |
| P50 | 105.17 |
| P90 | 132.69 |
| P95 | 139.10 |
| P99 | 144.86 |

### Config 3: batch=8, concurrency=8

**Total:** 1600 pairs in 3.26s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 130.00 |
| Min | 95.39 |
| Max | 167.80 |
| Std Dev | 12.21 |
| P50 | 128.35 |
| P90 | 149.79 |
| P95 | 155.22 |
| P99 | 161.64 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 490.75 |
| Min | 47.68 |
| Max | 83.86 |
| Std Dev | 5.69 |
| P50 | 62.33 |
| P90 | 68.33 |
| P95 | 71.54 |
| P99 | 75.31 |

### Config 4: batch=16, concurrency=2

**Total:** 3200 pairs in 7.34s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 73.32 |
| Min | 44.04 |
| Max | 133.79 |
| Std Dev | 21.72 |
| P50 | 69.85 |
| P90 | 104.86 |
| P95 | 109.26 |
| P99 | 133.18 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 436.08 |
| Min | 119.59 |
| Max | 363.27 |
| Std Dev | 65.92 |
| P50 | 229.05 |
| P90 | 328.03 |
| P95 | 338.58 |
| P99 | 350.84 |

### Config 5: batch=16, concurrency=4

**Total:** 3200 pairs in 6.26s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 125.04 |
| Min | 69.73 |
| Max | 198.49 |
| Std Dev | 26.52 |
| P50 | 117.10 |
| P90 | 162.15 |
| P95 | 172.36 |
| P99 | 189.60 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 511.02 |
| Min | 80.61 |
| Max | 229.46 |
| Std Dev | 26.79 |
| P50 | 136.63 |
| P90 | 166.87 |
| P95 | 171.03 |
| P99 | 177.74 |

### Config 6: batch=16, concurrency=8

**Total:** 3200 pairs in 6.04s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 240.43 |
| Min | 176.21 |
| Max | 328.28 |
| Std Dev | 31.76 |
| P50 | 240.82 |
| P90 | 280.75 |
| P95 | 300.25 |
| P99 | 325.48 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 529.48 |
| Min | 48.74 |
| Max | 90.80 |
| Std Dev | 8.60 |
| P50 | 66.44 |
| P90 | 78.90 |
| P95 | 80.93 |
| P99 | 83.11 |

### Config 7: batch=32, concurrency=2

**Total:** 6400 pairs in 11.18s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 111.59 |
| Min | 61.27 |
| Max | 225.42 |
| Std Dev | 25.51 |
| P50 | 104.61 |
| P90 | 147.86 |
| P95 | 157.26 |
| P99 | 185.88 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 572.35 |
| Min | 141.95 |
| Max | 522.30 |
| Std Dev | 61.71 |
| P50 | 305.91 |
| P90 | 372.57 |
| P95 | 383.61 |
| P99 | 434.54 |

### Config 8: batch=32, concurrency=4

**Total:** 6400 pairs in 13.53s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 269.87 |
| Min | 122.26 |
| Max | 418.19 |
| Std Dev | 60.08 |
| P50 | 281.35 |
| P90 | 338.36 |
| P95 | 355.42 |
| P99 | 384.72 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 473.01 |
| Min | 76.52 |
| Max | 261.74 |
| Std Dev | 32.05 |
| P50 | 113.74 |
| P90 | 174.21 |
| P95 | 182.54 |
| P99 | 197.93 |

### Config 9: batch=32, concurrency=8

**Total:** 6400 pairs in 9.74s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 388.38 |
| Min | 270.50 |
| Max | 457.89 |
| Std Dev | 21.01 |
| P50 | 388.37 |
| P90 | 406.36 |
| P95 | 413.51 |
| P99 | 453.23 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 657.35 |
| Min | 69.89 |
| Max | 118.30 |
| Std Dev | 4.77 |
| P50 | 82.39 |
| P90 | 86.73 |
| P95 | 90.51 |
| P99 | 93.78 |

### Config 10: batch=64, concurrency=2

**Total:** 12800 pairs in 18.08s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 180.80 |
| Min | 152.63 |
| Max | 297.53 |
| Std Dev | 18.88 |
| P50 | 177.02 |
| P90 | 199.17 |
| P95 | 212.28 |
| P99 | 248.43 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 707.80 |
| Min | 215.10 |
| Max | 419.31 |
| Std Dev | 31.38 |
| P50 | 361.54 |
| P90 | 389.96 |
| P95 | 394.47 |
| P99 | 412.63 |

### Config 11: batch=64, concurrency=4

**Total:** 12800 pairs in 18.42s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 368.08 |
| Min | 274.95 |
| Max | 461.26 |
| Std Dev | 31.23 |
| P50 | 363.25 |
| P90 | 412.67 |
| P95 | 425.83 |
| P99 | 432.90 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 694.73 |
| Min | 138.75 |
| Max | 232.77 |
| Std Dev | 14.71 |
| P50 | 176.19 |
| P90 | 191.02 |
| P95 | 195.28 |
| P99 | 209.89 |

### Config 12: batch=64, concurrency=8

**Total:** 12800 pairs in 20.18s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 805.03 |
| Min | 471.00 |
| Max | 1078.12 |
| Std Dev | 105.33 |
| P50 | 773.75 |
| P90 | 987.02 |
| P95 | 1003.42 |
| P99 | 1048.16 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 634.24 |
| Min | 59.36 |
| Max | 135.88 |
| Std Dev | 10.17 |
| P50 | 82.71 |
| P90 | 90.89 |
| P95 | 92.30 |
| P99 | 93.52 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 707.80 p/s | batch=64, conc=2 |
| Best Latency | 57.06ms | batch=8, conc=2 |
| Avg Throughput | 533.60 p/s | all configs |
| Avg Latency | 235.53ms | all configs |
