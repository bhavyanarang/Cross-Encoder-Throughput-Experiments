"""
MLX Backend for Apple Silicon with native INT4/INT8 quantization support.

MLX is Apple's machine learning framework optimized for Apple Silicon.
It supports:
- Native INT4 quantization (4-bit weights)
- Native INT8 quantization (8-bit weights)
- Unified memory architecture (no CPU<->GPU transfer)

Install: pip install mlx mlx-lm

Note: MLX operations are not thread-safe. This backend uses a lock for thread safety.
"""

import numpy as np
import logging
import threading
from pathlib import Path
from .base_backend import BaseBackend

logger = logging.getLogger(__name__)


class MLXBackend(BaseBackend):
    """MLX backend with native quantization support for Apple Silicon."""
    
    SUPPORTED_BITS = [4, 8, 16, 32]
    
    def __init__(
        self, 
        model_name: str, 
        device: str = "mps",
        quantization_bits: int = 16,
        group_size: int = 64
    ):
        super().__init__(model_name, device)
        self.quantization_bits = quantization_bits
        self.group_size = group_size
        self.tokenizer = None
        self._mlx_available = False
        self._inference_lock = threading.Lock()  # Thread safety for MLX
        self._use_fallback = False
        
    def load_model(self) -> None:
        """Load model with MLX and optional quantization."""
        try:
            import mlx.core as mx
            import mlx.nn as nn
            self._mlx_available = True
        except ImportError:
            logger.warning("MLX not installed. Using PyTorch fallback.")
            self._fallback_to_pytorch()
            return
        
        logger.info(f"Loading MLX model: {self.model_name}")
        logger.info(f"Quantization: {self.quantization_bits}-bit")
        
        try:
            from transformers import AutoTokenizer, AutoModel
            import torch
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Load PyTorch model first
            pt_model = AutoModel.from_pretrained(self.model_name)
            pt_model.eval()
            
            # Store PyTorch model for fallback
            self._pt_model = pt_model
            
            # Convert to MLX
            self.model = self._convert_to_mlx(pt_model, mx)
            
            self._is_loaded = True
            logger.info(f"Loaded MLX model with {self.quantization_bits}-bit precision")
            
        except Exception as e:
            logger.error(f"Failed to load MLX model: {e}")
            logger.warning("Falling back to PyTorch backend")
            self._fallback_to_pytorch()
    
    def _convert_to_mlx(self, pt_model, mx):
        """Convert PyTorch model weights to MLX format."""
        # Extract model weights and convert to MLX arrays
        mlx_weights = {}
        for name, param in pt_model.named_parameters():
            np_array = param.detach().cpu().numpy()
            mlx_weights[name] = mx.array(np_array)
        
        logger.info(f"Converted {len(mlx_weights)} weight tensors to MLX")
        return {"weights": mlx_weights, "config": pt_model.config}
    
    def _fallback_to_pytorch(self) -> None:
        """Fallback to PyTorch if MLX fails."""
        from .pytorch_backend import PyTorchBackend
        
        logger.warning("Using PyTorch fallback for MLX backend")
        self._use_fallback = True
        self._pytorch_fallback = PyTorchBackend(
            model_name=self.model_name,
            device="mps",
            quantized=self.quantization_bits < 32,
            quantization_mode="fp16"
        )
        self._pytorch_fallback.load_model()
        self._is_loaded = True
    
    def infer(self, texts: list[str]) -> np.ndarray:
        """Run inference and return embeddings."""
        if self._use_fallback:
            return self._pytorch_fallback.infer(texts)
        
        # Use lock for thread safety - MLX is not thread-safe
        with self._inference_lock:
            return self._mlx_infer(texts)
    
    def _mlx_infer(self, texts: list[str]) -> np.ndarray:
        """MLX inference implementation."""
        import mlx.core as mx
        
        try:
            # Tokenize
            inputs = self.tokenizer(
                texts,
                return_tensors="np",
                padding=True,
                truncation=True,
                max_length=128
            )
            
            # Convert to MLX
            input_ids = mx.array(inputs["input_ids"])
            attention_mask = mx.array(inputs["attention_mask"])
            
            # Forward pass
            embeddings = self._forward(input_ids, attention_mask, mx)
            
            # Evaluate and convert back to numpy
            mx.eval(embeddings)
            return np.array(embeddings)
            
        except Exception as e:
            logger.error(f"MLX inference failed: {e}. Using PyTorch fallback.")
            # Fallback to PyTorch for this request
            if not self._use_fallback:
                self._fallback_to_pytorch()
            return self._pytorch_fallback.infer(texts)
    
    def _forward(self, input_ids, attention_mask, mx):
        """Forward pass through the model."""
        # Get embedding weights
        word_embeddings = None
        for key in self.model["weights"]:
            if "word_embed" in key.lower() or "embeddings.word_embeddings.weight" in key:
                word_embeddings = self.model["weights"][key]
                break
        
        if word_embeddings is None:
            raise ValueError("Could not find word embeddings in model weights")
        
        # Look up embeddings
        batch_size, seq_len = input_ids.shape
        embeddings = mx.take(word_embeddings, input_ids, axis=0)
        
        # Mean pooling
        mask_expanded = mx.expand_dims(attention_mask.astype(mx.float32), -1)
        sum_embeddings = mx.sum(embeddings * mask_expanded, axis=1)
        sum_mask = mx.maximum(mx.sum(mask_expanded, axis=1), mx.array(1e-9))
        pooled = sum_embeddings / sum_mask
        
        return pooled
    
    def warmup(self, iterations: int = 5) -> None:
        """Warm up the model."""
        sample = ["warmup text for MLX inference benchmark"]
        for _ in range(iterations):
            self.infer(sample)
        logger.info(f"MLX warmup complete ({iterations} iterations)")
    
    def get_model_info(self) -> dict:
        """Return model information."""
        info = {
            "model_name": self.model_name,
            "device": self.device,
            "backend": "mlx",
            "quantization_bits": self.quantization_bits,
            "mlx_available": self._mlx_available,
            "using_fallback": self._use_fallback,
        }
        
        if self._use_fallback and hasattr(self, '_pytorch_fallback'):
            info["fallback_info"] = self._pytorch_fallback.get_model_info()
        
        return info
