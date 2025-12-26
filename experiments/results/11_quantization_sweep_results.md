# 11_quantization_sweep_int8

_Compare FP32, FP16, and INT8 quantization on MPS backend_

**Timestamp:** 2025-12-27 01:34:02

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 96 | 1 | 34368 | 60.06 | 167.5ms | 219.3ms | 291.1ms | 572.3 | 715.2 |

## Detailed Metrics

### Config 1: batch=96, concurrency=1

**Total:** 34368 pairs in 60.06s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 167.50 |
| Min | 127.15 |
| Max | 415.78 |
| Std Dev | 32.47 |
| P50 | 159.63 |
| P90 | 207.15 |
| P95 | 219.33 |
| P99 | 291.05 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 572.26 |
| Min | 230.89 |
| Max | 755.00 |
| Std Dev | 86.62 |
| P50 | 601.38 |
| P90 | 687.89 |
| P95 | 715.21 |
| P99 | 743.81 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 159.6ms (P50) | 655.16 | 602.04 | 755.00 | 179 |
| 159.6-179.0ms (P50-P75) | 575.23 | 537.60 | 600.72 | 89 |
| 179.0-207.2ms (P75-P90) | 509.31 | 464.03 | 535.78 | 54 |
| >= 207.2ms (P90+) | 413.53 | 230.89 | 462.01 | 36 |

**Correlation:** -0.945 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 572.26 p/s | batch=96, conc=1 |
| Best Latency | 167.50ms | batch=96, conc=1 |
| Avg Throughput | 572.26 p/s | all configs |
| Avg Latency | 167.50ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 3118.0 | 1136.6 | 3788.6 | 3096.6 | 3788.6 |
| GPU Utilization (%) | 73.6 | 44.5 | 94.2 | 74.3 | 84.4 |
| CPU Usage (%) | 0.9 | 0.6 | 4.0 | 0.8 | 1.4 |
| Tokenization (ms) | 40.9 | 35.1 | 85.7 | 39.0 | 52.3 |
| Inference (ms) | 129.3 | 89.7 | 332.3 | 119.4 | 181.7 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 46.8 | 34.8 | 69.7 | 46.5 | 54.8 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 24.3% |
| Queue Wait | 0.0% |
| Model Inference | 74.9% |
| Other/gRPC | 0.7% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 166.2 | 217.3 | 569.6 | 34848 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/11_quantization_sweep_timeseries.md`
