"""Parameter sweep utilities for experiments."""

from copy import deepcopy
from itertools import product
from typing import Any


def expand_sweep_config(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Expand a config with sweep parameters into multiple configs.

    Supports sweeps for:
    - model.backend (list of backends)
    - batching.timeout_ms (list of timeout values)
    - batching.max_batch_size (list of batch sizes)
    - experiment.batch_sizes (already supported)
    - experiment.concurrency_levels (already supported)

    Returns a list of config dictionaries, one for each combination.
    """
    # Find all sweep parameters
    sweep_params = {}

    # Check model.backend
    if "model" in config and "backend" in config["model"]:
        backend_val = config["model"]["backend"]
        if isinstance(backend_val, list):
            sweep_params["model.backend"] = backend_val

    # Check batching.timeout_ms
    if "batching" in config and "timeout_ms" in config["batching"]:
        timeout_val = config["batching"]["timeout_ms"]
        if isinstance(timeout_val, list):
            sweep_params["batching.timeout_ms"] = timeout_val

    # Check batching.max_batch_size
    if "batching" in config and "max_batch_size" in config["batching"]:
        batch_size_val = config["batching"]["max_batch_size"]
        if isinstance(batch_size_val, list):
            sweep_params["batching.max_batch_size"] = batch_size_val

    # If no sweep parameters, return single config
    if not sweep_params:
        return [config]

    # Generate all combinations
    param_names = list(sweep_params.keys())
    param_values = list(sweep_params.values())

    expanded_configs = []
    for combination in product(*param_values):
        new_config = deepcopy(config)

        # Apply this combination
        for param_name, value in zip(param_names, combination, strict=False):
            parts = param_name.split(".")
            target = new_config
            for part in parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            target[parts[-1]] = value

        expanded_configs.append(new_config)

    return expanded_configs


def get_sweep_name(config: dict[str, Any], base_name: str) -> str:
    """Generate a descriptive name for a sweep configuration."""
    parts = [base_name]

    # Add backend if it's part of the sweep
    if "model" in config and "backend" in config["model"]:
        backend = config["model"]["backend"]
        if isinstance(backend, str):
            parts.append(backend)

    # Add timeout if it's part of the sweep
    if "batching" in config and "timeout_ms" in config["batching"]:
        timeout = config["batching"]["timeout_ms"]
        if isinstance(timeout, (int, float)):
            parts.append(f"{int(timeout)}ms")

    # Add max_batch_size if it's part of the sweep
    if "batching" in config and "max_batch_size" in config["batching"]:
        max_batch = config["batching"]["max_batch_size"]
        if isinstance(max_batch, int):
            parts.append(f"batch{max_batch}")

    return "_".join(parts)
