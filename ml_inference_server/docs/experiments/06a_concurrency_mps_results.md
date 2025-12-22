# 06a_concurrency_mps

**Timestamp:** 2025-12-23 00:56:19

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 96 | 1 | 14400 | 21.92 | 146.1ms | 198.7ms | 233.0ms | 657.0 | 783.2 |
| 96 | 2 | 14400 | 19.20 | 256.0ms | 273.1ms | 280.9ms | 749.8 | 402.4 |
| 96 | 3 | 14400 | 19.29 | 385.8ms | 464.9ms | 493.3ms | 746.4 | 267.8 |
| 96 | 4 | 14400 | 19.01 | 503.5ms | 539.8ms | 564.5ms | 757.7 | 201.1 |
| 96 | 6 | 14400 | 19.95 | 797.5ms | 835.7ms | 867.7ms | 722.0 | 125.7 |
| 96 | 8 | 14400 | 23.11 | 1223.3ms | 1556.4ms | 1751.5ms | 623.1 | 92.5 |
| 96 | 12 | 14400 | 20.29 | 1605.8ms | 2618.9ms | 2697.9ms | 709.8 | 73.4 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=96, concurrency=1

**Total:** 14400 pairs in 21.92s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 146.09 |
| Min | 117.00 |
| Max | 320.09 |
| Std Dev | 26.57 |
| P50 | 137.68 |
| P90 | 175.39 |
| P95 | 198.66 |
| P99 | 233.01 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 656.99 |
| Min | 299.91 |
| Max | 820.51 |
| Std Dev | 92.59 |
| P50 | 697.28 |
| P90 | 768.33 |
| P95 | 783.21 |
| P99 | 812.18 |

### Config 2: batch=96, concurrency=2

**Total:** 14400 pairs in 19.20s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 256.02 |
| Min | 236.10 |
| Max | 285.22 |
| Std Dev | 10.50 |
| P50 | 256.17 |
| P90 | 269.68 |
| P95 | 273.13 |
| P99 | 280.91 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 749.81 |
| Min | 336.58 |
| Max | 406.61 |
| Std Dev | 15.32 |
| P50 | 374.75 |
| P90 | 392.79 |
| P95 | 402.44 |
| P99 | 405.39 |

### Config 3: batch=96, concurrency=3

**Total:** 14400 pairs in 19.29s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 385.77 |
| Min | 345.91 |
| Max | 509.21 |
| Std Dev | 27.96 |
| P50 | 380.92 |
| P90 | 400.15 |
| P95 | 464.93 |
| P99 | 493.28 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 746.38 |
| Min | 188.53 |
| Max | 277.53 |
| Std Dev | 15.61 |
| P50 | 252.02 |
| P90 | 264.31 |
| P95 | 267.85 |
| P99 | 276.42 |

### Config 4: batch=96, concurrency=4

**Total:** 14400 pairs in 19.01s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 503.50 |
| Min | 247.77 |
| Max | 579.69 |
| Std Dev | 35.59 |
| P50 | 504.54 |
| P90 | 531.16 |
| P95 | 539.77 |
| P99 | 564.55 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 757.67 |
| Min | 165.61 |
| Max | 387.45 |
| Std Dev | 23.76 |
| P50 | 190.27 |
| P90 | 198.54 |
| P95 | 201.08 |
| P99 | 298.40 |

### Config 5: batch=96, concurrency=6

**Total:** 14400 pairs in 19.95s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 797.54 |
| Min | 744.18 |
| Max | 881.55 |
| Std Dev | 23.33 |
| P50 | 795.14 |
| P90 | 826.44 |
| P95 | 835.74 |
| P99 | 867.67 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 721.98 |
| Min | 108.90 |
| Max | 129.00 |
| Std Dev | 3.45 |
| P50 | 120.73 |
| P90 | 124.32 |
| P95 | 125.72 |
| P99 | 128.17 |

### Config 6: batch=96, concurrency=8

**Total:** 14400 pairs in 23.11s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1223.30 |
| Min | 764.45 |
| Max | 1835.20 |
| Std Dev | 169.46 |
| P50 | 1229.20 |
| P90 | 1386.26 |
| P95 | 1556.38 |
| P99 | 1751.53 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 623.08 |
| Min | 52.31 |
| Max | 125.58 |
| Std Dev | 10.67 |
| P50 | 78.10 |
| P90 | 91.10 |
| P95 | 92.49 |
| P99 | 109.73 |

### Config 7: batch=96, concurrency=12

**Total:** 14400 pairs in 20.29s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1605.79 |
| Min | 1230.28 |
| Max | 2698.77 |
| Std Dev | 476.02 |
| P50 | 1392.59 |
| P90 | 2596.71 |
| P95 | 2618.87 |
| P99 | 2697.95 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 709.76 |
| Min | 35.57 |
| Max | 78.03 |
| Std Dev | 12.94 |
| P50 | 68.94 |
| P90 | 72.57 |
| P95 | 73.43 |
| P99 | 74.72 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 757.67 p/s | batch=96, conc=4 |
| Best Latency | 146.09ms | batch=96, conc=1 |
| Avg Throughput | 709.38 p/s | all configs |
| Avg Latency | 702.57ms | all configs |
