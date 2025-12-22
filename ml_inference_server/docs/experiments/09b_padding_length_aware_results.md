# 09b_padding_length_aware

**Timestamp:** 2025-12-23 04:20:49

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 4800 | 6.94 | 46.2ms | 65.0ms | 105.5ms | 692.0 | 873.7 |
| 64 | 1 | 9600 | 13.92 | 92.7ms | 126.9ms | 134.6ms | 689.9 | 881.9 |
| 96 | 1 | 14400 | 20.14 | 134.3ms | 177.6ms | 232.5ms | 714.8 | 893.2 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 4800 pairs in 6.94s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 46.23 |
| Min | 33.87 |
| Max | 118.55 |
| Std Dev | 11.92 |
| P50 | 43.40 |
| P90 | 53.26 |
| P95 | 64.98 |
| P99 | 105.47 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 692.00 |
| Min | 269.94 |
| Max | 944.72 |
| Std Dev | 121.73 |
| P50 | 737.32 |
| P90 | 859.62 |
| P95 | 873.69 |
| P99 | 927.87 |

### Config 2: batch=64, concurrency=1

**Total:** 9600 pairs in 13.92s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 92.75 |
| Min | 70.43 |
| Max | 141.73 |
| Std Dev | 16.08 |
| P50 | 91.17 |
| P90 | 114.20 |
| P95 | 126.86 |
| P99 | 134.59 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 689.90 |
| Min | 451.57 |
| Max | 908.71 |
| Std Dev | 113.59 |
| P50 | 701.95 |
| P90 | 853.38 |
| P95 | 881.91 |
| P99 | 896.43 |

### Config 3: batch=96, concurrency=1

**Total:** 14400 pairs in 20.14s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 134.27 |
| Min | 101.47 |
| Max | 252.96 |
| Std Dev | 24.61 |
| P50 | 129.24 |
| P90 | 160.13 |
| P95 | 177.56 |
| P99 | 232.49 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 714.84 |
| Min | 379.51 |
| Max | 946.10 |
| Std Dev | 112.49 |
| P50 | 742.79 |
| P90 | 866.16 |
| P95 | 893.21 |
| P99 | 933.03 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 714.84 p/s | batch=96, conc=1 |
| Best Latency | 46.23ms | batch=32, conc=1 |
| Avg Throughput | 698.91 p/s | all configs |
| Avg Latency | 91.08ms | all configs |
