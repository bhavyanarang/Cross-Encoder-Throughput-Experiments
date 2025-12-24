# 02_backend_mps (PARTIAL)

**Timestamp:** 2025-12-23 04:58:45

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `False`

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 32 | 1 | ERROR | - | - | - | - | - | - |

## Detailed Sub-Experiment Metrics

### Config 1: batch=32, concurrency=1 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "Socket closed"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"Socket closed"}"
>
