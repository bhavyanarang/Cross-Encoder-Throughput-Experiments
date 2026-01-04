#!/usr/bin/env python3

import logging

import hydra
from omegaconf import DictConfig

from src.server.grpc import serve
from src.server.services.orchestrator_service import OrchestratorService
from src.server.utils.config_loader import get_experiment_name, hydra_config_to_config

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

    experiment_config = cfg.get("experiment", {})
    concurrency_levels = experiment_config.get("concurrency_levels", [])

    if concurrency_levels:
        max_concurrency = max(concurrency_levels)

        recommended_workers = max(max_concurrency * 2, 16, config.server.grpc_workers)
        if config.server.grpc_workers < recommended_workers:
            if config.server.grpc_workers <= max_concurrency:
                logger.warning(
                    f"gRPC workers ({config.server.grpc_workers}) is less than max concurrency ({max_concurrency}). "
                    f"This will bottleneck throughput. Auto-adjusting to {recommended_workers}."
                )
            else:
                logger.info(
                    f"gRPC workers ({config.server.grpc_workers}) may be insufficient for concurrency {max_concurrency}. "
                    f"Auto-adjusting to {recommended_workers} for optimal throughput."
                )
            config.server.grpc_workers = recommended_workers

    logger.info(f"Loaded config: {experiment_name}")
    logger.info(f"gRPC server configured with {config.server.grpc_workers} worker threads")

    orchestrator = OrchestratorService(config, experiment_name)
    orchestrator.setup()
    orchestrator.start()

    logger.info(f"Starting gRPC server on port {config.server.grpc_port}...")
    serve(
        orchestrator,
        host=config.server.host,
        port=config.server.grpc_port,
        max_workers=config.server.grpc_workers,
        metrics=orchestrator.get_metrics(),
    )


if __name__ == "__main__":
    main()
