"""
MPS Backend - Cross-Encoder for Query-Document Scoring on Apple Silicon GPU.

Uses CrossEncoder from sentence-transformers with MPS acceleration.
Optimized with inference_mode, memory management, and proper synchronization.
Includes per-stage timing for tokenization vs model inference.
"""

import logging
import time
from typing import TYPE_CHECKING

import numpy as np
import torch
from sentence_transformers import CrossEncoder

from .base_backend import BaseBackend, InferenceResult
from .device_utils import apply_fp16, get_device_lock, sync_device
from .mixins import with_inference_mode

if TYPE_CHECKING:
    from core.config import ModelInstanceConfig

logger = logging.getLogger(__name__)


class MPSBackend(BaseBackend):
    """MPS cross-encoder backend for query-document scoring."""

    def __init__(
        self,
        model_name: str,
        device: str = "mps",
        use_fp16: bool = True,
        compile_model: bool = False,
        compile_mode: str = "reduce-overhead",
        sync_on_infer: bool = False,
        max_length: int | None = None,
    ):
        super().__init__(model_name, device)
        self.use_fp16 = use_fp16
        self.compile_model = compile_model
        self.compile_mode = compile_mode
        self.sync_on_infer = sync_on_infer
        self.actual_dtype = None
        self._max_length = max_length  # Will be set from config or model default in load_model
        # Global lock for GPU submission on this device (important for MPS stability).
        # This is shared across *all* MPSBackend instances in-process.
        self._device_lock = get_device_lock(self.device)

    @classmethod
    def from_config(cls, config: "ModelInstanceConfig") -> "MPSBackend":
        """Create MPSBackend from configuration."""
        return cls(
            model_name=config.name,
            device=config.device,
            use_fp16=config.use_fp16,
            compile_model=config.compile_model,
            compile_mode=getattr(config, "compile_mode", "reduce-overhead"),
            max_length=config.max_length,
        )

    def load_model(self) -> None:
        """Load cross-encoder model with MPS optimizations."""
        logger.info(f"Loading cross-encoder: {self.model_name}")
        logger.info(f"Device: {self.device}")
        logger.info(f"Precision: {'FP16' if self.use_fp16 else 'FP32'}")

        # Clear any existing memory before loading
        self.clear_memory()

        # Load CrossEncoder
        self.model = CrossEncoder(self.model_name, device=self.device)

        # Cache tokenizer reference for timing measurements
        self._tokenizer = self.model.tokenizer
        # Use configured max_length if provided, otherwise use model default
        if self._max_length is None:
            self._max_length = self.model.max_length
        else:
            logger.info(
                f"Using configured max_length: {self._max_length} (model default: {self.model.max_length})"
            )

        # Apply FP16 using utility
        if self.use_fp16 and self.device == "mps":
            _, self.actual_dtype = apply_fp16(self.model, self.device)
            logger.info(f"Loaded {self.model_name} on {self.device} ({self.actual_dtype.upper()})")
        else:
            self.actual_dtype = "float32"
            logger.info(f"Loaded {self.model_name} on {self.device} (FP32)")

        # Apply torch.compile if requested
        if self.compile_model:
            try:
                # Use aot_eager backend for MPS as inductor support is still experimental/limited
                backend = "aot_eager" if self.device == "mps" else "inductor"
                logger.info(
                    f"Compiling model with mode='{self.compile_mode}' backend='{backend}'..."
                )
                self.model.model = torch.compile(
                    self.model.model, mode=self.compile_mode, backend=backend
                )
                logger.info("Model compilation enabled")
            except Exception as e:
                logger.warning(f"Model compilation failed: {e}")

        self._is_loaded = True

    @with_inference_mode
    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        """
        Run cross-encoder inference on query-document pairs.
        Uses torch.inference_mode for better performance.
        Thread-safe: per-instance lock + global per-device lock for MPS GPU work.
        """
        self._acquire_for_inference()
        try:
            # CrossEncoder.predict performs both tokenization and forward pass.
            # To avoid Metal command buffer issues under concurrent load, serialize
            # the whole call on MPS.
            with self._device_lock:
                scores = self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)

            if self.sync_on_infer:
                with self._device_lock:
                    self.sync_device()

            return scores
        finally:
            self._release_after_inference()

    @with_inference_mode
    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """
        Run inference with separate timing for tokenization and model forward pass.
        Thread-safe: per-instance lock + global per-device lock for MPS GPU work.
        """
        self._acquire_for_inference()
        try:
            total_start = time.perf_counter()

            # Stage 1: Tokenization
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

            t_tokenize_ms = (time.perf_counter() - tokenize_start) * 1000

            # Stage 2: Model inference
            inference_start = time.perf_counter()

            # Important: serialize the GPU section (H2D copies + forward + D2H copy)
            # across all MPS backends to avoid Metal command buffer assertion failures.
            with self._device_lock:
                features = {k: v.to(self.device) for k, v in features.items()}

                sync_device(self.device)

                model_predictions = self.model.model(**features, return_dict=True)
                logits = model_predictions.logits

                if self.model.config.num_labels == 1:
                    scores = torch.sigmoid(logits).squeeze(-1)
                else:
                    scores = torch.softmax(logits, dim=-1)[:, 1]

                sync_device(self.device)
                scores_np = scores.cpu().numpy()

            t_model_inference_ms = (time.perf_counter() - inference_start) * 1000

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
        """Warm up the model with proper synchronization."""
        logger.info(f"Warming up MPS backend ({iterations} iterations)...")
        sample_pairs = [("warmup query", "warmup document")]

        for i in range(iterations):
            self.infer(sample_pairs)
            if (i + 1) % 5 == 0:
                self.sync_device()

        self.sync_device()
        self.clear_memory()
        logger.info("Warmup complete")

    def get_model_info(self) -> dict:
        """Return model information including memory stats."""
        info = {
            "model_name": self.model_name,
            "device": self.device,
            "backend": "mps",
            "use_fp16": self.use_fp16,
            "actual_dtype": self.actual_dtype,
            "model_type": "cross-encoder",
            "sync_on_infer": self.sync_on_infer,
        }

        if self.device == "mps" and torch.backends.mps.is_available():
            try:
                info["mps_memory_allocated"] = torch.mps.current_allocated_memory()
                info["mps_driver_memory"] = torch.mps.driver_allocated_memory()
            except (AttributeError, RuntimeError):
                pass

        return info
