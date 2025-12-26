#!/bin/bash
# Run experiments from 06a onwards (after 5b) - these are the experiments
# that benefit most from the fixed queue wait and padding metrics

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

TOTAL=${#EXPERIMENTS[@]}
COUNT=0

echo "=========================================="
echo "Running $TOTAL experiments from 06a onwards"
echo "=========================================="
echo ""

for exp in "${EXPERIMENTS[@]}"; do
    COUNT=$((COUNT + 1))
    echo ""
    echo "=========================================="
    echo "[$COUNT/$TOTAL] Running: $exp"
    echo "=========================================="

    ./scripts/run_experiment.sh "$exp" || {
        echo "Warning: Experiment $exp failed, continuing..."
    }

    echo "Completed: $exp"
    sleep 2
done

echo ""
echo "=========================================="
echo "All experiments completed!"
echo "Results in: experiments/results/"
echo "=========================================="
