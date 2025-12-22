# 10a_packing_disabled

**Timestamp:** 2025-12-23 03:23:14

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 4800 | 9.32 | 62.1ms | 99.5ms | 136.2ms | 515.0 | 839.6 |
| 64 | 1 | 9600 | 13.78 | 91.9ms | 121.8ms | 146.8ms | 696.6 | 889.0 |
| 96 | 1 | 14400 | 20.28 | 135.2ms | 170.3ms | 182.5ms | 709.9 | 888.0 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 4800 pairs in 9.32s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 62.12 |
| Min | 34.44 |
| Max | 153.22 |
| Std Dev | 22.98 |
| P50 | 61.87 |
| P90 | 84.91 |
| P95 | 99.49 |
| P99 | 136.20 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 514.97 |
| Min | 208.85 |
| Max | 929.19 |
| Std Dev | 185.81 |
| P50 | 517.30 |
| P90 | 822.55 |
| P95 | 839.57 |
| P99 | 908.66 |

### Config 2: batch=64, concurrency=1

**Total:** 9600 pairs in 13.78s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 91.86 |
| Min | 67.79 |
| Max | 149.74 |
| Std Dev | 16.96 |
| P50 | 87.95 |
| P90 | 114.85 |
| P95 | 121.77 |
| P99 | 146.78 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 696.57 |
| Min | 427.40 |
| Max | 944.15 |
| Std Dev | 117.93 |
| P50 | 727.65 |
| P90 | 859.46 |
| P95 | 888.95 |
| P99 | 908.82 |

### Config 3: batch=96, concurrency=1

**Total:** 14400 pairs in 20.28s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 135.20 |
| Min | 105.01 |
| Max | 561.25 |
| Std Dev | 39.50 |
| P50 | 131.13 |
| P90 | 157.66 |
| P95 | 170.28 |
| P99 | 182.47 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 709.91 |
| Min | 171.05 |
| Max | 914.17 |
| Std Dev | 108.44 |
| P50 | 732.12 |
| P90 | 867.02 |
| P95 | 888.00 |
| P99 | 907.13 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 709.91 p/s | batch=96, conc=1 |
| Best Latency | 62.12ms | batch=32, conc=1 |
| Avg Throughput | 640.48 p/s | all configs |
| Avg Latency | 96.39ms | all configs |
