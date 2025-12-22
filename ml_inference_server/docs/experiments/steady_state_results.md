# steady_state

**Timestamp:** 2025-12-22 23:58:31

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mlx`

**Dynamic Batching:** `True` (max_batch=96, timeout=20ms)

**Model Type:** Cross-Encoder

**Requests per config:** `500`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 96 | 3 | 48000 | 91.03 | 546.0ms | 713.5ms | 779.5ms | 527.3 | 208.6 |

## Detailed Sub-Experiment Metrics

### Config 1: batch=96, concurrency=3

**Total:** 48000 pairs in 91.03s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 545.97 |
| Min | 409.73 |
| Max | 975.26 |
| Std Dev | 76.63 |
| P50 | 528.37 |
| P90 | 671.38 |
| P95 | 713.54 |
| P99 | 779.54 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 527.32 |
| Min | 98.43 |
| Max | 234.30 |
| Std Dev | 21.73 |
| P50 | 181.69 |
| P90 | 203.75 |
| P95 | 208.55 |
| P99 | 216.98 |

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 527.32 p/s | batch=96, conc=3 |
| Best Latency | 545.97ms | batch=96, conc=3 |
| Avg Throughput | 527.32 p/s | all configs |
| Avg Latency | 545.97ms | all configs |
