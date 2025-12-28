#!/bin/bash
# Check for orphaned server and worker processes
# Usage: ./check_processes.sh

echo "=== Checking for server processes ==="
echo ""
echo "Main server processes (python.*src.main):"
pgrep -af "python.*src\.main" || echo "  ✓ None found"
echo ""

echo "Main server processes (python.*-m src.main):"
pgrep -af "python.*-m src\.main" || echo "  ✓ None found"
echo ""

echo "=== All Python processes (filtered) ==="
ps aux | egrep -i "python|src\.main|multiprocessing|spawn|forkserver" | head -n 80 || echo "  ✓ None found"
echo ""

echo "=== Process count summary ==="
MAIN_COUNT=$(pgrep -af "python.*src\.main" 2>/dev/null | wc -l | tr -d ' ')
PYTHON_COUNT=$(ps aux | grep -E "python" | grep -v grep | wc -l | tr -d ' ')
echo "Main server processes: $MAIN_COUNT"
echo "Total Python processes: $PYTHON_COUNT"
echo ""

# If main processes found, show process tree
MAIN_PIDS=$(pgrep -f "python.*src\.main" 2>/dev/null || true)
if [ -n "$MAIN_PIDS" ]; then
    echo "=== Process trees ==="
    for PID in $MAIN_PIDS; do
        echo "Tree for PID $PID:"
        if command -v pstree &> /dev/null; then
            pstree -p "$PID" 2>/dev/null || echo "  (Could not get tree)"
        else
            echo "  Parent PID $PID:"
            ps -o pid,ppid,command -ax | awk -v pid="$PID" 'NR==1 || $2==pid' || echo "  (Could not get tree)"
        fi
        echo ""
    done
fi
