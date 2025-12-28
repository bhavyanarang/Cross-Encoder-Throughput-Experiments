# Shutdown Reliability Fix Plan

## Problem Summary

The server shutdown path was not reliably cleaning up multiprocessing model worker processes. When a run was terminated "too hard" (or gRPC blocked signal handling), the parent `src.main` process could die while child `mp.Process` workers remained alive, causing:

- Extra Python worker processes holding MPS/Metal allocations
- GPU memory pressure/fragmentation (MPS doesn't always release immediately)
- CPU contention (tokenizer threads + gRPC threads + orphan workers)
- Next run starts new workers → overall throughput collapses

This matches symptoms: "good after hours idle" (system eventually clears/reaps) but "bad when I run it again" (leftovers still around).

## Code Changes Made

### 1. **src/main.py** - Guaranteed Cleanup
- Wrapped `serve()` call in `try/finally` block
- Ensures `orchestrator.stop()` is **always** called, even if gRPC server crashes or is interrupted
- Added proper exception handling for KeyboardInterrupt and other errors

### 2. **src/server/pool.py** - Improved Worker Lifecycle
- Changed workers from `daemon=True` to `daemon=False`
  - Non-daemon processes require explicit parent management
  - Prevents orphaned workers when parent dies unexpectedly
- Enhanced `stop()` method:
  - Better timeout handling with per-worker deadlines
  - Explicit termination logging
  - Detection and warning of workers that don't terminate

### 3. **src/server/grpc.py** - Graceful Server Shutdown
- Added exception handling around `wait_for_termination()`
- Calls `server.stop(grace=5)` on interruption to allow graceful shutdown
- Ensures gRPC server doesn't block signal propagation

### 4. **src/server/orchestrator.py** - Signal Handler Clarity
- Improved signal handler logging
- Note that cleanup happens both in signal handler AND main.py finally block (defense in depth)

### 5. **scripts/run_experiment.sh** - Better Process Tree Cleanup
- Increased graceful shutdown wait time from 1s to 5s
- Added process tree detection: finds child processes before killing parent
- Explicit cleanup of orphaned children after parent termination
- More aggressive cleanup of experiment-specific processes

## Diagnostic Tools Created

### 1. `scripts/check_orphans.sh`
**Quick check for orphaned processes and GPU memory**

```bash
./scripts/check_orphans.sh
```

**What it checks:**
- Python processes related to inference server
- Orphaned child processes (model workers)
- GPU memory allocation
- Process tree visualization
- System thermal state (if available)

**Output:** Summary indicating if orphaned workers are detected

### 2. `scripts/cleanup_orphans.sh`
**Clean up orphaned processes**

```bash
./scripts/cleanup_orphans.sh
```

**What it does:**
- Stops main server processes gracefully (SIGTERM → SIGKILL)
- Cleans up child processes explicitly
- Finds and kills orphaned workers (processes with PPID=1 or no parent)
- Cleans up ports 8080 and 50051

**Use when:** You see extra Python processes after stopping the server

### 3. `scripts/diagnose_performance.sh`
**Comprehensive diagnostic: Orphan workers vs Thermal throttling**

```bash
./scripts/diagnose_performance.sh [experiment_config.yaml]
```

**What it analyzes:**
1. **Process Analysis**: Expected vs actual process count
2. **GPU Memory**: Checks for elevated memory (indicates orphan workers or previous run)
3. **System Metrics**: If server is running, fetches CPU/GPU utilization, latency, throughput
4. **Port Analysis**: Checks which processes are using ports 8080/50051
5. **Diagnosis**: Provides clear conclusion:
   - 🔴 **ORPHAN WORKERS**: Extra processes + elevated GPU memory
   - 🟡 **LINGERING MEMORY**: GPU memory elevated but no active server
   - 🟢 **NO ISSUES**: Everything looks normal

**Use when:** Performance is degraded and you want to distinguish root cause

## How to Use (Investigation Workflow)

### Step 1: After a "bad rerun", check for orphans

```bash
./scripts/check_orphans.sh
```

**Expected output if clean:**
```
✓ No orphaned worker processes found
✓ GPU memory appears clean (0 MB allocated)
```

**Expected output if orphans exist:**
```
⚠ Found potentially orphaned worker processes:
  PID 12345 (PPID: 1): python ... _worker_main
⚠ GPU memory allocated: 512.34 MB
  → This may indicate orphaned workers holding GPU memory
```

### Step 2: If orphans detected, clean them up

```bash
./scripts/cleanup_orphans.sh
```

This will:
- Stop any running servers gracefully
- Kill orphaned workers
- Free up ports

### Step 3: Run comprehensive diagnostic (optional)

```bash
./scripts/diagnose_performance.sh experiments/10_multi_model_pool.yaml
```

This provides a full analysis and diagnosis.

### Step 4: Verify cleanup worked

```bash
./scripts/check_orphans.sh
```

Should now show clean state.

## Distinguishing Orphan Workers vs Thermal Throttling

### Orphan Workers (Code Issue - Fixed)
**Symptoms:**
- Extra Python processes beyond expected (1 main + N workers)
- GPU memory stays elevated after stopping server
- Process tree shows workers with PPID=1 (orphaned)
- Performance degrades on subsequent runs

**Evidence:**
```bash
# Check process count
ps aux | grep "python.*main.py" | wc -l
# Should be: 1 (main) + N (workers) = expected total
# If higher → orphans

# Check GPU memory when server is stopped
python3 -c "import torch; print(torch.mps.driver_allocated_memory() / 1024**2)"
# Should be ~0 MB if clean
# If > 100 MB → likely orphans holding memory
```

**Fix:** Run `./scripts/cleanup_orphans.sh` (or restart Mac)

### Thermal Throttling (System Issue)
**Symptoms:**
- CPU/GPU utilization stays high but latency increases
- Performance degrades after sustained load
- Dashboard shows high CPU% but throughput drops
- Performance recovers after idle period

**Evidence:**
```bash
# Check system thermal state (macOS)
sudo powermetrics -i 1000 -n 1 --samplers smc | grep -i temperature

# Check Activity Monitor → Energy tab
# Look for "Preventing Sleep" or high CPU usage from other processes
```

**Fix:**
- Let system cool down
- Check for other CPU-intensive processes
- Consider reducing batch size or worker count

## Testing the Fix

### Test 1: Normal Shutdown
```bash
# Start server
python -m src.main --experiment experiments/10_multi_model_pool.yaml

# In another terminal, stop gracefully
kill -TERM <PID>

# Check for orphans
./scripts/check_orphans.sh
# Should show: ✓ No orphaned processes
```

### Test 2: Hard Kill (SIGKILL)
```bash
# Start server
python -m src.main --experiment experiments/10_multi_model_pool.yaml

# Hard kill (simulates script timeout)
kill -9 <PID>

# Check for orphans
./scripts/check_orphans.sh
# With daemon=False, workers should still be cleaned up by OS
# But if any remain, cleanup_orphans.sh will find them
```

### Test 3: Script Interruption
```bash
# Run experiment
./scripts/run_experiment.sh experiments/10_multi_model_pool.yaml

# Interrupt with Ctrl+C during run

# Check for orphans
./scripts/check_orphans.sh
# Should show clean (improved cleanup in script)
```

## Monitoring in Production

Add to your experiment workflow:

```bash
# Before running experiment
./scripts/check_orphans.sh

# Run experiment
./scripts/run_experiment.sh experiments/your_experiment.yaml

# After experiment (if performance was poor)
./scripts/diagnose_performance.sh experiments/your_experiment.yaml
```

## Questions to Answer (When Debugging)

1. **When performance is "really low", which drops: throughput or latency spikes, or both?**
   - Both → Likely contention (orphans or throttling)
   - Latency only → May be throttling
   - Throughput only → May be resource exhaustion

2. **On a "bad rerun", do you see extra python processes after script finishes?**
   - Yes → Orphan workers confirmed
   - No → May be throttling or other issue

3. **Are you on Apple Silicon and does dashboard show GPU memory staying elevated after stopping?**
   - Yes → Orphan workers holding MPS allocations
   - No → May be throttling or other system issue

## Summary

**Code fixes ensure:**
- ✅ `orchestrator.stop()` always called (try/finally)
- ✅ Workers are non-daemon (explicit lifecycle management)
- ✅ Better process tree cleanup in scripts
- ✅ Graceful gRPC shutdown

**Diagnostic tools help:**
- ✅ Quickly identify orphan workers
- ✅ Distinguish orphans vs throttling
- ✅ Clean up orphaned processes
- ✅ Monitor system state

**Next steps:**
1. Run `./scripts/check_orphans.sh` after your next experiment
2. If orphans found, use `./scripts/cleanup_orphans.sh`
3. Use `./scripts/diagnose_performance.sh` for comprehensive analysis
4. Monitor process counts and GPU memory over multiple runs
