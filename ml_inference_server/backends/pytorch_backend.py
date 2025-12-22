"""
PyTorch Backend - Cross-Encoder for Query-Document Scoring.

Uses CrossEncoder from sentence-transformers for relevance scoring.
Optimized with torch.inference_mode and shared utilities.
"""

import torch
import numpy as np
import logging
from sentence_transformers import CrossEncoder
from .base_backend import BaseBackend, with_inference_mode

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
        # Use shared device resolution
        self.device = self.resolve_device(device)
        self.quantized = quantized
        self.quantization_mode = quantization_mode if quantized else "none"
        self.actual_dtype = None
    
    def load_model(self) -> None:
        """Load cross-encoder model."""
        logger.info(f"Loading cross-encoder: {self.model_name}")
        logger.info(f"Target device: {self.device}")
        
        # Load CrossEncoder
        self.model = CrossEncoder(self.model_name, device=self.device)
        
        if self.quantized:
            self._apply_quantization()
        else:
            self.actual_dtype = "float32"
            logger.info(f"Loaded {self.model_name} on {self.device} (FP32)")
        
        self._is_loaded = True
    
    def _apply_quantization(self) -> None:
        """Apply the specified quantization mode."""
        if self.quantization_mode == "fp16":
            # Use shared FP16 utility
            _, self.actual_dtype = self.apply_fp16(self.model, self.device, logger)
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
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            Array of relevance scores
        """
        # No need for np.array() - predict already returns numpy when convert_to_numpy=True
        return self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
    
    def warmup(self, iterations: int = 5) -> None:
        """Warm up the model with synchronization for accurate timing."""
        sample_pairs = [("warmup query", "warmup document")]
        for i in range(iterations):
            self.infer(sample_pairs)
            if (i + 1) % 2 == 0:
                logger.info(f"Warmup progress: {i + 1}/{iterations}")
        
        # Sync device to ensure all operations complete
        self.sync_device(self.device)
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
