#!/bin/bash
# Stop all running inference servers
# This script finds and kills all Python processes running src.main

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=========================================="
echo "Stopping all inference servers..."
echo -e "==========================================${NC}"

# Find all Python processes running src.main
PIDS=$(pgrep -f "python.*src.main" || true)

if [ -z "$PIDS" ]; then
    echo -e "${GREEN}No running servers found.${NC}"
    exit 0
fi

echo "Found server processes:"
for PID in $PIDS; do
    # Get process details
    CMD=$(ps -p $PID -o command= 2>/dev/null || echo "unknown")
    echo "  PID $PID: $CMD"
done

echo ""
echo "Stopping servers..."

# Try graceful shutdown first (SIGTERM)
for PID in $PIDS; do
    if kill -0 $PID 2>/dev/null; then
        echo "  Sending SIGTERM to PID $PID..."
        kill -TERM $PID 2>/dev/null || true
    fi
done

# Wait a moment for graceful shutdown
sleep 2

# Force kill any remaining processes (SIGKILL)
REMAINING=$(pgrep -f "python.*src.main" || true)
if [ -n "$REMAINING" ]; then
    echo ""
    echo "Force killing remaining processes..."
    for PID in $REMAINING; do
        if kill -0 $PID 2>/dev/null; then
            echo "  Sending SIGKILL to PID $PID..."
            kill -9 $PID 2>/dev/null || true
        fi
    done
fi

# Final check
FINAL_CHECK=$(pgrep -f "python.*src.main" || true)
if [ -z "$FINAL_CHECK" ]; then
    echo -e "\n${GREEN}✓ All servers stopped successfully.${NC}"
else
    echo -e "\n${RED}✗ Warning: Some processes may still be running:${NC}"
    for PID in $FINAL_CHECK; do
        echo "  PID $PID"
    done
    exit 1
fi

# Also check for any gRPC servers on port 50051
if lsof -ti:50051 > /dev/null 2>&1; then
    echo -e "${YELLOW}Warning: Port 50051 is still in use.${NC}"
    echo "You may need to manually check for other processes using this port."
fi

# Check for HTTP dashboard on port 8080
if lsof -ti:8080 > /dev/null 2>&1; then
    echo -e "${YELLOW}Warning: Port 8080 is still in use.${NC}"
    echo "You may need to manually check for other processes using this port."
fi
