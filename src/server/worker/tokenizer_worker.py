import logging
import time

from src.server.dto.inference import TokenizedBatch
from src.server.utils.tokenizer import TokenizerService
from src.server.worker.base import BaseWorker, setup_worker_environment

logger = logging.getLogger(__name__)


class TokenizerWorker(BaseWorker[list[tuple[str, str]], TokenizedBatch]):
    def __init__(self, worker_id: int, model_name: str, max_length: int = 512):
        super().__init__(worker_id, worker_type="tokenizer")
        self.model_name = model_name
        self.max_length = max_length
        self._tokenizer: TokenizerService | None = None

    def initialize(self) -> None:
        setup_worker_environment()
        self._tokenizer = TokenizerService(self.model_name, self.max_length)
        logger.info(f"Tokenizer worker {self.worker_id} loaded: {self.model_name}")
        self.set_ready()

    def process(self, pairs: list[tuple[str, str]]) -> TokenizedBatch:
        if not self._tokenizer:
            raise RuntimeError(f"Tokenizer worker {self.worker_id} not initialized")

        start_time = time.perf_counter()
        result = self._tokenizer.tokenize(pairs, device="cpu")
        latency_ms = (time.perf_counter() - start_time) * 1000

        self._record_metrics(
            latency_ms=latency_ms,
            total_tokens=result.total_tokens,
            num_queries=len(pairs),
        )

        return result

    def get_memory_mb(self) -> float:
        return 0.0


__all__ = ["TokenizerWorker"]
