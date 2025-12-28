#!/usr/bin/env python3
"""Convert Hydra config to client-readable YAML format."""

import sys
from pathlib import Path

import yaml
from omegaconf import OmegaConf


def hydra_to_client_config(
    experiment_name: str, project_root: Path, config_path: Path = None
) -> dict:
    """Convert Hydra experiment config to client-readable format."""

    if config_path:
        hydra_config_path = Path(config_path)
    else:
        hydra_config_path = project_root / "conf" / "experiment" / f"{experiment_name}.yaml"

    if not hydra_config_path.exists():
        raise FileNotFoundError(f"Hydra config not found: {hydra_config_path}")

    # Load Hydra config
    cfg = OmegaConf.load(hydra_config_path)
    cfg_dict = OmegaConf.to_container(cfg, resolve=True)

    # Convert to client format
    client_config = {
        "name": cfg_dict.get("name", experiment_name),
        "description": cfg_dict.get("description", ""),
    }

    # Convert model_pool to legacy model format for client compatibility
    if "model_pool" in cfg_dict and "instances" in cfg_dict["model_pool"]:
        instances = cfg_dict["model_pool"]["instances"]
        if instances and len(instances) > 0:
            first_instance = instances[0]
            client_config["model"] = {
                "name": first_instance.get("name", "cross-encoder/ms-marco-MiniLM-L-6-v2"),
                "backend": first_instance.get("backend", "mps"),
                "device": first_instance.get("device", "mps"),
            }

            # Handle quantization
            quantization = first_instance.get("quantization", "fp16")
            if quantization == "fp16":
                client_config["model"]["mps"] = {"fp16": True}
            elif quantization == "fp32":
                client_config["model"]["mps"] = {"fp16": False}
            elif quantization == "int8":
                client_config["model"]["quantized"] = True
                client_config["model"]["quantization_mode"] = "int8"

    # Convert batching
    if "batching" in cfg_dict:
        batching = cfg_dict["batching"]
        client_config["batching"] = {
            "enabled": batching.get("enabled", False),
            "max_batch_size": batching.get("max_batch_size", 32),
            "timeout_ms": batching.get("timeout_ms", 100),
            "length_aware_batching": batching.get("length_aware", False),
        }

    # Keep experiment section as-is (for client benchmark config)
    if "experiment" in cfg_dict:
        client_config["experiment"] = cfg_dict["experiment"]

    return client_config


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: hydra_to_client_config.py <experiment_name> [output_file] [--config-path PATH]"
        )
        sys.exit(1)

    experiment_name = sys.argv[1]
    project_root = Path(__file__).parent.parent
    config_path = None

    # Parse --config-path option
    if "--config-path" in sys.argv:
        idx = sys.argv.index("--config-path")
        if idx + 1 < len(sys.argv):
            config_path = Path(sys.argv[idx + 1])

    try:
        client_config = hydra_to_client_config(experiment_name, project_root, config_path)

        if len(sys.argv) > 2 and sys.argv[2] != "--config-path":
            output_file = Path(sys.argv[2])
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                yaml.dump(client_config, f, default_flow_style=False, sort_keys=False)
            print(f"Client config written to: {output_file}")
        else:
            yaml.dump(client_config, sys.stdout, default_flow_style=False, sort_keys=False)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
