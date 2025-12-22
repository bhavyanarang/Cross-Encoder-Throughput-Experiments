#!/bin/bash
# Run all experiments sequentially

cd "$(dirname "$0")"
source venv/bin/activate

echo "=========================================="
echo "Running All Experiments"
echo "=========================================="

# Find all experiment configs
EXPERIMENTS_DIR="ml_inference_server/experiments"
OUTPUT_DIR="ml_inference_server/docs/experiments"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Track results
TOTAL=0
SUCCESS=0
FAILED=0

# Run each experiment
for config in "$EXPERIMENTS_DIR"/*.yaml; do
    # Skip base_config.yaml
    if [[ "$(basename "$config")" == "base_config.yaml" ]]; then
        continue
    fi
    
    TOTAL=$((TOTAL + 1))
    EXPERIMENT_NAME=$(basename "$config" .yaml)
    OUTPUT_FILE="$OUTPUT_DIR/${EXPERIMENT_NAME}_results.md"
    
    echo ""
    echo "=========================================="
    echo "Experiment $TOTAL: $EXPERIMENT_NAME"
    echo "Config: $config"
    echo "=========================================="
    
    # Start server in background
    echo "Starting server..."
    python ml_inference_server/main.py --experiment "$config" > /tmp/server_${EXPERIMENT_NAME}.log 2>&1 &
    SERVER_PID=$!
    
    # Wait for server to start (model loading can take 30-60 seconds)
    echo "Waiting for server to initialize (up to 60s)..."
    sleep 45
    
    # Check if server is running
    if ! kill -0 $SERVER_PID 2>/dev/null; then
        echo "✗ Server failed to start!"
        echo "Check logs: /tmp/server_${EXPERIMENT_NAME}.log"
        FAILED=$((FAILED + 1))
        continue
    fi
    
    # Run client
    echo "Running benchmark..."
    if python ml_inference_server/client.py --experiment --config "$config" --output "$OUTPUT_FILE"; then
        echo "✓ Experiment completed successfully!"
        echo "Results: $OUTPUT_FILE"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "✗ Benchmark failed!"
        FAILED=$((FAILED + 1))
    fi
    
    # Stop server
    echo "Stopping server..."
    kill $SERVER_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null
    
    # Wait before next experiment
    sleep 2
done

echo ""
echo "=========================================="
echo "SUMMARY"
echo "=========================================="
echo "Total experiments: $TOTAL"
echo "Successful: $SUCCESS"
echo "Failed: $FAILED"
echo "=========================================="

if [ $FAILED -gt 0 ]; then
    exit 1
fi

