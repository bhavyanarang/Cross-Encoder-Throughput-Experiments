"""Compiled Backend using torch.compile for kernel fusion.

Uses PyTorch 2.0+ torch.compile for optimized inference with kernel fusion.
This is the Apple Silicon equivalent of TensorRT optimizations.
"""

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


class CompiledBackend(BaseBackend):
    """Compiled backend using torch.compile for kernel fusion.

    Supports compile modes:
    - "default": Good balance of compile time and runtime performance
    - "reduce-overhead": Reduces framework overhead, faster for small batches
    - "max-autotune": Maximum optimization, longer compile time

    Works on both MPS (Apple Silicon) and CUDA (NVIDIA) devices.
    """

    def __init__(
        self,
        model_name: str,
        device: str = "mps",
        quantization: str = "fp16",
        max_length: int = 512,
        compile_mode: str = "reduce-overhead",
    ):
        super().__init__(model_name, device, quantization, max_length)
        self._tokenizer: TokenizerService | None = None
        self._compile_mode = compile_mode
        self._compiled_model = None

    def load_model(self) -> None:
        logger.info(
            f"Loading {self.model_name} on {self.device} (compiled, mode={self._compile_mode})"
        )

        self.model = CrossEncoder(self.model_name, device=self.device)

        if self.quantization == "fp16":
            if self.device in ("mps", "cuda"):
                self.model.model.half()
                logger.info("Applied FP16")
        elif self.quantization == "int8" and self.device == "cpu":
            self.model.model = torch.quantization.quantize_dynamic(
                self.model.model, {torch.nn.Linear}, dtype=torch.qint8
            )
            logger.info("Applied INT8 dynamic quantization")

        # Compile the model
        try:
            self._compiled_model = torch.compile(
                self.model.model,
                mode=self._compile_mode,
                fullgraph=False,  # Allow graph breaks for compatibility
            )
            logger.info(f"Model compiled with mode={self._compile_mode}")
        except Exception as e:
            logger.warning(f"torch.compile failed: {e}. Using uncompiled model.")
            self._compiled_model = self.model.model

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
                out = self._compiled_model(**batch.features, return_dict=True)
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

    def warmup(self, iterations: int = 5) -> None:
        """Extended warmup for compiled models to trigger compilation."""
        dummy = [("warmup query", "warmup document")]

        # First inference triggers compilation
        logger.info("Triggering torch.compile compilation (first inference)...")
        self.infer(dummy)

        # Additional warmup iterations
        for _ in range(iterations - 1):
            self.infer(dummy)

        logger.info(f"Warmup complete: {iterations} iterations (compiled)")

    @classmethod
    def from_config(cls, config) -> "CompiledBackend":
        # Extract compiled-specific config
        compiled_config = getattr(config, "compiled", {}) or {}
        if isinstance(compiled_config, dict):
            compile_mode = compiled_config.get("mode", "reduce-overhead")
        else:
            compile_mode = getattr(compiled_config, "mode", "reduce-overhead")

        return cls(
            model_name=config.name if hasattr(config, "name") else config["name"],
            device=getattr(config, "device", "mps"),
            quantization=getattr(config, "quantization", "fp16"),
            max_length=getattr(config, "max_length", 512),
            compile_mode=compile_mode,
        )
