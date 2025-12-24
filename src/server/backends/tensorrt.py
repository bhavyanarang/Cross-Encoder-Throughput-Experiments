"""TensorRT Backend for NVIDIA GPUs."""

import logging

import numpy as np

from src.server.backends.base import BaseBackend

logger = logging.getLogger(__name__)


class TensorRTBackend(BaseBackend):
    """TensorRT backend for optimized CUDA inference.

    TODO: Implement TensorRT optimization pipeline:
    1. Export model to ONNX
    2. Convert ONNX to TensorRT engine
    3. Run inference with TensorRT runtime
    """

    def __init__(
        self,
        model_name: str,
        device: str = "cuda",
        quantization: str = "fp16",
        max_length: int = 512,
    ):
        super().__init__(model_name, device, quantization, max_length)
        self._engine = None

    def load_model(self) -> None:
        raise NotImplementedError(
            "TensorRT backend not yet implemented. Requires: tensorrt, torch2trt or polygraphy"
        )

    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        raise NotImplementedError("TensorRT backend not yet implemented")

    @classmethod
    def from_config(cls, config) -> "TensorRTBackend":
        return cls(
            model_name=config.name if hasattr(config, "name") else config["name"],
            device="cuda",
            quantization=getattr(config, "quantization", "fp16"),
            max_length=getattr(config, "max_length", 512),
        )
