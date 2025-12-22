"""
MLX-style Backend - Cross-Encoder for Query-Document Scoring on Apple Silicon.

NOTE: This backend uses PyTorch with MPS, styled after MLX quantization conventions.
For true MLX support, the mlx-lm library would be needed for LLMs.
CrossEncoder models are not natively supported by MLX yet.

Uses CrossEncoder from sentence-transformers with MPS acceleration and
MLX-style quantization bit configuration.
"""

import numpy as np
import logging
import torch
from sentence_transformers import CrossEncoder
from .base_backend import BaseBackend, with_inference_mode

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
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            Array of relevance scores
        """
        # predict already returns numpy, no wrapper needed
        return self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
    
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
