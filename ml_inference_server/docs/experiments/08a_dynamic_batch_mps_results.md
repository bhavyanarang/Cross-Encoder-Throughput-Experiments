# 08a_dynamic_batch_mps

**Timestamp:** 2025-12-23 02:51:44

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Device:** `mps`

**Backend:** `mps`

**Dynamic Batching:** `True` (max_batch=96, timeout=20ms)

**Model Type:** Cross-Encoder

**Requests per config:** `200`

## Results Summary

| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |
|-------|------|-------|---------|---------|---------|---------|--------|--------|
| 8 | 2 | ERROR | - | - | - | - | - | - |
| 8 | 4 | ERROR | - | - | - | - | - | - |
| 8 | 8 | ERROR | - | - | - | - | - | - |
| 16 | 2 | ERROR | - | - | - | - | - | - |
| 16 | 4 | ERROR | - | - | - | - | - | - |
| 16 | 8 | ERROR | - | - | - | - | - | - |
| 32 | 2 | ERROR | - | - | - | - | - | - |
| 32 | 4 | ERROR | - | - | - | - | - | - |
| 32 | 8 | ERROR | - | - | - | - | - | - |
| 64 | 2 | ERROR | - | - | - | - | - | - |
| 64 | 4 | ERROR | - | - | - | - | - | - |
| 64 | 8 | ERROR | - | - | - | - | - | - |

## Detailed Sub-Experiment Metrics

### Config 1: batch=8, concurrency=2 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "Socket closed"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"Socket closed", grpc_status:14}"
>

### Config 2: batch=8, concurrency=4 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>

### Config 3: batch=8, concurrency=8 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>

### Config 4: batch=16, concurrency=2 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>

### Config 5: batch=16, concurrency=4 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>

### Config 6: batch=16, concurrency=8 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>

### Config 7: batch=32, concurrency=2 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)", grpc_status:14}"
>

### Config 8: batch=32, concurrency=4 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>

### Config 9: batch=32, concurrency=8 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>

### Config 10: batch=64, concurrency=2 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>

### Config 11: batch=64, concurrency=4 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>

### Config 12: batch=64, concurrency=8 - **ERROR**

Error: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>
