"""Backend implementations for model inference."""

from .base import BaseBackend
from .mps import MPSBackend
from .pytorch import PyTorchBackend

BACKENDS = {
    "pytorch": PyTorchBackend,
    "mps": MPSBackend,
}


def create_backend(config) -> BaseBackend:
    """Create backend from config."""
    backend_type = config.backend if hasattr(config, "backend") else config.get("backend", "mps")
    if backend_type not in BACKENDS:
        raise ValueError(f"Unknown backend: {backend_type}. Available: {list(BACKENDS.keys())}")
    return BACKENDS[backend_type].from_config(config)


__all__ = ["BaseBackend", "MPSBackend", "PyTorchBackend", "create_backend", "BACKENDS"]
