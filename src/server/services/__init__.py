from src.server.pool import BaseWorkerPool
from src.server.services.metrics_service import MetricsService
from src.server.services.orchestrator_service import OrchestratorService
from src.server.services.service_base import BaseService, PoolBasedService
from src.server.worker import BaseWorker, get_worker_gpu_memory, setup_worker_environment


# Lazy imports to avoid circular dependencies
def __getattr__(name):
    if name == "ModelPool":
        from src.server.pool.model_pool import ModelPool

        return ModelPool
    elif name == "TokenizerPool":
        from src.server.pool.tokenizer_pool import TokenizerPool

        return TokenizerPool
    elif name == "ModelWorker":
        from src.server.worker.model_worker import ModelWorker

        return ModelWorker
    elif name == "TokenizerService":
        from src.server.worker.tokenizer_worker import TokenizerService

        return TokenizerService
    elif name == "TokenizerWorker":
        from src.server.worker.tokenizer_worker import TokenizerWorker

        return TokenizerWorker
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "BaseWorker",
    "BaseWorkerPool",
    "BaseService",
    "PoolBasedService",
    "setup_worker_environment",
    "get_worker_gpu_memory",
    "ModelPool",
    "ModelWorker",
    "TokenizerService",
    "TokenizerPool",
    "TokenizerWorker",
    "OrchestratorService",
    "MetricsService",
]
