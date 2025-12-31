import logging
import queue
from typing import TYPE_CHECKING

from src.server.dto.pipeline import TokenizationQueueItem
from src.server.services.service_base import PoolBasedService

if TYPE_CHECKING:
    from src.server.pool.tokenizer_pool import TokenizerPool

logger = logging.getLogger(__name__)


class TokenizationService(PoolBasedService):
    """Tokenization service operating in pipeline mode only.
    
    All tokenization operations are asynchronous via queue-based pipeline.
    Results are automatically pushed to the inference queue.
    """
    
    def __init__(self, tokenizer_pool: "TokenizerPool"):
        super().__init__(tokenizer_pool)
        self._tokenizer_pool = tokenizer_pool
        self._inference_queue: queue.Queue | None = None

    def set_inference_queue(self, inference_queue: queue.Queue) -> None:
        """
        Set the inference queue for pipeline mode processing.
        
        Tokenization results will be automatically pushed to this queue.
        
        Args:
            inference_queue: Queue to push tokenized batches to
        """
        self._inference_queue = inference_queue
        self._tokenizer_pool.set_inference_queue(inference_queue)
        logger.info("Tokenization service pipeline queue set")

    def submit_pipeline(self, tokenization_item: TokenizationQueueItem) -> None:
        """
        Submit a request to the tokenization pipeline.
        
        The tokenization result will be automatically pushed to the inference queue.
        
        Args:
            tokenization_item: Item containing request and pairs
        """
        if not self.is_started:
            raise RuntimeError("Tokenization service not started")
        
        self._tokenizer_pool.submit_pipeline(tokenization_item)

    def get_worker_metrics(self) -> list[dict]:
        if not self.is_started:
            return []
        return self._tokenizer_pool.get_worker_metrics()

    def reset_worker_metrics(self) -> None:
        if self.is_started:
            self._tokenizer_pool.reset_worker_metrics()



__all__ = [
    "TokenizationService",
]
