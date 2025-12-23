"""
Base Backend - Abstract base class for cross-encoder inference backends.

Defines the interface that all backend implementations must follow.
"""

from abc import ABC, abstractmethod
import time
import threading
import numpy as np
import logging
from dataclasses import dataclass
from typing import Optional

from .device_utils import resolve_device, sync_device, clear_memory, apply_fp16

logger = logging.getLogger(__name__)


@dataclass
class InferenceResult:
    """Result from inference with timing breakdown and padding analysis."""
    scores: np.ndarray
    t_tokenize_ms: float = 0.0
    t_model_inference_ms: float = 0.0
    total_ms: float = 0.0
    
    # Padding analysis metrics
    total_tokens: int = 0           # Total tokens in the batch (including padding)
    real_tokens: int = 0            # Actual content tokens (excluding padding)
    padded_tokens: int = 0          # Number of padding tokens
    padding_ratio: float = 0.0      # Fraction of tokens that are padding (0-1)
    max_seq_length: int = 0         # Longest sequence in batch
    avg_seq_length: float = 0.0     # Average sequence length before padding
    batch_size: int = 0             # Number of sequences in batch


class BaseBackend(ABC):
    """Abstract base class for cross-encoder inference backends."""
    
    def __init__(self, model_name: str, device: str = "mps"):
        self.model_name = model_name
        self.device = resolve_device(device)
        self.model = None
        self._is_loaded = False
        self._tokenizer = None
        
        # Thread safety and busy state tracking
        self._inference_lock = threading.Lock()
        self._is_busy = False
        self._pending_requests = 0
        self._pending_lock = threading.Lock()
    
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
    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """
        Run inference with timing breakdown for tokenization and model inference.
        
        All backends must implement this method to satisfy LSP.
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            InferenceResult with scores and timing breakdown
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
        """Check if model is loaded."""
        return self._is_loaded
    
    @property
    def is_busy(self) -> bool:
        """Check if backend is currently processing a request."""
        return self._is_busy
    
    @property
    def pending_requests(self) -> int:
        """Get number of pending requests in queue."""
        return self._pending_requests
    
    # ================== Thread Safety Helpers ==================
    
    def _acquire_for_inference(self) -> None:
        """Acquire lock and mark as busy."""
        with self._pending_lock:
            self._pending_requests += 1
        self._inference_lock.acquire()
        self._is_busy = True
    
    def _release_after_inference(self) -> None:
        """Release lock and mark as not busy."""
        self._is_busy = False
        self._inference_lock.release()
        with self._pending_lock:
            self._pending_requests -= 1
    
    # ================== Device Utilities (delegated) ==================
    
    def sync_device(self) -> None:
        """Synchronize GPU operations for accurate timing."""
        sync_device(self.device)
    
    def clear_memory(self) -> None:
        """Clear GPU memory cache."""
        clear_memory(self.device)
    
    def apply_fp16_to_model(self) -> tuple[bool, str]:
        """Apply FP16 precision to the loaded model."""
        return apply_fp16(self.model, self.device)
    
    # ================== Default infer_with_timing ==================
    
    def _default_infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """
        Default implementation of infer_with_timing.
        
        Wraps infer() with overall timing but no stage breakdown.
        Subclasses should override for more detailed timing.
        """
        self._acquire_for_inference()
        try:
            start = time.perf_counter()
            self.sync_device()
            scores = self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
            self.sync_device()
            total_ms = (time.perf_counter() - start) * 1000
            
            return InferenceResult(
                scores=scores,
                t_tokenize_ms=0.0,
                t_model_inference_ms=total_ms,
                total_ms=total_ms,
                batch_size=len(pairs),
            )
        finally:
            self._release_after_inference()
    
    # ================== Factory Method ==================
    
    @classmethod
    def from_config(cls, config) -> "BaseBackend":
        """
        Create backend instance from configuration.
        
        Subclasses should override this to handle their specific config options.
        
        Args:
            config: ModelInstanceConfig or dict with configuration
            
        Returns:
            Configured backend instance
        """
        raise NotImplementedError("Subclasses must implement from_config")
