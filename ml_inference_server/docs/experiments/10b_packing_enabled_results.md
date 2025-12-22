# 10b_packing_enabled (PARTIAL)

**Timestamp:** 2025-12-23 04:13:53

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `150`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | 4800 | 20.80 | 138.6ms | 210.0ms | 243.5ms | 230.8 | 294.3 |
| 64 | 1 | ERROR | - | - | - | - | - | - |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1

**Total:** 4800 pairs in 20.80s

#### Latency (ms)
| Metric | Value |
|--------|-------|
| Average | 138.62 |
| Min | 93.86 |
| Max | 264.59 |
| Std Dev | 29.08 |
| P50 | 129.53 |
| P90 | 180.41 |
| P95 | 209.99 |
| P99 | 243.51 |

#### Throughput (pairs/s)
| Metric | Value |
|--------|-------|
| Average | 230.82 |
| Min | 120.94 |
| Max | 340.93 |
| Std Dev | 38.93 |
| P50 | 247.05 |
| P90 | 275.84 |
| P95 | 294.29 |
| P99 | 311.58 |

### Config 2: batch=64, concurrency=1 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "Socket closed"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"Socket closed"}"
>

## Overall Summary

| Metric | Value | Config |
|--------|-------|--------|
| Best Throughput | 230.82 p/s | batch=32, conc=1 |
| Best Latency | 138.62ms | batch=32, conc=1 |
| Avg Throughput | 230.82 p/s | all configs |
| Avg Latency | 138.62ms | all configs |
