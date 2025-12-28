from copy import deepcopy
from itertools import product
from typing import Any


def expand_sweep_config(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Expand sweep configs with arrays into multiple configs.

    Supports both old format (model.backend) and new Hydra format (model_pool.instances[0].backend).
    """

    sweep_params = {}

    # Old format: model.backend
    if "model" in config and "backend" in config["model"]:
        backend_val = config["model"]["backend"]
        if isinstance(backend_val, list):
            sweep_params["model.backend"] = backend_val

    # Old format: model.quantization_mode
    if "model" in config and "quantization_mode" in config["model"]:
        qmode_val = config["model"]["quantization_mode"]
        if isinstance(qmode_val, list):
            sweep_params["model.quantization_mode"] = qmode_val

    # Old format: model.compiled.mode
    if "model" in config and "compiled" in config["model"]:
        if isinstance(config["model"]["compiled"], dict) and "mode" in config["model"]["compiled"]:
            compile_mode_val = config["model"]["compiled"]["mode"]
            if isinstance(compile_mode_val, list):
                sweep_params["model.compiled.mode"] = compile_mode_val

    # New Hydra format: model_pool.instances[0].backend
    if "model_pool" in config and "instances" in config["model_pool"]:
        instances = config["model_pool"]["instances"]
        if instances and isinstance(instances, list) and len(instances) > 0:
            first_instance = instances[0]
            if isinstance(first_instance, dict):
                # Backend sweep
                if "backend" in first_instance and isinstance(first_instance["backend"], list):
                    sweep_params["model_pool.instances.0.backend"] = first_instance["backend"]
                # Quantization sweep
                if "quantization" in first_instance and isinstance(
                    first_instance["quantization"], list
                ):
                    sweep_params["model_pool.instances.0.quantization"] = first_instance[
                        "quantization"
                    ]
                # Compile mode sweep
                if "compile_mode" in first_instance and isinstance(
                    first_instance["compile_mode"], list
                ):
                    sweep_params["model_pool.instances.0.compile_mode"] = first_instance[
                        "compile_mode"
                    ]

    # Batching sweeps (same format in both old and new)
    if "batching" in config and "timeout_ms" in config["batching"]:
        timeout_val = config["batching"]["timeout_ms"]
        if isinstance(timeout_val, list):
            sweep_params["batching.timeout_ms"] = timeout_val

    if "batching" in config and "max_batch_size" in config["batching"]:
        batch_size_val = config["batching"]["max_batch_size"]
        if isinstance(batch_size_val, list):
            sweep_params["batching.max_batch_size"] = batch_size_val

    if not sweep_params:
        return [config]

    param_names = list(sweep_params.keys())
    param_values = list(sweep_params.values())

    expanded_configs = []
    for combination in product(*param_values):
        new_config = deepcopy(config)

        for param_name, value in zip(param_names, combination, strict=False):
            parts = param_name.split(".")
            target = new_config

            # Navigate to the parent of the target field
            for i, part in enumerate(parts[:-1]):
                # Check if next part is a digit (array index)
                is_next_array = i + 1 < len(parts) - 1 and parts[i + 1].isdigit()

                if part.isdigit():
                    # Array index - target should be a list
                    part_idx = int(part)
                    if isinstance(target, list):
                        while len(target) <= part_idx:
                            target.append({})
                        target = target[part_idx]
                    else:
                        # This shouldn't happen in normal flow
                        raise ValueError(f"Expected list at index {part_idx}, got {type(target)}")
                else:
                    # Regular dict key
                    if part not in target:
                        # If next part is a digit, create a list, otherwise a dict
                        target[part] = [] if is_next_array else {}
                    target = target[part]

            # Set the final value
            final_key = parts[-1]
            if isinstance(target, dict):
                target[final_key] = value
            elif isinstance(target, list):
                # Shouldn't happen, but handle it
                if len(target) == 0:
                    target.append({})
                if isinstance(target[0], dict):
                    target[0][final_key] = value
                else:
                    target[0] = {final_key: value}

        # Special handling for quantization_mode (old format)
        param_dict = dict(zip(param_names, combination, strict=False))
        if "model.quantization_mode" in param_dict:
            qmode = param_dict["model.quantization_mode"]
            if qmode == "int8":
                new_config.setdefault("model", {})["quantized"] = True
            elif qmode == "fp16":
                new_config.setdefault("model", {}).setdefault("mps", {})["fp16"] = True
                new_config["model"]["quantized"] = False
            elif qmode == "fp32":
                new_config.setdefault("model", {}).setdefault("mps", {})["fp16"] = False
                new_config["model"]["quantized"] = False

        expanded_configs.append(new_config)

    return expanded_configs


def get_sweep_name(config: dict[str, Any], base_name: str) -> str:
    """Generate a name for a sweep config based on its parameters."""

    parts = [base_name]

    # Old format: model.backend
    if "model" in config and "backend" in config["model"]:
        backend = config["model"]["backend"]
        if isinstance(backend, str):
            parts.append(backend)

    # Old format: model.quantization_mode
    if "model" in config and "quantization_mode" in config["model"]:
        qmode = config["model"]["quantization_mode"]
        if isinstance(qmode, str):
            parts.append(qmode)

    # Old format: model.compiled.mode
    if "model" in config and "compiled" in config["model"]:
        compiled = config["model"]["compiled"]
        if isinstance(compiled, dict) and "mode" in compiled:
            mode = compiled["mode"]
            if isinstance(mode, str):
                # Convert mode to shorter name
                mode_map = {"reduce-overhead": "ro", "max-autotune": "ma", "default": "def"}
                parts.append(mode_map.get(mode, mode))

    # New Hydra format: model_pool.instances[0].backend
    if "model_pool" in config and "instances" in config["model_pool"]:
        instances = config["model_pool"]["instances"]
        if instances and isinstance(instances, list) and len(instances) > 0:
            first_instance = instances[0]
            if isinstance(first_instance, dict):
                if "backend" in first_instance and isinstance(first_instance["backend"], str):
                    parts.append(first_instance["backend"])
                if "quantization" in first_instance and isinstance(
                    first_instance["quantization"], str
                ):
                    parts.append(first_instance["quantization"])
                if "compile_mode" in first_instance and isinstance(
                    first_instance["compile_mode"], str
                ):
                    mode = first_instance["compile_mode"]
                    mode_map = {"reduce-overhead": "ro", "max-autotune": "ma", "default": "def"}
                    parts.append(mode_map.get(mode, mode))

    # Batching parameters (same format in both)
    if "batching" in config and "timeout_ms" in config["batching"]:
        timeout = config["batching"]["timeout_ms"]
        if isinstance(timeout, (int, float)):
            parts.append(f"{int(timeout)}ms")

    if "batching" in config and "max_batch_size" in config["batching"]:
        max_batch = config["batching"]["max_batch_size"]
        if isinstance(max_batch, int):
            parts.append(f"batch{max_batch}")

    return "_".join(parts)
