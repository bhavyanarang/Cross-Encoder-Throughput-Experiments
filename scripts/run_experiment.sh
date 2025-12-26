#!/bin/bash
# Run a single experiment with graceful interrupt handling
# Usage: ./run_experiment.sh experiments/02_backend_mps.yaml

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SERVER_PID=""
CLIENT_PID=""
EXPERIMENT_NAME=""
OUTPUT_FILE=""
INTERRUPTED=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Cleanup function - called on exit or interrupt
cleanup() {
    local exit_code=$?

    if [ "$INTERRUPTED" = true ]; then
        echo -e "\n${YELLOW}=========================================="
        echo "Interrupt received - cleaning up..."
        echo -e "==========================================${NC}"
    fi

    # Stop client if running
    if [ -n "$CLIENT_PID" ] && kill -0 "$CLIENT_PID" 2>/dev/null; then
        echo "Stopping client (PID: $CLIENT_PID)..."
        kill -TERM "$CLIENT_PID" 2>/dev/null || true
        wait "$CLIENT_PID" 2>/dev/null || true
    fi

    # Stop server if running
    if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "Stopping server (PID: $SERVER_PID)..."
        kill -TERM "$SERVER_PID" 2>/dev/null || true
        sleep 1
        if kill -0 "$SERVER_PID" 2>/dev/null; then
            kill -9 "$SERVER_PID" 2>/dev/null || true
        fi
        wait "$SERVER_PID" 2>/dev/null || true
    fi

    # Also kill any orphaned python processes from this experiment
    pkill -f "python.*main.py.*$EXPERIMENT_CONFIG" 2>/dev/null || true

    if [ "$INTERRUPTED" = true ]; then
        echo -e "${YELLOW}Cleanup complete.${NC}"
        if [ -f "$OUTPUT_FILE" ]; then
            echo -e "${GREEN}Partial results may have been saved to: $OUTPUT_FILE${NC}"
        fi
    fi

    exit $exit_code
}

# Handle interrupt signals
handle_interrupt() {
    INTERRUPTED=true
    echo -e "\n${YELLOW}Caught interrupt signal...${NC}"
    cleanup
}

# Set up trap handlers
trap handle_interrupt SIGINT SIGTERM
trap cleanup EXIT

# Validate arguments
if [ -z "$1" ]; then
    echo "Usage: $0 <experiment_config>"
    echo "Example: $0 experiments/02_backend_mps.yaml"
    exit 1
fi

EXPERIMENT_CONFIG="$1"

# Validate config file exists
if [ ! -f "$PROJECT_ROOT/$EXPERIMENT_CONFIG" ] && [ ! -f "$EXPERIMENT_CONFIG" ]; then
    echo -e "${RED}Error: Config file not found: $EXPERIMENT_CONFIG${NC}"
    exit 1
fi

# Use absolute path if relative path given
if [ -f "$PROJECT_ROOT/$EXPERIMENT_CONFIG" ]; then
    EXPERIMENT_CONFIG="$PROJECT_ROOT/$EXPERIMENT_CONFIG"
fi

# Check if config has sweep parameters (lists)
HAS_SWEEPS=$(python3 << PYTHON
import sys
import yaml
from pathlib import Path

config_path = "$EXPERIMENT_CONFIG"
with open(config_path) as f:
    config = yaml.safe_load(f)

has_sweeps = False
if "model" in config:
    if "backend" in config["model"] and isinstance(config["model"]["backend"], list):
        has_sweeps = True
    if "quantization_mode" in config["model"] and isinstance(config["model"]["quantization_mode"], list):
        has_sweeps = True
    if "compiled" in config["model"] and "mode" in config["model"]["compiled"]:
        if isinstance(config["model"]["compiled"]["mode"], list):
            has_sweeps = True

if "batching" in config:
    if "timeout_ms" in config["batching"] and isinstance(config["batching"]["timeout_ms"], list):
        has_sweeps = True
    if "max_batch_size" in config["batching"] and isinstance(config["batching"]["max_batch_size"], list):
        has_sweeps = True

print("true" if has_sweeps else "false")
PYTHON
)

# If sweeps detected, use sweep script
if [ "$HAS_SWEEPS" = "true" ]; then
    echo -e "${BLUE}Detected sweep parameters, using sweep handler...${NC}"
    "$SCRIPT_DIR/run_sweep_experiment.sh" "$EXPERIMENT_CONFIG"
    exit $?
fi

EXPERIMENT_NAME=$(basename "$EXPERIMENT_CONFIG" .yaml)

# Check if we're part of a sweep (consolidated output)
if [ -n "$SWEEP_RESULTS_FILE" ]; then
    OUTPUT_FILE="$SWEEP_RESULTS_FILE"
    TIMESERIES_FILE="$SWEEP_TIMESERIES_FILE"
    IS_SWEEP="true"
    APPEND_MODE=$([ "${SWEEP_CONFIG_NUM:-1}" -gt 1 ] && echo "true" || echo "false")
else
    OUTPUT_FILE="$PROJECT_ROOT/experiments/results/${EXPERIMENT_NAME}_results.md"
    TIMESERIES_FILE="$PROJECT_ROOT/experiments/distribution/${EXPERIMENT_NAME}_timeseries.md"
    IS_SWEEP="false"
    APPEND_MODE="false"
fi

echo -e "${GREEN}=========================================="
echo "Running experiment: $EXPERIMENT_NAME"
echo "Config: $EXPERIMENT_CONFIG"
echo "Output: $OUTPUT_FILE"
if [ "$IS_SWEEP" = "true" ]; then
    echo "Mode: Sweep (config ${SWEEP_CONFIG_NUM}/${SWEEP_TOTAL_CONFIGS}, append=$APPEND_MODE)"
fi
echo -e "==========================================${NC}"
echo ""
echo "Press Ctrl+C to interrupt (results will be saved if possible)"
echo ""

cd "$PROJECT_ROOT"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo -e "${YELLOW}Warning: No virtual environment found, using system Python${NC}"
fi

# Create output directory
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Ensure ports are free before starting
echo "Checking ports..."
if lsof -ti:8080 > /dev/null 2>&1; then
    echo "Port 8080 is in use, killing existing processes..."
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    sleep 1
fi
if lsof -ti:50051 > /dev/null 2>&1; then
    echo "Port 50051 is in use, killing existing processes..."
    lsof -ti:50051 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Start server in background
echo "Starting server..."
python -m src.main --experiment "$EXPERIMENT_CONFIG" &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for server to start (model loading can take 30-60 seconds)
echo "Waiting for server to initialize (up to 180s)..."
WAIT_TIME=0
MAX_WAIT=180
SERVER_READY=false

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    # Check if server process is still alive
    if ! kill -0 $SERVER_PID 2>/dev/null; then
        echo -e "${RED}Error: Server process died during initialization${NC}"
        exit 1
    fi

    # Try to connect to the server
    if curl -s http://localhost:8080/metrics > /dev/null 2>&1; then
        SERVER_READY=true
        break
    fi

    sleep 2
    WAIT_TIME=$((WAIT_TIME + 2))
    echo "  Waiting... ${WAIT_TIME}s"
done

if [ "$SERVER_READY" = false ]; then
    echo -e "${RED}Error: Server failed to become ready within ${MAX_WAIT}s${NC}"
    exit 1
fi

echo -e "${GREEN}Server is ready!${NC}"

# Reset metrics before running the benchmark
echo "Resetting metrics..."
curl -s http://localhost:8080/reset > /dev/null 2>&1 || true

# Run client
echo ""
echo "Running benchmark..."

# Build client command with sweep options (use array for proper quoting)
CLIENT_ARGS=(--experiment --config "$EXPERIMENT_CONFIG" --output "$OUTPUT_FILE")

if [ "$IS_SWEEP" = "true" ]; then
    CLIENT_ARGS+=(--timeseries-file "$TIMESERIES_FILE")
    if [ "$APPEND_MODE" = "true" ]; then
        CLIENT_ARGS+=(--append)
    fi
fi

python -m src.run_client "${CLIENT_ARGS[@]}" &
CLIENT_PID=$!

# Wait for client to complete
wait $CLIENT_PID
CLIENT_EXIT=$?
CLIENT_PID=""

if [ $CLIENT_EXIT -eq 0 ]; then
    echo -e "\n${GREEN}=========================================="
    echo "Experiment completed successfully!"
    echo "Results: $OUTPUT_FILE"
    echo "Latency vs Throughput data included in results"
    echo -e "==========================================${NC}"

    # Generate static dashboard from timeseries data
    echo ""
    echo "Generating static dashboard from timeseries data..."
    SNAPSHOT_DIR="$PROJECT_ROOT/images"
    mkdir -p "$SNAPSHOT_DIR"
    SNAPSHOT_FILE="$SNAPSHOT_DIR/${EXPERIMENT_NAME}.html"

    # Generate static dashboard from timeseries markdown
    if python -m src.screenshot --experiment "$EXPERIMENT_NAME" --output "$SNAPSHOT_FILE" 2>&1 | grep -v "Warning\|Error" || true; then
        if [ -f "$SNAPSHOT_FILE" ]; then
            echo -e "${GREEN}Static dashboard saved: $SNAPSHOT_FILE${NC}"
        else
            echo -e "${YELLOW}Warning: Dashboard file not created${NC}"
        fi
    else
        echo -e "${YELLOW}Warning: Dashboard generation had issues${NC}"
    fi
else
    echo -e "\n${RED}=========================================="
    echo "Experiment failed with exit code: $CLIENT_EXIT"
    echo -e "==========================================${NC}"
    exit 1
fi

# Stop server after snapshot is captured
echo "Stopping server..."
if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill -TERM "$SERVER_PID" 2>/dev/null || true
    sleep 2
    if kill -0 "$SERVER_PID" 2>/dev/null; then
        kill -9 "$SERVER_PID" 2>/dev/null || true
    fi
    wait "$SERVER_PID" 2>/dev/null || true
fi
SERVER_PID=""

# Ensure ports are actually free
if lsof -ti:8080 > /dev/null 2>&1; then
    echo "Cleaning up port 8080..."
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    sleep 1
fi
if lsof -ti:50051 > /dev/null 2>&1; then
    echo "Cleaning up port 50051..."
    lsof -ti:50051 | xargs kill -9 2>/dev/null || true
    sleep 1
fi
