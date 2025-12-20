from abc import ABC, abstractmethod
import numpy as np


class BaseBackend(ABC):
    """Abstract base class for inference backends."""
    
    def __init__(self, model_name: str, device: str = "mps"):
        self.model_name = model_name
        self.device = device
        self.model = None
        self._is_loaded = False
    
    @abstractmethod
    def load_model(self) -> None:
        """Load the model into memory."""
        pass
    
    @abstractmethod
    def infer(self, texts: list[str]) -> np.ndarray:
        """Run inference on input texts and return embeddings."""
        pass
    
    @abstractmethod
    def warmup(self, iterations: int = 5) -> None:
        """Warm up the model with dummy inference calls."""
        pass
    
    @abstractmethod
    def get_model_info(self) -> dict:
        """Return information about the loaded model."""
        pass
    
    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

