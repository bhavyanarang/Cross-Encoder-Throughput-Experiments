from .base_backend import BaseBackend, with_inference_mode
from .pytorch_backend import PyTorchBackend
from .onnx_backend import ONNXBackend
from .mlx_backend import MLXBackend
from .mps_backend import MPSBackend
from .compiled_backend import CompiledBackend


def create_backend(config: dict) -> BaseBackend:
    """Factory function to create the appropriate backend based on config."""
    backend_type = config.get("model", {}).get("backend", "pytorch")
    model_name = config["model"]["name"]
    device = config["model"].get("device", "mps")
    
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
        # torch.compile backend with kernel fusion (Apple Silicon TensorRT equivalent)
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
    "BaseBackend", 
    "PyTorchBackend", 
    "ONNXBackend", 
    "MLXBackend", 
    "MPSBackend", 
    "CompiledBackend", 
    "create_backend",
    "with_inference_mode",
]

