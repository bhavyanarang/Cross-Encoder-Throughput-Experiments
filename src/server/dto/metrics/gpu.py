import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.server.services.inference_service import InferenceService
    from src.server.pool.model_pool import ModelPool

logger = logging.getLogger(__name__)


class GPUMemoryProvider:
    def __init__(self):
        self._inference_service: InferenceService | None = None
        self._pool: ModelPool | None = None

    def set_inference_service(self, inference_service: "InferenceService") -> None:
        self._inference_service = inference_service

    def set_pool(self, pool: "ModelPool") -> None:
        self._pool = pool

    def _try_get_memory(self, source_name: str, getter: callable) -> float | None:
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

    def get_memory_mb(self) -> float:
        if self._inference_service is not None:
            memory = self._try_get_memory(
                "inference service", self._inference_service.get_gpu_memory_mb
            )
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
