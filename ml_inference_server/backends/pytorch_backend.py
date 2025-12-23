"""
PyTorch Backend - Cross-Encoder for Query-Document Scoring.

Uses CrossEncoder from sentence-transformers for relevance scoring.
Optimized with torch.inference_mode and shared utilities.
"""

import time
import torch
import numpy as np
import logging
from sentence_transformers import CrossEncoder
from typing import TYPE_CHECKING

from .base_backend import BaseBackend, InferenceResult
from .device_utils import apply_fp16, sync_device
from .mixins import with_inference_mode

if TYPE_CHECKING:
    from core.config import ModelInstanceConfig

logger = logging.getLogger(__name__)


class PyTorchBackend(BaseBackend):
    """PyTorch cross-encoder backend for query-document scoring."""
    
    QUANTIZATION_MODES = {
        "none": "FP32 (no quantization)",
        "fp16": "FP16 (half precision)",
        "int8": "INT8 (dynamic quantization, CPU only)",
    }
    
    def __init__(
        self, 
        model_name: str, 
        device: str = "mps", 
        quantized: bool = False,
        quantization_mode: str = "fp16"
    ):
        super().__init__(model_name, device)
        self.quantized = quantized
        self.quantization_mode = quantization_mode if quantized else "none"
        self.actual_dtype = None
    
    @classmethod
    def from_config(cls, config: "ModelInstanceConfig") -> "PyTorchBackend":
        """Create PyTorchBackend from configuration."""
        return cls(
            model_name=config.name,
            device=config.device,
            quantized=config.use_fp16,
            quantization_mode="fp16" if config.use_fp16 else "none",
        )
    
    def load_model(self) -> None:
        """Load cross-encoder model."""
        logger.info(f"Loading cross-encoder: {self.model_name}")
        logger.info(f"Target device: {self.device}")
        
        self.model = CrossEncoder(self.model_name, device=self.device)
        self._tokenizer = self.model.tokenizer
        self._max_length = self.model.max_length
        
        if self.quantized:
            self._apply_quantization()
        else:
            self.actual_dtype = "float32"
            logger.info(f"Loaded {self.model_name} on {self.device} (FP32)")
        
        self._is_loaded = True
    
    def _apply_quantization(self) -> None:
        """Apply the specified quantization mode."""
        if self.quantization_mode == "fp16":
            _, self.actual_dtype = apply_fp16(self.model, self.device)
            if self.actual_dtype == "float32":
                self.quantized = False
            else:
                logger.info(f"Loaded {self.model_name} on {self.device} (FP16)")
        else:
            logger.warning(f"Quantization mode {self.quantization_mode} not supported for cross-encoder")
            self.quantized = False
            self.actual_dtype = "float32"
    
    @with_inference_mode
    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        """
        Run cross-encoder inference on query-document pairs.
        Uses torch.inference_mode for better performance.
        """
        self._acquire_for_inference()
        try:
            return self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
        finally:
            self._release_after_inference()
    
    @with_inference_mode
    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """
        Run inference with timing breakdown.
        
        For PyTorchBackend, we use simplified timing (no tokenization breakdown).
        """
        self._acquire_for_inference()
        try:
            total_start = time.perf_counter()
            
            # Tokenization stage
            tokenize_start = time.perf_counter()
            texts = [[pair[0], pair[1]] for pair in pairs]
            features = self._tokenizer(
                texts,
                padding=True,
                truncation='longest_first',
                return_tensors="pt",
                max_length=self._max_length
            )
            
            # Padding analysis
            attention_mask = features['attention_mask']
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
    
    def warmup(self, iterations: int = 5) -> None:
        """Warm up the model with synchronization for accurate timing."""
        logger.info(f"Warming up PyTorch backend ({iterations} iterations)...")
        sample_pairs = [("warmup query", "warmup document")]
        for i in range(iterations):
            self.infer(sample_pairs)
            if (i + 1) % 2 == 0:
                logger.info(f"Warmup progress: {i + 1}/{iterations}")
        
        self.sync_device()
        logger.info(f"Warmup complete ({iterations} iterations)")
    
    def get_model_info(self) -> dict:
        """Return model information."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "quantized": self.quantized,
            "quantization_mode": self.quantization_mode,
            "actual_dtype": self.actual_dtype,
            "backend": "pytorch",
            "model_type": "cross-encoder",
        }
