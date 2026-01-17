import logging

from sentence_transformers import CrossEncoder

from src.server.backends.device import apply_fp16
from src.server.backends.torch_base import TorchBackend

logger = logging.getLogger(__name__)

MLX_AVAILABLE = True


class MLXBackend(TorchBackend):
    def __init__(
        self,
        model_name: str,
        device: str = "mps",
        quantization: str = "fp16",
        max_length: int = 512,
        bits: int = 16,
        group_size: int = 64,
    ):
        super().__init__(model_name, "mps", quantization, max_length)
        self._bits = bits
        self._group_size = group_size
        self._use_mlx = MLX_AVAILABLE

    def load_model(self) -> None:
        if self._use_mlx:
            logger.info(f"Loading {self.model_name} with MLX backend (bits={self._bits})")
        else:
            logger.warning("MLX not available, using MPS backend as fallback")
            logger.info(f"Loading {self.model_name} on mps ({self.quantization})")

        self.model = CrossEncoder(self.model_name, device=self.device)

        if self.quantization == "fp16":
            applied, msg = apply_fp16(self.model.model, self.device)
            if applied:
                logger.info(f"Applied {msg}")

        self._is_loaded = True

    @classmethod
    def from_config(cls, config) -> "MLXBackend":
        mlx_config = getattr(config, "mlx", {}) or {}
        if isinstance(mlx_config, dict):
            bits = mlx_config.get("bits", 16)
            group_size = mlx_config.get("group_size", 64)
        else:
            bits = getattr(mlx_config, "bits", 16)
            group_size = getattr(mlx_config, "group_size", 64)

        return cls(
            model_name=config.name if hasattr(config, "name") else config["name"],
            device=getattr(config, "device", "mps"),
            quantization=getattr(config, "quantization", "fp16"),
            max_length=getattr(config, "max_length", 512),
            bits=bits,
            group_size=group_size,
        )
