# 05a_batch_size_mps

**Timestamp:** 2025-12-23 02:26:31

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 1200 | 5.07 | 33.8ms | 57.4ms | 62.3ms | 236.6 | 507.9 |
| 16 | 1 | 2400 | 6.42 | 42.8ms | 70.3ms | 76.5ms | 373.8 | 685.2 |
| 32 | 1 | 4800 | 8.84 | 58.9ms | 89.3ms | 123.5ms | 543.1 | 854.1 |
| 48 | 1 | 7200 | 11.37 | 75.8ms | 108.0ms | 171.4ms | 633.0 | 874.7 |
| 64 | 1 | 9600 | 14.61 | 97.4ms | 132.5ms | 194.5ms | 657.2 | 879.6 |
| 96 | 1 | 14400 | 20.31 | 135.3ms | 165.6ms | 231.0ms | 709.1 | 906.1 |
| 128 | 1 | 19200 | 25.96 | 173.0ms | 215.9ms | 283.4ms | 739.6 | 910.9 |
| 192 | 1 | 28800 | 41.27 | 275.1ms | 409.3ms | 486.6ms | 697.8 | 891.6 |
| 256 | 1 | 38400 | 51.90 | 345.9ms | 417.7ms | 506.8ms | 739.9 | 900.4 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=8, concurrency=1

**Total:** 1200 pairs in 5.07s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 33.81 |
| Min | 14.74 |
| Max | 105.41 |
| Std Dev | 15.94 |
| P50 | 26.26 |
| P90 | 53.93 |
| P95 | 57.40 |
| P99 | 62.33 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 236.56 |
| Min | 75.90 |
| Max | 542.75 |
| Std Dev | 127.68 |
| P50 | 304.64 |
| P90 | 463.10 |
| P95 | 507.85 |
| P99 | 524.71 |

### Config 2: batch=16, concurrency=1

**Total:** 2400 pairs in 6.42s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 42.79 |
| Min | 21.61 |
| Max | 79.20 |
| Std Dev | 17.09 |
| P50 | 33.00 |
| P90 | 65.82 |
| P95 | 70.32 |
| P99 | 76.54 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 373.83 |
| Min | 202.02 |
| Max | 740.51 |
| Std Dev | 161.10 |
| P50 | 484.83 |
| P90 | 639.04 |
| P95 | 685.24 |
| P99 | 731.32 |

### Config 3: batch=32, concurrency=1

**Total:** 4800 pairs in 8.84s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 58.91 |
| Min | 33.99 |
| Max | 139.33 |
| Std Dev | 20.67 |
| P50 | 50.60 |
| P90 | 85.57 |
| P95 | 89.29 |
| P99 | 123.55 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 543.05 |
| Min | 229.67 |
| Max | 941.37 |
| Std Dev | 185.63 |
| P50 | 632.44 |
| P90 | 832.92 |
| P95 | 854.12 |
| P99 | 926.08 |

### Config 4: batch=48, concurrency=1

**Total:** 7200 pairs in 11.37s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 75.81 |
| Min | 50.08 |
| Max | 195.18 |
| Std Dev | 22.58 |
| P50 | 67.03 |
| P90 | 102.04 |
| P95 | 108.02 |
| P99 | 171.39 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 633.05 |
| Min | 245.93 |
| Max | 958.50 |
| Std Dev | 154.98 |
| P50 | 716.14 |
| P90 | 857.01 |
| P95 | 874.72 |
| P99 | 900.12 |

### Config 5: batch=64, concurrency=1

**Total:** 9600 pairs in 14.61s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 97.36 |
| Min | 70.39 |
| Max | 214.70 |
| Std Dev | 24.09 |
| P50 | 91.29 |
| P90 | 122.60 |
| P95 | 132.47 |
| P99 | 194.53 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 657.19 |
| Min | 298.09 |
| Max | 909.19 |
| Std Dev | 134.76 |
| P50 | 701.06 |
| P90 | 855.18 |
| P95 | 879.60 |
| P99 | 907.05 |

### Config 6: batch=96, concurrency=1

**Total:** 14400 pairs in 20.31s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 135.35 |
| Min | 101.96 |
| Max | 501.78 |
| Std Dev | 36.95 |
| P50 | 131.68 |
| P90 | 160.14 |
| P95 | 165.57 |
| P99 | 230.99 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 709.13 |
| Min | 191.32 |
| Max | 941.57 |
| Std Dev | 116.25 |
| P50 | 729.05 |
| P90 | 875.26 |
| P95 | 906.13 |
| P99 | 935.47 |

### Config 7: batch=128, concurrency=1

**Total:** 19200 pairs in 25.96s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 173.03 |
| Min | 134.01 |
| Max | 366.96 |
| Std Dev | 29.67 |
| P50 | 167.26 |
| P90 | 202.91 |
| P95 | 215.94 |
| P99 | 283.43 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 739.63 |
| Min | 348.81 |
| Max | 955.18 |
| Std Dev | 104.73 |
| P50 | 765.29 |
| P90 | 882.80 |
| P95 | 910.94 |
| P99 | 945.74 |

### Config 8: batch=192, concurrency=1

**Total:** 28800 pairs in 41.27s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 275.11 |
| Min | 206.01 |
| Max | 516.14 |
| Std Dev | 60.79 |
| P50 | 257.83 |
| P90 | 358.44 |
| P95 | 409.27 |
| P99 | 486.59 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 697.79 |
| Min | 372.00 |
| Max | 932.01 |
| Std Dev | 121.33 |
| P50 | 744.68 |
| P90 | 876.88 |
| P95 | 891.56 |
| P99 | 906.64 |

### Config 9: batch=256, concurrency=1

**Total:** 38400 pairs in 51.90s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 345.94 |
| Min | 272.48 |
| Max | 700.79 |
| Std Dev | 51.76 |
| P50 | 337.09 |
| P90 | 396.01 |
| P95 | 417.72 |
| P99 | 506.83 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 739.91 |
| Min | 365.30 |
| Max | 939.52 |
| Std Dev | 91.15 |
| P50 | 759.43 |
| P90 | 888.92 |
| P95 | 900.41 |
| P99 | 921.25 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 739.91 p/s | batch=256, conc=1 |
| Best Latency | 33.81ms | batch=8, conc=1 |
| Avg Throughput | 592.24 p/s | all configs |
| Avg Latency | 137.57ms | all configs |
