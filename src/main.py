#!/usr/bin/env python3
"""Main entry point for inference server."""

import argparse
import logging

from src.models.config_loader import get_experiment_name, load_config
from src.server.grpc import serve
from src.server.orchestrator import ServerOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Inference Server")
    parser.add_argument("--experiment", "-e", required=True, help="Experiment config YAML")
    parser.add_argument("--grpc-port", type=int, help="Override gRPC port")
    parser.add_argument("--http-port", type=int, help="Override HTTP port")
    args = parser.parse_args()

    config = load_config(args.experiment)
    experiment_name = get_experiment_name(config, args.experiment)

    if args.grpc_port:
        config.server.grpc_port = args.grpc_port
    if args.http_port:
        config.server.http_port = args.http_port

    logger.info(f"Loaded config: {experiment_name}")

    orchestrator = ServerOrchestrator(config, experiment_name)
    orchestrator.setup()
    orchestrator.start()

    logger.info(f"Starting gRPC server on port {config.server.grpc_port}...")
    serve(
        orchestrator.get_inference_handler(),
        host=config.server.host,
        port=config.server.grpc_port,
        max_workers=config.server.grpc_workers,
        metrics=orchestrator.get_metrics(),
    )


if __name__ == "__main__":
    main()
