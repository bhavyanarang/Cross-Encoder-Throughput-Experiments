#!/bin/bash
# Run an experiment with parameter sweeps
# Detects lists in config (backend, timeout_ms, max_batch_size) and runs experiments for each combination
# Usage: ./run_sweep_experiment.sh experiments/08_dynamic_batch_timeout.yaml

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "Usage: $0 <hydra_config_path>"
    echo "Example: $0 conf/experiments/01_backend_comparison.yaml"
    exit 1
fi

EXPERIMENT_CONFIG="$1"
if [ ! -f "$EXPERIMENT_CONFIG" ] && [ ! -f "$PROJECT_ROOT/$EXPERIMENT_CONFIG" ]; then
    echo -e "${RED}Error: Config file not found: $EXPERIMENT_CONFIG${NC}"
    exit 1
fi

if [ -f "$PROJECT_ROOT/$EXPERIMENT_CONFIG" ]; then
    EXPERIMENT_CONFIG="$PROJECT_ROOT/$EXPERIMENT_CONFIG"
fi

# Extract experiment name from path
EXPERIMENT_NAME=$(basename "$EXPERIMENT_CONFIG" .yaml)

cd "$PROJECT_ROOT"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Use Python to expand sweep configs
echo -e "${BLUE}Detecting sweep parameters...${NC}"
TEMP_OUTPUT=$(mktemp)
python3 << PYTHON_SCRIPT > "$TEMP_OUTPUT"
import sys
import yaml
from pathlib import Path
from itertools import product
from copy import deepcopy

config_path = "$EXPERIMENT_CONFIG"
with open(config_path) as f:
    config = yaml.safe_load(f)

# Load base config
base_path = Path(config_path).parent / "base_config.yaml"
base_config = {}
if base_path.exists():
    with open(base_path) as f:
        base_config = yaml.safe_load(f) or {}
# Simple merge
for key, value in base_config.items():
    if key not in config:
        config[key] = value
    elif isinstance(value, dict) and isinstance(config.get(key), dict):
        config[key] = {**value, **config[key]}

# Find sweep parameters
# Supports both old format (model.backend) and new Hydra format (model_pool.instances[0].backend)
sweeps = {}

# Old format: model.backend
if "model" in config:
    if "backend" in config["model"]:
        backend_val = config["model"]["backend"]
        if isinstance(backend_val, list):
            sweeps["model.backend"] = backend_val
    if "quantization_mode" in config["model"]:
        qmode_val = config["model"]["quantization_mode"]
        if isinstance(qmode_val, list):
            sweeps["model.quantization_mode"] = qmode_val
    if "compiled" in config["model"] and "mode" in config["model"]["compiled"]:
        compile_mode_val = config["model"]["compiled"]["mode"]
        if isinstance(compile_mode_val, list):
            sweeps["model.compiled.mode"] = compile_mode_val

# New Hydra format: model_pool.instances[0].backend
if "model_pool" in config and "instances" in config["model_pool"]:
    instances = config["model_pool"]["instances"]
    if instances and isinstance(instances, list) and len(instances) > 0:
        first_instance = instances[0]
        if isinstance(first_instance, dict):
            if "backend" in first_instance and isinstance(first_instance["backend"], list):
                sweeps["model_pool.instances.0.backend"] = first_instance["backend"]
            if "quantization" in first_instance and isinstance(first_instance["quantization"], list):
                sweeps["model_pool.instances.0.quantization"] = first_instance["quantization"]
            if "compile_mode" in first_instance and isinstance(first_instance["compile_mode"], list):
                sweeps["model_pool.instances.0.compile_mode"] = first_instance["compile_mode"]

# Batching sweeps (same format in both old and new)
if "batching" in config:
    if "timeout_ms" in config["batching"]:
        timeout_val = config["batching"]["timeout_ms"]
        if isinstance(timeout_val, list):
            sweeps["batching.timeout_ms"] = timeout_val
    if "max_batch_size" in config["batching"]:
        batch_val = config["batching"]["max_batch_size"]
        if isinstance(batch_val, list):
            sweeps["batching.max_batch_size"] = batch_val

# Generate all combinations
if not sweeps:
    # No sweeps, just return the original config path
    print(f"NO_SWEEP:{config_path}")
else:
    param_names = list(sweeps.keys())
    param_values = list(sweeps.values())

    import tempfile
    import os

    temp_dir = tempfile.mkdtemp(prefix="sweep_")
    configs = []

    for i, combination in enumerate(product(*param_values)):
        new_config = deepcopy(config)
        for param_name, value in zip(param_names, combination):
            parts = param_name.split(".")
            target = new_config
            # Navigate to parent of target field
            for j, part in enumerate(parts[:-1]):
                is_next_array = j + 1 < len(parts) - 1 and parts[j + 1].isdigit()
                if part.isdigit():
                    # Array index
                    part_idx = int(part)
                    if isinstance(target, list):
                        while len(target) <= part_idx:
                            target.append({})
                        target = target[part_idx]
                    else:
                        # Shouldn't happen, but handle it
                        prev_key = parts[j - 1] if j > 0 else None
                        if prev_key and prev_key in target:
                            if not isinstance(target[prev_key], list):
                                target[prev_key] = [target[prev_key]]
                            while len(target[prev_key]) <= part_idx:
                                target[prev_key].append({})
                            target = target[prev_key][part_idx]
                else:
                    # Regular dict key
                    if part not in target:
                        target[part] = [] if is_next_array else {}
                    target = target[part]
            # Set final value
            final_key = parts[-1]
            if isinstance(target, dict):
                target[final_key] = value
            elif isinstance(target, list) and len(target) > 0:
                if isinstance(target[0], dict):
                    target[0][final_key] = value

        # Special handling for quantization_mode
        param_dict = dict(zip(param_names, combination))
        if "model.quantization_mode" in param_dict:
            qmode = param_dict["model.quantization_mode"]
            if qmode == "int8":
                new_config["model"]["quantized"] = True
            elif qmode == "fp16":
                new_config["model"]["quantized"] = False
                if "mps" in new_config.get("model", {}):
                    new_config["model"]["mps"]["fp16"] = True
            elif qmode == "fp32":
                new_config["model"]["quantized"] = False
                if "mps" in new_config.get("model", {}):
                    new_config["model"]["mps"]["fp16"] = False

        # Generate name
        name_parts = [Path(config_path).stem]
        # Create a dict for easy lookup
        param_dict = dict(zip(param_names, combination))

        # Old format parameters
        if "model.backend" in param_dict:
            name_parts.append(str(param_dict["model.backend"]))
        if "model.quantization_mode" in param_dict:
            name_parts.append(str(param_dict["model.quantization_mode"]))
        if "model.compiled.mode" in param_dict:
            mode_val = param_dict["model.compiled.mode"]
            # Convert mode to shorter name
            mode_map = {"reduce-overhead": "ro", "max-autotune": "ma", "default": "def"}
            name_parts.append(mode_map.get(mode_val, mode_val))

        # New Hydra format parameters
        if "model_pool.instances.0.backend" in param_dict:
            name_parts.append(str(param_dict["model_pool.instances.0.backend"]))
        if "model_pool.instances.0.quantization" in param_dict:
            name_parts.append(str(param_dict["model_pool.instances.0.quantization"]))
        if "model_pool.instances.0.compile_mode" in param_dict:
            mode_val = param_dict["model_pool.instances.0.compile_mode"]
            mode_map = {"reduce-overhead": "ro", "max-autotune": "ma", "default": "def"}
            name_parts.append(mode_map.get(mode_val, mode_val))

        # Batching parameters (same in both formats)
        if "batching.timeout_ms" in param_dict:
            name_parts.append(f"{param_dict['batching.timeout_ms']}ms")
        if "batching.max_batch_size" in param_dict:
            name_parts.append(f"batch{param_dict['batching.max_batch_size']}")

        new_config["name"] = "_".join(name_parts)

        # Write temp config
        temp_config = os.path.join(temp_dir, f"config_{i}.yaml")
        with open(temp_config, "w") as f:
            yaml.dump(new_config, f)
        configs.append(temp_config)

    # Print temp dir and configs
    print(f"TEMP_DIR:{temp_dir}")
    for c in configs:
        print(c)
PYTHON_SCRIPT

# Parse output
TEMP_DIR=""
CONFIGS=()
FIRST_LINE=true
while IFS= read -r line; do
    if [[ $line == TEMP_DIR:* ]]; then
        TEMP_DIR="${line#TEMP_DIR:}"
    el    if [[ $line == NO_SWEEP:* ]]; then
        # No sweeps, run normally using Hydra config
        NO_SWEEP_CONFIG="${line#NO_SWEEP:}"
        EXPERIMENT_NAME=$(basename "$NO_SWEEP_CONFIG" .yaml)
        "$SCRIPT_DIR/run_experiment.sh" "$EXPERIMENT_NAME"
        rm -f "$TEMP_OUTPUT"
        exit $?
    else
        CONFIGS+=("$line")
    fi
done < "$TEMP_OUTPUT"
rm -f "$TEMP_OUTPUT"

# If no sweeps detected, run normally using Hydra config
if [ ${#CONFIGS[@]} -eq 0 ] || [ -z "$TEMP_DIR" ]; then
    echo -e "${GREEN}No sweep parameters detected, running single experiment...${NC}"
    "$SCRIPT_DIR/run_experiment.sh" "$EXPERIMENT_NAME"
    exit $?
fi

echo -e "${GREEN}Found ${#CONFIGS[@]} sweep configuration(s)${NC}"

# Get original experiment name for consolidated output
ORIGINAL_EXPERIMENT_NAME=$(basename "$EXPERIMENT_CONFIG" .yaml)
RESULTS_DIR="$PROJECT_ROOT/experiments/results"
DISTRIBUTION_DIR="$PROJECT_ROOT/experiments/distribution"
export SWEEP_ORIGINAL_NAME="$ORIGINAL_EXPERIMENT_NAME"
export SWEEP_RESULTS_FILE="$RESULTS_DIR/${ORIGINAL_EXPERIMENT_NAME}_results.md"
export SWEEP_TIMESERIES_FILE="$DISTRIBUTION_DIR/${ORIGINAL_EXPERIMENT_NAME}_timeseries.md"

# Initialize output files (clear existing)
mkdir -p "$RESULTS_DIR" "$DISTRIBUTION_DIR"
> "$SWEEP_RESULTS_FILE"
> "$SWEEP_TIMESERIES_FILE"

echo "Consolidated results will be saved to:"
echo "  Results: $SWEEP_RESULTS_FILE"
echo "  Timeseries: $SWEEP_TIMESERIES_FILE"

# Run each config
SUCCESS=0
FAILED=0
for i in "${!CONFIGS[@]}"; do
    config="${CONFIGS[$i]}"
    config_num=$((i + 1))
    total=${#CONFIGS[@]}

    echo -e "\n${BLUE}=========================================="
    echo "Sweep Config $config_num/$total"
    echo "==========================================${NC}"

    # Tell run_experiment.sh this is part of a sweep
    export SWEEP_CONFIG_NUM="$config_num"
    export SWEEP_TOTAL_CONFIGS="$total"

    # Convert temp config to client format
    TEMP_CLIENT_CONFIG=$(mktemp)
    CONFIG_EXPERIMENT_NAME=$(basename "$config" .yaml)
    python3 "$SCRIPT_DIR/hydra_to_client_config.py" "$CONFIG_EXPERIMENT_NAME" "$TEMP_CLIENT_CONFIG" --config-path "$config" || {
        echo -e "${RED}Failed to convert config for client${NC}"
        FAILED=$((FAILED + 1))
        rm -f "$TEMP_CLIENT_CONFIG"
        continue
    }

    # Temporarily copy temp config to conf/experiment/ so run_experiment.sh can find it
    TEMP_HYDRA_CONFIG="$PROJECT_ROOT/conf/experiment/${CONFIG_EXPERIMENT_NAME}.yaml"
    cp "$config" "$TEMP_HYDRA_CONFIG"

    # Run experiment with temp config
    if "$SCRIPT_DIR/run_experiment.sh" "$CONFIG_EXPERIMENT_NAME"; then
        SUCCESS=$((SUCCESS + 1))
    else
        FAILED=$((FAILED + 1))
    fi

    # Cleanup
    rm -f "$TEMP_CLIENT_CONFIG" "$TEMP_HYDRA_CONFIG"

    # Brief pause between sweep configs to ensure cleanup completes
    if [ $config_num -lt $total ]; then
        echo "Waiting for cleanup to complete before next config..."
        sleep 2
    fi
done

# Cleanup sweep env vars
unset SWEEP_ORIGINAL_NAME SWEEP_RESULTS_FILE SWEEP_TIMESERIES_FILE SWEEP_CONFIG_NUM SWEEP_TOTAL_CONFIGS

# Cleanup temp dir
if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi

# Summary
echo -e "\n${BLUE}=========================================="
echo "Sweep Summary"
echo "==========================================${NC}"
echo -e "${GREEN}Successful: $SUCCESS${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

exit $FAILED
