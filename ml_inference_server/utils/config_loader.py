import os
from typing import Any

import yaml


def deep_merge(base: dict[Any, Any], override: dict[Any, Any]) -> dict[Any, Any]:
    """Deep merge two dictionaries, with override taking precedence."""
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def load_experiment_config(experiment_path: str, base_config_path: str = None) -> dict[Any, Any]:
    """
    Load an experiment configuration, merging it with the base config.

    Args:
        experiment_path: Path to the experiment config file
        base_config_path: Path to the base config (defaults to experiments/base_config.yaml)

    Returns:
        Merged configuration dictionary
    """
    # Determine base config path
    if base_config_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_config_path = os.path.join(script_dir, "..", "experiments", "base_config.yaml")

    # Load base config
    with open(base_config_path) as f:
        base_config = yaml.safe_load(f)

    # Load experiment config
    with open(experiment_path) as f:
        experiment_config = yaml.safe_load(f)

    # Merge configs (experiment overrides base)
    merged_config = deep_merge(base_config, experiment_config)

    # Add metadata
    merged_config["_experiment_name"] = experiment_config.get("name", "unnamed")
    merged_config["_experiment_description"] = experiment_config.get("description", "")
    merged_config["_experiment_path"] = experiment_path

    return merged_config


def list_available_experiments(experiments_dir: str = None) -> list:
    """
    List all available experiment configurations.

    Args:
        experiments_dir: Path to experiments directory

    Returns:
        List of experiment config file paths
    """
    if experiments_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        experiments_dir = os.path.join(script_dir, "..", "experiments")

    experiments = []
    for filename in os.listdir(experiments_dir):
        if filename.endswith(".yaml") and filename != "base_config.yaml":
            experiments.append(os.path.join(experiments_dir, filename))

    return sorted(experiments)
