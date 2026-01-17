#!/bin/bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${YELLOW}=========================================="
echo "Stopping all inference servers..."
echo -e "==========================================${NC}"

cd "$PROJECT_ROOT"

PIDS=$(pgrep -f "python.*src.main" || true)

if [ -n "$PIDS" ]; then
    echo "Found server processes:"
    for PID in $PIDS; do
        CMD=$(ps -p $PID -o command= 2>/dev/null || echo "unknown")
        echo "  PID $PID: $CMD"
    done

    echo ""
    echo "Stopping servers..."

    for PID in $PIDS; do
        if kill -0 $PID 2>/dev/null; then
            echo "  Sending SIGTERM to PID $PID..."
            kill -TERM $PID 2>/dev/null || true
        fi
    done

    sleep 2

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
else
    echo -e "${GREEN}No running Python servers found.${NC}"
fi

FINAL_CHECK=$(pgrep -f "python.*src.main" || true)
if [ -z "$FINAL_CHECK" ]; then
    echo -e "${GREEN}✓ All Python servers stopped.${NC}"
else
    echo -e "${RED}✗ Warning: Some Python processes may still be running${NC}"
fi

echo ""
echo "Stopping Docker containers..."
if docker compose ps -q 2>/dev/null | grep -q .; then
    docker compose down --remove-orphans
    echo -e "${GREEN}✓ Docker containers stopped.${NC}"
else
    echo -e "${GREEN}No Docker containers running.${NC}"
fi

for PORT in 50051 8080 8000; do
    if lsof -ti:$PORT > /dev/null 2>&1; then
        echo -e "${YELLOW}Cleaning up port $PORT...${NC}"
        lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    fi
done

echo ""
echo -e "${GREEN}=========================================="
echo "Cleanup complete."
echo -e "==========================================${NC}"
