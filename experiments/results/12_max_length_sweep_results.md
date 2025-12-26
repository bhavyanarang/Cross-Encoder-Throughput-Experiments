# 12_max_length_sweep_mps

_Test max sequence length=512 on MPS and MLX backends_

**Timestamp:** 2025-12-27 01:35:39

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `mps` | **Device:** `mps`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 64 | 1 | 32000 | 55.51 | 110.9ms | 157.6ms | 194.7ms | 576.5 | 736.4 |

## Detailed Metrics

### Config 1: batch=64, concurrency=1

**Total:** 32000 pairs in 55.51s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 110.85 |
| Min | 78.82 |
| Max | 360.94 |
| Std Dev | 25.03 |
| P50 | 106.11 |
| P90 | 134.87 |
| P95 | 157.63 |
| P99 | 194.66 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 576.48 |
| Min | 177.31 |
| Max | 812.03 |
| Std Dev | 98.70 |
| P50 | 603.16 |
| P90 | 714.35 |
| P95 | 736.39 |
| P99 | 771.36 |

#### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 106.1ms (P50) | 674.82 | 603.50 | 812.03 | 250 |
| 106.1-117.1ms (P50-P75) | 575.70 | 546.73 | 602.81 | 125 |
| 117.1-134.9ms (P75-P90) | 512.93 | 474.56 | 546.14 | 75 |
| >= 134.9ms (P90+) | 396.88 | 177.31 | 474.41 | 50 |

**Correlation:** -0.925 (negative correlation expected: lower latency = higher throughput)

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 576.48 p/s | batch=64, conc=1 |
| Best Latency | 110.85ms | batch=64, conc=1 |
| Avg Throughput | 576.48 p/s | all configs |
| Avg Latency | 110.85ms | all configs |

## Dashboard Metrics Summary

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 2405.7 | 1212.6 | 2734.6 | 2460.8 | 2734.6 |
| GPU Utilization (%) | 73.5 | 57.6 | 82.2 | 74.1 | 80.1 |
| CPU Usage (%) | 1.1 | 0.7 | 1.5 | 1.1 | 1.3 |
| Tokenization (ms) | 28.9 | 22.6 | 142.6 | 26.0 | 42.4 |
| Inference (ms) | 83.6 | 55.4 | 148.7 | 80.4 | 119.8 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 45.3 | 35.6 | 59.4 | 44.6 | 52.8 |

### Stage Breakdown

| Stage | Percentage |
|-------|------------|
| Tokenization | 24.8% |
| Queue Wait | 0.0% |
| Model Inference | 74.3% |
| Other/gRPC | 0.9% |

### Per-Worker Statistics

| Worker ID | Avg Latency (ms) | P95 Latency (ms) | Throughput (q/s) | Queries |
|-----------|------------------|------------------|------------------|--------|
| 0 | 109.7 | 156.5 | 572.9 | 32320 |

## Dashboard Time-Series Data

Full time-series data is available in: `distribution/12_max_length_sweep_timeseries.md`
