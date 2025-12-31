import logging
import queue
from typing import TYPE_CHECKING

from src.server.services.service_base import PoolBasedService

if TYPE_CHECKING:
    from src.server.pool.model_pool import ModelPool

logger = logging.getLogger(__name__)


class InferenceService(PoolBasedService):
    """Inference service operating in pipeline mode only.
    
    All inference operations are asynchronous via queue-based pipeline.
    """
    
    def __init__(self, model_pool: "ModelPool"):
        super().__init__(model_pool)
        self._model_pool = model_pool
        self._inference_queue: queue.Queue | None = None

    def set_inference_queue(self, inference_queue: queue.Queue) -> None:
        """
        Set the inference queue for pipeline mode processing.
        
        Args:
            inference_queue: Queue to consume tokenized batches from
        """
        self._inference_queue = inference_queue
        self._model_pool.set_inference_queue(inference_queue)
        logger.info("Inference service pipeline queue set")

    def get_gpu_memory_mb(self) -> float:
        if not self.is_started:
            return 0.0
        return self._model_pool.get_gpu_memory_mb()

    def get_worker_metrics(self) -> list[dict]:
        if not self.is_started:
            return []
        return self._model_pool.get_worker_metrics()

    def reset_worker_metrics(self) -> None:
        if self.is_started:
            self._model_pool.reset_worker_metrics()



__all__ = [
    "InferenceService",
]
