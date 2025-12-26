#!/bin/bash
# Run all experiments sequentially with graceful interrupt handling
# Saves progress and shows summary even if interrupted

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EXPERIMENTS_DIR="$PROJECT_ROOT/experiments"
OUTPUT_DIR="$PROJECT_ROOT/experiments/results"
SERVER_PID=""
CLIENT_PID=""
INTERRUPTED=false

# Tracking
TOTAL=0
SUCCESS=0
FAILED=0
SKIPPED=0
COMPLETED_EXPERIMENTS=()
FAILED_EXPERIMENTS=()
CURRENT_EXPERIMENT=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print summary of completed experiments
print_summary() {
    echo ""
    echo -e "${BLUE}=========================================="
    echo "EXPERIMENT RUN SUMMARY"
    echo -e "==========================================${NC}"
    echo "Total experiments: $TOTAL"
    echo -e "  ${GREEN}Successful: $SUCCESS${NC}"
    echo -e "  ${RED}Failed: $FAILED${NC}"
    if [ "$INTERRUPTED" = true ]; then
        echo -e "  ${YELLOW}Skipped (interrupted): $SKIPPED${NC}"
    fi
    echo ""

    if [ ${#COMPLETED_EXPERIMENTS[@]} -gt 0 ]; then
        echo -e "${GREEN}Completed experiments:${NC}"
        for exp in "${COMPLETED_EXPERIMENTS[@]}"; do
            echo "  ✓ $exp"
        done
        echo ""
    fi

    if [ ${#FAILED_EXPERIMENTS[@]} -gt 0 ]; then
        echo -e "${RED}Failed experiments:${NC}"
        for exp in "${FAILED_EXPERIMENTS[@]}"; do
            echo "  ✗ $exp"
        done
        echo ""
    fi

    echo "Results directory: $OUTPUT_DIR"
    echo -e "${BLUE}==========================================${NC}"
}

# Cleanup function
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

    # Kill any orphaned python processes
    pkill -f "python.*main.py" 2>/dev/null || true

    # Print summary
    print_summary

    exit $exit_code
}

# Handle interrupt signals
handle_interrupt() {
    INTERRUPTED=true

    # Count remaining experiments as skipped
    # This is approximate since we're in the middle of iteration
    if [ -n "$CURRENT_EXPERIMENT" ]; then
        FAILED_EXPERIMENTS+=("$CURRENT_EXPERIMENT (interrupted)")
        FAILED=$((FAILED + 1))
    fi

    cleanup
}

# Set up trap handlers
trap handle_interrupt SIGINT SIGTERM
trap cleanup EXIT

cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo -e "${BLUE}=========================================="
echo "Running All Experiments"
echo -e "==========================================${NC}"
echo ""
echo "Press Ctrl+C to interrupt (completed results will be preserved)"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Count total experiments first
for config in "$EXPERIMENTS_DIR"/*.yaml; do
    if [[ "$(basename "$config")" == "base_config.yaml" ]]; then
        continue
    fi
    TOTAL=$((TOTAL + 1))
done

echo "Found $TOTAL experiments to run"
echo ""

# Run each experiment
CURRENT_NUM=0
for config in "$EXPERIMENTS_DIR"/*.yaml; do
    # Skip base_config.yaml
    if [[ "$(basename "$config")" == "base_config.yaml" ]]; then
        continue
    fi

    CURRENT_NUM=$((CURRENT_NUM + 1))
    EXPERIMENT_NAME=$(basename "$config" .yaml)
    CURRENT_EXPERIMENT="$EXPERIMENT_NAME"
    OUTPUT_FILE="$OUTPUT_DIR/${EXPERIMENT_NAME}_results.md"

    echo -e "${BLUE}=========================================="
    echo "Experiment $CURRENT_NUM/$TOTAL: $EXPERIMENT_NAME"
    echo "Config: $config"
    echo -e "==========================================${NC}"

    # Use run_experiment.sh which handles sweep detection automatically
    # This ensures sweep configs are properly expanded before server starts
    if "$SCRIPT_DIR/run_experiment.sh" "$config"; then
        echo -e "${GREEN}✓ Experiment completed successfully!${NC}"
        SUCCESS=$((SUCCESS + 1))
        COMPLETED_EXPERIMENTS+=("$EXPERIMENT_NAME")

        # Generate static dashboard from timeseries data
        echo "Generating static dashboard from timeseries data..."
        SNAPSHOT_DIR="$PROJECT_ROOT/images"
        mkdir -p "$SNAPSHOT_DIR"
        SNAPSHOT_FILE="$SNAPSHOT_DIR/${EXPERIMENT_NAME}.html"

        # Generate static dashboard from timeseries markdown
        if python -m src.screenshot --experiment "$EXPERIMENT_NAME" --output "$SNAPSHOT_FILE" 2>&1 | grep -v "Warning\|Error" || true; then
            if [ -f "$SNAPSHOT_FILE" ]; then
                echo -e "${GREEN}  Static dashboard saved: $SNAPSHOT_FILE${NC}"
            else
                echo -e "${YELLOW}  Warning: Dashboard file not created${NC}"
            fi
        else
            echo -e "${YELLOW}  Warning: Dashboard generation had issues${NC}"
        fi
    else
        echo -e "${RED}✗ Experiment failed!${NC}"
        FAILED=$((FAILED + 1))
        FAILED_EXPERIMENTS+=("$EXPERIMENT_NAME (experiment failed)")
    fi

    # Clear current experiment tracking
    CURRENT_EXPERIMENT=""

    # Brief pause before next experiment
    echo ""
    sleep 2
done

# Calculate skipped (only if interrupted)
if [ "$INTERRUPTED" = true ]; then
    SKIPPED=$((TOTAL - SUCCESS - FAILED))
fi

# Exit with error if any failed
if [ $FAILED -gt 0 ]; then
    exit 1
fi
