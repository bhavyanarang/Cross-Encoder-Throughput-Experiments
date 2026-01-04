import logging
import os
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from src.server.pool.model_pool import ModelPool
    from src.server.services.orchestrator_service import OrchestratorService

logger = logging.getLogger(__name__)


class ProcessMonitorService:
    def __init__(self):
        self._process = None
        self._initialized = False
        self._orchestrator: Optional["OrchestratorService"] = None
        self._pool: Optional["ModelPool"] = None

    def _init_process(self) -> None:
        if self._initialized:
            return
        try:
            import psutil

            self._process = psutil.Process(os.getpid())
            self._process.cpu_percent()
        except ImportError:
            self._process = None
        self._initialized = True

    def get_cpu_percent(self) -> float:
        self._init_process()
        if self._process:
            try:
                return self._process.cpu_percent(interval=None)
            except Exception:
                pass
        return 0.0

    def set_inference_service(self, orchestrator: "OrchestratorService") -> None:
        self._orchestrator = orchestrator

    def set_pool(self, pool: "ModelPool") -> None:
        self._pool = pool

    def _try_get_memory(self, source_name: str, getter: Callable[[], float]) -> Optional[float]:
        try:
            memory = getter()
            if memory > 0:
                return memory
            logger.debug(
                f"{source_name} returned 0 GPU memory - workers may not have models loaded yet"
            )
        except Exception as e:
            logger.debug(f"Error getting GPU memory from {source_name}: {e}")
        return None

    def get_gpu_memory_mb(self) -> float:
        if self._orchestrator is not None:
            memory = self._try_get_memory("orchestrator", self._orchestrator.get_gpu_memory_mb)
            if memory is not None:
                return memory

        if self._pool is not None:
            memory = self._try_get_memory("pool", self._pool.get_gpu_memory_mb)
            if memory is not None:
                return memory

        try:
            import torch

            if torch.backends.mps.is_available():
                memory = self._try_get_memory(
                    "main process (driver)",
                    lambda: torch.mps.driver_allocated_memory() / (1024 * 1024),
                )
                if memory is not None:
                    return memory
                memory = self._try_get_memory(
                    "main process (current)",
                    lambda: torch.mps.current_allocated_memory() / (1024 * 1024),
                )
                if memory is not None:
                    return memory
        except Exception as e:
            logger.debug(f"Error getting GPU memory from main process: {e}")

        return 0.0


__all__ = ["ProcessMonitorService"]
