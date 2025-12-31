# Proposed Code Fixes (Implement After Confirming Orphans)

**Status:** These fixes should be implemented **after** confirming orphan processes are the root cause via diagnostic scripts.

**Note:** `src/server/pool.py` already has `daemon=False` and improved `stop()` - those are good!

---

## Fix 1: Guarantee Cleanup in `src/main.py` (CRITICAL)

**Problem:** `serve()` blocks forever. If gRPC exits or raises, `orchestrator.stop()` is never called.

**Change:**

```python
def main():
    parser = argparse.ArgumentParser(description="Inference Server")
    parser.add_argument("--experiment", "-e", required=True, help="Experiment config YAML")
    parser.add_argument("--grpc-port", type=int, help="Override gRPC port")
    parser.add_argument("--http-port", type=int, help="Override HTTP port")
    args = parser.parse_args()

    config = load_config(args.experiment)
    experiment_name = get_experiment_name(config, args.experiment)

    if args.grpc_port:
        config.server.grpc_port = args.grpc_port
    if args.http_port:
        config.server.http_port = args.http_port

    logger.info(f"Loaded config: {experiment_name}")

    orchestrator = ServerOrchestrator(config, experiment_name)
    orchestrator.setup()
    orchestrator.start()

    try:
        logger.info(f"Starting gRPC server on port {config.server.grpc_port}...")
        serve(
            orchestrator.get_inference_handler(),
            host=config.server.host,
            port=config.server.grpc_port,
            max_workers=config.server.grpc_workers,
            metrics=orchestrator.get_metrics(),
        )
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
    finally:
        logger.info("Shutting down orchestrator...")
        orchestrator.stop()
        logger.info("Shutdown complete")
```

**Why:** Ensures `orchestrator.stop()` always runs, cleaning up tokenizer pool + model pool even if gRPC crashes.

---

## Fix 2: Make gRPC Server Stoppable (OPTIONAL but Robust)

**Problem:** `server.wait_for_termination()` blocks without a shutdown path. Signal handlers in orchestrator may not propagate cleanly.

**Change in `src/server/grpc.py`:**

```python
def serve(
    inference_handler: "InferenceInterface",
    host: str = "0.0.0.0",
    port: int = 50051,
    max_workers: int = 10,
    metrics=None,
):
    """Start gRPC server.

    The server runs until interrupted. Signal handlers set in orchestrator.start()
    will handle SIGTERM/SIGINT and trigger shutdown.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    inference_pb2_grpc.add_InferenceServiceServicer_to_server(
        InferenceServicer(inference_handler, metrics), server
    )
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logger.info(f"gRPC server listening on {host}:{port}")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("gRPC server interrupted")
        server.stop(grace=5)  # Give 5 seconds for graceful shutdown
    except Exception as e:
        logger.error(f"gRPC server error: {e}", exc_info=True)
        server.stop(grace=5)
        raise
```

**Why:** Allows graceful gRPC shutdown on interruption, giving time for in-flight requests to complete.

---

## Fix 3: Complete ModelPool.stop() Cleanup (RECOMMENDED)

**Problem:** `_result_thread` is a daemon thread with infinite loop. It keeps running while process lives, and queues aren't explicitly closed.

**Change in `src/server/pool.py`:**

```python
def stop(self, timeout_s: float = 30.0) -> None:
    if not self._is_started:
        return

    logger.info(f"Stopping pool with {self.num_workers} workers...")

    # Send stop signals to all workers
    for _ in range(self.num_workers):
        try:
            self._input_queue.put(_STOP, timeout=5.0)
        except Exception as e:
            logger.warning(f"Error sending stop signal to worker: {e}")

    # Wait for graceful shutdown with timeout
    deadline = time.time() + timeout_s
    for i, p in enumerate(self._processes):
        remaining = max(0, deadline - time.time())
        if remaining <= 0:
            logger.warning(f"Timeout waiting for worker {i}, forcing termination")
            if p.is_alive():
                p.terminate()
        else:
            p.join(timeout=remaining)
            if p.is_alive():
                logger.warning(f"Worker {i} still alive after join, terminating")
                p.terminate()
                # Give terminate a moment, then force kill if needed
                p.join(timeout=2.0)
                if p.is_alive():
                    logger.error(f"Worker {i} did not terminate, may be orphaned")

    # Close queues to signal result thread to exit
    try:
        self._input_queue.close()
        self._output_queue.close()
        self._memory_queue.close()
    except Exception as e:
        logger.debug(f"Error closing queues: {e}")

    # Wait for result thread to finish (it will exit when queues are closed)
    if self._result_thread and self._result_thread.is_alive():
        self._result_thread.join(timeout=2.0)
        if self._result_thread.is_alive():
            logger.warning("Result thread did not exit cleanly")

    # Final cleanup
    for p in self._processes:
        if p.is_alive():
            logger.error(f"Worker process {p.pid} still alive after cleanup")

    self._processes.clear()
    self._ready_events.clear()
    self._is_started = False
    logger.info("Pool stopped")
```

**Also update `_result_loop` to handle queue closure:**

```python
def _result_loop(self) -> None:
    while True:
        try:
            result = self._output_queue.get()
            if not isinstance(result, WorkResult):
                continue

            self._request_counts[result.worker_id] = (
                self._request_counts.get(result.worker_id, 0) + 1
            )

            future = self._pending.pop(result.req_id, None)
            if future and not future.cancelled():
                future.set_result(result)
        except (EOFError, OSError):
            # Queue closed, exit cleanly
            logger.debug("Result loop exiting (queue closed)")
            break
        except Exception as e:
            logger.error(f"Result loop error: {e}")
            time.sleep(0.1)
```

**Why:**
- Closes queues explicitly, signaling result thread to exit
- Waits for result thread to finish
- Prevents resource leaks from daemon threads

---

## Fix 4: Improve Script Shutdown Logic (RECOMMENDED)

**Problem:** Script escalates to `kill -9` after only 2s. MPS workers may need longer to exit cleanly.

**Change in `scripts/run_experiment.sh`:**

Replace the cleanup function's server stopping logic:

```bash
# Stop server if running
if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "Stopping server (PID: $SERVER_PID)..."

    # Get child processes before killing parent
    CHILD_PIDS=$(pgrep -P "$SERVER_PID" 2>/dev/null || true)

    # Send SIGTERM
    kill -TERM "$SERVER_PID" 2>/dev/null || true

    # Wait in loop (max 10s total, checking every 1s - never >10s sleep)
    WAIT_COUNT=0
    MAX_WAIT=10
    while [ $WAIT_COUNT -lt $MAX_WAIT ] && kill -0 "$SERVER_PID" 2>/dev/null; do
        sleep 1
        WAIT_COUNT=$((WAIT_COUNT + 1))
    done

    # Force kill if still alive
    if kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "  Server did not stop gracefully, forcing termination..."
        kill -9 "$SERVER_PID" 2>/dev/null || true
    fi

    wait "$SERVER_PID" 2>/dev/null || true

    # Clean up orphaned children explicitly
    if [ -n "$CHILD_PIDS" ]; then
        for CHILD_PID in $CHILD_PIDS; do
            if kill -0 "$CHILD_PID" 2>/dev/null; then
                echo "  Cleaning up orphaned child process $CHILD_PID..."
                kill -TERM "$CHILD_PID" 2>/dev/null || true
                sleep 1
                if kill -0 "$CHILD_PID" 2>/dev/null; then
                    kill -9 "$CHILD_PID" 2>/dev/null || true
                fi
            fi
        done
    fi
fi
```

**Why:**
- Gives workers more time to exit cleanly (10s vs 2s)
- Explicitly cleans up child processes
- Reduces chance of orphaned workers

---

## Implementation Order

1. **Fix 1 (main.py)** - Most critical, ensures cleanup always happens
2. **Fix 3 (pool.py)** - Completes cleanup, prevents resource leaks
3. **Fix 4 (script)** - Improves shutdown reliability
4. **Fix 2 (grpc.py)** - Optional, adds robustness

---

## Testing After Implementation

1. Run diagnostic scripts before/after:
   ```bash
   ./scripts/count_processes.sh before
   # Start server, run test, stop server
   ./scripts/count_processes.sh after
   ```

2. Check for orphans:
   ```bash
   ./scripts/check_processes.sh
   ./scripts/check_ports.sh
   ```

3. Verify GPU memory releases:
   ```bash
   # After stopping server
   curl -s http://localhost:8080/metrics 2>/dev/null | grep gpu_memory_mb || echo "Server stopped"
   ```

4. Run multiple consecutive experiments and verify process count doesn't grow.

