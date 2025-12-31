#!/bin/bash
# Comprehensive diagnostic script to distinguish orphan workers vs thermal throttling
# Usage: ./diagnose_performance.sh [experiment_config]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

EXPERIMENT_CONFIG="${1:-}"

echo -e "${BLUE}=========================================="
echo "Performance Diagnostic: Orphan Workers vs Thermal Throttling"
echo -e "==========================================${NC}\n"

cd "$PROJECT_ROOT"

# Activate virtualenv if available
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# 1. Process count check
echo -e "${YELLOW}[1] Process Analysis${NC}"
echo "─────────────────────────────────────"

MAIN_PROCESSES=$(pgrep -f "python.*src.main" 2>/dev/null || true)
ALL_PYTHON=$(pgrep -f "python.*main.py" 2>/dev/null || true)

EXPECTED_PROCESSES=1  # 1 main + N workers (workers are children)
if [ -n "$EXPERIMENT_CONFIG" ]; then
    # Try to determine expected worker count from config
    if [ -f "$EXPERIMENT_CONFIG" ]; then
        WORKER_COUNT=$(python3 << PYTHON
import yaml
with open("$EXPERIMENT_CONFIG") as f:
    config = yaml.safe_load(f)
    instances = config.get("model_pool", {}).get("instances", [])
    print(len(instances) if instances else 1)
PYTHON
        )
        EXPECTED_PROCESSES=$((1 + WORKER_COUNT))
    fi
fi

ACTUAL_COUNT=$(echo "$ALL_PYTHON" | wc -w | tr -d ' ')
echo "  Expected processes: $EXPECTED_PROCESSES (1 main + $((EXPECTED_PROCESSES - 1)) workers)"
echo "  Actual Python processes: $ACTUAL_COUNT"

if [ "$ACTUAL_COUNT" -gt "$EXPECTED_PROCESSES" ]; then
    EXTRA=$((ACTUAL_COUNT - EXPECTED_PROCESSES))
    echo -e "  ${RED}⚠ $EXTRA extra process(es) detected → ORPHAN WORKERS LIKELY${NC}"
    ORPHAN_INDICATOR=true
else
    echo -e "  ${GREEN}✓ Process count looks normal${NC}"
    ORPHAN_INDICATOR=false
fi

# Show process tree
if [ -n "$MAIN_PROCESSES" ]; then
    echo ""
    echo "  Process tree:"
    for PID in $MAIN_PROCESSES; do
        CHILDREN=$(pgrep -P "$PID" 2>/dev/null || true)
        CHILD_COUNT=$(echo "$CHILDREN" | wc -w | tr -d ' ')
        echo "    Main PID $PID → $CHILD_COUNT child(ren)"
        if [ "$CHILD_COUNT" -gt 0 ]; then
            for CHILD_PID in $CHILDREN; do
                CMD=$(ps -p "$CHILD_PID" -o command= 2>/dev/null | cut -c1-60 || echo "unknown")
                echo "      └─ $CHILD_PID: $CMD"
            done
        fi
    done
fi

# 2. GPU Memory check
echo -e "\n${YELLOW}[2] GPU Memory Analysis${NC}"
echo "─────────────────────────────────────"

GPU_MEMORY=$(python3 << 'PYTHON'
import sys
try:
    import torch
    if torch.backends.mps.is_available():
        mem_mb = torch.mps.driver_allocated_memory() / (1024 * 1024)
        print(f"{mem_mb:.2f}")
    else:
        print("0.00")
except Exception as e:
    print(f"ERROR: {e}")
PYTHON
)

if [[ "$GPU_MEMORY" == ERROR* ]]; then
    echo -e "  ${RED}✗ Error: $GPU_MEMORY${NC}"
    GPU_MEMORY=0
else
    echo "  GPU Memory Allocated: ${GPU_MEMORY} MB"
fi

# Threshold: > 100MB suggests something is holding memory
if (( $(echo "$GPU_MEMORY > 100" | bc -l 2>/dev/null || echo 0) )); then
    if [ "$ORPHAN_INDICATOR" = true ]; then
        echo -e "  ${RED}⚠ Elevated GPU memory + orphan processes → ORPHAN WORKERS CONFIRMED${NC}"
    else
        echo -e "  ${YELLOW}⚠ Elevated GPU memory (may be from active server or previous run)${NC}"
    fi
    GPU_ELEVATED=true
else
    echo -e "  ${GREEN}✓ GPU memory looks clean${NC}"
    GPU_ELEVATED=false
fi

# 3. System metrics (if server is running)
echo -e "\n${YELLOW}[3] System Metrics (if server is running)${NC}"
echo "─────────────────────────────────────"

if curl -s http://localhost:8080/metrics > /dev/null 2>&1; then
    echo "  Server is running, fetching metrics..."

    # Get metrics JSON
    METRICS_JSON=$(curl -s http://localhost:8080/metrics 2>/dev/null || echo "{}")

    CPU_PERCENT=$(echo "$METRICS_JSON" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('cpu_percent', 0))" 2>/dev/null || echo "0")
    GPU_UTIL=$(echo "$METRICS_JSON" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('estimated_gpu_utilization_pct', 0))" 2>/dev/null || echo "0")
    LATENCY=$(echo "$METRICS_JSON" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('avg_ms', 0))" 2>/dev/null || echo "0")
    THROUGHPUT=$(echo "$METRICS_JSON" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('throughput_qps', 0))" 2>/dev/null || echo "0")

    echo "  CPU Usage: ${CPU_PERCENT}%"
    echo "  GPU Utilization: ${GPU_UTIL}%"
    echo "  Avg Latency: ${LATENCY} ms"
    echo "  Throughput: ${THROUGHPUT} QPS"

    # Analyze for throttling vs contention
    if (( $(echo "$CPU_PERCENT > 80" | bc -l 2>/dev/null || echo 0) )) && (( $(echo "$LATENCY > 100" | bc -l 2>/dev/null || echo 0) )); then
        if [ "$ORPHAN_INDICATOR" = true ]; then
            echo -e "  ${RED}⚠ High CPU + High Latency + Orphan Processes → CONTENTION LIKELY${NC}"
        else
            echo -e "  ${YELLOW}⚠ High CPU + High Latency → Possible thermal throttling${NC}"
        fi
    fi
else
    echo "  Server is not running (cannot fetch metrics)"
fi

# 4. Port check
echo -e "\n${YELLOW}[4] Port Analysis${NC}"
echo "─────────────────────────────────────"

for PORT in 8080 50051; do
    PIDS=$(lsof -ti:$PORT 2>/dev/null || true)
    if [ -n "$PIDS" ]; then
        PID_COUNT=$(echo "$PIDS" | wc -w | tr -d ' ')
        echo "  Port $PORT: In use by $PID_COUNT process(es)"
        for PID in $PIDS; do
            CMD=$(ps -p "$PID" -o command= 2>/dev/null | cut -c1-60 || echo "unknown")
            echo "    PID $PID: $CMD"
        done
    else
        echo "  Port $PORT: Free"
    fi
done

# 5. Summary and diagnosis
echo -e "\n${BLUE}=========================================="
echo "Diagnosis"
echo -e "==========================================${NC}"

if [ "$ORPHAN_INDICATOR" = true ]; then
    echo -e "${RED}🔴 PRIMARY ISSUE: ORPHAN WORKER PROCESSES${NC}"
    echo ""
    echo "  Evidence:"
    echo "    • Extra Python processes detected ($EXTRA more than expected)"
    if [ "$GPU_ELEVATED" = true ]; then
        echo "    • GPU memory elevated (${GPU_MEMORY} MB)"
    fi
    echo ""
    echo "  Impact:"
    echo "    • GPU memory pressure/fragmentation"
    echo "    • CPU contention from extra processes"
    echo "    • Reduced throughput on subsequent runs"
    echo ""
    echo "  Solution:"
    echo "    ./scripts/cleanup_orphans.sh"
    echo ""
elif [ "$GPU_ELEVATED" = true ] && [ -z "$MAIN_PROCESSES" ]; then
    echo -e "${YELLOW}🟡 SECONDARY ISSUE: LINGERING GPU MEMORY${NC}"
    echo ""
    echo "  Evidence:"
    echo "    • GPU memory elevated (${GPU_MEMORY} MB) but no active server"
    echo ""
    echo "  Possible causes:"
    echo "    • Previous run didn't clean up properly"
    echo "    • MPS driver hasn't released memory yet"
    echo ""
    echo "  Solution:"
    echo "    • Wait a few minutes for MPS to release"
    echo "    • Or restart your Mac to force cleanup"
    echo ""
else
    echo -e "${GREEN}🟢 NO OBVIOUS ISSUES DETECTED${NC}"
    echo ""
    echo "  If performance is still poor, consider:"
    echo "    • Thermal throttling (check Activity Monitor → Energy)"
    echo "    • System load from other processes"
    echo "    • macOS power management (check pmset -g therm)"
    echo ""
fi

echo ""

