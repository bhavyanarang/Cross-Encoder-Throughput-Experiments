#!/bin/bash
# Run a sweep experiment (config with array parameters)
# This script generates individual configs for each combination and runs them

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "Usage: $0 <config_path>"
    exit 1
fi

CONFIG_PATH="$1"
EXPERIMENT_NAME=$(basename "$CONFIG_PATH" .yaml)

echo -e "${BLUE}=========================================="
echo "Running Sweep Experiment: $EXPERIMENT_NAME"
echo "Config: $CONFIG_PATH"
echo -e "==========================================${NC}"

cd "$PROJECT_ROOT"

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

OUTPUT_DIR="$PROJECT_ROOT/experiments/results"
TIMESERIES_DIR="$PROJECT_ROOT/experiments/distribution"
mkdir -p "$OUTPUT_DIR" "$TIMESERIES_DIR"

SWEEP_RESULTS_FILE="$OUTPUT_DIR/${EXPERIMENT_NAME}_results.md"
SWEEP_TIMESERIES_FILE="$TIMESERIES_DIR/${EXPERIMENT_NAME}_timeseries.md"

rm -f "$SWEEP_RESULTS_FILE" "$SWEEP_TIMESERIES_FILE"

TEMP_CONFIG_DIR=$(mktemp -d)
trap "rm -rf $TEMP_CONFIG_DIR" EXIT

python3 << PYTHON_GENERATE_CONFIGS
import yaml
import itertools
import os
from pathlib import Path

config_path = "$CONFIG_PATH"
temp_dir = "$TEMP_CONFIG_DIR"
experiment_name = "$EXPERIMENT_NAME"

with open(config_path) as f:
    config = yaml.safe_load(f)

sweep_params = {}
base_config = config.copy()

if "model_pool" in config and "instances" in config["model_pool"]:
    instances = config["model_pool"]["instances"]
    if instances and isinstance(instances, list) and len(instances) > 0:
        first_instance = instances[0]
        if isinstance(first_instance, dict):
            for key in ["backend", "quantization", "compile_mode"]:
                if key in first_instance and isinstance(first_instance[key], list):
                    sweep_params[f"model_pool.instances.0.{key}"] = first_instance[key]

if "batching" in config:
    for key in ["timeout_ms", "max_batch_size"]:
        if key in config["batching"] and isinstance(config["batching"][key], list):
            sweep_params[f"batching.{key}"] = config["batching"][key]

if not sweep_params:
    print("NO_SWEEPS")
    exit(0)

print(f"Sweep parameters found: {list(sweep_params.keys())}")

param_names = list(sweep_params.keys())
param_values = list(sweep_params.values())
combinations = list(itertools.product(*param_values))

print(f"Total combinations: {len(combinations)}")

manifest = []
for idx, combo in enumerate(combinations):
    sweep_config = yaml.safe_load(yaml.dump(config))

    combo_desc_parts = []
    for param_name, value in zip(param_names, combo):
        parts = param_name.split(".")
        obj = sweep_config
        for part in parts[:-1]:
            if part.isdigit():
                obj = obj[int(part)]
            else:
                obj = obj[part]
        final_key = parts[-1]
        obj[final_key] = value
        combo_desc_parts.append(f"{final_key}={value}")

    combo_desc = "_".join(combo_desc_parts)
    config_filename = f"{experiment_name}_config_{idx}.yaml"
    config_path_out = os.path.join(temp_dir, config_filename)

    with open(config_path_out, 'w') as f:
        f.write("# @package _global_\n\n")
        yaml.dump(sweep_config, f, default_flow_style=False, sort_keys=False)

    manifest.append({
        "idx": idx,
        "path": config_path_out,
        "desc": combo_desc
    })

manifest_path = os.path.join(temp_dir, "manifest.yaml")
with open(manifest_path, 'w') as f:
    yaml.dump(manifest, f)

print(f"Generated {len(manifest)} configurations")
PYTHON_GENERATE_CONFIGS

MANIFEST_PATH="$TEMP_CONFIG_DIR/manifest.yaml"
if [ ! -f "$MANIFEST_PATH" ]; then
    echo -e "${YELLOW}No sweep parameters found, running as single experiment${NC}"
    "$SCRIPT_DIR/run_experiment.sh" "$EXPERIMENT_NAME"
    exit $?
fi

TOTAL_CONFIGS=$(python3 -c "import yaml; print(len(yaml.safe_load(open('$MANIFEST_PATH'))))")
echo -e "${GREEN}Running $TOTAL_CONFIGS sweep configurations${NC}"

SUCCESSFUL=0
FAILED=0

for ((i=0; i<$TOTAL_CONFIGS; i++)); do
    CONFIG_INFO=$(python3 << PYTHON_GET_CONFIG
import yaml
manifest = yaml.safe_load(open("$MANIFEST_PATH"))
item = manifest[$i]
print(f"{item['path']}|{item['desc']}")
PYTHON_GET_CONFIG
    )

    CONFIG_FILE=$(echo "$CONFIG_INFO" | cut -d'|' -f1)
    CONFIG_DESC=$(echo "$CONFIG_INFO" | cut -d'|' -f2)

    echo ""
    echo -e "${BLUE}------------------------------------------"
    echo "Sweep $((i+1))/$TOTAL_CONFIGS: $CONFIG_DESC"
    echo -e "------------------------------------------${NC}"

    export SWEEP_TEMP_CONFIG_PATH="$CONFIG_FILE"
    export SWEEP_RESULTS_FILE="$SWEEP_RESULTS_FILE"
    export SWEEP_TIMESERIES_FILE="$SWEEP_TIMESERIES_FILE"
    export SWEEP_CONFIG_NUM=$((i+1))
    export SWEEP_TOTAL_CONFIGS=$TOTAL_CONFIGS
    export SWEEP_CONFIG_DESC="$CONFIG_DESC"

    if "$SCRIPT_DIR/run_experiment.sh" "$EXPERIMENT_NAME"; then
        SUCCESSFUL=$((SUCCESSFUL+1))
        echo -e "${GREEN}✓ Configuration $((i+1)) completed${NC}"
    else
        FAILED=$((FAILED+1))
        echo -e "${RED}✗ Configuration $((i+1)) failed${NC}"
    fi

    unset SWEEP_TEMP_CONFIG_PATH SWEEP_RESULTS_FILE SWEEP_TIMESERIES_FILE
    unset SWEEP_CONFIG_NUM SWEEP_TOTAL_CONFIGS SWEEP_CONFIG_DESC
done

echo ""
echo -e "${GREEN}=========================================="
echo "Sweep Experiment Complete: $EXPERIMENT_NAME"
echo "==========================================${NC}"
echo "Total configurations: $TOTAL_CONFIGS"
echo -e "  ${GREEN}Successful: $SUCCESSFUL${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "  ${RED}Failed: $FAILED${NC}"
fi
echo ""
echo "Results: $SWEEP_RESULTS_FILE"
echo "Timeseries: $SWEEP_TIMESERIES_FILE"
