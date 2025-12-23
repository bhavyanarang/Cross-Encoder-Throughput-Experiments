"""
Model Pool Manager.

Manages multiple model instances and routes requests to available backends.
Supports eager loading and configurable routing strategies.
"""

import threading
import logging
from typing import TYPE_CHECKING, Optional, Tuple

from backends import create_backend, BaseBackend, InferenceResult
from .routing import RoutingStrategy, create_router

if TYPE_CHECKING:
    from core.config import ModelPoolConfig, ModelInstanceConfig

logger = logging.getLogger(__name__)


class ModelPool:
    """
    Manages a pool of model backend instances.
    
    Features:
    - Eager loading of all configured model instances
    - Configurable routing strategies (round_robin, least_busy)
    - Thread-safe backend acquisition and release
    - Unified interface for inference across all backends
    
    Usage:
        pool = ModelPool(config)
        pool.load_all()
        
        # Direct inference (routing handled internally)
        result = pool.infer_with_timing(pairs)
        
        # Or acquire specific backend
        backend, idx = pool.acquire_backend()
        try:
            scores = backend.infer(pairs)
        finally:
            pool.release_backend(idx)
    """
    
    def __init__(
        self,
        config: "ModelPoolConfig",
        routing_strategy: Optional[RoutingStrategy] = None,
    ):
        """
        Initialize model pool.
        
        Args:
            config: ModelPoolConfig with instance configurations
            routing_strategy: Optional custom routing strategy.
                             If None, creates from config.routing_strategy
        """
        self.config = config
        self.backends: list[BaseBackend] = []
        self._lock = threading.Lock()
        self._is_loaded = False
        
        # Create router from config or use provided
        if routing_strategy is not None:
            self.router = routing_strategy
        else:
            self.router = create_router(config.routing_strategy)
        
        logger.info(f"ModelPool initialized with {len(config.instances)} instance(s), "
                   f"routing={config.routing_strategy}")
    
    @classmethod
    def from_legacy_config(cls, config: dict) -> "ModelPool":
        """
        Create ModelPool from legacy single-model config format.
        
        Args:
            config: Legacy dict config with 'model' key
            
        Returns:
            ModelPool with single backend instance
        """
        from core.config import ModelPoolConfig, ModelInstanceConfig
        
        model_config = config.get("model", {})
        
        instance = ModelInstanceConfig(
            name=model_config.get("name", "cross-encoder/ms-marco-MiniLM-L-6-v2"),
            device=model_config.get("device", "mps"),
            backend=model_config.get("backend", "mps"),
            use_fp16=model_config.get("mps", {}).get("fp16", True),
        )
        
        pool_config = ModelPoolConfig(
            instances=[instance],
            routing_strategy="round_robin",
        )
        
        return cls(pool_config)
    
    def load_all(self) -> None:
        """
        Eager load all model instances.
        
        Loads each configured model, runs warmup, and adds to pool.
        """
        logger.info(f"Loading {len(self.config.instances)} model instance(s)...")
        
        for i, instance_config in enumerate(self.config.instances):
            logger.info(f"Loading instance {i + 1}/{len(self.config.instances)}: "
                       f"{instance_config.name} ({instance_config.backend})")
            
            backend = create_backend(instance_config)
            backend.load_model()
            backend.warmup()
            
            with self._lock:
                self.backends.append(backend)
            
            logger.info(f"Instance {i + 1} loaded successfully")
        
        self._is_loaded = True
        logger.info(f"ModelPool ready with {len(self.backends)} backend(s)")
    
    def acquire_backend(self) -> Tuple[BaseBackend, int]:
        """
        Acquire a backend for inference using the configured routing strategy.
        
        Returns:
            Tuple of (backend, index) where index can be used for release
            
        Raises:
            RuntimeError: If pool is not loaded
            ValueError: If no backends available
        """
        if not self._is_loaded:
            raise RuntimeError("ModelPool not loaded. Call load_all() first.")
        
        with self._lock:
            if not self.backends:
                raise ValueError("No backends available in pool")
            
            backend = self.router.select_backend(self.backends)
            idx = self.backends.index(backend)
            
            return backend, idx
    
    def release_backend(self, idx: int) -> None:
        """
        Release a previously acquired backend.
        
        Currently a no-op since busy state is tracked in the backend itself.
        Kept for API symmetry and future enhancements.
        
        Args:
            idx: Backend index from acquire_backend
        """
        pass
    
    def infer(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """
        Run inference using an available backend.
        
        Automatically selects backend using routing strategy.
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            InferenceResult with scores and timing
        """
        backend, idx = self.acquire_backend()
        try:
            return backend.infer_with_timing(pairs)
        finally:
            self.release_backend(idx)
    
    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """
        Run inference with timing breakdown.
        
        Alias for infer() - all inference goes through infer_with_timing.
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            InferenceResult with scores and timing breakdown
        """
        return self.infer(pairs)
    
    def get_pool_info(self) -> dict:
        """Get information about the model pool."""
        return {
            "num_instances": len(self.backends),
            "routing_strategy": self.config.routing_strategy,
            "is_loaded": self._is_loaded,
            "instances": [b.get_model_info() for b in self.backends],
            "busy_count": sum(1 for b in self.backends if b.is_busy),
            "total_pending": sum(b.pending_requests for b in self.backends),
        }
    
    def reset_router(self) -> None:
        """Reset the routing strategy state."""
        self.router.reset()
    
    @property
    def is_loaded(self) -> bool:
        """Check if all models are loaded."""
        return self._is_loaded
    
    @property
    def num_backends(self) -> int:
        """Get number of backend instances."""
        return len(self.backends)
    
    def __len__(self) -> int:
        """Get number of backend instances."""
        return len(self.backends)


__all__ = ["ModelPool"]

