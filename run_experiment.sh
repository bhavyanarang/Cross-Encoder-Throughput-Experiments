#!/bin/bash
# Run a single experiment
# Usage: ./run_experiment.sh experiments/minilm_baseline.yaml

if [ -z "$1" ]; then
    echo "Usage: $0 <experiment_config>"
    echo "Example: $0 ml_inference_server/experiments/minilm_baseline.yaml"
    exit 1
fi

EXPERIMENT_CONFIG="$1"
EXPERIMENT_NAME=$(basename "$EXPERIMENT_CONFIG" .yaml)

echo "=========================================="
echo "Running experiment: $EXPERIMENT_NAME"
echo "Config: $EXPERIMENT_CONFIG"
echo "=========================================="

cd "$(dirname "$0")"
source venv/bin/activate

# Start server in background
echo "Starting server..."
python ml_inference_server/main.py --experiment "$EXPERIMENT_CONFIG" &
SERVER_PID=$!

# Wait for server to start (model loading can take 30-60 seconds)
echo "Waiting for server to initialize (up to 60s)..."
sleep 45

# Check if server is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "Error: Server failed to start"
    exit 1
fi

# Run client
echo "Running benchmark..."
python ml_inference_server/client.py --experiment --config "$EXPERIMENT_CONFIG" --output "ml_inference_server/docs/experiments/${EXPERIMENT_NAME}_results.md"
CLIENT_EXIT=$?

# Stop server
echo "Stopping server..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

if [ $CLIENT_EXIT -eq 0 ]; then
    echo "=========================================="
    echo "Experiment completed successfully!"
    echo "Results: ml_inference_server/docs/experiments/${EXPERIMENT_NAME}_results.md"
    echo "=========================================="
else
    echo "=========================================="
    echo "Experiment failed!"
    echo "=========================================="
    exit 1
fi

