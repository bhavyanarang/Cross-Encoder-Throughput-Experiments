# 04_backend_compiled

**Timestamp:** 2025-12-23 01:37:51

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `compiled`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 6400 | 29.97 | 149.8ms | 178.9ms | 201.3ms | 213.5 | 261.7 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 6400 pairs in 29.97s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 149.84 |
| Min | 111.14 |
| Max | 1510.97 |
| Std Dev | 98.06 |
| P50 | 138.34 |
| P90 | 165.42 |
| P95 | 178.88 |
| P99 | 201.30 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 213.53 |
| Min | 21.18 |
| Max | 287.92 |
| Std Dev | 28.70 |
| P50 | 231.31 |
| P90 | 255.91 |
| P95 | 261.74 |
| P99 | 270.45 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 213.53 p/s | batch=32, conc=1 |
| Best Latency | 149.84ms | batch=32, conc=1 |
| Avg Throughput | 213.53 p/s | all configs |
| Avg Latency | 149.84ms | all configs |
