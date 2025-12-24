# Multi-Model Process Pool (2x MPS)

**Timestamp:** 2025-12-24 20:28:03

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `500`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 8 | 32000 | 67.05 | 1066.2ms | 1274.1ms | 1879.4ms | 477.2 | 72.3 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=64, concurrency=8

**Total:** 32000 pairs in 67.05s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 1066.16 |
| Min | 820.19 |
| Max | 2490.01 |
| Std Dev | 169.44 |
| P50 | 1037.80 |
| P90 | 1212.25 |
| P95 | 1274.09 |
| P99 | 1879.45 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 477.22 |
| Min | 25.70 |
| Max | 78.03 |
| Std Dev | 7.34 |
| P50 | 61.67 |
| P90 | 69.82 |
| P95 | 72.27 |
| P99 | 76.05 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 477.22 p/s | batch=64, conc=8 |
| Best Latency | 1066.16ms | batch=64, conc=8 |
| Avg Throughput | 477.22 p/s | all configs |
| Avg Latency | 1066.16ms | all configs |
