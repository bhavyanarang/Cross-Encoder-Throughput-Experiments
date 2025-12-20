import yaml
import subprocess
import sys
import os
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

# Generate proto files if not present
proto_dir = os.path.join(os.path.dirname(__file__), "proto")
if not os.path.exists(os.path.join(proto_dir, "inference_pb2.py")):
    logger.info("Generating proto files...")
    subprocess.run([
        sys.executable, "-m", "grpc_tools.protoc",
        f"-I{proto_dir}",
        f"--python_out={proto_dir}",
        f"--grpc_python_out={proto_dir}",
        os.path.join(proto_dir, "inference.proto"),
    ], check=True)

from backends import create_backend
from metrics import MetricsCollector
from metrics.http_server import start_metrics_server, set_metrics_collector
from server.scheduler import Scheduler
from server.grpc_server import serve
from utils import load_experiment_config


def main():
    parser = argparse.ArgumentParser(description="ML Inference Server")
    parser.add_argument("--config", default="config.yaml", help="Path to config file (legacy)")
    parser.add_argument("--experiment", help="Path to experiment config (e.g., experiments/minilm_baseline.yaml)")
    parser.add_argument("--quantized", action="store_true", help="Enable quantization (overrides config)")
    parser.add_argument("--device", help="Device to use (overrides config: mps, cpu)")
    parser.add_argument("--model-name", help="Model name (overrides config)")
    args = parser.parse_args()

    # Load config - either experiment or legacy config
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

    logger.info(f"Loading model: {config['model']['name']}")
    logger.info(f"Device: {config['model'].get('device', 'mps')}")
    logger.info(f"Backend: {config['model'].get('backend', 'pytorch')}")
    if config["model"].get("quantized", False):
        logger.info(f"Quantization: {config['model'].get('quantization_mode', 'fp16').upper()}")
    else:
        logger.info("Quantization: DISABLED")
    
    # Initialize backend using factory
    backend = create_backend(config)
    backend.load_model()
    backend.warmup()
    
    # Log model info
    model_info = backend.get_model_info()
    logger.info(f"Model info: {model_info}")

    # Initialize metrics and scheduler
    metrics = MetricsCollector()
    set_metrics_collector(metrics)
    
    scheduler = Scheduler(
        backend=backend,
        metrics=metrics,
        batching_enabled=config["batching"]["enabled"],
        max_batch_size=config["batching"]["max_batch_size"],
        timeout_ms=config["batching"]["timeout_ms"],
    )

    # Start metrics HTTP server
    start_metrics_server(port=8080)
    logger.info("=" * 50)
    logger.info("Monitor metrics at: http://localhost:8080")
    logger.info("JSON endpoint: http://localhost:8080/metrics")
    logger.info("=" * 50)

    # Start gRPC server
    serve(scheduler, config["server"]["host"], config["server"]["port"])


if __name__ == "__main__":
    main()
