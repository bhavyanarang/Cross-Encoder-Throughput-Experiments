# 09a_padding_baseline

**Timestamp:** 2025-12-23 03:08:40

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 4800 | 9.01 | 60.0ms | 90.2ms | 201.5ms | 532.9 | 850.4 |
| 64 | 1 | 9600 | 13.75 | 91.7ms | 121.6ms | 160.9ms | 698.0 | 885.6 |
| 96 | 1 | 14400 | 19.89 | 132.6ms | 161.1ms | 178.1ms | 724.0 | 897.8 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 4800 pairs in 9.01s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 60.04 |
| Min | 34.56 |
| Max | 203.39 |
| Std Dev | 29.19 |
| P50 | 49.88 |
| P90 | 81.84 |
| P95 | 90.16 |
| P99 | 201.45 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 532.87 |
| Min | 157.33 |
| Max | 926.00 |
| Std Dev | 190.67 |
| P50 | 641.60 |
| P90 | 836.84 |
| P95 | 850.40 |
| P99 | 913.97 |

### Config 2: batch=64, concurrency=1

**Total:** 9600 pairs in 13.75s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 91.66 |
| Min | 69.49 |
| Max | 173.51 |
| Std Dev | 19.07 |
| P50 | 86.94 |
| P90 | 113.81 |
| P95 | 121.61 |
| P99 | 160.93 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 698.03 |
| Min | 368.85 |
| Max | 921.01 |
| Std Dev | 122.68 |
| P50 | 736.10 |
| P90 | 873.37 |
| P95 | 885.63 |
| P99 | 899.59 |

### Config 3: batch=96, concurrency=1

**Total:** 14400 pairs in 19.89s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 132.57 |
| Min | 102.60 |
| Max | 472.13 |
| Std Dev | 32.86 |
| P50 | 129.65 |
| P90 | 157.17 |
| P95 | 161.07 |
| P99 | 178.09 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 723.98 |
| Min | 203.34 |
| Max | 935.64 |
| Std Dev | 106.18 |
| P50 | 740.44 |
| P90 | 883.03 |
| P95 | 897.84 |
| P99 | 914.29 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 723.98 p/s | batch=96, conc=1 |
| Best Latency | 60.04ms | batch=32, conc=1 |
| Avg Throughput | 651.63 p/s | all configs |
| Avg Latency | 94.76ms | all configs |
