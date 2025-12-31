#!/bin/bash
# Clean up orphaned worker processes
# Usage: ./cleanup_orphans.sh

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
echo "Cleaning Up Orphaned Processes"
echo -e "==========================================${NC}\n"

# Find all main processes
MAIN_PROCESSES=$(pgrep -f "python.*src.main" 2>/dev/null || true)

if [ -n "$MAIN_PROCESSES" ]; then
    echo -e "${YELLOW}Found main server processes. Stopping gracefully...${NC}"
    for PID in $MAIN_PROCESSES; do
        echo "  Stopping PID $PID..."
        kill -TERM "$PID" 2>/dev/null || true

        # Wait up to 5 seconds
        WAIT_COUNT=0
        while [ $WAIT_COUNT -lt 5 ] && kill -0 "$PID" 2>/dev/null; do
            sleep 1
            WAIT_COUNT=$((WAIT_COUNT + 1))
        done

        if kill -0 "$PID" 2>/dev/null; then
            echo "    Force killing..."
            kill -9 "$PID" 2>/dev/null || true
        fi

        # Clean up children
        CHILDREN=$(pgrep -P "$PID" 2>/dev/null || true)
        if [ -n "$CHILDREN" ]; then
            for CHILD_PID in $CHILDREN; do
                echo "    Cleaning up child $CHILD_PID..."
                kill -TERM "$CHILD_PID" 2>/dev/null || true
                sleep 1
                if kill -0 "$CHILD_PID" 2>/dev/null; then
                    kill -9 "$CHILD_PID" 2>/dev/null || true
                fi
            done
        fi
    done
fi

# Find orphaned workers (processes with no parent or parent is init)
echo -e "\n${YELLOW}Looking for orphaned worker processes...${NC}"
ALL_PYTHON=$(pgrep -f "python.*main.py\|python.*_worker_main" 2>/dev/null || true)
CLEANED_COUNT=0

if [ -n "$ALL_PYTHON" ]; then
    for PID in $ALL_PYTHON; do
        PPID=$(ps -p "$PID" -o ppid= 2>/dev/null | tr -d ' ' || echo "")
        # Check if parent is init (1) or if it's a standalone process
        if [ "$PPID" = "1" ] || [ -z "$PPID" ]; then
            CMD=$(ps -p "$PID" -o command= 2>/dev/null || echo "unknown")
            if echo "$CMD" | grep -q "main.py\|_worker_main\|ModelPool"; then
                echo "  Found orphaned process $PID: $CMD"
                kill -TERM "$PID" 2>/dev/null || true
                sleep 1
                if kill -0 "$PID" 2>/dev/null; then
                    kill -9 "$PID" 2>/dev/null || true
                fi
                CLEANED_COUNT=$((CLEANED_COUNT + 1))
            fi
        fi
    done
fi

# Clean up ports
echo -e "\n${YELLOW}Cleaning up ports...${NC}"
for PORT in 8080 50051; do
    PIDS=$(lsof -ti:$PORT 2>/dev/null || true)
    if [ -n "$PIDS" ]; then
        echo "  Port $PORT is in use, cleaning up..."
        for PID in $PIDS; do
            kill -TERM "$PID" 2>/dev/null || true
            sleep 1
            if kill -0 "$PID" 2>/dev/null; then
                kill -9 "$PID" 2>/dev/null || true
            fi
        done
    fi
done

echo -e "\n${GREEN}=========================================="
echo "Cleanup Complete"
echo -e "==========================================${NC}"
if [ "$CLEANED_COUNT" -gt 0 ]; then
    echo -e "Cleaned up ${CLEANED_COUNT} orphaned process(es)"
else
    echo "No orphaned processes found"
fi
echo ""

