"""
Routing Strategies for Model Pool.

Implements different strategies for selecting which backend instance
should handle an incoming request.
"""

import logging
import threading
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

            logger.debug(
                f"RoundRobin selected backend {self._index % len(backends)}, busy={backend.is_busy}"
            )
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

        logger.debug(
            f"LeastBusy selected backend with {selected.pending_requests} pending requests"
        )
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


class FirstIdleRouter(RoutingStrategy):
    """
    First-idle routing strategy.

    Routes requests to the first idle (not busy) model instance.
    If all instances are busy, routes to the one with fewest pending requests.
    Optimized for maximizing throughput when you have multiple model replicas.
    """

    def select_backend(self, backends: list["BaseBackend"]) -> "BaseBackend":
        """Select the first idle backend, or least busy if all are busy."""
        if not backends:
            raise ValueError("No backends available for routing")

        # First pass: find any idle backend
        for backend in backends:
            if not backend.is_busy:
                logger.debug("FirstIdle: found idle backend")
                return backend

        # All busy - select one with fewest pending requests
        selected = min(backends, key=lambda b: b.pending_requests)
        logger.debug(
            f"FirstIdle: all busy, selecting backend with {selected.pending_requests} pending"
        )
        return selected

    def reset(self) -> None:
        """No state to reset."""
        pass


class SmartIdleRouter(RoutingStrategy):
    """
    Smart idle-based routing with utilization tracking.

    Routes to idle backends first, with fallback to round-robin among busy ones.
    Tracks which backends have been selected to ensure balanced distribution
    when all backends are idle.
    """

    def __init__(self):
        self._last_selected = 0
        self._lock = threading.Lock()

    def select_backend(self, backends: list["BaseBackend"]) -> "BaseBackend":
        """Select backend with smart idle-aware routing."""
        if not backends:
            raise ValueError("No backends available for routing")

        with self._lock:
            n = len(backends)

            # Collect idle backends
            idle_backends = [(i, b) for i, b in enumerate(backends) if not b.is_busy]

            if idle_backends:
                # Round-robin among idle backends starting from last selected
                for offset in range(n):
                    idx = (self._last_selected + offset) % n
                    if not backends[idx].is_busy:
                        self._last_selected = (idx + 1) % n
                        logger.debug(f"SmartIdle: selected idle backend {idx}")
                        return backends[idx]

            # All busy - select least busy
            selected_idx, selected = min(enumerate(backends), key=lambda x: x[1].pending_requests)
            self._last_selected = (selected_idx + 1) % n
            logger.debug(
                f"SmartIdle: all busy, selected backend {selected_idx} with {selected.pending_requests} pending"
            )
            return selected

    def reset(self) -> None:
        """Reset the round-robin index."""
        with self._lock:
            self._last_selected = 0


def create_router(strategy_name: str) -> RoutingStrategy:
    """
    Factory function to create a routing strategy.

    Args:
        strategy_name: Name of the strategy:
            - "round_robin": Distribute evenly across backends
            - "least_busy": Route to backend with fewest pending requests
            - "first_available": Route to first non-busy backend
            - "first_idle": Route to first idle backend (optimized for replicas)
            - "smart_idle": Smart idle-aware routing with balanced distribution

    Returns:
        RoutingStrategy instance

    Raises:
        ValueError: If strategy name is unknown
    """
    strategies = {
        "round_robin": RoundRobinRouter,
        "least_busy": LeastBusyRouter,
        "first_available": FirstAvailableRouter,
        "first_idle": FirstIdleRouter,
        "smart_idle": SmartIdleRouter,
    }

    if strategy_name not in strategies:
        raise ValueError(
            f"Unknown routing strategy: {strategy_name}. Available: {list(strategies.keys())}"
        )

    return strategies[strategy_name]()


__all__ = [
    "RoutingStrategy",
    "RoundRobinRouter",
    "LeastBusyRouter",
    "FirstAvailableRouter",
    "FirstIdleRouter",
    "SmartIdleRouter",
    "create_router",
]
