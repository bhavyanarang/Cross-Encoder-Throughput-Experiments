"""Device utilities for GPU/accelerator management."""

import logging

import torch

logger = logging.getLogger(__name__)


def resolve_device(device: str) -> str:
    """Resolve device string to available device."""
    if device == "mps":
        if torch.backends.mps.is_available():
            return "mps"
        logger.warning("MPS not available, falling back to CPU")
        return "cpu"
    if device == "cuda":
        if torch.cuda.is_available():
            return "cuda"
        logger.warning("CUDA not available, falling back to CPU")
        return "cpu"
    return "cpu"


def sync_device(device: str) -> None:
    """Synchronize device for accurate timing."""
    if device == "mps":
        torch.mps.synchronize()
    elif device == "cuda":
        torch.cuda.synchronize()


def clear_memory(device: str) -> None:
    """Clear device memory cache."""
    if device == "mps":
        torch.mps.empty_cache()
    elif device == "cuda":
        torch.cuda.empty_cache()


def apply_fp16(model, device: str) -> tuple[bool, str]:
    """Apply FP16 to model if device supports it."""
    if device == "cuda":
        model.half()
        return True, "FP16 (CUDA)"
    if device == "mps":
        model.half()
        return True, "FP16 (MPS)"
    return False, "FP32 (CPU)"
