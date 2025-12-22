# cross_encoder_mlx_int8

**Timestamp:** 2025-12-22 23:12:50

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `500`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 26.27 | 209.9ms | 277.1ms | 317.2ms | 609.1 | 183.1 |
| 32 | 8 | 16000 | 25.62 | 408.8ms | 526.7ms | 614.4ms | 624.5 | 90.5 |
| 64 | 4 | 32000 | 46.99 | 375.5ms | 462.4ms | 576.3ms | 681.0 | 198.7 |
| 64 | 8 | 32000 | 47.57 | 758.9ms | 923.9ms | 1007.7ms | 672.6 | 95.9 |
| 128 | 4 | 64000 | 89.12 | 712.8ms | 794.4ms | 846.1ms | 718.1 | 196.9 |
| 128 | 8 | 64000 | 96.13 | 1532.3ms | 1694.3ms | 1724.8ms | 665.7 | 94.0 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=4

**Total:** 16000 pairs in 26.27s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 209.89 |
| Min | 98.71 |
| Max | 354.91 |
| Std Dev | 32.50 |
| P50 | 201.45 |
| P90 | 249.55 |
| P95 | 277.13 |
| P99 | 317.19 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 609.06 |
| Min | 90.16 |
| Max | 324.18 |
| Std Dev | 21.92 |
| P50 | 158.85 |
| P90 | 178.50 |
| P95 | 183.06 |
| P99 | 198.36 |

### Config 2: batch=32, concurrency=8

**Total:** 16000 pairs in 25.62s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 408.78 |
| Min | 275.59 |
| Max | 651.36 |
| Std Dev | 57.08 |
| P50 | 391.43 |
| P90 | 487.33 |
| P95 | 526.69 |
| P99 | 614.36 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 624.48 |
| Min | 49.13 |
| Max | 116.12 |
| Std Dev | 9.34 |
| P50 | 81.75 |
| P90 | 89.09 |
| P95 | 90.48 |
| P99 | 93.46 |

### Config 3: batch=64, concurrency=4

**Total:** 32000 pairs in 46.99s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 375.49 |
| Min | 233.81 |
| Max | 616.06 |
| Std Dev | 49.25 |
| P50 | 365.90 |
| P90 | 423.40 |
| P95 | 462.42 |
| P99 | 576.27 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 681.00 |
| Min | 103.89 |
| Max | 273.72 |
| Std Dev | 19.76 |
| P50 | 174.91 |
| P90 | 192.78 |
| P95 | 198.74 |
| P99 | 218.74 |

### Config 4: batch=64, concurrency=8

**Total:** 32000 pairs in 47.57s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 758.92 |
| Min | 631.94 |
| Max | 1044.67 |
| Std Dev | 82.18 |
| P50 | 731.41 |
| P90 | 869.83 |
| P95 | 923.88 |
| P99 | 1007.68 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 672.63 |
| Min | 61.26 |
| Max | 101.28 |
| Std Dev | 8.45 |
| P50 | 87.50 |
| P90 | 94.75 |
| P95 | 95.87 |
| P99 | 97.98 |

### Config 5: batch=128, concurrency=4

**Total:** 64000 pairs in 89.12s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 712.79 |
| Min | 557.04 |
| Max | 870.71 |
| Std Dev | 42.99 |
| P50 | 705.95 |
| P90 | 768.40 |
| P95 | 794.42 |
| P99 | 846.05 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 718.14 |
| Min | 147.01 |
| Max | 229.79 |
| Std Dev | 10.58 |
| P50 | 181.32 |
| P90 | 192.73 |
| P95 | 196.87 |
| P99 | 201.44 |

### Config 6: batch=128, concurrency=8

**Total:** 64000 pairs in 96.13s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1532.31 |
| Min | 785.88 |
| Max | 1774.33 |
| Std Dev | 115.05 |
| P50 | 1529.73 |
| P90 | 1675.07 |
| P95 | 1694.31 |
| P99 | 1724.83 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 665.74 |
| Min | 72.14 |
| Max | 162.87 |
| Std Dev | 8.30 |
| P50 | 83.67 |
| P90 | 90.17 |
| P95 | 93.96 |
| P99 | 98.64 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 718.14 p/s | batch=128, conc=4 |
| Best Latency | 209.89ms | batch=32, conc=4 |
| Avg Throughput | 661.84 p/s | all configs |
| Avg Latency | 666.36ms | all configs |
