# 07b_dynamic_batch_enabled

_Dynamic batching enabled with max_batch=96, timeout=50ms_

**Timestamp:** 2025-12-26 16:17:45

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

**Dynamic Batching:** enabled (max_batch=96, timeout=50ms)

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 16000 | 23.33 | 186.4ms | 240.5ms | 288.3ms | 686.0 | 209.6 |

## Detailed Metrics

### Config 1: batch=32, concurrency=4

**Total:** 16000 pairs in 23.33s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 186.42 |
| Min | 148.06 |
| Max | 588.54 |
| Std Dev | 44.79 |
| P50 | 175.06 |
| P90 | 223.10 |
| P95 | 240.47 |
| P99 | 288.31 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 685.95 |
| Min | 54.37 |
| Max | 216.12 |
| Std Dev | 25.30 |
| P50 | 182.80 |
| P90 | 206.36 |
| P95 | 209.56 |
| P99 | 214.49 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 175.1ms (P50) | 195.90 | 182.80 | 216.12 | 250 |
| 175.1-196.4ms (P50-P75) | 173.16 | 162.93 | 182.80 | 125 |
| 196.4-223.1ms (P75-P90) | 154.36 | 143.44 | 162.92 | 75 |
| >= 223.1ms (P90+) | 125.85 | 54.37 | 143.40 | 50 |

**Correlation:** -0.876 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 685.95 p/s | batch=32, conc=4 |
| Best Latency | 186.42ms | batch=32, conc=4 |
| Avg Throughput | 685.95 p/s | all configs |
| Avg Latency | 186.42ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 3365.5 | 1288.6 | 4096.6 | 3710.6 | 4096.6 |
| GPU Utilization (%) | 99.3 | 64.1 | 100.0 | 100.0 | 100.0 |
| CPU Usage (%) | 1.6 | 1.2 | 2.3 | 1.6 | 2.1 |
| Tokenization (ms) | 44.0 | 15.4 | 55.4 | 43.8 | 50.5 |
| Inference (ms) | 131.9 | 57.3 | 208.3 | 125.9 | 180.7 |
| Queue Wait (ms) | 4.6 | 1.1 | 153.8 | 1.3 | 2.0 |
| Padding Waste (%) | 48.2 | 39.6 | 59.5 | 47.5 | 55.9 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 24.3% |
| Queue Wait | 1.2% |
| Model Inference | 73.8% |
| Other/gRPC | 0.7% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 183.6 | 239.0 | 672.7 | 16160 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/07b_dynamic_batch_enabled_timeseries.md`
