import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.server.pool.model_pool import ModelPool
    from src.server.pool.tokenizer_pool import TokenizerPool

logger = logging.getLogger(__name__)


@dataclass
class MetricsCollector:
    experiment_name: str = ""
    experiment_description: str = ""
    backend_type: str = ""
    device: str = ""

    _model_pool: Optional["ModelPool"] = None
    _tokenizer_pool: Optional["TokenizerPool"] = None

    def set_pool(self, pool: "ModelPool") -> None:
        self._model_pool = pool

    def set_tokenizer_pool(self, pool: "TokenizerPool") -> None:
        self._tokenizer_pool = pool

    def set_experiment_info(
        self, name: str = "", description: str = "", backend: str = "", device: str = ""
    ) -> None:
        self.experiment_name = name
        self.experiment_description = description
        self.backend_type = backend
        self.device = device
        logger.info(f"Experiment: {name} | Backend: {backend} | Device: {device}")
