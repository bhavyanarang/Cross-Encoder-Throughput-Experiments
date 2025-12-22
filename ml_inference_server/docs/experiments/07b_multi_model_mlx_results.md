# 07b_multi_model_mlx

**Timestamp:** 2025-12-23 01:05:09

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `100`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 3200 | 5.48 | 218.7ms | 262.8ms | 290.8ms | 583.5 | 180.9 |
| 32 | 8 | 3200 | 4.80 | 376.9ms | 410.7ms | 417.7ms | 667.1 | 95.2 |
| 32 | 16 | 3200 | 4.93 | 758.5ms | 975.7ms | 991.4ms | 649.2 | 67.2 |
| 32 | 24 | 3200 | 5.16 | 1143.7ms | 1482.7ms | 1503.7ms | 620.4 | 62.0 |
| 64 | 4 | 6400 | 11.90 | 471.6ms | 666.5ms | 716.7ms | 538.0 | 182.6 |
| 64 | 8 | 6400 | 9.47 | 743.6ms | 901.7ms | 917.9ms | 675.5 | 107.6 |
| 64 | 16 | 6400 | 9.18 | 1415.8ms | 1903.1ms | 1936.9ms | 696.9 | 71.7 |
| 64 | 24 | 6400 | 9.79 | 2167.6ms | 2953.0ms | 3028.0ms | 653.4 | 69.1 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=4

**Total:** 3200 pairs in 5.48s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 218.68 |
| Min | 165.83 |
| Max | 291.87 |
| Std Dev | 28.65 |
| P50 | 214.74 |
| P90 | 256.33 |
| P95 | 262.76 |
| P99 | 290.77 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 583.50 |
| Min | 109.64 |
| Max | 192.97 |
| Std Dev | 19.11 |
| P50 | 149.02 |
| P90 | 174.57 |
| P95 | 180.91 |
| P99 | 192.52 |

### Config 2: batch=32, concurrency=8

**Total:** 3200 pairs in 4.80s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 376.85 |
| Min | 189.61 |
| Max | 418.24 |
| Std Dev | 37.77 |
| P50 | 387.11 |
| P90 | 406.09 |
| P95 | 410.67 |
| P99 | 417.65 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 667.09 |
| Min | 76.51 |
| Max | 168.77 |
| Std Dev | 13.59 |
| P50 | 82.66 |
| P90 | 91.64 |
| P95 | 95.19 |
| P99 | 151.04 |

### Config 3: batch=32, concurrency=16

**Total:** 3200 pairs in 4.93s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 758.53 |
| Min | 459.91 |
| Max | 994.43 |
| Std Dev | 206.21 |
| P50 | 910.01 |
| P90 | 969.25 |
| P95 | 975.69 |
| P99 | 991.43 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 649.23 |
| Min | 32.18 |
| Max | 69.58 |
| Std Dev | 13.38 |
| P50 | 35.16 |
| P90 | 65.80 |
| P95 | 67.18 |
| P99 | 68.85 |

### Config 4: batch=32, concurrency=24

**Total:** 3200 pairs in 5.16s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1143.71 |
| Min | 389.51 |
| Max | 1519.96 |
| Std Dev | 270.92 |
| P50 | 1140.47 |
| P90 | 1461.53 |
| P95 | 1482.67 |
| P99 | 1503.67 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 620.44 |
| Min | 21.05 |
| Max | 82.15 |
| Std Dev | 11.92 |
| P50 | 28.06 |
| P90 | 38.86 |
| P95 | 62.03 |
| P99 | 65.52 |

### Config 5: batch=64, concurrency=4

**Total:** 6400 pairs in 11.90s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 471.65 |
| Min | 332.77 |
| Max | 728.41 |
| Std Dev | 108.91 |
| P50 | 467.49 |
| P90 | 634.16 |
| P95 | 666.53 |
| P99 | 716.73 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 538.03 |
| Min | 87.86 |
| Max | 192.32 |
| Std Dev | 30.67 |
| P50 | 136.92 |
| P90 | 181.35 |
| P95 | 182.64 |
| P99 | 189.86 |

### Config 6: batch=64, concurrency=8

**Total:** 6400 pairs in 9.47s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 743.58 |
| Min | 343.40 |
| Max | 930.60 |
| Std Dev | 89.00 |
| P50 | 744.51 |
| P90 | 814.74 |
| P95 | 901.71 |
| P99 | 917.89 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 675.49 |
| Min | 68.77 |
| Max | 186.37 |
| Std Dev | 15.97 |
| P50 | 85.96 |
| P90 | 95.71 |
| P95 | 107.61 |
| P99 | 179.28 |

### Config 7: batch=64, concurrency=16

**Total:** 6400 pairs in 9.18s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1415.81 |
| Min | 873.31 |
| Max | 1955.24 |
| Std Dev | 418.37 |
| P50 | 1696.72 |
| P90 | 1843.39 |
| P95 | 1903.13 |
| P99 | 1936.88 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 696.85 |
| Min | 32.73 |
| Max | 73.28 |
| Std Dev | 15.69 |
| P50 | 37.72 |
| P90 | 70.23 |
| P95 | 71.68 |
| P99 | 72.33 |

### Config 8: batch=64, concurrency=24

**Total:** 6400 pairs in 9.79s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 2167.64 |
| Min | 883.39 |
| Max | 3056.25 |
| Std Dev | 561.45 |
| P50 | 2073.94 |
| P90 | 2854.43 |
| P95 | 2952.98 |
| P99 | 3027.98 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 653.44 |
| Min | 20.94 |
| Max | 72.45 |
| Std Dev | 13.03 |
| P50 | 30.86 |
| P90 | 39.25 |
| P95 | 69.10 |
| P99 | 70.16 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 696.85 p/s | batch=64, conc=16 |
| Best Latency | 218.68ms | batch=32, conc=4 |
| Avg Throughput | 635.51 p/s | all configs |
| Avg Latency | 912.05ms | all configs |
