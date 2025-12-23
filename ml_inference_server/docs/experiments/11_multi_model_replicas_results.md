# Multi-Model Replicas (3x MPS) (PARTIAL)

**Timestamp:** 2025-12-24 04:04:03

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 6400 | 15.39 | 305.9ms | 571.8ms | 641.5ms | 415.8 | 209.8 |
| 32 | 8 | 6400 | 10.95 | 430.6ms | 541.6ms | 670.6ms | 584.2 | 107.6 |
| 32 | 12 | 6400 | 12.79 | 748.9ms | 1044.8ms | 1112.5ms | 500.3 | 56.7 |
| 64 | 4 | 12800 | 26.55 | 527.3ms | 947.5ms | 1098.0ms | 482.2 | 199.7 |
| 64 | 8 | 12800 | 26.11 | 1028.0ms | 1484.0ms | 1592.4ms | 490.3 | 94.6 |
| 64 | 12 | 12800 | 26.48 | 1551.2ms | 1994.0ms | 2152.9ms | 483.4 | 55.5 |
| 128 | 4 | 25600 | 50.85 | 1010.3ms | 1702.5ms | 1902.1ms | 503.4 | 199.6 |
| 128 | 8 | 8064 | 15.93 | 1906.1ms | 2459.3ms | 2472.8ms | 506.3 | 122.7 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=4

**Total:** 6400 pairs in 15.39s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 305.90 |
| Min | 120.57 |
| Max | 778.15 |
| Std Dev | 135.25 |
| P50 | 269.16 |
| P90 | 499.62 |
| P95 | 571.76 |
| P99 | 641.48 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 415.78 |
| Min | 41.12 |
| Max | 265.42 |
| Std Dev | 50.75 |
| P50 | 118.89 |
| P90 | 193.46 |
| P95 | 209.84 |
| P99 | 223.73 |

### Config 2: batch=32, concurrency=8

**Total:** 6400 pairs in 10.95s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 430.60 |
| Min | 69.12 |
| Max | 705.50 |
| Std Dev | 97.99 |
| P50 | 460.02 |
| P90 | 526.09 |
| P95 | 541.57 |
| P99 | 670.62 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 584.24 |
| Min | 45.36 |
| Max | 462.99 |
| Std Dev | 36.18 |
| P50 | 69.56 |
| P90 | 105.32 |
| P95 | 107.62 |
| P99 | 186.78 |

### Config 3: batch=32, concurrency=12

**Total:** 6400 pairs in 12.79s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 748.95 |
| Min | 72.10 |
| Max | 1173.61 |
| Std Dev | 169.55 |
| P50 | 774.75 |
| P90 | 942.08 |
| P95 | 1044.85 |
| P99 | 1112.52 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 500.27 |
| Min | 27.27 |
| Max | 443.84 |
| Std Dev | 34.64 |
| P50 | 41.30 |
| P90 | 53.02 |
| P95 | 56.65 |
| P99 | 174.55 |

### Config 4: batch=64, concurrency=4

**Total:** 12800 pairs in 26.55s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 527.26 |
| Min | 164.52 |
| Max | 1141.58 |
| Std Dev | 209.60 |
| P50 | 419.37 |
| P90 | 797.17 |
| P95 | 947.53 |
| P99 | 1098.03 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 482.16 |
| Min | 56.06 |
| Max | 389.01 |
| Std Dev | 48.52 |
| P50 | 152.61 |
| P90 | 190.22 |
| P95 | 199.73 |
| P99 | 222.80 |

### Config 5: batch=64, concurrency=8

**Total:** 12800 pairs in 26.11s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1028.02 |
| Min | 117.85 |
| Max | 1612.42 |
| Std Dev | 261.55 |
| P50 | 1049.50 |
| P90 | 1382.93 |
| P95 | 1483.97 |
| P99 | 1592.38 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 490.30 |
| Min | 39.69 |
| Max | 543.07 |
| Std Dev | 42.10 |
| P50 | 60.98 |
| P90 | 91.45 |
| P95 | 94.60 |
| P99 | 191.07 |

### Config 6: batch=64, concurrency=12

**Total:** 12800 pairs in 26.48s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1551.24 |
| Min | 110.35 |
| Max | 2247.42 |
| Std Dev | 321.46 |
| P50 | 1512.49 |
| P90 | 1874.33 |
| P95 | 1993.98 |
| P99 | 2152.95 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 483.40 |
| Min | 28.48 |
| Max | 579.98 |
| Std Dev | 45.50 |
| P50 | 42.31 |
| P90 | 48.41 |
| P95 | 55.45 |
| P99 | 209.48 |

### Config 7: batch=128, concurrency=4

**Total:** 25600 pairs in 50.85s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1010.28 |
| Min | 456.16 |
| Max | 1922.36 |
| Std Dev | 379.43 |
| P50 | 813.80 |
| P90 | 1574.95 |
| P95 | 1702.47 |
| P99 | 1902.08 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 503.45 |
| Min | 66.58 |
| Max | 280.60 |
| Std Dev | 44.86 |
| P50 | 157.29 |
| P90 | 193.49 |
| P95 | 199.58 |
| P99 | 207.73 |

### Config 8: batch=128, concurrency=8

**Total:** 8064 pairs in 15.93s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1906.11 |
| Min | 247.36 |
| Max | 2473.81 |
| Std Dev | 498.95 |
| P50 | 2138.71 |
| P90 | 2397.53 |
| P95 | 2459.28 |
| P99 | 2472.84 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 506.34 |
| Min | 51.74 |
| Max | 517.47 |
| Std Dev | 63.63 |
| P50 | 59.85 |
| P90 | 93.32 |
| P95 | 122.74 |
| P99 | 356.89 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 584.24 p/s | batch=32, conc=8 |
| Best Latency | 305.90ms | batch=32, conc=4 |
| Avg Throughput | 495.74 p/s | all configs |
| Avg Latency | 938.54ms | all configs |
