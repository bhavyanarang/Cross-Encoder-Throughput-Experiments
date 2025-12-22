# 04_backend_onnx

**Timestamp:** 2025-12-23 00:30:49

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `onnx`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 6400 | 56.96 | 284.8ms | 363.0ms | 406.3ms | 112.4 | 118.3 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 6400 pairs in 56.96s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 284.80 |
| Min | 269.85 |
| Max | 413.71 |
| Std Dev | 27.94 |
| P50 | 275.51 |
| P90 | 298.84 |
| P95 | 362.99 |
| P99 | 406.31 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 112.36 |
| Min | 77.35 |
| Max | 118.58 |
| Std Dev | 8.58 |
| P50 | 116.15 |
| P90 | 118.15 |
| P95 | 118.31 |
| P99 | 118.48 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 112.36 p/s | batch=32, conc=1 |
| Best Latency | 284.80ms | batch=32, conc=1 |
| Avg Throughput | 112.36 p/s | all configs |
| Avg Latency | 284.80ms | all configs |
