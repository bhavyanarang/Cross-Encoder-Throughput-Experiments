"""
Backends module - Model inference backend implementations.

Provides a registry of backend implementations and a factory function
to create backends from configuration.
"""

from typing import Type, Dict, TYPE_CHECKING

from .base_backend import BaseBackend, InferenceResult
from .mixins import with_inference_mode, TimedInferenceMixin, ThreadSafeInferenceMixin
from .device_utils import resolve_device, sync_device, clear_memory, apply_fp16

if TYPE_CHECKING:
    from core.config import ModelInstanceConfig

# Backend registry
_BACKEND_REGISTRY: Dict[str, Type[BaseBackend]] = {}


def register_backend(name: str):
    """
    Decorator to register a backend class.
    
    Usage:
        @register_backend("mps")
        class MPSBackend(BaseBackend):
            ...
    """
    def decorator(cls: Type[BaseBackend]) -> Type[BaseBackend]:
        _BACKEND_REGISTRY[name] = cls
        return cls
    return decorator


def get_registered_backends() -> list[str]:
    """Get list of registered backend names."""
    return list(_BACKEND_REGISTRY.keys())


# Import and register backends
from .pytorch_backend import PyTorchBackend
from .onnx_backend import ONNXBackend
from .mlx_backend import MLXBackend
from .mps_backend import MPSBackend
from .compiled_backend import CompiledBackend

# Register backends
_BACKEND_REGISTRY["pytorch"] = PyTorchBackend
_BACKEND_REGISTRY["onnx"] = ONNXBackend
_BACKEND_REGISTRY["mlx"] = MLXBackend
_BACKEND_REGISTRY["mps"] = MPSBackend
_BACKEND_REGISTRY["compiled"] = CompiledBackend


def create_backend(config) -> BaseBackend:
    """
    Factory function to create the appropriate backend based on config.
    
    Supports both new ModelInstanceConfig and legacy dict config format.
    
    Args:
        config: ModelInstanceConfig or dict with configuration
        
    Returns:
        Configured backend instance
        
    Raises:
        ValueError: If backend type is unknown
    """
    # Handle dict config (legacy format)
    if isinstance(config, dict):
        return _create_backend_from_dict(config)
    
    # Handle ModelInstanceConfig (new format)
    backend_type = config.backend
    if backend_type not in _BACKEND_REGISTRY:
        raise ValueError(f"Unknown backend: {backend_type}. Available: {list(_BACKEND_REGISTRY.keys())}")
    
    backend_cls = _BACKEND_REGISTRY[backend_type]
    return backend_cls.from_config(config)


def _create_backend_from_dict(config: dict) -> BaseBackend:
    """
    Create backend from legacy dict config format.
    
    Maintains backward compatibility with existing config files.
    """
    backend_type = config.get("model", {}).get("backend", "pytorch")
    model_name = config["model"]["name"]
    device = config["model"].get("device", "mps")
    
    if backend_type not in _BACKEND_REGISTRY:
        raise ValueError(f"Unknown backend: {backend_type}. Available: {list(_BACKEND_REGISTRY.keys())}")
    
    if backend_type == "onnx":
        onnx_config = config.get("model", {}).get("onnx", {})
        return ONNXBackend(
            model_name=model_name,
            device=device,
            optimize=onnx_config.get("optimize", True),
            use_coreml=onnx_config.get("use_gpu", True),
        )
    elif backend_type == "mlx":
        mlx_config = config.get("model", {}).get("mlx", {})
        return MLXBackend(
            model_name=model_name,
            device=device,
            quantization_bits=mlx_config.get("bits", 16),
            group_size=mlx_config.get("group_size", 64),
        )
    elif backend_type == "mps":
        mps_config = config.get("model", {}).get("mps", {})
        return MPSBackend(
            model_name=model_name,
            device=device,
            use_fp16=mps_config.get("fp16", True),
            compile_model=mps_config.get("compile", False),
        )
    elif backend_type == "compiled":
        compiled_config = config.get("model", {}).get("compiled", {})
        return CompiledBackend(
            model_name=model_name,
            device=device,
            compile_mode=compiled_config.get("mode", "reduce-overhead"),
            use_fp16=compiled_config.get("fp16", True),
        )
    else:
        # Default to PyTorch backend
        quantized = config["model"].get("quantized", False)
        quantization_mode = config["model"].get("quantization_mode", "fp16")
        return PyTorchBackend(
            model_name=model_name,
            device=device,
            quantized=quantized,
            quantization_mode=quantization_mode,
        )


__all__ = [
    # Base classes
    "BaseBackend",
    "InferenceResult",
    # Backend implementations
    "PyTorchBackend",
    "ONNXBackend",
    "MLXBackend",
    "MPSBackend",
    "CompiledBackend",
    # Factory and registry
    "create_backend",
    "register_backend",
    "get_registered_backends",
    # Mixins and utilities
    "with_inference_mode",
    "TimedInferenceMixin",
    "ThreadSafeInferenceMixin",
    # Device utilities
    "resolve_device",
    "sync_device",
    "clear_memory",
    "apply_fp16",
]
