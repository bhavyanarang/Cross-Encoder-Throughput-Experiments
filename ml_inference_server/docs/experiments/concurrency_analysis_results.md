# concurrency_analysis

**Timestamp:** 2025-12-23 00:01:48

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `True` (max_batch=64, timeout=25ms)

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 1 | 12800 | 24.15 | 120.7ms | 173.4ms | 188.5ms | 530.0 | 690.9 |
| 64 | 2 | 12800 | 21.53 | 215.2ms | 248.3ms | 256.0ms | 594.4 | 331.5 |
| 64 | 3 | 12800 | 22.53 | 336.6ms | 474.4ms | 570.6ms | 568.2 | 221.3 |
| 64 | 4 | 12800 | 27.01 | 539.1ms | 856.3ms | 1109.9ms | 473.9 | 158.7 |
| 64 | 6 | 12800 | 25.95 | 775.0ms | 1093.7ms | 1227.9ms | 493.2 | 112.5 |
| 64 | 8 | 12800 | 21.04 | 839.9ms | 929.5ms | 950.0ms | 608.4 | 82.3 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=64, concurrency=1

**Total:** 12800 pairs in 24.15s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 120.72 |
| Min | 82.35 |
| Max | 223.87 |
| Std Dev | 23.18 |
| P50 | 117.11 |
| P90 | 146.79 |
| P95 | 173.45 |
| P99 | 188.52 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 530.04 |
| Min | 285.88 |
| Max | 777.19 |
| Std Dev | 91.56 |
| P50 | 546.49 |
| P90 | 662.42 |
| P95 | 690.87 |
| P99 | 732.72 |

### Config 2: batch=64, concurrency=2

**Total:** 12800 pairs in 21.53s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 215.15 |
| Min | 185.46 |
| Max | 258.40 |
| Std Dev | 16.16 |
| P50 | 212.28 |
| P90 | 242.06 |
| P95 | 248.29 |
| P99 | 256.01 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 594.40 |
| Min | 247.68 |
| Max | 345.08 |
| Std Dev | 21.53 |
| P50 | 301.49 |
| P90 | 323.34 |
| P95 | 331.46 |
| P99 | 339.28 |

### Config 3: batch=64, concurrency=3

**Total:** 12800 pairs in 22.53s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 336.58 |
| Min | 229.87 |
| Max | 582.33 |
| Std Dev | 55.67 |
| P50 | 321.45 |
| P90 | 378.96 |
| P95 | 474.35 |
| P99 | 570.57 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 568.23 |
| Min | 109.90 |
| Max | 278.42 |
| Std Dev | 24.66 |
| P50 | 199.10 |
| P90 | 216.96 |
| P95 | 221.27 |
| P99 | 226.50 |

### Config 4: batch=64, concurrency=4

**Total:** 12800 pairs in 27.01s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 539.11 |
| Min | 239.69 |
| Max | 1157.42 |
| Std Dev | 157.72 |
| P50 | 474.58 |
| P90 | 728.96 |
| P95 | 856.33 |
| P99 | 1109.93 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 473.91 |
| Min | 55.30 |
| Max | 267.02 |
| Std Dev | 29.74 |
| P50 | 134.86 |
| P90 | 155.23 |
| P95 | 158.71 |
| P99 | 187.37 |

### Config 5: batch=64, concurrency=6

**Total:** 12800 pairs in 25.95s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 774.97 |
| Min | 470.11 |
| Max | 1254.93 |
| Std Dev | 162.49 |
| P50 | 718.68 |
| P90 | 1038.12 |
| P95 | 1093.71 |
| P99 | 1227.87 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 493.21 |
| Min | 51.00 |
| Max | 136.14 |
| Std Dev | 15.99 |
| P50 | 89.05 |
| P90 | 101.14 |
| P95 | 112.45 |
| P99 | 119.31 |

### Config 6: batch=64, concurrency=8

**Total:** 12800 pairs in 21.04s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 839.91 |
| Min | 713.97 |
| Max | 962.57 |
| Std Dev | 44.80 |
| P50 | 838.90 |
| P90 | 891.42 |
| P95 | 929.49 |
| P99 | 949.96 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 608.42 |
| Min | 66.49 |
| Max | 89.64 |
| Std Dev | 4.08 |
| P50 | 76.29 |
| P90 | 81.17 |
| P95 | 82.31 |
| P99 | 87.69 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 608.42 p/s | batch=64, conc=8 |
| Best Latency | 120.72ms | batch=64, conc=1 |
| Avg Throughput | 544.70 p/s | all configs |
| Avg Latency | 471.07ms | all configs |
