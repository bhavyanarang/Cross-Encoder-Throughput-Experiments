# 02_backend_mps

**Timestamp:** 2025-12-23 04:54:06

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 6400 | 10.57 | 52.8ms | 81.2ms | 97.1ms | 605.3 | 866.4 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 6400 pairs in 10.57s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 52.85 |
| Min | 34.43 |
| Max | 143.54 |
| Std Dev | 17.24 |
| P50 | 45.10 |
| P90 | 75.94 |
| P95 | 81.18 |
| P99 | 97.07 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 605.35 |
| Min | 222.94 |
| Max | 929.33 |
| Std Dev | 170.61 |
| P50 | 709.52 |
| P90 | 847.53 |
| P95 | 866.42 |
| P99 | 912.41 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 605.35 p/s | batch=32, conc=1 |
| Best Latency | 52.85ms | batch=32, conc=1 |
| Avg Throughput | 605.35 p/s | all configs |
| Avg Latency | 52.85ms | all configs |
