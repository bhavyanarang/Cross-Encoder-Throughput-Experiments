import torch
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
from .base_backend import BaseBackend

logger = logging.getLogger(__name__)


class PyTorchBackend(BaseBackend):
    """PyTorch backend with support for various quantization levels."""
    
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
        # Prefer MPS on Apple Silicon
        if device == "mps" and torch.backends.mps.is_available():
            self.device = "mps"
        elif device == "cuda" and torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"
        
        self.quantized = quantized
        self.quantization_mode = quantization_mode if quantized else "none"
        self.actual_dtype = None
    
    def load_model(self) -> None:
        """Load model with optional quantization."""
        logger.info(f"Loading model: {self.model_name}")
        logger.info(f"Target device: {self.device}")
        
        self.model = SentenceTransformer(self.model_name, device=self.device)
        
        if self.quantized:
            self._apply_quantization()
        else:
            self.actual_dtype = "float32"
            logger.info(f"Loaded {self.model_name} on {self.device} (FP32)")
        
        self._is_loaded = True
        self._verify_model_dtype()
    
    def _apply_quantization(self) -> None:
        """Apply the specified quantization mode."""
        if self.quantization_mode == "int8":
            self._apply_int8_quantization()
        elif self.quantization_mode == "fp16":
            self._apply_fp16_quantization()
        else:
            logger.warning(f"Unknown quantization mode: {self.quantization_mode}")
            self.quantized = False
            self.actual_dtype = "float32"
    
    def _apply_int8_quantization(self) -> None:
        """Apply INT8 dynamic quantization (CPU only, x86 only)."""
        import platform
        
        # Check if INT8 is supported (not on Apple Silicon)
        is_arm = platform.machine() in ("arm64", "aarch64")
        if is_arm:
            logger.warning("INT8 quantization not supported on ARM/Apple Silicon.")
            logger.warning("Falling back to FP16 quantization.")
            self._apply_fp16_quantization()
            return
        
        if self.device != "cpu":
            logger.warning(f"INT8 quantization requires CPU. Moving model to CPU.")
            self.device = "cpu"
            self.model = SentenceTransformer(self.model_name, device="cpu")
        
        try:
            quantized_any = False
            if hasattr(self.model, '_modules'):
                for module_name, module in self.model._modules.items():
                    if hasattr(module, 'auto_model'):
                        original_size = self._get_model_size(module.auto_model)
                        self.model._modules[module_name].auto_model = torch.quantization.quantize_dynamic(
                            module.auto_model, 
                            {torch.nn.Linear}, 
                            dtype=torch.qint8
                        )
                        new_size = self._get_model_size(self.model._modules[module_name].auto_model)
                        quantized_any = True
                        logger.info(f"Quantized {module_name}: {original_size:.1f}MB -> {new_size:.1f}MB")
            
            if quantized_any:
                self.actual_dtype = "int8"
                logger.info(f"Loaded {self.model_name} on {self.device} (INT8 QUANTIZED)")
            else:
                logger.warning("Could not find transformer modules to quantize.")
                self.quantized = False
                self.actual_dtype = "float32"
        except RuntimeError as e:
            if "NoQEngine" in str(e):
                logger.warning(f"INT8 engine not available: {e}")
                logger.warning("Falling back to FP16 quantization.")
                self._apply_fp16_quantization()
            else:
                raise
    
    def _apply_fp16_quantization(self) -> None:
        """Apply FP16 half precision."""
        try:
            if hasattr(self.model, '_modules'):
                for module_name, module in self.model._modules.items():
                    if hasattr(module, 'auto_model'):
                        self.model._modules[module_name].auto_model = module.auto_model.half()
            
            self.actual_dtype = "float16"
            logger.info(f"Loaded {self.model_name} on {self.device} (FP16 QUANTIZED)")
        except Exception as e:
            logger.warning(f"FP16 quantization failed: {e}")
            self.quantized = False
            self.actual_dtype = "float32"
    
    def _get_model_size(self, model) -> float:
        """Get model size in MB."""
        param_size = sum(p.nelement() * p.element_size() for p in model.parameters())
        buffer_size = sum(b.nelement() * b.element_size() for b in model.buffers())
        return (param_size + buffer_size) / 1024 / 1024
    
    def _verify_model_dtype(self) -> None:
        """Verify the actual dtype of model parameters."""
        if hasattr(self.model, '_modules'):
            for module_name, module in self.model._modules.items():
                if hasattr(module, 'auto_model'):
                    for name, param in module.auto_model.named_parameters():
                        actual = str(param.dtype)
                        logger.info(f"Verified dtype for {module_name}: {actual}")
                        break
                    break
    
    def infer(self, texts: list[str]) -> np.ndarray:
        """Run inference and return embeddings."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    def warmup(self, iterations: int = 5) -> None:
        """Warm up the model."""
        sample = ["warmup text for inference benchmark"]
        for _ in range(iterations):
            self.infer(sample)
        logger.info(f"Warmup complete ({iterations} iterations)")
    
    def get_model_info(self) -> dict:
        """Return model information."""
        info = {
            "model_name": self.model_name,
            "device": self.device,
            "quantized": self.quantized,
            "quantization_mode": self.quantization_mode,
            "actual_dtype": self.actual_dtype,
            "backend": "pytorch",
        }
        
        if self._is_loaded and hasattr(self.model, '_modules'):
            for module_name, module in self.model._modules.items():
                if hasattr(module, 'auto_model'):
                    info["model_size_mb"] = self._get_model_size(module.auto_model)
                    break
        
        return info
