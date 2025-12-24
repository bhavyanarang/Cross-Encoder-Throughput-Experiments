# Tuning Process Pool (4x MPS + Compile)

**Timestamp:** 2025-12-24 04:46:26

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `True` (max_batch=256, timeout=200ms)

**Model Type:** Cross-Encoder

**Requests per config:** `500`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 8 | 16000 | 31.04 | 493.8ms | 707.0ms | 2466.0ms | 515.5 | 92.8 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=8

**Total:** 16000 pairs in 31.04s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 493.83 |
| Min | 293.14 |
| Max | 2749.14 |
| Std Dev | 275.65 |
| P50 | 436.94 |
| P90 | 640.87 |
| P95 | 707.00 |
| P99 | 2465.97 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 515.45 |
| Min | 11.64 |
| Max | 109.16 |
| Std Dev | 15.12 |
| P50 | 73.24 |
| P90 | 88.49 |
| P95 | 92.81 |
| P99 | 99.82 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 515.45 p/s | batch=32, conc=8 |
| Best Latency | 493.83ms | batch=32, conc=8 |
| Avg Throughput | 515.45 p/s | all configs |
| Avg Latency | 493.83ms | all configs |
