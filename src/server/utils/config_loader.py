import logging
from pathlib import Path

import yaml
from omegaconf import DictConfig, OmegaConf

from src.server.dto.config import (
    BatchConfig,
    Config,
    ModelConfig,
    PoolConfig,
    ServerConfig,
    TokenizerPoolConfig,
)

logger = logging.getLogger(__name__)


def _deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _parse_model_instances(data: dict) -> list[ModelConfig]:
    instances = []

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
        instances.append(ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2"))

    return instances


def _parse_batching_config(data: dict) -> BatchConfig:
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
    if "tokenizer_pool" not in data:
        return TokenizerPoolConfig()

    tp = data["tokenizer_pool"]
    return TokenizerPoolConfig(
        enabled=tp.get("enabled", False),
        num_workers=tp.get("num_workers", 1),
        model_name=tp.get("model_name", ""),
    )


def _parse_server_config(data: dict) -> ServerConfig:
    if "server" not in data:
        return ServerConfig()

    s = data["server"]
    return ServerConfig(
        host=s.get("host", "0.0.0.0"),
        grpc_port=s.get("grpc_port", s.get("port", 50051)),
        http_port=s.get("http_port", 8080),
        prometheus_port=s.get("prometheus_port", 8000),
        grpc_workers=s.get("grpc_workers", 10),
    )


def load_config(config_path: str) -> Config:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    base_config_path = path.parent / "base_config.yaml"
    base_config = {}
    if base_config_path.exists():
        with open(base_config_path) as f:
            base_config = yaml.safe_load(f) or {}

    with open(path) as f:
        exp_config = yaml.safe_load(f) or {}

    data = _deep_merge(base_config, exp_config)

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


def hydra_config_to_config(cfg: DictConfig) -> Config:
    cfg_dict = OmegaConf.to_container(cfg, resolve=True)

    instances = []
    if "model_pool" in cfg_dict and "instances" in cfg_dict["model_pool"]:
        for m in cfg_dict["model_pool"]["instances"]:
            instances.append(
                ModelConfig(
                    name=m.get("name", "cross-encoder/ms-marco-MiniLM-L-6-v2"),
                    device=m.get("device", "mps"),
                    backend=m.get("backend", "mps"),
                    quantization=m.get("quantization", "fp16"),
                    compile_model=m.get("compile_model", False),
                    compile_mode=m.get("compile_mode", None),
                    max_length=m.get("max_length", 512),
                    onnx_optimize=m.get("onnx_optimize", True),
                )
            )
    else:
        instances.append(ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2"))

    tokenizer_pool = TokenizerPoolConfig(
        enabled=cfg_dict.get("tokenizer_pool", {}).get("enabled", True),
        num_workers=cfg_dict.get("tokenizer_pool", {}).get("num_workers", 3),
        model_name=cfg_dict.get("tokenizer_pool", {}).get("model_name", ""),
    )

    batching = BatchConfig(
        enabled=cfg_dict.get("batching", {}).get("enabled", False),
        max_batch_size=cfg_dict.get("batching", {}).get("max_batch_size", 8),
        timeout_ms=float(cfg_dict.get("batching", {}).get("timeout_ms", 100.0)),
        length_aware=cfg_dict.get("batching", {}).get("length_aware", False),
    )

    server = ServerConfig(
        host=cfg_dict.get("server", {}).get("host", "0.0.0.0"),
        grpc_port=cfg_dict.get("server", {}).get("grpc_port", 50051),
        http_port=cfg_dict.get("server", {}).get("http_port", 8080),
        prometheus_port=cfg_dict.get("server", {}).get("prometheus_port", 8000),
        grpc_workers=cfg_dict.get("server", {}).get("grpc_workers", 10),
    )

    return Config(
        model_pool=PoolConfig(instances=instances),
        tokenizer_pool=tokenizer_pool,
        batching=batching,
        server=server,
        name=cfg_dict.get("name", ""),
        description=cfg_dict.get("description", ""),
    )


def get_experiment_name(config: Config, config_path: str | None = None) -> str:
    if config.name:
        return config.name
    if config_path:
        return Path(config_path).stem
    return "experiment"


__all__ = ["load_config", "get_experiment_name", "hydra_config_to_config"]
