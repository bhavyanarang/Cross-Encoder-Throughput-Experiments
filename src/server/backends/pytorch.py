"""PyTorch CPU/CUDA Backend."""

import logging
import time

import numpy as np
import torch
from sentence_transformers import CrossEncoder

from src.models import InferenceResult
from src.server.backends.base import BaseBackend
from src.server.backends.device import sync_device
from src.server.services.tokenizer import TokenizerService

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
        self._tokenizer: TokenizerService | None = None

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

        self._tokenizer = TokenizerService(self.model_name, self.max_length)
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
    def from_config(cls, config) -> "PyTorchBackend":
        return cls(
            model_name=config.name if hasattr(config, "name") else config["name"],
            device=getattr(config, "device", "cpu"),
            quantization=getattr(config, "quantization", "fp32"),
            max_length=getattr(config, "max_length", 512),
        )
