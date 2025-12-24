"""
Core module - Configuration, protocols, and exceptions for the ML inference server.
"""

from .config import (
    BatchingConfig,
    ExperimentConfig,
    ModelInstanceConfig,
    ModelPoolConfig,
    ScreenshotConfig,
    ServerConfig,
)
from .exceptions import (
    BackendError,
    ConfigurationError,
    InferenceError,
    InferenceServerError,
    ModelLoadError,
    RoutingError,
)
from .protocols import InferenceBackend, RoutingStrategy

__all__ = [
    # Config
    "ModelInstanceConfig",
    "ModelPoolConfig",
    "BatchingConfig",
    "ServerConfig",
    "ExperimentConfig",
    "ScreenshotConfig",
    # Protocols
    "InferenceBackend",
    "RoutingStrategy",
    # Exceptions
    "InferenceServerError",
    "BackendError",
    "ModelLoadError",
    "InferenceError",
    "ConfigurationError",
    "RoutingError",
]
