# Metrics Calculation Issues

## CRITICAL

1. **inference_service.py:428-430** - `t_mp_queue_receive_ms` incorrectly subtracts inference time:
   ```python
   t_mp_queue_receive_ms = max(0.0, t_mp_queue_receive_total_ms - result.t_model_inference_ms)
   ```
   Should be: `t_mp_queue_receive_total_ms` (includes inference wait)

2. **inference_service.py:444-448, 471-473** - `total_ms` excludes `t_queue_wait_ms`:
   ```python
   total_ms = ... + t_mp_queue_send_ms + t_mp_queue_receive_ms  # Missing t_queue_wait_ms
   ```

3. **orchestrator_service.py:145-150** - Pipeline `total_ms` doesn't match stage sum (missing gRPC overhead)

## MEDIUM

4. **grpc.py:80** - Worker metrics record `total_latency` (includes gRPC) instead of inference-only

5. **collector.py:230** - `effective_query_count` uses `max()` instead of `sum()` for worker queries

6. **collector.py:111-112** - GPU utilization uses 10ms window but filters use 1.0s window

7. **stage.py:38-42** - Zero values filtered out, affecting stage averages

## MINOR

8. **inference_service.py:57** - Dead code: unused `time.perf_counter()` call

9. **collector.py:242-248** - Stage sum validation compares against `total_avg` which excludes gRPC overhead

