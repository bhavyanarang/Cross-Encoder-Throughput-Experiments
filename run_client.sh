#!/bin/bash
# Run the benchmark client with graceful interrupt handling

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLIENT_PID=""

# Colors
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

cd "$SCRIPT_DIR"
source venv/bin/activate

echo -e "${GREEN}Starting Benchmark Client...${NC}"
echo "Press Ctrl+C to stop"
echo ""

cd ml_inference_server
python client.py "$@" &
CLIENT_PID=$!

# Wait for client process
wait $CLIENT_PID
