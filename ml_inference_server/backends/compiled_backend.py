"""
Compiled Backend - Cross-Encoder with torch.compile for kernel fusion.

Uses PyTorch 2.0+ torch.compile() for optimized inference with kernel fusion.
This is the Apple Silicon equivalent of TensorRT's kernel fusion.
Optimized with inference_mode and proper warmup for compilation.
"""

import torch
import numpy as np
import logging
from sentence_transformers import CrossEncoder
from .base_backend import BaseBackend, with_inference_mode

logger = logging.getLogger(__name__)


class CompiledBackend(BaseBackend):
    """Compiled cross-encoder backend with torch.compile kernel fusion."""
    
    COMPILE_MODES = {
        "default": "Balanced compilation (default)",
        "reduce-overhead": "Minimize CPU overhead",
        "max-autotune": "Maximum optimization with autotuning",
    }
    
    # Common batch sizes to pre-compile for dynamic batching
    WARMUP_BATCH_SIZES = [1, 2, 4, 8, 16, 32]
    
    def __init__(
        self, 
        model_name: str, 
        device: str = "mps", 
        compile_mode: str = "reduce-overhead",
        use_fp16: bool = True,
        dynamic_shapes: bool = True,  # Enable dynamic shape support
    ):
        super().__init__(model_name, device)
        
        # Use shared device resolution
        self.device = self.resolve_device(device)
        
        self.compile_mode = compile_mode
        self.use_fp16 = use_fp16 and self.device == "mps"
        self.dynamic_shapes = dynamic_shapes
        self.actual_dtype = None
        self._is_compiled = False
    
    def load_model(self) -> None:
        """Load and compile the cross-encoder model."""
        logger.info(f"Loading cross-encoder: {self.model_name}")
        logger.info(f"Device: {self.device}")
        logger.info(f"Compile mode: {self.compile_mode}")
        
        # Clear memory before loading
        self.clear_memory(self.device)
        
        # Load CrossEncoder
        self.model = CrossEncoder(self.model_name, device=self.device)
        
        # Apply FP16 using shared utility
        if self.use_fp16:
            _, self.actual_dtype = self.apply_fp16(self.model, self.device, logger)
        else:
            self.actual_dtype = "float32"
        
        # Compile the model's forward pass with torch.compile
        logger.info(f"Compiling model with mode='{self.compile_mode}'...")
        try:
            # Compile the underlying transformer model with dynamic shapes
            self.model.model = torch.compile(
                self.model.model,
                mode=self.compile_mode,
                backend="inductor",  # Uses kernel fusion
                fullgraph=False,  # Allow graph breaks for compatibility
                dynamic=self.dynamic_shapes,  # Support variable batch sizes
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
        """
        Run cross-encoder inference with compiled model.
        Uses torch.inference_mode for better performance.
        
        Args:
            pairs: List of (query, document) tuples
            
        Returns:
            Array of relevance scores
        """
        # predict already returns numpy, no wrapper needed
        return self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
    
    def warmup(self, iterations: int = 10) -> None:
        """
        Warm up the compiled model with strategic batch sizes.
        Pre-compiles graphs for common batch sizes to avoid JIT compilation during inference.
        """
        logger.info(f"Warming up compiled model ({iterations} iterations)...")
        
        sample_pairs = [("warmup query", "warmup document")]
        
        # First, trigger compilation for common batch sizes
        for batch_size in self.WARMUP_BATCH_SIZES:
            batch = sample_pairs * batch_size
            self.infer(batch)
            self.sync_device(self.device)
        
        logger.info("Compiled graphs for batch sizes: " + str(self.WARMUP_BATCH_SIZES))
        
        # Then run additional iterations for stability
        for i in range(iterations):
            batch = sample_pairs * min(i + 1, 8)
            self.infer(batch)
            if (i + 1) % 5 == 0:
                logger.info(f"Warmup progress: {i + 1}/{iterations}")
        
        # Final sync and memory cleanup
        self.sync_device(self.device)
        self.clear_memory(self.device)
        
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

