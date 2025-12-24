"""
Compiled Backend - Cross-Encoder with torch.compile for kernel fusion.

Uses PyTorch 2.0+ torch.compile() for optimized inference with kernel fusion.
This is the Apple Silicon equivalent of TensorRT's kernel fusion.
"""

import logging
import time
from typing import TYPE_CHECKING

import numpy as np
import torch
from sentence_transformers import CrossEncoder

from .base_backend import BaseBackend, InferenceResult
from .device_utils import apply_fp16, clear_memory, sync_device
from .mixins import with_inference_mode

if TYPE_CHECKING:
    from core.config import ModelInstanceConfig

logger = logging.getLogger(__name__)


class CompiledBackend(BaseBackend):
    """Compiled cross-encoder backend with torch.compile kernel fusion."""

    COMPILE_MODES = {
        "default": "Balanced compilation (default)",
        "reduce-overhead": "Minimize CPU overhead",
        "max-autotune": "Maximum optimization with autotuning",
    }

    WARMUP_BATCH_SIZES = [1, 2, 4, 8, 16, 32]

    def __init__(
        self,
        model_name: str,
        device: str = "mps",
        compile_mode: str = "reduce-overhead",
        use_fp16: bool = True,
        dynamic_shapes: bool = True,
    ):
        super().__init__(model_name, device)
        self.compile_mode = compile_mode
        self.use_fp16 = use_fp16 and self.device == "mps"
        self.dynamic_shapes = dynamic_shapes
        self.actual_dtype = None
        self._is_compiled = False
        self._max_length = None

    @classmethod
    def from_config(cls, config: "ModelInstanceConfig") -> "CompiledBackend":
        """Create CompiledBackend from configuration."""
        return cls(
            model_name=config.name,
            device=config.device,
            compile_mode=config.compile_mode,
            use_fp16=config.use_fp16,
        )

    def load_model(self) -> None:
        """Load and compile the cross-encoder model."""
        logger.info(f"Loading cross-encoder: {self.model_name}")
        logger.info(f"Device: {self.device}")
        logger.info(f"Compile mode: {self.compile_mode}")

        clear_memory(self.device)

        self.model = CrossEncoder(self.model_name, device=self.device)
        self._tokenizer = self.model.tokenizer
        self._max_length = self.model.max_length

        if self.use_fp16:
            _, self.actual_dtype = apply_fp16(self.model, self.device)
        else:
            self.actual_dtype = "float32"

        # Compile the model
        logger.info(f"Compiling model with mode='{self.compile_mode}'...")
        try:
            self.model.model = torch.compile(
                self.model.model,
                mode=self.compile_mode,
                backend="inductor",
                fullgraph=False,
                dynamic=self.dynamic_shapes,
            )
            self._is_compiled = True
            logger.info("Model compiled successfully with inductor backend")
        except Exception as e:
            logger.warning(f"torch.compile failed: {e}")
            logger.warning("Falling back to eager execution")
            self._is_compiled = False

        self._is_loaded = True
        logger.info(f"Loaded {self.model_name} on {self.device} ({self.actual_dtype})")

    @with_inference_mode
    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        """Run cross-encoder inference with compiled model."""
        self._acquire_for_inference()
        try:
            return self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
        finally:
            self._release_after_inference()

    @with_inference_mode
    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """Run inference with timing breakdown."""
        self._acquire_for_inference()
        try:
            total_start = time.perf_counter()

            # Tokenization stage
            tokenize_start = time.perf_counter()
            texts = [[pair[0], pair[1]] for pair in pairs]
            features = self._tokenizer(
                texts,
                padding=True,
                truncation="longest_first",
                return_tensors="pt",
                max_length=self._max_length,
            )

            # Padding analysis
            attention_mask = features["attention_mask"]
            batch_size, max_seq_length = attention_mask.shape
            real_tokens_per_seq = attention_mask.sum(dim=1)
            total_real_tokens = int(real_tokens_per_seq.sum().item())
            total_tokens = batch_size * max_seq_length
            padded_tokens = total_tokens - total_real_tokens
            padding_ratio = padded_tokens / total_tokens if total_tokens > 0 else 0.0
            avg_seq_length = float(real_tokens_per_seq.float().mean().item())

            features = {k: v.to(self.device) for k, v in features.items()}
            t_tokenize_ms = (time.perf_counter() - tokenize_start) * 1000

            # Inference stage
            inference_start = time.perf_counter()
            sync_device(self.device)

            model_predictions = self.model.model(**features, return_dict=True)
            logits = model_predictions.logits

            if self.model.config.num_labels == 1:
                scores = torch.sigmoid(logits).squeeze(-1)
            else:
                scores = torch.softmax(logits, dim=-1)[:, 1]

            sync_device(self.device)
            t_model_inference_ms = (time.perf_counter() - inference_start) * 1000

            scores_np = scores.cpu().numpy()
            total_ms = (time.perf_counter() - total_start) * 1000

            return InferenceResult(
                scores=scores_np,
                t_tokenize_ms=t_tokenize_ms,
                t_model_inference_ms=t_model_inference_ms,
                total_ms=total_ms,
                total_tokens=total_tokens,
                real_tokens=total_real_tokens,
                padded_tokens=padded_tokens,
                padding_ratio=padding_ratio,
                max_seq_length=max_seq_length,
                avg_seq_length=avg_seq_length,
                batch_size=batch_size,
            )
        finally:
            self._release_after_inference()

    def warmup(self, iterations: int = 10) -> None:
        """Warm up the compiled model with strategic batch sizes."""
        logger.info(f"Warming up compiled model ({iterations} iterations)...")

        sample_pairs = [("warmup query", "warmup document")]

        # Pre-compile for common batch sizes
        for batch_size in self.WARMUP_BATCH_SIZES:
            batch = sample_pairs * batch_size
            self.infer(batch)
            sync_device(self.device)

        logger.info("Compiled graphs for batch sizes: " + str(self.WARMUP_BATCH_SIZES))

        # Additional warmup iterations
        for i in range(iterations):
            batch = sample_pairs * min(i + 1, 8)
            self.infer(batch)
            if (i + 1) % 5 == 0:
                logger.info(f"Warmup progress: {i + 1}/{iterations}")

        sync_device(self.device)
        clear_memory(self.device)

        logger.info("Warmup complete (model compiled)")

    def get_model_info(self) -> dict:
        """Return model information."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "backend": "compiled",
            "compile_mode": self.compile_mode,
            "actual_dtype": self.actual_dtype,
            "use_fp16": self.use_fp16,
            "dynamic_shapes": self.dynamic_shapes,
            "is_compiled": self._is_compiled,
            "model_type": "cross-encoder",
            "kernel_fusion": self._is_compiled,
        }
