"""
ML Inference Server - Main Entry Point

Starts the gRPC server for cross-encoder inference with:
- Configurable backends (MPS, MLX, PyTorch, ONNX, Compiled)
- Model pool for multi-model support
- Metrics dashboard
- Optional screenshot capture
"""

import argparse
import logging
import os
import subprocess
import sys

import yaml

# Configure logging ONCE at entry point
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Generate proto files if not present
proto_dir = os.path.join(os.path.dirname(__file__), "proto")
if not os.path.exists(os.path.join(proto_dir, "inference_pb2.py")):
    logger.info("Generating proto files...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            f"-I{proto_dir}",
            f"--python_out={proto_dir}",
            f"--grpc_python_out={proto_dir}",
            os.path.join(proto_dir, "inference.proto"),
        ],
        check=True,
    )

from metrics import MetricsCollector
from metrics.http_server import set_metrics_collector, start_metrics_server
from server.grpc_server import serve
from server.model_pool import ModelPool
from server.scheduler import Scheduler
from utils import configure_screenshots, load_experiment_config


def create_model_pool_from_config(config: dict) -> ModelPool:
    """
    Create ModelPool from config, supporting both new and legacy formats.

    Args:
        config: Configuration dictionary

    Returns:
        Configured ModelPool instance (process-based for true parallelism)
    """
    from core.config import ModelInstanceConfig, ModelPoolConfig

    # Check for new model_pool format
    if "model_pool" in config:
        pool_data = config["model_pool"]
        instances = [ModelInstanceConfig(**inst) for inst in pool_data.get("instances", [])]
        pool_config = ModelPoolConfig(
            instances=instances,
            routing_strategy=pool_data.get("routing_strategy", "round_robin"),
        )
        return ModelPool(pool_config)

    # Fall back to legacy single-model format
    from core.config import ModelInstanceConfig, ModelPoolConfig

    model_data = config.get("model", {})
    instance = ModelInstanceConfig(
        name=model_data.get("name", "cross-encoder/ms-marco-MiniLM-L-6-v2"),
        device=model_data.get("device", "mps"),
        backend=model_data.get("backend", "mps"),
        use_fp16=model_data.get("mps", {}).get("fp16", True),
        max_length=model_data.get("max_length"),
    )
    pool_config = ModelPoolConfig(
        instances=[instance],
        routing_strategy="round_robin",
    )
    return ModelPool(pool_config)


def main():
    parser = argparse.ArgumentParser(description="ML Inference Server")
    parser.add_argument("--config", default="config.yaml", help="Path to config file (legacy)")
    parser.add_argument(
        "--experiment", help="Path to experiment config (e.g., experiments/minilm_baseline.yaml)"
    )
    parser.add_argument(
        "--quantized", action="store_true", help="Enable quantization (overrides config)"
    )
    parser.add_argument("--device", help="Device to use (overrides config: mps, cpu)")
    parser.add_argument("--model-name", help="Model name (overrides config)")
    parser.add_argument(
        "--multi-model", type=int, default=1, help="Number of model instances (default: 1)"
    )
    args = parser.parse_args()

    # Load config
    if args.experiment:
        logger.info(f"Loading experiment config: {args.experiment}")
        config = load_experiment_config(args.experiment)
        logger.info(f"Experiment: {config.get('_experiment_name', 'unnamed')}")
        logger.info(f"Description: {config.get('_experiment_description', 'N/A')}")
    else:
        logger.info(f"Loading legacy config: {args.config}")
        with open(args.config) as f:
            config = yaml.safe_load(f)

    # Override config with CLI arguments
    if args.quantized:
        config["model"]["quantized"] = True
    if args.device:
        config["model"]["device"] = args.device
    if args.model_name:
        config["model"]["name"] = args.model_name

    # Configure screenshot functionality
    screenshot_config = config.get("screenshot", {})
    configure_screenshots(
        enabled=screenshot_config.get("enabled", False),
        output_dir=screenshot_config.get("output_dir", "docs/experiments/screenshots"),
    )

    logger.info(f"Loading model: {config['model']['name']}")
    logger.info(f"Device: {config['model'].get('device', 'mps')}")
    logger.info(f"Backend: {config['model'].get('backend', 'pytorch')}")
    if config["model"].get("quantized", False):
        logger.info(f"Quantization: {config['model'].get('quantization_mode', 'fp16').upper()}")
    else:
        logger.info("Quantization: DISABLED")

    # Create model pool (always process-based for true parallelism)
    if args.multi_model > 1 and "model_pool" not in config:
        # Create pool config from legacy config with multiple instances
        from core.config import ModelInstanceConfig, ModelPoolConfig

        instance = ModelInstanceConfig(
            name=config["model"]["name"],
            device=config["model"].get("device", "mps"),
            backend=config["model"].get("backend", "mps"),
            use_fp16=config["model"].get("mps", {}).get("fp16", True),
            max_length=config["model"].get("max_length"),
        )
        pool_config = ModelPoolConfig(
            instances=[instance] * args.multi_model,
            routing_strategy="round_robin",
        )
        model_pool = ModelPool(pool_config)
    else:
        model_pool = create_model_pool_from_config(config)

    # Start the process pool
    model_pool.start()

    # Log pool info
    pool_info = model_pool.get_pool_info()
    logger.info(
        f"Model pool: {pool_info['num_instances']} instances, "
        f"routing={pool_info.get('routing_strategy', 'N/A')}"
    )

    # Initialize metrics and scheduler
    metrics = MetricsCollector()
    set_metrics_collector(metrics)

    # Set model pool reference for per-instance metrics
    MetricsCollector.set_model_pool(model_pool)

    # Set experiment info for dashboard display
    metrics.set_experiment_info(
        name=config.get("_experiment_name", "Manual Run"),
        description=config.get("_experiment_description", ""),
        backend=config["model"].get("backend", "pytorch"),
        device=config["model"].get("device", "mps"),
    )

    # Check for length-aware batching option
    enable_length_aware = config.get("batching", {}).get("length_aware_batching", False)
    if enable_length_aware:
        logger.info("Length-aware batching: ENABLED (sorting pairs by length)")

    # Create scheduler with model pool
    scheduler = Scheduler(
        model_pool=model_pool,
        metrics=metrics,
        batching_enabled=config["batching"]["enabled"],
        max_batch_size=config["batching"]["max_batch_size"],
        timeout_ms=config["batching"]["timeout_ms"],
        enable_length_aware_batching=enable_length_aware,
    )

    # Start metrics HTTP server
    start_metrics_server(port=8080)
    logger.info("=" * 50)
    logger.info("Monitor metrics at: http://localhost:8080")
    logger.info("JSON endpoint: http://localhost:8080/metrics")
    logger.info("=" * 50)

    # Start gRPC server
    serve(
        scheduler,
        config["server"]["host"],
        config["server"]["port"],
        max_workers=config.get("server", {}).get("grpc_workers", 10),
    )


if __name__ == "__main__":
    main()
