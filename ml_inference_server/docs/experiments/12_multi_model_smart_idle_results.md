# Multi-Model Smart Idle (4x MPS) (PARTIAL)

**Timestamp:** 2025-12-24 04:23:22

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `True` (max_batch=128, timeout=200ms)

**Model Type:** Cross-Encoder

**Requests per config:** `500`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 8 | 28416 | 54.19 | 966.8ms | 1268.7ms | 1371.3ms | 524.3 | 76.3 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=64, concurrency=8

**Total:** 28416 pairs in 54.19s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 966.83 |
| Min | 203.71 |
| Max | 1513.87 |
| Std Dev | 144.09 |
| P50 | 927.27 |
| P90 | 1185.52 |
| P95 | 1268.70 |
| P99 | 1371.33 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 524.34 |
| Min | 42.28 |
| Max | 314.18 |
| Std Dev | 15.97 |
| P50 | 69.02 |
| P90 | 74.60 |
| P95 | 76.29 |
| P99 | 85.89 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 524.34 p/s | batch=64, conc=8 |
| Best Latency | 966.83ms | batch=64, conc=8 |
| Avg Throughput | 524.34 p/s | all configs |
| Avg Latency | 966.83ms | all configs |
