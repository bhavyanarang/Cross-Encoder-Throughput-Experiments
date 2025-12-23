"""
Protocol definitions for type safety and interface contracts.

Using Python's Protocol for structural subtyping (duck typing with type hints).
"""

from typing import Protocol, runtime_checkable, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from backends.base_backend import InferenceResult


@runtime_checkable
class InferenceBackend(Protocol):
    """Protocol for inference backend implementations."""
    
    model_name: str
    device: str
    
    def load_model(self) -> None:
        """Load the model into memory."""
        ...
    
    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        """Run inference on query-document pairs."""
        ...
    
    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> "InferenceResult":
        """Run inference with timing breakdown."""
        ...
    
    def warmup(self, iterations: int = 5) -> None:
        """Warm up the model with dummy inference calls."""
        ...
    
    def get_model_info(self) -> dict:
        """Return information about the loaded model."""
        ...
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        ...
    
    @property
    def is_busy(self) -> bool:
        """Check if backend is currently processing."""
        ...
    
    @property
    def pending_requests(self) -> int:
        """Number of pending requests in queue."""
        ...


@runtime_checkable
class RoutingStrategy(Protocol):
    """Protocol for model pool routing strategies."""
    
    def select_backend(self, backends: list[InferenceBackend]) -> InferenceBackend:
        """Select the next backend to handle a request."""
        ...
    
    def reset(self) -> None:
        """Reset routing state (e.g., for round-robin index)."""
        ...

