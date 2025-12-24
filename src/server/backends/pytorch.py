"""PyTorch CPU/CUDA Backend."""

import logging

import numpy as np
from sentence_transformers import CrossEncoder

from src.server.backends.base import BaseBackend

logger = logging.getLogger(__name__)


class PyTorchBackend(BaseBackend):
    def __init__(
        self,
        model_name: str,
        device: str = "cpu",
        quantization: str = "fp32",
        max_length: int = 512,
    ):
        super().__init__(model_name, device, quantization, max_length)

    def load_model(self) -> None:
        logger.info(f"Loading {self.model_name} on {self.device} ({self.quantization})")
        self.model = CrossEncoder(self.model_name, device=self.device)

        if self.quantization == "fp16" and self.device == "cuda":
            self.model.model.half()
            logger.info("Applied FP16")
        elif self.quantization == "int8":
            import torch

            self.model.model = torch.quantization.quantize_dynamic(
                self.model.model, {torch.nn.Linear}, dtype=torch.qint8
            )
            logger.info("Applied INT8 quantization")

        self._is_loaded = True

    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        self._acquire()
        try:
            return self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
        finally:
            self._release()

    @classmethod
    def from_config(cls, config) -> "PyTorchBackend":
        return cls(
            model_name=config.name if hasattr(config, "name") else config["name"],
            device=getattr(config, "device", "cpu"),
            quantization=getattr(config, "quantization", "fp32"),
            max_length=getattr(config, "max_length", 512),
        )
