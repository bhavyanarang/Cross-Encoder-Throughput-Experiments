import logging

from .base import BaseBackend
from .compiled import CompiledBackend
from .cuda import CUDABackend
from .mlx_backend import MLXBackend
from .mps import MPSBackend
from .pytorch import PyTorchBackend
from .tensorrt import TensorRTBackend

logger = logging.getLogger(__name__)

BACKENDS = {
    "pytorch": PyTorchBackend,
    "mps": MPSBackend,
    "cuda": CUDABackend,
    "mlx": MLXBackend,
    "compiled": CompiledBackend,
    "tensorrt": TensorRTBackend,
}


def create_backend(config) -> BaseBackend:
    backend_type = config.backend if hasattr(config, "backend") else config.get("backend", "mps")

    if backend_type not in BACKENDS:
        available = list(BACKENDS.keys())
        raise ValueError(f"Unknown backend: {backend_type}. Available: {available}")

    return BACKENDS[backend_type].from_config(config)


__all__ = [
    "BaseBackend",
    "PyTorchBackend",
    "MPSBackend",
    "CUDABackend",
    "MLXBackend",
    "CompiledBackend",
    "TensorRTBackend",
    "create_backend",
    "BACKENDS",
]
