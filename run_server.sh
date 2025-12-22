#!/bin/bash
# Run the ML inference server with graceful shutdown handling

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_PID=""

# Colors
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

cd "$SCRIPT_DIR"
source venv/bin/activate

echo -e "${GREEN}Starting ML Inference Server...${NC}"
echo "Press Ctrl+C to stop"
echo ""

cd ml_inference_server
python main.py "$@" &
SERVER_PID=$!

# Wait for server process
wait $SERVER_PID
