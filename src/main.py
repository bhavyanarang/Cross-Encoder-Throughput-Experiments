#!/usr/bin/env python3

import logging

import hydra
from omegaconf import DictConfig

from src.server.grpc import serve
from src.server.models.config_loader import get_experiment_name, hydra_config_to_config
from src.server.services.orchestrator_service import OrchestratorService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def main(cfg: DictConfig) -> None:
    config = hydra_config_to_config(cfg)
    experiment_name = get_experiment_name(config)
    if not experiment_name:
        experiment_name = cfg.get("name", "experiment")

    if cfg.get("grpc_port"):
        config.server.grpc_port = cfg.grpc_port
    if cfg.get("http_port"):
        config.server.http_port = cfg.http_port

    logger.info(f"Loaded config: {experiment_name}")

    orchestrator = OrchestratorService(config, experiment_name)
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
