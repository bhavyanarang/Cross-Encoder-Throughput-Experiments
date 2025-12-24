#!/bin/bash
# Run the benchmark client

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
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

cd "$SCRIPT_DIR"
source venv/bin/activate

echo -e "${GREEN}Starting Benchmark Client...${NC}"
echo "Press Ctrl+C to stop"
echo ""

export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
python -c "
from src.client import InferenceClient

client = InferenceClient('localhost', 50051)
pairs = [(f'query {i}', f'document {i}') for i in range(1000)]
result = client.benchmark(pairs, batch_size=32, num_requests=100, concurrency=1)
print(f'Latency: avg={result[\"latency_avg_ms\"]:.1f}ms, p95={result[\"latency_p95_ms\"]:.1f}ms')
print(f'Throughput: {result[\"throughput_avg\"]:.1f} pairs/s')
client.close()
" &
CLIENT_PID=$!

wait $CLIENT_PID
