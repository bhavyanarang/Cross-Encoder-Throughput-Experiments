"""Configuration loader for experiment configs."""

import logging
from pathlib import Path

import yaml

from src.models import (
    BatchConfig,
    Config,
    ModelConfig,
    PoolConfig,
    ServerConfig,
    TokenizerPoolConfig,
)

logger = logging.getLogger(__name__)


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dictionaries, with override taking precedence."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _parse_model_instances(data: dict) -> list[ModelConfig]:
    """Parse model instances from config data."""
    instances = []

    # Check model_pool.instances first (multi-model format)
    if "model_pool" in data and "instances" in data["model_pool"]:
        for m in data["model_pool"]["instances"]:
            instances.append(
                ModelConfig(
                    name=m.get("name", "cross-encoder/ms-marco-MiniLM-L-6-v2"),
                    device=m.get("device", "mps"),
                    backend=m.get("backend", "mps"),
                    quantization=m.get(
                        "quantization", m.get("use_fp16", True) and "fp16" or "fp32"
                    ),
                    compile_model=m.get("compile", False),
                    max_length=m.get("max_length", 512),
                )
            )
    elif "models" in data:
        for m in data["models"]:
            instances.append(
                ModelConfig(
                    name=m.get("name", "cross-encoder/ms-marco-MiniLM-L-6-v2"),
                    device=m.get("device", "mps"),
                    backend=m.get("backend", "mps"),
                    quantization=m.get("quantization", "fp16"),
                    compile_model=m.get("compile", False),
                    max_length=m.get("max_length", 512),
                )
            )
    elif "model" in data:
        m = data["model"]
        instances.append(
            ModelConfig(
                name=m.get("name", "cross-encoder/ms-marco-MiniLM-L-6-v2"),
                device=m.get("device", "mps"),
                backend=m.get("backend", "mps"),
                quantization=m.get("quantization", "fp16"),
                compile_model=m.get("compile", False),
                max_length=m.get("max_length", 512),
            )
        )
    else:
        instances.append(ModelConfig())

    return instances


def _parse_batching_config(data: dict) -> BatchConfig:
    """Parse batching configuration from data."""
    if "batching" not in data:
        return BatchConfig()

    b = data["batching"]
    return BatchConfig(
        enabled=b.get("enabled", False),
        max_batch_size=b.get("max_batch_size", 8),
        timeout_ms=b.get("timeout_ms", 100),
        length_aware=b.get("length_aware", False),
    )


def _parse_tokenizer_pool_config(data: dict) -> TokenizerPoolConfig:
    """Parse tokenizer pool configuration from data."""
    if "tokenizer_pool" not in data:
        return TokenizerPoolConfig()

    tp = data["tokenizer_pool"]
    return TokenizerPoolConfig(
        enabled=tp.get("enabled", False),
        num_workers=tp.get("num_workers", 1),
        model_name=tp.get("model_name", ""),
    )


def _parse_server_config(data: dict) -> ServerConfig:
    """Parse server configuration from data."""
    if "server" not in data:
        return ServerConfig()

    s = data["server"]
    return ServerConfig(
        host=s.get("host", "0.0.0.0"),
        grpc_port=s.get("grpc_port", 50051),
        http_port=s.get("http_port", 8080),
        grpc_workers=s.get("grpc_workers", 10),
    )


def load_config(config_path: str) -> Config:
    """Load configuration from YAML file, merging with base_config.yaml."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    # Load base config first
    base_config_path = path.parent / "base_config.yaml"
    base_config = {}
    if base_config_path.exists():
        with open(base_config_path) as f:
            base_config = yaml.safe_load(f) or {}

    # Load experiment config
    with open(path) as f:
        exp_config = yaml.safe_load(f) or {}

    # Deep merge: base_config values are defaults, exp_config overrides
    data = _deep_merge(base_config, exp_config)

    # Parse all configuration sections
    instances = _parse_model_instances(data)
    batching = _parse_batching_config(data)
    tokenizer_pool = _parse_tokenizer_pool_config(data)
    server = _parse_server_config(data)

    return Config(
        model_pool=PoolConfig(instances=instances),
        tokenizer_pool=tokenizer_pool,
        batching=batching,
        server=server,
        name=data.get("name", ""),
        description=data.get("description", ""),
    )


def get_experiment_name(config: Config, config_path: str) -> str:
    """Get experiment name from config or derive from filename."""
    if config.name:
        return config.name
    # Extract name from filename (e.g., "experiments/07a_test.yaml" -> "07a_test")
    return Path(config_path).stem


__all__ = ["load_config", "get_experiment_name"]
