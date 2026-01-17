# inference_only

**Timestamp:** 2026-01-01 23:21:14

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Backend:** `pytorch` | **Device:** `mps`

## Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 4 | 14976 | 61.69 | 520.8ms | 531.3ms | 556.7ms | 242.8 | 62.0 |
| 32 | 8 | 33760 | 63.87 | 471.0ms | 544.0ms | 554.3ms | 528.5 | 1159.5 |
| 32 | 16 | 66400 | 67.68 | 492.6ms | 578.7ms | 638.2ms | 981.1 | 601.1 |
| 64 | 4 | 30144 | 61.83 | 518.6ms | 542.1ms | 545.1ms | 487.5 | 122.8 |
| 64 | 8 | 19712 | 129.01 | 440.6ms | 561.3ms | 567.0ms | 152.8 | 1464.7 |
| 64 | 16 | ERROR | - | - | - | - | - | - |
| 128 | 4 | ERROR | - | - | - | - | - | - |
| 128 | 8 | ERROR | - | - | - | - | - | - |
| 128 | 16 | ERROR | - | - | - | - | - | - |

## Detailed Metrics

### Run 1

**Total:** 14976 pairs in 61.69s

### Latency

| Metric | Value |
|--------|-------|
| Average | 520.77 |
| Min | 15.69 |
| Max | 2017.49 |
| Std Dev | 108.20 |
| P50 | 522.04 |
| P90 | 529.04 |
| P95 | 531.33 |
| P99 | 556.74 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 242.76 |
| Min | 15.86 |
| Max | 2039.09 |
| Std Dev | 180.98 |
| P50 | 61.30 |
| P90 | 61.84 |
| P95 | 61.96 |
| P99 | 1294.92 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 522.0ms (P50) | 108.50 | 61.30 | 2039.09 | 234 |
| 522.0-525.0ms (P50-P75) | 61.15 | 60.95 | 61.30 | 117 |
| 525.0-529.0ms (P75-P90) | 60.71 | 60.49 | 60.95 | 70 |
| >= 529.0ms (P90+) | 57.61 | 15.86 | 60.48 | 47 |

**Correlation:** -0.610 (negative correlation expected: lower latency = higher throughput)

### Run 2

**Total:** 33760 pairs in 63.87s

### Latency

| Metric | Value |
|--------|-------|
| Average | 470.95 |
| Min | 22.20 |
| Max | 4034.24 |
| Std Dev | 259.54 |
| P50 | 531.65 |
| P90 | 540.79 |
| P95 | 543.98 |
| P99 | 554.29 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 528.54 |
| Min | 7.93 |
| Max | 1441.47 |
| Std Dev | 365.22 |
| P50 | 60.19 |
| P90 | 983.39 |
| P95 | 1159.50 |
| P99 | 1337.80 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 531.7ms (P50) | 363.36 | 60.19 | 1441.47 | 527 |
| 531.7-535.5ms (P50-P75) | 60.01 | 59.76 | 60.19 | 264 |
| 535.5-540.8ms (P75-P90) | 59.53 | 59.18 | 59.75 | 158 |
| >= 540.8ms (P90+) | 55.89 | 7.93 | 59.17 | 106 |

**Correlation:** -0.711 (negative correlation expected: lower latency = higher throughput)

### Run 3

**Total:** 66400 pairs in 67.68s

### Latency

| Metric | Value |
|--------|-------|
| Average | 492.65 |
| Min | 47.76 |
| Max | 8074.11 |
| Std Dev | 441.50 |
| P50 | 558.66 |
| P90 | 573.34 |
| P95 | 578.73 |
| P99 | 638.21 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 981.10 |
| Min | 3.96 |
| Max | 669.95 |
| Std Dev | 199.83 |
| P50 | 57.28 |
| P90 | 562.85 |
| P95 | 601.12 |
| P99 | 640.71 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 558.7ms (P50) | 253.06 | 57.28 | 669.95 | 1037 |
| 558.7-565.3ms (P50-P75) | 56.96 | 56.61 | 57.28 | 519 |
| 565.3-573.3ms (P75-P90) | 56.24 | 55.81 | 56.60 | 311 |
| >= 573.3ms (P90+) | 51.38 | 3.96 | 55.81 | 208 |

**Correlation:** -0.499 (negative correlation expected: lower latency = higher throughput)

### Run 4

**Total:** 30144 pairs in 61.83s

### Latency

| Metric | Value |
|--------|-------|
| Average | 518.64 |
| Min | 22.91 |
| Max | 2021.97 |
| Std Dev | 131.31 |
| P50 | 531.77 |
| P90 | 539.07 |
| P95 | 542.14 |
| P99 | 545.12 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 487.51 |
| Min | 31.65 |
| Max | 2794.08 |
| Std Dev | 378.72 |
| P50 | 120.35 |
| P90 | 121.94 |
| P95 | 122.80 |
| P99 | 2090.13 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 531.8ms (P50) | 275.23 | 120.36 | 2794.08 | 235 |
| 531.8-535.9ms (P50-P75) | 119.87 | 119.42 | 120.35 | 118 |
| 535.9-539.1ms (P75-P90) | 119.09 | 118.73 | 119.41 | 70 |
| >= 539.1ms (P90+) | 113.57 | 31.65 | 118.72 | 48 |

**Correlation:** -0.764 (negative correlation expected: lower latency = higher throughput)

### Run 5

**Total:** 19712 pairs in 129.01s

### Latency

| Metric | Value |
|--------|-------|
| Average | 440.62 |
| Min | 38.67 |
| Max | 576.43 |
| Std Dev | 209.08 |
| P50 | 549.48 |
| P90 | 558.48 |
| P95 | 561.33 |
| P99 | 567.00 |

### Throughput

| Metric | Value |
|--------|-------|
| Average | 152.79 |
| Min | 111.03 |
| Max | 1655.09 |
| Std Dev | 517.13 |
| P50 | 116.47 |
| P90 | 1364.77 |
| P95 | 1464.74 |
| P99 | 1607.07 |

### Latency vs Throughput Analysis

| Latency Range | Avg Throughput | Min Throughput | Max Throughput | Count |
|---------------|----------------|----------------|----------------|-------|
| < 549.5ms (P50) | 661.98 | 116.48 | 1655.09 | 154 |
| 549.5-554.1ms (P50-P75) | 116.01 | 115.51 | 116.47 | 77 |
| 554.1-558.5ms (P75-P90) | 115.08 | 114.60 | 115.50 | 46 |
| >= 558.5ms (P90+) | 113.72 | 111.03 | 114.58 | 31 |

**Correlation:** -0.992 (negative correlation expected: lower latency = higher throughput)

### Run 6

Error: No requests completed

### Run 7

Error: No requests completed

### Run 8

Error: No requests completed

### Run 9

Error: No requests completed

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 981.10 p/s | batch=32, conc=16 |
| Best Latency | 440.62ms | batch=64, conc=8 |
| Avg Throughput | 478.54 p/s | all configs |
| Avg Latency | 488.73ms | all configs |

## Dashboard Metrics

| Metric | Avg | Min | Max | P50 | P95 |
|--------|-----|-----|-----|-----|-----|
| GPU Memory (MB) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| GPU Utilization (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| CPU Usage (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Tokenization (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Inference (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Queue Wait (ms) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Padding Waste (%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

Full time-series data is available in: `distribution/inference_only_timeseries.md`
