#!/bin/bash
# Diagnostic script to check for orphaned worker processes vs thermal throttling
# Usage: ./check_orphans.sh [experiment_config]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=========================================="
echo "Orphan Worker & Throttling Diagnostic"
echo -e "==========================================${NC}\n"

# Check for Python processes related to inference server
echo -e "${YELLOW}1. Checking for Python processes...${NC}"
MAIN_PROCESSES=$(pgrep -f "python.*src.main" 2>/dev/null || true)
ALL_PYTHON=$(pgrep -f "python.*main.py" 2>/dev/null || true)

if [ -z "$MAIN_PROCESSES" ] && [ -z "$ALL_PYTHON" ]; then
    echo -e "  ${GREEN}✓ No server processes found${NC}"
else
    echo -e "  ${YELLOW}Found Python processes:${NC}"
    for PID in $MAIN_PROCESSES $ALL_PYTHON; do
        CMD=$(ps -p "$PID" -o command= 2>/dev/null || echo "unknown")
        PPID=$(ps -p "$PID" -o ppid= 2>/dev/null | tr -d ' ' || echo "unknown")
        echo "    PID $PID (PPID: $PPID): $CMD"
    done
fi

# Check for child processes (model workers)
echo -e "\n${YELLOW}2. Checking for orphaned child processes (model workers)...${NC}"
ORPHANED_COUNT=0
if [ -n "$MAIN_PROCESSES" ]; then
    for MAIN_PID in $MAIN_PROCESSES; do
        CHILDREN=$(pgrep -P "$MAIN_PID" 2>/dev/null || true)
        if [ -n "$CHILDREN" ]; then
            echo "  Main process $MAIN_PID has children:"
            for CHILD_PID in $CHILDREN; do
                CMD=$(ps -p "$CHILD_PID" -o command= 2>/dev/null || echo "unknown")
                echo "    Child PID $CHILD_PID: $CMD"
            done
        fi
    done
else
    # Check for standalone worker processes (orphaned)
    STANDALONE_WORKERS=$(pgrep -f "python.*_worker_main\|python.*ModelPool" 2>/dev/null || true)
    if [ -n "$STANDALONE_WORKERS" ]; then
        echo -e "  ${RED}⚠ Found potentially orphaned worker processes:${NC}"
        for PID in $STANDALONE_WORKERS; do
            CMD=$(ps -p "$PID" -o command= 2>/dev/null || echo "unknown")
            PPID=$(ps -p "$PID" -o ppid= 2>/dev/null | tr -d ' ' || echo "unknown")
            echo "    PID $PID (PPID: $PPID): $CMD"
            ORPHANED_COUNT=$((ORPHANED_COUNT + 1))
        done
    else
        echo -e "  ${GREEN}✓ No orphaned worker processes found${NC}"
    fi
fi

# Check GPU memory
echo -e "\n${YELLOW}3. Checking GPU memory (MPS)...${NC}"
cd "$PROJECT_ROOT"

# Activate virtualenv if available
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

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
    echo -e "  ${RED}✗ Error checking GPU memory: $GPU_MEMORY${NC}"
elif (( $(echo "$GPU_MEMORY > 0" | bc -l) )); then
    echo -e "  ${YELLOW}⚠ GPU memory allocated: ${GPU_MEMORY} MB${NC}"
    if [ "$ORPHANED_COUNT" -gt 0 ]; then
        echo -e "  ${RED}  → This may indicate orphaned workers holding GPU memory${NC}"
    fi
else
    echo -e "  ${GREEN}✓ GPU memory appears clean (0 MB allocated)${NC}"
fi

# Check CPU/thermal state (macOS)
echo -e "\n${YELLOW}4. Checking system state (CPU/thermal)...${NC}"
if command -v powermetrics &> /dev/null; then
    echo "  Running powermetrics snapshot (requires sudo)..."
    CPU_TEMP=$(sudo powermetrics -i 1000 -n 1 --samplers smc 2>/dev/null | grep -i "cpu die temperature" | head -1 | awk '{print $4}' || echo "unknown")
    if [ "$CPU_TEMP" != "unknown" ]; then
        echo "  CPU Temperature: ${CPU_TEMP}°C"
    fi
else
    echo "  powermetrics not available (requires Xcode Command Line Tools)"
fi

# Check process tree
echo -e "\n${YELLOW}5. Process tree for main processes...${NC}"
if [ -n "$MAIN_PROCESSES" ]; then
    for MAIN_PID in $MAIN_PROCESSES; do
        echo "  Process tree for PID $MAIN_PID:"
        pstree -p "$MAIN_PID" 2>/dev/null || ps -f -p "$MAIN_PID" $(pgrep -P "$MAIN_PID" 2>/dev/null | tr '\n' ' ') 2>/dev/null || echo "    (Could not get process tree)"
    done
else
    echo "  No main processes found"
fi

# Summary
echo -e "\n${BLUE}=========================================="
echo "Summary"
echo -e "==========================================${NC}"

if [ "$ORPHANED_COUNT" -gt 0 ]; then
    echo -e "${RED}⚠ ORPHANED WORKERS DETECTED: $ORPHANED_COUNT process(es)${NC}"
    echo "  → This likely causes performance degradation"
    echo "  → Run: ./scripts/cleanup_orphans.sh to clean up"
elif [ -n "$MAIN_PROCESSES" ]; then
    echo -e "${YELLOW}ℹ Server processes are running (expected if server is active)${NC}"
else
    echo -e "${GREEN}✓ No orphaned processes detected${NC}"
fi

if (( $(echo "$GPU_MEMORY > 100" | bc -l 2>/dev/null || echo 0) )); then
    echo -e "${YELLOW}⚠ GPU memory is elevated: ${GPU_MEMORY} MB${NC}"
    if [ "$ORPHANED_COUNT" -eq 0 ]; then
        echo "  → May indicate thermal throttling or previous run not fully cleaned"
    fi
fi

echo ""
