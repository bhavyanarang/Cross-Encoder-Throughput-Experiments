"""
Device utilities for backend operations.

Extracted from BaseBackend static methods to standalone module functions.
Provides device resolution, synchronization, memory management, and FP16 conversion.
"""

import logging
import threading
from typing import Tuple, Any

logger = logging.getLogger(__name__)

# NOTE: On Apple Silicon, PyTorch MPS uses a shared Metal context.
# Submitting GPU work concurrently from multiple Python threads can be unstable
# for some workloads. We expose a per-device lock so backends can serialize
# GPU sections while still allowing CPU work (e.g., tokenization) to run in parallel.
_DEVICE_LOCKS: dict[str, threading.Lock] = {}
_DEVICE_LOCKS_GUARD = threading.Lock()


def get_device_lock(device: str) -> threading.Lock:
    """
    Get a shared (process-wide) lock for a device.

    Currently most relevant for "mps" where concurrent command buffer submission
    can lead to Metal validation/assertion failures.
    """
    with _DEVICE_LOCKS_GUARD:
        lock = _DEVICE_LOCKS.get(device)
        if lock is None:
            lock = threading.Lock()
            _DEVICE_LOCKS[device] = lock
        return lock


def resolve_device(requested_device: str) -> str:
    """
    Resolve the actual device to use, preferring MPS on Apple Silicon.
    
    Args:
        requested_device: Requested device (mps, cuda, cpu)
        
    Returns:
        Actual available device
    """
    try:
        import torch
        if requested_device == "mps" and torch.backends.mps.is_available():
            return "mps"
        elif requested_device == "cuda" and torch.cuda.is_available():
            return "cuda"
    except ImportError:
        pass
    return "cpu"


def sync_device(device: str) -> None:
    """
    Synchronize GPU operations for accurate timing.
    
    Args:
        device: Device to synchronize (mps, cuda, cpu)
    """
    try:
        import torch
        if device == "mps":
            torch.mps.synchronize()
        elif device == "cuda":
            torch.cuda.synchronize()
    except (ImportError, RuntimeError):
        pass


def clear_memory(device: str) -> None:
    """
    Clear GPU memory cache to reduce fragmentation.
    
    Args:
        device: Device to clear cache for (mps, cuda, cpu)
    """
    try:
        import torch
        if device == "mps":
            torch.mps.empty_cache()
        elif device == "cuda":
            torch.cuda.empty_cache()
    except (ImportError, RuntimeError, AttributeError):
        pass


def apply_fp16(model: Any, device: str) -> Tuple[bool, str]:
    """
    Apply FP16 quantization to a CrossEncoder model.
    
    Args:
        model: CrossEncoder model instance
        device: Target device
        
    Returns:
        Tuple of (success: bool, actual_dtype: str)
    """
    if device != "mps":
        logger.info("FP16 only supported on MPS, using FP32")
        return False, "float32"
    
    try:
        model.model = model.model.half()
        logger.info("Applied FP16 precision")
        return True, "float16"
    except Exception as e:
        logger.warning(f"FP16 conversion failed: {e}, using FP32")
        return False, "float32"


def get_gpu_memory_mb(device: str) -> float:
    """
    Get current GPU memory usage in MB.
    
    Args:
        device: Device to query (mps, cuda)
        
    Returns:
        Memory usage in MB, or 0.0 if unavailable
    """
    try:
        import torch
        if device == "mps" and torch.backends.mps.is_available():
            allocated = torch.mps.current_allocated_memory()
            return allocated / (1024 * 1024)
        elif device == "cuda" and torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated()
            return allocated / (1024 * 1024)
    except Exception:
        pass
    return 0.0


def get_device_info(device: str) -> dict:
    """
    Get information about the specified device.
    
    Args:
        device: Device to query
        
    Returns:
        Dictionary with device information
    """
    info = {"device": device, "available": False}
    
    try:
        import torch
        if device == "mps":
            info["available"] = torch.backends.mps.is_available()
            if info["available"]:
                info["memory_allocated_mb"] = get_gpu_memory_mb(device)
                try:
                    info["driver_memory_mb"] = torch.mps.driver_allocated_memory() / (1024 * 1024)
                except (AttributeError, RuntimeError):
                    pass
        elif device == "cuda":
            info["available"] = torch.cuda.is_available()
            if info["available"]:
                info["device_count"] = torch.cuda.device_count()
                info["device_name"] = torch.cuda.get_device_name(0)
                info["memory_allocated_mb"] = get_gpu_memory_mb(device)
        elif device == "cpu":
            info["available"] = True
    except ImportError:
        pass
    
    return info

