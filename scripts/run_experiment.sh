#!/bin/bash
# Run a single experiment with graceful interrupt handling
# Usage: ./run_experiment.sh experiments/minilm_baseline.yaml

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
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
        # Give it time to shut down gracefully
        sleep 1
        # Force kill if still running
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
    echo "Example: $0 ml_inference_server/experiments/minilm_baseline.yaml"
    exit 1
fi

EXPERIMENT_CONFIG="$1"
EXPERIMENT_NAME=$(basename "$EXPERIMENT_CONFIG" .yaml)
OUTPUT_FILE="ml_inference_server/docs/experiments/${EXPERIMENT_NAME}_results.md"

# Validate config file exists
if [ ! -f "$EXPERIMENT_CONFIG" ]; then
    echo -e "${RED}Error: Config file not found: $EXPERIMENT_CONFIG${NC}"
    exit 1
fi

echo -e "${GREEN}=========================================="
echo "Running experiment: $EXPERIMENT_NAME"
echo "Config: $EXPERIMENT_CONFIG"
echo "Output: $OUTPUT_FILE"
echo -e "==========================================${NC}"
echo ""
echo "Press Ctrl+C to interrupt (results will be saved if possible)"
echo ""

cd "$SCRIPT_DIR"
source venv/bin/activate

# Start server in background
echo "Starting server..."
python ml_inference_server/main.py --experiment "$EXPERIMENT_CONFIG" &
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

# Run client
echo ""
echo "Running benchmark..."
python ml_inference_server/client.py \
    --experiment \
    --config "$EXPERIMENT_CONFIG" \
    --output "$OUTPUT_FILE" &
CLIENT_PID=$!

# Wait for client to complete
wait $CLIENT_PID
CLIENT_EXIT=$?
CLIENT_PID=""

if [ $CLIENT_EXIT -eq 0 ]; then
    echo ""
    echo "Capturing dashboard screenshot..."

    # Create screenshots directory
    SCREENSHOT_DIR="ml_inference_server/docs/experiments/screenshots"
    mkdir -p "$SCREENSHOT_DIR"

    # Generate screenshot filename with timestamp
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    SCREENSHOT_FILE="${SCREENSHOT_DIR}/${EXPERIMENT_NAME}_${TIMESTAMP}.png"

    # Capture screenshot (with fallback if playwright not available)
    python ml_inference_server/utils/screenshot.py \
        --output "$SCREENSHOT_FILE" \
        --url "http://localhost:8080" \
        --wait 1.5 \
        --width 1400 \
        --height 1200 2>&1 || {
        echo -e "${YELLOW}Note: Screenshot capture requires playwright. Install with:${NC}"
        echo "  uv pip install playwright && playwright install chromium"
    }

    echo -e "\n${GREEN}=========================================="
    echo "Experiment completed successfully!"
    echo "Results: $OUTPUT_FILE"
    if [ -f "$SCREENSHOT_FILE" ]; then
        echo "Screenshot: $SCREENSHOT_FILE"
    fi
    echo -e "==========================================${NC}"
else
    echo -e "\n${RED}=========================================="
    echo "Experiment failed with exit code: $CLIENT_EXIT"
    echo -e "==========================================${NC}"
    exit 1
fi
