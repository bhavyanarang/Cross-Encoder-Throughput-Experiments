from abc import ABC, abstractmethod
import numpy as np
import logging
from functools import wraps
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

# Type variable for decorator
F = TypeVar('F', bound=Callable)


def with_inference_mode(func: F) -> F:
    """Decorator to run inference in torch.inference_mode for better performance."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            import torch
            with torch.inference_mode():
                return func(self, *args, **kwargs)
        except ImportError:
            return func(self, *args, **kwargs)
    return wrapper


class BaseBackend(ABC):
    """Abstract base class for cross-encoder inference backends."""
    
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
    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        """
        Run cross-encoder inference on query-document pairs.
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            Array of relevance scores, one per pair
        """
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
    
    # ================== Shared Utilities ==================
    
    @staticmethod
    def apply_fp16(model, device: str, logger) -> tuple:
        """
        Apply FP16 quantization to a CrossEncoder model.
        
        Returns:
            Tuple of (success: bool, actual_dtype: str)
        """
        if device != "mps":
            logger.info("FP16 only supported on MPS, using FP32")
            return False, "float32"
        
        try:
            model.model = model.model.half()
            logger.info("Applied FP16 precision")
            return True, "float16"
        except Exception as e:
            logger.warning(f"FP16 conversion failed: {e}, using FP32")
            return False, "float32"
    
    @staticmethod
    def resolve_device(requested_device: str) -> str:
        """Resolve the actual device to use, preferring MPS on Apple Silicon."""
        try:
            import torch
            if requested_device == "mps" and torch.backends.mps.is_available():
                return "mps"
            elif requested_device == "cuda" and torch.cuda.is_available():
                return "cuda"
        except ImportError:
            pass
        return "cpu"
    
    @staticmethod
    def sync_device(device: str) -> None:
        """Synchronize GPU operations for accurate timing."""
        try:
            import torch
            if device == "mps":
                torch.mps.synchronize()
            elif device == "cuda":
                torch.cuda.synchronize()
        except (ImportError, RuntimeError):
            pass
    
    @staticmethod
    def clear_memory(device: str) -> None:
        """Clear GPU memory cache to reduce fragmentation."""
        try:
            import torch
            if device == "mps":
                torch.mps.empty_cache()
            elif device == "cuda":
                torch.cuda.empty_cache()
        except (ImportError, RuntimeError, AttributeError):
            pass
