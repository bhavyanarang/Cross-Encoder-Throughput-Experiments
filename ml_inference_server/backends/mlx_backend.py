"""
MLX-style Backend - Cross-Encoder for Query-Document Scoring on Apple Silicon.

NOTE: This backend uses PyTorch with MPS, styled after MLX quantization conventions.
For true MLX support, the mlx-lm library would be needed for LLMs.
CrossEncoder models are not natively supported by MLX yet.

Uses CrossEncoder from sentence-transformers with MPS acceleration and
MLX-style quantization bit configuration.
Includes per-stage timing for tokenization vs model inference.
"""

import time
import threading
import numpy as np
import logging
import torch
from sentence_transformers import CrossEncoder
from .base_backend import BaseBackend, InferenceResult, with_inference_mode

logger = logging.getLogger(__name__)


class MLXBackend(BaseBackend):
    """
    MLX-style cross-encoder backend for query-document scoring.
    
    Uses PyTorch/MPS under the hood with MLX-style quantization config.
    The quantization_bits parameter maps to precision:
    - 32 bits -> FP32
    - 16 bits -> FP16
    - 8/4 bits -> FP16 (true INT8/INT4 requires specialized libraries)
    """
    
    SUPPORTED_BITS = [4, 8, 16, 32]
    
    def __init__(
        self, 
        model_name: str, 
        device: str = "mps",
        quantization_bits: int = 16,
        group_size: int = 64  # Preserved for future MLX compatibility
    ):
        super().__init__(model_name, device)
        self.quantization_bits = quantization_bits
        self.group_size = group_size
        self.model = None
        self.actual_dtype = None
        self._tokenizer = None
        self._max_length = None
        
        # Thread lock for serializing inference calls (MPS is NOT thread-safe)
        self._inference_lock = threading.Lock()
        
        # Use shared device resolution
        self.device = self.resolve_device(device)
        
        # Log if using fallback mode
        if quantization_bits < 16:
            logger.warning(
                f"INT{quantization_bits} quantization requested but not available for CrossEncoder. "
                "Using FP16 instead. For true low-bit quantization, use dedicated MLX models."
            )
        
    def load_model(self) -> None:
        """Load cross-encoder model with MLX-style configuration."""
        logger.info(f"Loading cross-encoder: {self.model_name}")
        logger.info(f"Device: {self.device}")
        logger.info(f"Requested precision: {self.quantization_bits} bits")
        
        # Clear memory before loading
        self.clear_memory(self.device)
        
        # Load CrossEncoder
        self.model = CrossEncoder(self.model_name, device=self.device)
        
        # Cache tokenizer reference for timing measurements
        self._tokenizer = self.model.tokenizer
        self._max_length = self.model.max_length
        
        # Apply FP16 for any bits <= 16 on MPS
        if self.quantization_bits <= 16 and self.device == "mps":
            _, self.actual_dtype = self.apply_fp16(self.model, self.device, logger)
        else:
            self.actual_dtype = "float32"
        
        logger.info(f"Loaded {self.model_name} on {self.device} ({self.actual_dtype.upper()})")
        self._is_loaded = True
    
    @with_inference_mode
    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        """
        Run cross-encoder inference on query-document pairs.
        Uses torch.inference_mode for better performance.
        Thread-safe: uses lock to serialize MPS operations.
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            Array of relevance scores
        """
        with self._inference_lock:
            # predict already returns numpy, no wrapper needed
            return self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
    
    @with_inference_mode
    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """
        Run inference with separate timing for tokenization and model forward pass.
        
        This method manually performs tokenization and model inference to 
        get accurate timing breakdown for bottleneck analysis.
        Thread-safe: uses lock to serialize MPS operations.
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            InferenceResult with scores and timing breakdown
        """
        with self._inference_lock:
            total_start = time.perf_counter()
            
            # Stage 1: Tokenization
            tokenize_start = time.perf_counter()
            
            # Use batch tokenization for better performance
            texts = [[pair[0], pair[1]] for pair in pairs]
            features = self._tokenizer(
                texts,
                padding=True,
                truncation='longest_first',
                return_tensors="pt",
                max_length=self._max_length
            )
            
            # Move to device
            features = {k: v.to(self.device) for k, v in features.items()}
            
            t_tokenize_ms = (time.perf_counter() - tokenize_start) * 1000
            
            # Stage 2: Model inference
            inference_start = time.perf_counter()
            
            # Sync before inference for accurate timing
            self.sync_device(self.device)
            
            # Forward pass
            model_predictions = self.model.model(**features, return_dict=True)
            logits = model_predictions.logits
            
            # Apply activation function based on model config
            if self.model.config.num_labels == 1:
                scores = torch.sigmoid(logits).squeeze(-1)
            else:
                scores = torch.softmax(logits, dim=-1)[:, 1]
            
            # Sync after inference for accurate timing
            self.sync_device(self.device)
            
            t_model_inference_ms = (time.perf_counter() - inference_start) * 1000
            
            # Convert to numpy
            scores_np = scores.cpu().numpy()
            
            total_ms = (time.perf_counter() - total_start) * 1000
            
            return InferenceResult(
                scores=scores_np,
                t_tokenize_ms=t_tokenize_ms,
                t_model_inference_ms=t_model_inference_ms,
                total_ms=total_ms
            )
    
    def warmup(self, iterations: int = 10) -> None:
        """Warm up the model with proper synchronization."""
        logger.info(f"Warming up MLX backend ({iterations} iterations)...")
        sample_pairs = [("warmup query", "warmup document")]
        
        for i in range(iterations):
            self.infer(sample_pairs)
            if (i + 1) % 5 == 0:
                self.sync_device(self.device)
        
        # Final sync and cleanup
        self.sync_device(self.device)
        self.clear_memory(self.device)
        logger.info("Warmup complete")
    
    def get_model_info(self) -> dict:
        """Return model information."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "backend": "mlx",
            "quantization_bits": self.quantization_bits,
            "actual_dtype": self.actual_dtype,
            "group_size": self.group_size,
            "model_type": "cross-encoder",
            "note": "Uses PyTorch/MPS with MLX-style config",
        }
