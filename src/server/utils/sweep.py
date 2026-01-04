from copy import deepcopy
from itertools import product
from typing import Any


def expand_sweep_config(config: dict[str, Any]) -> list[dict[str, Any]]:
    sweep_params = {}
    if "model" in config and "backend" in config["model"]:
        backend_val = config["model"]["backend"]
        if isinstance(backend_val, list):
            sweep_params["model.backend"] = backend_val

    if "model" in config and "quantization_mode" in config["model"]:
        qmode_val = config["model"]["quantization_mode"]
        if isinstance(qmode_val, list):
            sweep_params["model.quantization_mode"] = qmode_val

    if "model" in config and "compiled" in config["model"]:
        if isinstance(config["model"]["compiled"], dict) and "mode" in config["model"]["compiled"]:
            compile_mode_val = config["model"]["compiled"]["mode"]
            if isinstance(compile_mode_val, list):
                sweep_params["model.compiled.mode"] = compile_mode_val

    if "model_pool" in config and "instances" in config["model_pool"]:
        instances = config["model_pool"]["instances"]
        if instances and isinstance(instances, list) and len(instances) > 0:
            first_instance = instances[0]
            if isinstance(first_instance, dict):
                if "backend" in first_instance and isinstance(first_instance["backend"], list):
                    sweep_params["model_pool.instances.0.backend"] = first_instance["backend"]
                if "quantization" in first_instance and isinstance(
                    first_instance["quantization"], list
                ):
                    sweep_params["model_pool.instances.0.quantization"] = first_instance[
                        "quantization"
                    ]
                if "compile_mode" in first_instance and isinstance(
                    first_instance["compile_mode"], list
                ):
                    sweep_params["model_pool.instances.0.compile_mode"] = first_instance[
                        "compile_mode"
                    ]
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

        for param_name, value in zip(param_names, combination):
            parts = param_name.split(".")
            target = new_config

            for i, part in enumerate(parts[:-1]):
                is_next_array = i + 1 < len(parts) - 1 and parts[i + 1].isdigit()

                if part.isdigit():
                    part_idx = int(part)
                    if isinstance(target, list):
                        while len(target) <= part_idx:
                            target.append({})
                        target = target[part_idx]
                    else:
                        raise ValueError(f"Expected list at index {part_idx}, got {type(target)}")
                else:
                    if part not in target:
                        target[part] = [] if is_next_array else {}
                    target = target[part]
            final_key = parts[-1]
            if isinstance(target, dict):
                target[final_key] = value
            elif isinstance(target, list):
                if len(target) == 0:
                    target.append({})
                if isinstance(target[0], dict):
                    target[0][final_key] = value
                else:
                    target[0] = {final_key: value}
        param_dict = dict(zip(param_names, combination))
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
    parts = [base_name]
    if "model" in config and "backend" in config["model"]:
        backend = config["model"]["backend"]
        if isinstance(backend, str):
            parts.append(backend)

    if "model" in config and "quantization_mode" in config["model"]:
        qmode = config["model"]["quantization_mode"]
        if isinstance(qmode, str):
            parts.append(qmode)

    if "model" in config and "compiled" in config["model"]:
        compiled = config["model"]["compiled"]
        if isinstance(compiled, dict) and "mode" in compiled:
            mode = compiled["mode"]
            if isinstance(mode, str):
                mode_map = {"reduce-overhead": "ro", "max-autotune": "ma", "default": "def"}
                parts.append(mode_map.get(mode, mode))
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

    if "batching" in config and "timeout_ms" in config["batching"]:
        timeout = config["batching"]["timeout_ms"]
        if isinstance(timeout, (int, float)):
            parts.append(f"{int(timeout)}ms")

    if "batching" in config and "max_batch_size" in config["batching"]:
        max_batch = config["batching"]["max_batch_size"]
        if isinstance(max_batch, int):
            parts.append(f"batch{max_batch}")

    return "_".join(parts)
