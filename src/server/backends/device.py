"""Device utilities for GPU/accelerator management."""

import logging

import torch

logger = logging.getLogger(__name__)


def resolve_device(device: str) -> str:
    """Resolve device string to available device.

    Args:
        device: Requested device ("mps", "cuda", "cpu", or "cuda:N")

    Returns:
        Resolved device string that is available on the system.
    """
    if device == "mps":
        if torch.backends.mps.is_available():
            return "mps"
        logger.warning("MPS not available, falling back to CPU")
        return "cpu"

    if device == "cuda" or device.startswith("cuda:"):
        if torch.cuda.is_available():
            return device
        logger.warning("CUDA not available, falling back to CPU")
        return "cpu"

    return "cpu"


def sync_device(device: str) -> None:
    """Synchronize device for accurate timing."""
    if device == "mps":
        torch.mps.synchronize()
    elif device == "cuda" or device.startswith("cuda:"):
        torch.cuda.synchronize()


def clear_memory(device: str) -> None:
    """Clear device memory cache."""
    if device == "mps":
        torch.mps.empty_cache()
    elif device == "cuda" or device.startswith("cuda:"):
        torch.cuda.empty_cache()


def get_gpu_memory_mb(device: str) -> float:
    """Get current GPU memory usage in MB."""
    if device == "mps":
        try:
            return torch.mps.current_allocated_memory() / (1024 * 1024)
        except Exception:
            return 0.0
    elif device == "cuda" or device.startswith("cuda:"):
        try:
            return torch.cuda.memory_allocated() / (1024 * 1024)
        except Exception:
            return 0.0
    return 0.0


def get_device_info(device: str) -> dict:
    """Get device information."""
    info = {"device": device, "type": "cpu", "name": "CPU"}

    if device == "mps":
        info["type"] = "mps"
        info["name"] = "Apple Silicon GPU"
        info["available"] = torch.backends.mps.is_available()
    elif device == "cuda" or device.startswith("cuda:"):
        info["type"] = "cuda"
        if torch.cuda.is_available():
            device_idx = 0
            if ":" in device:
                device_idx = int(device.split(":")[1])
            info["name"] = torch.cuda.get_device_name(device_idx)
            props = torch.cuda.get_device_properties(device_idx)
            info["total_memory_gb"] = props.total_memory / (1024**3)
            info["available"] = True
        else:
            info["available"] = False
    else:
        info["available"] = True

    return info


def apply_fp16(model, device: str) -> tuple[bool, str]:
    """Apply FP16 to model if device supports it."""
    if device == "cuda" or device.startswith("cuda:"):
        model.half()
        return True, "FP16 (CUDA)"
    if device == "mps":
        model.half()
        return True, "FP16 (MPS)"
    return False, "FP32 (CPU)"
