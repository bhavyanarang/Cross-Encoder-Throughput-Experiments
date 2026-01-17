#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CLIENT_PID=""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

cleanup() {
    if [ -n "$CLIENT_PID" ] && kill -0 "$CLIENT_PID" 2>/dev/null; then
        echo -e "\n${YELLOW}Stopping client...${NC}"
        kill -TERM "$CLIENT_PID" 2>/dev/null || true
        wait "$CLIENT_PID" 2>/dev/null || true
        echo -e "${GREEN}Client stopped.${NC}"
    fi
}

trap cleanup SIGINT SIGTERM EXIT

cd "$PROJECT_ROOT"

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

echo -e "${GREEN}Starting Benchmark Client...${NC}"
echo "Press Ctrl+C to stop"
echo ""

export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
python -m src.run_client "$@" &
CLIENT_PID=$!

wait $CLIENT_PID
