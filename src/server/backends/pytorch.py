import logging

import torch
from sentence_transformers import CrossEncoder

from src.server.backends.device import apply_fp16
from src.server.backends.torch_base import TorchBackend

logger = logging.getLogger(__name__)


class PyTorchBackend(TorchBackend):
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

        if self.quantization == "fp16":
            applied, msg = apply_fp16(self.model.model, self.device)
            if applied:
                logger.info(f"Applied {msg}")
        elif self.quantization == "int8":
            self.model.model = torch.quantization.quantize_dynamic(
                self.model.model, {torch.nn.Linear}, dtype=torch.qint8
            )
            logger.info("Applied INT8 quantization")

        self._is_loaded = True

    @classmethod
    def from_config(cls, config) -> "PyTorchBackend":
        return cls(
            model_name=config.name if hasattr(config, "name") else config["name"],
            device=getattr(config, "device", "cpu"),
            quantization=getattr(config, "quantization", "fp32"),
            max_length=getattr(config, "max_length", 512),
        )
