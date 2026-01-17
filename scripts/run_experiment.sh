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
TEMP_CLIENT_CONFIG=""

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

    # Clean up temp client config
    if [ -n "$TEMP_CLIENT_CONFIG" ] && [ -f "$TEMP_CLIENT_CONFIG" ]; then
        rm -f "$TEMP_CLIENT_CONFIG"
    fi

    # Clean up temp client config
    if [ -n "$TEMP_CLIENT_CONFIG" ] && [ -f "$TEMP_CLIENT_CONFIG" ]; then
        rm -f "$TEMP_CLIENT_CONFIG"
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
    echo "Usage: $0 <experiment_name>"
    echo "Example: $0 10_multi_model_pool"
    echo "         $0 experiment=10_multi_model_pool"
    echo ""
    echo "Note: Only Hydra configs from conf/experiment/ are supported"
    exit 1
fi

EXPERIMENT_CONFIG="$1"

# Extract experiment name from Hydra format or use directly
if [[ "$EXPERIMENT_CONFIG" == *"="* ]]; then
    EXPERIMENT_NAME=$(echo "$EXPERIMENT_CONFIG" | cut -d'=' -f2)
    HYDRA_CONFIG="$EXPERIMENT_CONFIG"
else
    EXPERIMENT_NAME="$EXPERIMENT_CONFIG"
    HYDRA_CONFIG="experiment=${EXPERIMENT_NAME}"
fi

# Check if this is a sweep temp config
if [ -n "$SWEEP_TEMP_CONFIG_PATH" ]; then
    HYDRA_CONFIG_PATH="$SWEEP_TEMP_CONFIG_PATH"
    if [ ! -f "$HYDRA_CONFIG_PATH" ]; then
        echo -e "${RED}Error: Sweep temp config not found: $HYDRA_CONFIG_PATH${NC}"
        exit 1
    fi
else
    # Validate Hydra config exists in conf/experiment/
    HYDRA_CONFIG_PATH="$PROJECT_ROOT/conf/experiment/${EXPERIMENT_NAME}.yaml"
    if [ ! -f "$HYDRA_CONFIG_PATH" ]; then
        echo -e "${RED}Error: Hydra config not found: $HYDRA_CONFIG_PATH${NC}"
        echo "Available experiments:"
        ls -1 "$PROJECT_ROOT/conf/experiment/"*.yaml 2>/dev/null | xargs -n1 basename | sed 's/.yaml$//' | sed 's/^/  - /' || echo "  (none found)"
        exit 1
    fi
fi

# Check if config has sweep parameters (arrays in Hydra config)
# BUT: Don't check if we're already running from sweep script (SWEEP_TEMP_CONFIG_PATH is set)
if [ -z "$SWEEP_TEMP_CONFIG_PATH" ]; then
    HAS_SWEEPS=$(python3 << PYTHON
import sys
import yaml
from pathlib import Path

config_path = "$HYDRA_CONFIG_PATH"
try:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    has_sweeps = False
    # Check model_pool.instances[0] for arrays
    if "model_pool" in config and "instances" in config["model_pool"]:
        instances = config["model_pool"]["instances"]
        if instances and isinstance(instances, list) and len(instances) > 0:
            first_instance = instances[0]
            if isinstance(first_instance, dict):
                if "backend" in first_instance and isinstance(first_instance["backend"], list):
                    has_sweeps = True
                if "quantization" in first_instance and isinstance(first_instance["quantization"], list):
                    has_sweeps = True
                if "compile_mode" in first_instance and isinstance(first_instance["compile_mode"], list):
                    has_sweeps = True

    # Check batching for arrays
    if "batching" in config:
        if "timeout_ms" in config["batching"] and isinstance(config["batching"]["timeout_ms"], list):
            has_sweeps = True
        if "max_batch_size" in config["batching"] and isinstance(config["batching"]["max_batch_size"], list):
            has_sweeps = True

    print("true" if has_sweeps else "false")
except Exception:
    print("false")
PYTHON
    )

    # If sweeps detected, use sweep script
    if [ "$HAS_SWEEPS" = "true" ]; then
        echo -e "${BLUE}Detected sweep parameters, using sweep handler...${NC}"
        "$SCRIPT_DIR/run_sweep_experiment.sh" "$HYDRA_CONFIG_PATH"
        exit $?
    fi
else
    # Already part of a sweep, don't check again
    HAS_SWEEPS="false"
fi

# Generate client config from Hydra config
# If in a sweep, pass the temp config path so it uses the right config
TEMP_CLIENT_CONFIG=$(mktemp)
if [ -n "$SWEEP_TEMP_CONFIG_PATH" ]; then
    python3 "$SCRIPT_DIR/hydra_to_client_config.py" "$EXPERIMENT_NAME" "$TEMP_CLIENT_CONFIG" --config-path "$SWEEP_TEMP_CONFIG_PATH" || {
        echo -e "${RED}Error: Failed to convert Hydra config to client format${NC}"
        exit 1
    }
else
    python3 "$SCRIPT_DIR/hydra_to_client_config.py" "$EXPERIMENT_NAME" "$TEMP_CLIENT_CONFIG" || {
        echo -e "${RED}Error: Failed to convert Hydra config to client format${NC}"
        exit 1
    }
fi
CLIENT_CONFIG_PATH="$TEMP_CLIENT_CONFIG"

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


# Start observability stack
echo "Starting observability services..."
"$SCRIPT_DIR/start_services.sh"

# Capture start time (seconds)
START_TIME=$(date +%s.%N)

# Start server in background
echo "Starting server..."
if [ -n "$SWEEP_TEMP_CONFIG_PATH" ]; then
    # For sweep temp configs, copy to conf/experiment with proper Hydra defaults
    # Use a unique temp name to avoid overwriting the original config
    SWEEP_TEMP_NAME="_sweep_temp_${EXPERIMENT_NAME}_$$"
    TEMP_HYDRA_CONFIG="$PROJECT_ROOT/conf/experiment/${SWEEP_TEMP_NAME}.yaml"

    # Add Hydra defaults if not present
    python3 << PYTHON_FIX_HYDRA
import yaml
from pathlib import Path

temp_config_path = "$HYDRA_CONFIG_PATH"
final_config_path = "$TEMP_HYDRA_CONFIG"

with open(temp_config_path) as f:
    config = yaml.safe_load(f)

# Ensure defaults are present for Hydra composition
if 'defaults' not in config or not config['defaults']:
    config['defaults'] = [
        {'override /model_pool': 'default'},
        {'override /batching': 'default'},
        {'override /tokenizer_pool': 'default'},
        {'override /server': 'default'},
    ]

with open(final_config_path, 'w') as f:
    # Write package directive first
    f.write('# @package _global_\n\n')
    # Write rest of config
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)
PYTHON_FIX_HYDRA

    python -m src.main experiment=$SWEEP_TEMP_NAME &
else
    python -m src.main $HYDRA_CONFIG &
fi
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
    if curl -s http://localhost:8000/metrics > /dev/null 2>&1; then
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
curl -s http://localhost:8000/reset > /dev/null 2>&1 || true

# Run client
echo ""
echo "Running benchmark..."

# Build client command with sweep options (use array for proper quoting)
# Client still uses YAML configs - use the resolved config path
if [ -n "$CLIENT_CONFIG_PATH" ] && [ -f "$CLIENT_CONFIG_PATH" ]; then
    CLIENT_CONFIG="$CLIENT_CONFIG_PATH"
else
    # Fallback to original config
    CLIENT_CONFIG="$EXPERIMENT_CONFIG"
fi
CLIENT_ARGS=(--experiment --config "$CLIENT_CONFIG" --output "$OUTPUT_FILE" --timeseries-file "$TIMESERIES_FILE")

if [ "$IS_SWEEP" = "true" ]; then
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

    # Capture end time
    END_TIME=$(date +%s.%N)

    # Snapshot Grafana Dashboard
    echo ""
    echo "Snapshotting Grafana dashboard..."
    if python3 "$PROJECT_ROOT/src/utils/snapshot_dashboard.py" --start "$START_TIME" --end "$END_TIME" --name "Run: $EXPERIMENT_NAME"; then
        echo -e "${GREEN}Dashboard snapshot saved.${NC}"
    else
        echo -e "${YELLOW}Warning: Dashboard snapshot failed.${NC}"
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

# Clean up temp sweep config if it was created
if [ -n "$SWEEP_TEMP_CONFIG_PATH" ] && [ -n "$SWEEP_TEMP_NAME" ]; then
    TEMP_HYDRA_CONFIG="$PROJECT_ROOT/conf/experiment/${SWEEP_TEMP_NAME}.yaml"
    if [ -f "$TEMP_HYDRA_CONFIG" ]; then
        rm -f "$TEMP_HYDRA_CONFIG"
    fi
fi

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
