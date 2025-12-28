#!/bin/bash
# Run the inference server

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SERVER_PID=""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

cleanup() {
    if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        echo -e "\n${YELLOW}Shutting down server...${NC}"
        kill -TERM "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
        echo -e "${GREEN}Server stopped.${NC}"
    fi
}

trap cleanup SIGINT SIGTERM EXIT

cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo -e "${GREEN}Starting Inference Server...${NC}"
echo "Press Ctrl+C to stop"
echo ""

# Use experiment config if provided, otherwise use default
CONFIG="${1:-experiments/02_backend_mps.yaml}"

export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
python -m src.main experiment_path="$CONFIG" &
SERVER_PID=$!

wait $SERVER_PID
