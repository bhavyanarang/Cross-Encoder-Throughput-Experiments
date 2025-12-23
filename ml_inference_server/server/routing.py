"""
Routing Strategies for Model Pool.

Implements different strategies for selecting which backend instance
should handle an incoming request.
"""

import threading
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backends import BaseBackend

logger = logging.getLogger(__name__)


class RoutingStrategy(ABC):
    """Abstract base class for routing strategies."""
    
    @abstractmethod
    def select_backend(self, backends: list["BaseBackend"]) -> "BaseBackend":
        """
        Select the next backend to handle a request.
        
        Args:
            backends: List of available backend instances
            
        Returns:
            Selected backend instance
            
        Raises:
            ValueError: If no backends available
        """
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """Reset routing state (e.g., counters, indices)."""
        pass


class RoundRobinRouter(RoutingStrategy):
    """
    Round-robin routing strategy.
    
    Distributes requests evenly across all backends in a circular fashion.
    Prefers non-busy backends when available.
    """
    
    def __init__(self):
        self._index = 0
        self._lock = threading.Lock()
    
    def select_backend(self, backends: list["BaseBackend"]) -> "BaseBackend":
        """Select next backend using round-robin, preferring non-busy ones."""
        if not backends:
            raise ValueError("No backends available for routing")
        
        with self._lock:
            # Try to find a non-busy backend
            available = [b for b in backends if not b.is_busy]
            
            if available:
                # Round-robin among available backends
                backend = available[self._index % len(available)]
            else:
                # All busy - round-robin among all backends
                backend = backends[self._index % len(backends)]
            
            self._index += 1
            
            logger.debug(f"RoundRobin selected backend {self._index % len(backends)}, busy={backend.is_busy}")
            return backend
    
    def reset(self) -> None:
        """Reset the round-robin index."""
        with self._lock:
            self._index = 0


class LeastBusyRouter(RoutingStrategy):
    """
    Least-busy routing strategy.
    
    Routes requests to the backend with the fewest pending requests.
    Falls back to first backend if all have equal load.
    """
    
    def select_backend(self, backends: list["BaseBackend"]) -> "BaseBackend":
        """Select the backend with fewest pending requests."""
        if not backends:
            raise ValueError("No backends available for routing")
        
        # Find backend with minimum pending requests
        selected = min(backends, key=lambda b: b.pending_requests)
        
        logger.debug(f"LeastBusy selected backend with {selected.pending_requests} pending requests")
        return selected
    
    def reset(self) -> None:
        """No state to reset for least-busy routing."""
        pass


class FirstAvailableRouter(RoutingStrategy):
    """
    First-available routing strategy.
    
    Routes to the first non-busy backend, or first backend if all busy.
    Simple strategy that minimizes latency when load is low.
    """
    
    def select_backend(self, backends: list["BaseBackend"]) -> "BaseBackend":
        """Select the first non-busy backend."""
        if not backends:
            raise ValueError("No backends available for routing")
        
        for backend in backends:
            if not backend.is_busy:
                return backend
        
        # All busy - return first one
        return backends[0]
    
    def reset(self) -> None:
        """No state to reset."""
        pass


def create_router(strategy_name: str) -> RoutingStrategy:
    """
    Factory function to create a routing strategy.
    
    Args:
        strategy_name: Name of the strategy ("round_robin", "least_busy", "first_available")
        
    Returns:
        RoutingStrategy instance
        
    Raises:
        ValueError: If strategy name is unknown
    """
    strategies = {
        "round_robin": RoundRobinRouter,
        "least_busy": LeastBusyRouter,
        "first_available": FirstAvailableRouter,
    }
    
    if strategy_name not in strategies:
        raise ValueError(f"Unknown routing strategy: {strategy_name}. Available: {list(strategies.keys())}")
    
    return strategies[strategy_name]()


__all__ = [
    "RoutingStrategy",
    "RoundRobinRouter",
    "LeastBusyRouter",
    "FirstAvailableRouter",
    "create_router",
]

