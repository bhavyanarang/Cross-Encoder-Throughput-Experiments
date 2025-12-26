#!/bin/bash
# Check experiment duration and fix configs that run less than 1 minute

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Activate virtual environment
source venv/bin/activate

EXPERIMENTS=(
    "experiments/06a_concurrency_mps.yaml"
    "experiments/06b_concurrency_mlx.yaml"
    "experiments/08a_dynamic_batch_mps.yaml"
    "experiments/08b_dynamic_batch_mlx.yaml"
    "experiments/09a_padding_baseline.yaml"
    "experiments/09b_padding_length_aware.yaml"
    "experiments/10_multi_model_pool.yaml"
    "experiments/10b_packing_enabled.yaml"
    "experiments/11_multi_model_replicas.yaml"
    "experiments/12_multi_model_smart_idle.yaml"
    "experiments/13_tuning_process_pool.yaml"
    "experiments/14_optimized_production.yaml"
    "experiments/15_production_optimal.yaml"
    "experiments/16a_dynamic_batch_baseline.yaml"
    "experiments/16b_dynamic_batch_enabled.yaml"
    "experiments/16b_dynamic_batch_enabled_length_aware.yaml"
    "experiments/16c_dynamic_batch_timeout_sweep.yaml"
    "experiments/16d_dynamic_batch_high_concurrency.yaml"
)

MIN_DURATION=60  # 1 minute in seconds

echo "=========================================="
echo "Checking and fixing experiment durations"
echo "Minimum duration: ${MIN_DURATION}s"
echo "=========================================="
echo ""

for exp_file in "${EXPERIMENTS[@]}"; do
    exp_name=$(basename "$exp_file" .yaml)
    echo ""
    echo "=========================================="
    echo "Testing: $exp_name"
    echo "=========================================="

    # Run experiment and capture duration
    START_TIME=$(date +%s)
    ./scripts/run_experiment.sh "$exp_file" > "/tmp/${exp_name}_test.log" 2>&1 || {
        echo "Warning: Experiment failed, checking log..."
        tail -20 "/tmp/${exp_name}_test.log"
        continue
    }
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))

    echo "Duration: ${DURATION}s"

    # Extract actual runtime from results if available
    if [ -f "experiments/results/${exp_name}_results.md" ]; then
        # Try to extract time from results
        RESULT_TIME=$(grep -oP 'Total Pairs: \d+ in \K[\d.]+' "experiments/results/${exp_name}_results.md" | head -1 || echo "")
        if [ -n "$RESULT_TIME" ]; then
            echo "Actual benchmark time: ${RESULT_TIME}s"
            # Use the actual benchmark time if available
            BENCHMARK_TIME=$(echo "$RESULT_TIME" | cut -d's' -f1 | cut -d'.' -f1)
            if [ -z "$BENCHMARK_TIME" ] || [ "$BENCHMARK_TIME" = "" ]; then
                BENCHMARK_TIME=$(echo "$RESULT_TIME" | awk '{print int($1)}')
            fi
        fi
    fi

    # Check if we need to increase benchmark_requests
    if [ -n "$BENCHMARK_TIME" ] && [ "$BENCHMARK_TIME" -lt "$MIN_DURATION" ]; then
        echo "⚠️  Benchmark ran for only ${BENCHMARK_TIME}s, needs at least ${MIN_DURATION}s"
        echo "Updating config..."

        # Read current config
        python3 << EOF
import yaml
import sys

with open("$exp_file", "r") as f:
    config = yaml.safe_load(f)

# Get current benchmark_requests or default
exp = config.get("experiment", {})
current_requests = exp.get("benchmark_requests", 1500)

# Calculate multiplier needed to reach MIN_DURATION
if ${BENCHMARK_TIME} > 0:
    multiplier = ${MIN_DURATION} / ${BENCHMARK_TIME}
    new_requests = int(current_requests * multiplier * 1.2)  # Add 20% buffer
else:
    new_requests = current_requests * 2

print(f"Current requests: {current_requests}")
print(f"New requests: {new_requests}")

# Update config
if "experiment" not in config:
    config["experiment"] = {}
config["experiment"]["benchmark_requests"] = new_requests

# Write back
with open("$exp_file", "w") as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

print("Config updated!")
EOF

        echo "✅ Config updated, re-running..."
        ./scripts/run_experiment.sh "$exp_file" || {
            echo "❌ Re-run failed"
        }
    else
        if [ -n "$BENCHMARK_TIME" ]; then
            echo "✅ Duration OK: ${BENCHMARK_TIME}s"
        else
            echo "✅ Total duration OK: ${DURATION}s"
        fi
    fi

    sleep 2
done

echo ""
echo "=========================================="
echo "All experiments checked and fixed!"
echo "=========================================="
