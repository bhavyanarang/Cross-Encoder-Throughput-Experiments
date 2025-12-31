# Quick Reference: Diagnostic & Fix Workflow

## When You Experience a "Slow Rerun"

### Step 1: Gather Evidence (5 minutes)

```bash
# Check for orphaned servers/ports
./scripts/check_ports.sh

# Check for orphaned processes
./scripts/check_processes.sh

# If server is running, check metrics
./scripts/check_metrics.sh

# Count processes before/after
./scripts/count_processes.sh before
# ... start server, test, stop ...
./scripts/count_processes.sh after
```

### Step 2: Analyze Results

**If you see:**
- ✅ Ports still held by Python processes → **Orphan servers**
- ✅ Extra Python processes after stopping → **Orphan workers**
- ✅ Process count grows after each run → **Process leak**
- ✅ GPU memory elevated after stopping → **Orphan workers holding MPS**

**Then:** Implement fixes from `PROPOSED_FIXES.md`

**If you see:**
- ✅ No extra processes
- ✅ High CPU% + high latency → **Thermal throttling**
- ✅ `tokenize_ms` spikes → **Tokenizer bottleneck**

**Then:** Address thermal/tokenizer issues (not code cleanup)

### Step 3: Share Evidence (if needed)

Run these and share output:

```bash
lsof -nP -iTCP:50051 -sTCP:LISTEN || true
lsof -nP -iTCP:8080 -sTCP:LISTEN || true
pgrep -af "python.*src\.main" || true
ps aux | egrep -i "python|src\.main|multiprocessing|spawn|forkserver" | head -n 80
curl -s http://localhost:8080/metrics | head -c 2000
```

## Monitoring During Runs

### Monitor Metrics (every 2s)
```bash
./scripts/monitor_metrics.sh
```

### Monitor Processes (every 2s)
```bash
./scripts/monitor_processes.sh
```

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `check_ports.sh` | Check if ports 50051/8080 are held |
| `check_processes.sh` | Find orphaned server/worker processes |
| `check_metrics.sh` | Fetch and display server metrics |
| `count_processes.sh` | Count processes before/after runs |
| `monitor_metrics.sh` | Continuous metrics monitoring (2s interval) |
| `monitor_processes.sh` | Continuous process monitoring (2s interval) |

## Expected Process Count

For experiment with N model instances:
- **Expected:** 1 main process + N worker processes = (N+1) total
- **Bad:** More than (N+1) processes after stopping

## Decision Tree

```
Orphan processes found?
├─ Yes → Implement PROPOSED_FIXES.md
└─ No → Check thermal throttling / tokenizer bottleneck
```

## Files Created

- `DIAGNOSTIC_WORKFLOW.md` - Detailed diagnostic steps
- `PROPOSED_FIXES.md` - Code changes to implement after confirming orphans
- `QUICK_REFERENCE.md` - This file (quick commands)

