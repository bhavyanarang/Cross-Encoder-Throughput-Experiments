"""
Backward compatibility module. Base classes have been moved to their respective modules:
- BaseWorker is now in src.server.worker.base
- BaseWorkerPool is now in src.server.pool.base
"""

# Re-export for backward compatibility
from src.server.worker.base import BaseWorker, get_worker_gpu_memory, setup_worker_environment
from src.server.pool.base import BaseWorkerPool

__all__ = [
    "BaseWorker",
    "BaseWorkerPool",
    "setup_worker_environment",
    "get_worker_gpu_memory",
]
