# 05a_batch_size_mps (PARTIAL)

**Timestamp:** 2025-12-23 05:31:04

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 1 | 1200 | 7.05 | 47.0ms | 91.8ms | 166.2ms | 170.3 | 435.8 |
| 16 | 1 | 2400 | 9.62 | 64.1ms | 135.0ms | 173.0ms | 249.5 | 580.1 |
| 32 | 1 | 4800 | 10.80 | 72.0ms | 143.6ms | 186.4ms | 444.3 | 833.2 |
| 48 | 1 | 7200 | 14.20 | 94.6ms | 127.7ms | 161.0ms | 507.0 | 742.5 |
| 64 | 1 | 9600 | 20.02 | 133.5ms | 187.3ms | 269.8ms | 479.4 | 698.9 |
| 96 | 1 | 14400 | 27.57 | 183.8ms | 253.4ms | 287.2ms | 522.3 | 666.5 |
| 128 | 1 | 19200 | 43.25 | 288.3ms | 399.8ms | 479.4ms | 444.0 | 617.0 |
| 192 | 1 | ERROR | - | - | - | - | - | - |

## Detailed Sub-Experiment Metrics

### Config 1: batch=8, concurrency=1

**Total:** 1200 pairs in 7.05s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 46.97 |
| Min | 13.90 |
| Max | 226.04 |
| Std Dev | 30.33 |
| P50 | 41.16 |
| P90 | 72.51 |
| P95 | 91.81 |
| P99 | 166.20 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 170.30 |
| Min | 35.39 |
| Max | 575.51 |
| Std Dev | 121.22 |
| P50 | 194.37 |
| P90 | 402.24 |
| P95 | 435.85 |
| P99 | 540.20 |

### Config 2: batch=16, concurrency=1

**Total:** 2400 pairs in 9.62s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 64.12 |
| Min | 22.66 |
| Max | 237.83 |
| Std Dev | 36.36 |
| P50 | 55.93 |
| P90 | 101.51 |
| P95 | 134.99 |
| P99 | 173.04 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 249.50 |
| Min | 67.27 |
| Max | 706.11 |
| Std Dev | 153.74 |
| P50 | 286.08 |
| P90 | 527.68 |
| P95 | 580.10 |
| P99 | 692.86 |

### Config 3: batch=32, concurrency=1

**Total:** 4800 pairs in 10.80s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 72.01 |
| Min | 35.51 |
| Max | 202.67 |
| Std Dev | 34.86 |
| P50 | 58.04 |
| P90 | 111.17 |
| P95 | 143.62 |
| P99 | 186.44 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 444.28 |
| Min | 157.89 |
| Max | 901.26 |
| Std Dev | 206.09 |
| P50 | 551.33 |
| P90 | 807.07 |
| P95 | 833.22 |
| P99 | 884.23 |

### Config 4: batch=48, concurrency=1

**Total:** 7200 pairs in 14.20s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 94.65 |
| Min | 52.18 |
| Max | 173.51 |
| Std Dev | 21.99 |
| P50 | 94.51 |
| P90 | 120.95 |
| P95 | 127.71 |
| P99 | 160.98 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 507.04 |
| Min | 276.64 |
| Max | 919.86 |
| Std Dev | 123.93 |
| P50 | 507.86 |
| P90 | 718.81 |
| P95 | 742.50 |
| P99 | 798.73 |

### Config 5: batch=64, concurrency=1

**Total:** 9600 pairs in 20.02s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 133.47 |
| Min | 85.69 |
| Max | 309.71 |
| Std Dev | 33.88 |
| P50 | 128.01 |
| P90 | 165.22 |
| P95 | 187.28 |
| P99 | 269.76 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 479.42 |
| Min | 206.64 |
| Max | 746.87 |
| Std Dev | 103.11 |
| P50 | 499.98 |
| P90 | 652.39 |
| P95 | 698.86 |
| P99 | 732.83 |

### Config 6: batch=96, concurrency=1

**Total:** 14400 pairs in 27.57s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 183.76 |
| Min | 124.34 |
| Max | 382.28 |
| Std Dev | 35.83 |
| P50 | 179.09 |
| P90 | 221.51 |
| P95 | 253.39 |
| P99 | 287.18 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 522.31 |
| Min | 251.13 |
| Max | 772.08 |
| Std Dev | 89.98 |
| P50 | 536.05 |
| P90 | 649.39 |
| P95 | 666.52 |
| P99 | 738.35 |

### Config 7: batch=128, concurrency=1

**Total:** 19200 pairs in 43.25s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 288.28 |
| Min | 188.36 |
| Max | 508.86 |
| Std Dev | 62.58 |
| P50 | 284.84 |
| P90 | 367.17 |
| P95 | 399.82 |
| P99 | 479.42 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 443.95 |
| Min | 251.54 |
| Max | 679.57 |
| Std Dev | 94.11 |
| P50 | 449.38 |
| P90 | 590.10 |
| P95 | 617.01 |
| P99 | 649.33 |

### Config 8: batch=192, concurrency=1 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "Socket closed"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"Socket closed"}"
>

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 522.31 p/s | batch=96, conc=1 |
| Best Latency | 46.97ms | batch=8, conc=1 |
| Avg Throughput | 402.40 p/s | all configs |
| Avg Latency | 126.18ms | all configs |
