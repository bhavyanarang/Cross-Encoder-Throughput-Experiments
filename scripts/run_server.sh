#!/bin/bash
# Run the inference server

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
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

cd "$SCRIPT_DIR"
source venv/bin/activate

echo -e "${GREEN}Starting Inference Server...${NC}"
echo "Press Ctrl+C to stop"
echo ""

export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
python -c "
from src.models import Config, ModelConfig, PoolConfig
from src.server import ModelPool, Scheduler
from src.frontend import start_dashboard
from src.server.grpc import serve

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

config = Config(
    model_pool=PoolConfig(
        instances=[ModelConfig(name='cross-encoder/ms-marco-MiniLM-L-6-v2', device='mps', backend='mps')]
    )
)

pool = ModelPool(config.model_pool)
pool.start()
scheduler = Scheduler(pool)
start_dashboard(8080)
print('Dashboard: http://localhost:8080')
serve(scheduler, '0.0.0.0', 50051)
" &
SERVER_PID=$!

wait $SERVER_PID
