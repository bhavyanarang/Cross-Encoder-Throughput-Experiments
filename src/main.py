#!/usr/bin/env python3
"""Main entry point for inference server."""

import argparse
import logging
import signal
import sys
import threading
from pathlib import Path

import yaml

from src.frontend.server import start_dashboard
from src.models import BatchConfig, Config, ModelConfig, PoolConfig, ServerConfig
from src.server.grpc import serve
from src.server.metrics import MetricsCollector
from src.server.pool import ModelPool
from src.server.scheduler import Scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


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
    def deep_merge(base, override):
        """Deep merge two dictionaries, with override taking precedence."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    data = deep_merge(base_config, exp_config)

    # Handle experiment format with models list
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

    batching = BatchConfig()
    if "batching" in data:
        b = data["batching"]
        batching = BatchConfig(
            enabled=b.get("enabled", False),
            max_batch_size=b.get("max_batch_size", 8),
            timeout_ms=b.get("timeout_ms", 100),
            length_aware=b.get("length_aware", False),
        )

    server = ServerConfig()
    if "server" in data:
        s = data["server"]
        server = ServerConfig(
            host=s.get("host", "0.0.0.0"),
            grpc_port=s.get("grpc_port", 50051),
            http_port=s.get("http_port", 8080),
            grpc_workers=s.get("grpc_workers", 10),
        )

    return Config(
        model_pool=PoolConfig(instances=instances),
        batching=batching,
        server=server,
        name=data.get("name", ""),
        description=data.get("description", ""),
    )


def main():
    parser = argparse.ArgumentParser(description="Inference Server")
    parser.add_argument("--experiment", "-e", required=True, help="Experiment config YAML")
    parser.add_argument("--grpc-port", type=int, help="Override gRPC port")
    parser.add_argument("--http-port", type=int, help="Override HTTP port")
    args = parser.parse_args()

    config = load_config(args.experiment)

    # Use experiment filename as fallback if name is not set
    experiment_name = config.name
    if not experiment_name:
        # Extract name from filename (e.g., "experiments/07a_test.yaml" -> "07a_test")
        experiment_name = Path(args.experiment).stem

    logger.info(f"Loaded config: {experiment_name}")

    if args.grpc_port:
        config.server.grpc_port = args.grpc_port
    if args.http_port:
        config.server.http_port = args.http_port

    # Create model pool
    pool = ModelPool(config.model_pool)

    # Create metrics collector
    metrics = MetricsCollector()
    metrics.set_pool(pool)  # Pass pool reference for GPU memory queries
    metrics.set_experiment_info(
        name=experiment_name,
        description=config.description,
        backend=config.model_pool.instances[0].backend
        if config.model_pool.instances
        else "pytorch",
        device=config.model_pool.instances[0].device if config.model_pool.instances else "cpu",
    )

    # Handle shutdown
    shutdown_event = threading.Event()

    def handle_signal(signum, frame):
        logger.info("Shutdown signal received")
        shutdown_event.set()
        pool.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # Start pool
    logger.info(f"Starting pool with {len(config.model_pool.instances)} instances...")
    pool.start()

    # Create scheduler
    scheduler = Scheduler(
        pool,
        batching_enabled=config.batching.enabled,
        max_batch_size=config.batching.max_batch_size,
        timeout_ms=config.batching.timeout_ms,
        length_aware=config.batching.length_aware,
    )

    # Start dashboard
    start_dashboard(config.server.http_port, metrics)

    # Start gRPC server (blocking)
    logger.info(f"Starting gRPC server on port {config.server.grpc_port}...")
    serve(
        scheduler,
        host=config.server.host,
        port=config.server.grpc_port,
        max_workers=config.server.grpc_workers,
        metrics=metrics,
    )


if __name__ == "__main__":
    main()
