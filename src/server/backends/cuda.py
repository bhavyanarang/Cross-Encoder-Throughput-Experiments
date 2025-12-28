import logging
import time

import numpy as np
import torch
from sentence_transformers import CrossEncoder

from src.server.backends.base import BaseBackend
from src.server.backends.device import sync_device
from src.server.models import InferenceResult
from src.server.services.tokenization_service import TokenizerService

logger = logging.getLogger(__name__)


class CUDABackend(BaseBackend):
    def __init__(
        self,
        model_name: str,
        device: str = "cuda",
        quantization: str = "fp16",
        max_length: int = 512,
        use_amp: bool = True,
    ):
        super().__init__(model_name, device, quantization, max_length)
        self._tokenizer: TokenizerService | None = None
        self._use_amp = use_amp and quantization == "fp16"

    def load_model(self) -> None:
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is not available. Install CUDA-enabled PyTorch.")

        logger.info(f"Loading {self.model_name} on {self.device} ({self.quantization})")

        device_name = torch.cuda.get_device_name(0)
        total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        logger.info(f"CUDA Device: {device_name}, Memory: {total_memory:.1f} GB")

        self.model = CrossEncoder(self.model_name, device=self.device)

        if self.quantization == "fp16":
            self.model.model.half()
            logger.info("Applied FP16")
        elif self.quantization == "int8":
            self.model.model = torch.quantization.quantize_dynamic(
                self.model.model, {torch.nn.Linear}, dtype=torch.qint8
            )
            logger.info("Applied INT8 dynamic quantization")

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
                if self._use_amp:
                    with torch.cuda.amp.autocast():
                        out = self.model.model(**batch.features, return_dict=True)
                else:
                    out = self.model.model(**batch.features, return_dict=True)

                logits = out.logits
                if self.model.config.num_labels == 1:
                    scores = torch.sigmoid(logits).squeeze(-1)
                else:
                    scores = torch.softmax(logits, dim=-1)[:, 1]

            sync_device(self.device)
            t_inf = (time.perf_counter() - inf_start) * 1000
            scores_np = scores.float().cpu().numpy()

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

    def get_gpu_memory_mb(self) -> float:
        if torch.cuda.is_available():
            return torch.cuda.memory_allocated() / (1024 * 1024)
        return 0.0

    @classmethod
    def from_config(cls, config) -> "CUDABackend":
        return cls(
            model_name=config.name if hasattr(config, "name") else config["name"],
            device="cuda",
            quantization=getattr(config, "quantization", "fp16"),
            max_length=getattr(config, "max_length", 512),
        )
