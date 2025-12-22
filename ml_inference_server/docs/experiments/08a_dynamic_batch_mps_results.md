# 08a_dynamic_batch_mps

**Timestamp:** 2025-12-23 01:09:16

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `True` (max_batch=96, timeout=20ms)

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 2 | 1600 | 5.87 | 58.7ms | 95.4ms | 105.9ms | 272.5 | 246.1 |
| 8 | 4 | 1600 | 3.44 | 68.6ms | 82.9ms | 105.7ms | 465.6 | 140.9 |
| 8 | 8 | 1600 | 3.34 | 133.1ms | 160.2ms | 169.7ms | 479.4 | 71.3 |
| 16 | 2 | 3200 | 7.24 | 72.3ms | 110.7ms | 120.3ms | 441.7 | 343.1 |
| 16 | 4 | 3200 | 5.95 | 118.5ms | 149.6ms | 160.4ms | 538.0 | 163.2 |
| 16 | 8 | 3200 | 5.92 | 235.9ms | 268.8ms | 292.0ms | 540.4 | 78.1 |
| 32 | 2 | 6400 | 11.48 | 114.6ms | 170.0ms | 187.3ms | 557.3 | 376.0 |
| 32 | 4 | 6400 | 12.03 | 239.8ms | 333.8ms | 365.6ms | 532.0 | 187.9 |
| 32 | 8 | 6400 | 10.22 | 406.8ms | 460.5ms | 472.4ms | 626.1 | 89.6 |
| 64 | 2 | 12800 | 17.80 | 177.8ms | 201.7ms | 211.4ms | 719.2 | 393.6 |
| 64 | 4 | 12800 | 18.01 | 359.6ms | 428.9ms | 478.4ms | 710.8 | 195.3 |
| 64 | 8 | 12800 | 20.05 | 799.5ms | 934.5ms | 963.7ms | 638.4 | 90.4 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=8, concurrency=2

**Total:** 1600 pairs in 5.87s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 58.70 |
| Min | 29.67 |
| Max | 134.67 |
| Std Dev | 21.16 |
| P50 | 58.24 |
| P90 | 85.78 |
| P95 | 95.37 |
| P99 | 105.91 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 272.46 |
| Min | 59.40 |
| Max | 269.63 |
| Std Dev | 54.96 |
| P50 | 137.35 |
| P90 | 235.46 |
| P95 | 246.14 |
| P99 | 263.89 |

### Config 2: batch=8, concurrency=4

**Total:** 1600 pairs in 3.44s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 68.61 |
| Min | 54.58 |
| Max | 107.41 |
| Std Dev | 8.89 |
| P50 | 67.04 |
| P90 | 79.12 |
| P95 | 82.93 |
| P99 | 105.72 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 465.61 |
| Min | 74.48 |
| Max | 146.57 |
| Std Dev | 13.44 |
| P50 | 119.34 |
| P90 | 134.35 |
| P95 | 140.89 |
| P99 | 144.99 |

### Config 3: batch=8, concurrency=8

**Total:** 1600 pairs in 3.34s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 133.12 |
| Min | 98.38 |
| Max | 172.33 |
| Std Dev | 14.23 |
| P50 | 131.87 |
| P90 | 153.26 |
| P95 | 160.18 |
| P99 | 169.67 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 479.39 |
| Min | 46.42 |
| Max | 81.32 |
| Std Dev | 6.40 |
| P50 | 60.67 |
| P90 | 68.60 |
| P95 | 71.25 |
| P99 | 79.52 |

### Config 4: batch=16, concurrency=2

**Total:** 3200 pairs in 7.24s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 72.30 |
| Min | 33.46 |
| Max | 136.82 |
| Std Dev | 21.67 |
| P50 | 71.08 |
| P90 | 104.21 |
| P95 | 110.73 |
| P99 | 120.26 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 441.70 |
| Min | 116.94 |
| Max | 478.21 |
| Std Dev | 70.70 |
| P50 | 225.10 |
| P90 | 330.13 |
| P95 | 343.06 |
| P99 | 416.61 |

### Config 5: batch=16, concurrency=4

**Total:** 3200 pairs in 5.95s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 118.47 |
| Min | 69.98 |
| Max | 167.59 |
| Std Dev | 16.76 |
| P50 | 116.05 |
| P90 | 140.25 |
| P95 | 149.58 |
| P99 | 160.36 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 537.99 |
| Min | 95.47 |
| Max | 228.64 |
| Std Dev | 19.82 |
| P50 | 137.87 |
| P90 | 158.96 |
| P95 | 163.16 |
| P99 | 200.95 |

### Config 6: batch=16, concurrency=8

**Total:** 3200 pairs in 5.92s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 235.86 |
| Min | 186.05 |
| Max | 296.06 |
| Std Dev | 19.63 |
| P50 | 236.09 |
| P90 | 258.61 |
| P95 | 268.83 |
| P99 | 291.96 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 540.44 |
| Min | 54.04 |
| Max | 86.00 |
| Std Dev | 5.65 |
| P50 | 67.77 |
| P90 | 75.04 |
| P95 | 78.06 |
| P99 | 85.01 |

### Config 7: batch=32, concurrency=2

**Total:** 6400 pairs in 11.48s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 114.62 |
| Min | 63.36 |
| Max | 205.18 |
| Std Dev | 26.96 |
| P50 | 106.54 |
| P90 | 157.57 |
| P95 | 170.04 |
| P99 | 187.32 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 557.34 |
| Min | 155.96 |
| Max | 505.02 |
| Std Dev | 61.10 |
| P50 | 300.35 |
| P90 | 366.55 |
| P95 | 375.96 |
| P99 | 412.75 |

### Config 8: batch=32, concurrency=4

**Total:** 6400 pairs in 12.03s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 239.81 |
| Min | 106.61 |
| Max | 383.52 |
| Std Dev | 54.37 |
| P50 | 230.21 |
| P90 | 316.96 |
| P95 | 333.82 |
| P99 | 365.62 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 531.98 |
| Min | 83.44 |
| Max | 300.16 |
| Std Dev | 31.59 |
| P50 | 139.00 |
| P90 | 177.92 |
| P95 | 187.86 |
| P99 | 203.42 |

### Config 9: batch=32, concurrency=8

**Total:** 6400 pairs in 10.22s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 406.84 |
| Min | 154.90 |
| Max | 475.60 |
| Std Dev | 35.14 |
| P50 | 409.85 |
| P90 | 448.73 |
| P95 | 460.54 |
| P99 | 472.42 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 626.11 |
| Min | 67.28 |
| Max | 206.59 |
| Std Dev | 10.80 |
| P50 | 78.08 |
| P90 | 87.55 |
| P95 | 89.61 |
| P99 | 96.50 |

### Config 10: batch=64, concurrency=2

**Total:** 12800 pairs in 17.80s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 177.82 |
| Min | 156.25 |
| Max | 214.63 |
| Std Dev | 11.69 |
| P50 | 175.82 |
| P90 | 193.29 |
| P95 | 201.71 |
| P99 | 211.42 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 719.18 |
| Min | 298.18 |
| Max | 409.61 |
| Std Dev | 22.78 |
| P50 | 364.02 |
| P90 | 390.33 |
| P95 | 393.57 |
| P99 | 401.12 |

### Config 11: batch=64, concurrency=4

**Total:** 12800 pairs in 18.01s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 359.60 |
| Min | 310.65 |
| Max | 492.36 |
| Std Dev | 32.79 |
| P50 | 350.45 |
| P90 | 411.13 |
| P95 | 428.91 |
| P99 | 478.41 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 710.82 |
| Min | 129.99 |
| Max | 206.02 |
| Std Dev | 14.43 |
| P50 | 182.62 |
| P90 | 193.22 |
| P95 | 195.32 |
| P99 | 201.96 |

### Config 12: batch=64, concurrency=8

**Total:** 12800 pairs in 20.05s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 799.53 |
| Min | 494.11 |
| Max | 981.82 |
| Std Dev | 76.97 |
| P50 | 784.86 |
| P90 | 899.19 |
| P95 | 934.52 |
| P99 | 963.69 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 638.39 |
| Min | 65.19 |
| Max | 129.53 |
| Std Dev | 7.99 |
| P50 | 81.54 |
| P90 | 89.50 |
| P95 | 90.43 |
| P99 | 94.40 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 719.18 p/s | batch=64, conc=2 |
| Best Latency | 58.70ms | batch=8, conc=2 |
| Avg Throughput | 543.45 p/s | all configs |
| Avg Latency | 232.11ms | all configs |
