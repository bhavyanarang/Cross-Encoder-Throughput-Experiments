# 10b_padding_length_aware

_Length-aware batching enabled (sorted by length)_

**Timestamp:** 2025-12-26 16:37:51

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=64, timeout=50ms)

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 1 | 32000 | 46.85 | 93.6ms | 131.5ms | 191.1ms | 683.1 | 834.2 |

## Detailed Metrics

### Config 1: batch=64, concurrency=1

**Total:** 32000 pairs in 46.85s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 93.56 |
| Min | 68.62 |
| Max | 264.04 |
| Std Dev | 21.66 |
| P50 | 87.11 |
| P90 | 116.18 |
| P95 | 131.49 |
| P99 | 191.06 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 683.05 |
| Min | 242.38 |
| Max | 932.71 |
| Std Dev | 111.14 |
| P50 | 734.74 |
| P90 | 818.12 |
| P95 | 834.17 |
| P99 | 873.92 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 87.1ms (P50) | 791.14 | 735.20 | 932.71 | 250 |
| 87.1-96.1ms (P50-P75) | 696.70 | 665.76 | 734.28 | 125 |
| 96.1-116.2ms (P75-P90) | 615.48 | 550.92 | 665.44 | 75 |
| >= 116.2ms (P90+) | 461.45 | 242.38 | 550.38 | 50 |

**Correlation:** -0.940 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 683.05 p/s | batch=64, conc=1 |
| Best Latency | 93.56ms | batch=64, conc=1 |
| Avg Throughput | 683.05 p/s | all configs |
| Avg Latency | 93.56ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 2355.4 | 1158.6 | 2734.6 | 2540.8 | 2734.6 |
| GPU Utilization (%) | 69.8 | 37.7 | 93.0 | 69.9 | 77.2 |
| CPU Usage (%) | 1.3 | 0.8 | 1.6 | 1.3 | 1.5 |
| Tokenization (ms) | 24.2 | 19.3 | 51.1 | 23.5 | 27.3 |
| Inference (ms) | 65.2 | 49.1 | 172.5 | 62.0 | 98.7 |
| Queue Wait (ms) | 1.3 | 1.1 | 3.8 | 1.3 | 1.3 |
| Padding Waste (%) | 45.1 | 34.1 | 59.8 | 44.9 | 53.8 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 26.2% |
| Queue Wait | 1.4% |
| Model Inference | 71.2% |
| Other/gRPC | 1.1% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 92.5 | 131.6 | 678.0 | 32320 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/10b_padding_length_aware_timeseries.md`
