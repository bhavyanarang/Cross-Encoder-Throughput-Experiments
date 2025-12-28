# Diagnostic Workflow: Orphan Processes vs Thermal Throttling

## Quick Start: Gather Evidence

Run these commands when you experience a "slow rerun":

```bash
# 1. Check ports (orphaned servers)
./scripts/check_ports.sh

# 2. Check processes (orphaned workers)
./scripts/check_processes.sh

# 3. Check metrics (if server running)
./scripts/check_metrics.sh

# 4. Count processes before/after
./scripts/count_processes.sh before
# ... start server, run test, stop server ...
./scripts/count_processes.sh after
```

## Detailed Workflow

### Step 0: Define "Slow"

When server is running (good or bad state), capture:

```bash
curl -s http://localhost:8080/metrics | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("throughput_qps:", d.get("throughput_qps"))
print("avg_ms:", d.get("avg_ms"))
print("tokenize_ms:", d.get("stage_timings", {}).get("avg_tokenize_ms"))
print("inference_ms:", d.get("stage_timings", {}).get("avg_inference_ms"))
print("queue_wait_ms:", d.get("stage_timings", {}).get("avg_queue_wait_ms"))
print("gpu_memory_mb:", d.get("gpu_memory_mb"))
print("cpu_percent:", d.get("cpu_percent"))
'
```

**Compare "good" vs "bad" runs** to identify which metric regresses.

### Step 1: Check for Orphan Processes (Highest Priority)

#### 1.1 Check Ports
```bash
lsof -nP -iTCP:50051 -sTCP:LISTEN
lsof -nP -iTCP:8080 -sTCP:LISTEN
```
**Bad sign:** Python PIDs listening when server should be stopped.

#### 1.2 Check Server Processes
```bash
pgrep -af "python.*src\.main"
pgrep -af "python.*-m src\.main"
```
**Bad sign:** Processes found after stopping server.

#### 1.3 Check Worker Processes
```bash
ps aux | egrep -i "python|src\.main|multiprocessing|spawn|forkserver" | head -n 80
```
**Expected:** 1 main + N workers (N = number of model instances)
**Bad sign:** Multiple sets of workers, or workers with PPID=1 (orphaned)

#### 1.4 Count Before/After
```bash
# Before starting server
./scripts/count_processes.sh before

# After stopping server
./scripts/count_processes.sh after
```
**Bad sign:** Count grows after each run.

### Step 2: Check GPU Memory Retention

#### 2.1 Via Dashboard (Best)
```bash
curl -s http://localhost:8080/metrics | grep -o '"gpu_memory_mb":[0-9.]*'
```
**Bad sign:** GPU memory stays high after stopping server.

#### 2.2 OS-Level (macOS)
```bash
vm_stat
sysctl -n hw.memsize
```

### Step 3: Determine Which Stage Regresses

Compare stage timings from `/metrics`:

- **Orphan contention:** `inference_ms` ↑ and/or `mp_queue_receive_ms` ↑, GPU memory ↑, process count ↑
- **Tokenizer bottleneck:** `tokenize_ms` ↑, CPU usage ↑, inference similar
- **Queue issues:** `queue_wait_ms` ↑ (should be near-zero without batching)

### Step 4: Monitoring Loops

#### Monitor Metrics (every 2s)
```bash
./scripts/monitor_metrics.sh
```

#### Monitor Processes (every 2s)
```bash
./scripts/monitor_processes.sh
```

## Decision Tree

### Case A: Orphan Processes Found
**Evidence:**
- Ports still held by Python processes
- Extra Python processes after stopping
- Process count grows after each run
- GPU memory elevated after stopping

**Fix:** Implement code changes in `PROPOSED_FIXES.md`
**Expected:** Reruns stable without "hours idle"

### Case B: No Orphans, CPU/GPU Throttling
**Evidence:**
- No extra processes
- High CPU% + high latency during slow periods
- Performance recovers after idle

**Fix:** Reduce concurrency, add cooldown, check power mode
**Expected:** Consistent performance with thermal management

### Case C: No Orphans, Tokenization Spikes
**Evidence:**
- No extra processes
- `tokenize_ms` balloons
- CPU usage high on tokenization

**Fix:** Adjust tokenizer pool sizing, queue size, CPU pinning
**Expected:** Balanced tokenization throughput

## What to Share for Analysis

When you have a "bad rerun", share:

1. **Port check:**
   ```bash
   lsof -nP -iTCP:50051 -sTCP:LISTEN || true
   lsof -nP -iTCP:8080 -sTCP:LISTEN || true
   ```

2. **Process check:**
   ```bash
   pgrep -af "python.*src\.main" || true
   ps aux | egrep -i "python|src\.main|multiprocessing|spawn|forkserver" | head -n 80
   ```

3. **Metrics (first 2000 chars):**
   ```bash
   curl -s http://localhost:8080/metrics | head -c 2000
   ```
