import logging
import time

import numpy as np
import torch
from sentence_transformers import CrossEncoder

from src.server.backends.base import BaseBackend
from src.server.backends.device import sync_device
from src.server.dto import InferenceResult

logger = logging.getLogger(__name__)

MLX_AVAILABLE = True


class MLXBackend(BaseBackend):
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
            self.model.model.half()
            logger.info("Applied FP16")

        self._is_loaded = True

    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        self._acquire()
        try:
            return self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
        finally:
            self._release()

    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        self._acquire()
        try:
            total_start = time.perf_counter()
            batch = self._tokenizer.tokenize(pairs, self.device)

            inf_start = time.perf_counter()
            sync_device(self.device)

            with torch.inference_mode():
                out = self.model.model(**batch.features, return_dict=True)
                logits = out.logits
                if self.model.config.num_labels == 1:
                    scores = torch.sigmoid(logits).squeeze(-1)
                else:
                    scores = torch.softmax(logits, dim=-1)[:, 1]

            sync_device(self.device)
            t_inf = (time.perf_counter() - inf_start) * 1000
            scores_np = scores.cpu().numpy()

            return InferenceResult(
                scores=scores_np,
                t_tokenize_ms=batch.tokenize_time_ms,
                t_model_inference_ms=t_inf,
                total_ms=(time.perf_counter() - total_start) * 1000,
                total_tokens=batch.total_tokens,
                real_tokens=batch.real_tokens,
                padded_tokens=batch.padded_tokens,
                padding_ratio=batch.padding_ratio,
                max_seq_length=batch.max_seq_length,
                avg_seq_length=batch.avg_seq_length,
                batch_size=batch.batch_size,
            )
        finally:
            self._release()

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
