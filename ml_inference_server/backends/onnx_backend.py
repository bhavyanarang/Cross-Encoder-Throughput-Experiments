import numpy as np
import logging
import os
from pathlib import Path
from .base_backend import BaseBackend

logger = logging.getLogger(__name__)


class ONNXBackend(BaseBackend):
    """ONNX Runtime backend for optimized inference."""
    
    def __init__(
        self, 
        model_name: str, 
        device: str = "mps",
        optimize: bool = True,
        use_coreml: bool = True
    ):
        super().__init__(model_name, device)
        self.optimize = optimize
        self.use_coreml = use_coreml and device == "mps"
        self.tokenizer = None
        self.session = None
        self.providers = []
    
    def load_model(self) -> None:
        """Load model with ONNX Runtime."""
        try:
            import onnxruntime as ort
            from transformers import AutoTokenizer
        except ImportError as e:
            logger.error("ONNX Runtime not installed. Install with: pip install onnxruntime")
            raise ImportError("onnxruntime is required for ONNX backend") from e
        
        logger.info(f"Loading ONNX model: {self.model_name}")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Determine ONNX model path
        onnx_path = self._get_or_export_onnx_model()
        
        # Configure providers
        self.providers = self._get_providers(ort)
        
        # Create session with optimization
        sess_options = ort.SessionOptions()
        if self.optimize:
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        self.session = ort.InferenceSession(
            onnx_path, 
            sess_options=sess_options,
            providers=self.providers
        )
        
        self._is_loaded = True
        logger.info(f"Loaded ONNX model on {self.providers}")
    
    def _get_providers(self, ort) -> list:
        """Get available execution providers."""
        available = ort.get_available_providers()
        logger.info(f"Available ONNX providers: {available}")
        
        providers = []
        
        # Try CoreML for macOS
        if self.use_coreml and "CoreMLExecutionProvider" in available:
            providers.append("CoreMLExecutionProvider")
            logger.info("Using CoreML provider for MPS acceleration")
        
        # Fallback to CPU
        if "CPUExecutionProvider" in available:
            providers.append("CPUExecutionProvider")
        
        return providers if providers else ["CPUExecutionProvider"]
    
    def _get_or_export_onnx_model(self) -> str:
        """Get ONNX model path, exporting if necessary."""
        # Check for cached ONNX model
        cache_dir = Path.home() / ".cache" / "onnx_models"
        model_safe_name = self.model_name.replace("/", "_")
        onnx_path = cache_dir / f"{model_safe_name}.onnx"
        
        if onnx_path.exists():
            logger.info(f"Using cached ONNX model: {onnx_path}")
            return str(onnx_path)
        
        # Export model to ONNX
        logger.info("Exporting model to ONNX format...")
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            from optimum.onnxruntime import ORTModelForFeatureExtraction
            
            # Use Optimum to export and optimize
            ort_model = ORTModelForFeatureExtraction.from_pretrained(
                self.model_name,
                export=True
            )
            ort_model.save_pretrained(str(cache_dir / model_safe_name))
            
            # Find the exported ONNX file
            exported_path = cache_dir / model_safe_name / "model.onnx"
            if exported_path.exists():
                return str(exported_path)
            
        except ImportError:
            logger.warning("Optimum not installed. Using fallback export method.")
            return self._fallback_export(onnx_path)
        
        return str(onnx_path)
    
    def _fallback_export(self, onnx_path: Path) -> str:
        """Fallback ONNX export using PyTorch."""
        import torch
        from transformers import AutoModel
        
        logger.info("Exporting with PyTorch ONNX export (legacy mode)...")
        
        model = AutoModel.from_pretrained(self.model_name)
        model.eval()
        
        # Create dummy inputs
        dummy_input = self.tokenizer(
            "This is a sample sentence for ONNX export.",
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        )
        
        # Export to ONNX using legacy export (compatible with all PyTorch versions)
        try:
            # Try new dynamo-based export first
            torch.onnx.export(
                model,
                (dummy_input["input_ids"], dummy_input["attention_mask"]),
                str(onnx_path),
                input_names=["input_ids", "attention_mask"],
                output_names=["last_hidden_state"],
                dynamic_axes={
                    "input_ids": {0: "batch_size", 1: "sequence"},
                    "attention_mask": {0: "batch_size", 1: "sequence"},
                    "last_hidden_state": {0: "batch_size", 1: "sequence"}
                },
                opset_version=14
            )
        except Exception as e:
            # Fallback to older export method
            logger.warning(f"Dynamo export failed: {e}, trying legacy export")
            with torch.no_grad():
                torch.onnx.export(
                    model,
                    (dummy_input["input_ids"], dummy_input["attention_mask"]),
                    str(onnx_path),
                    input_names=["input_ids", "attention_mask"],
                    output_names=["last_hidden_state"],
                    dynamic_axes={
                        "input_ids": {0: "batch_size", 1: "sequence"},
                        "attention_mask": {0: "batch_size", 1: "sequence"},
                        "last_hidden_state": {0: "batch_size", 1: "sequence"}
                    },
                    opset_version=14,
                    do_constant_folding=True
                )
        
        logger.info(f"Exported ONNX model to: {onnx_path}")
        return str(onnx_path)
    
    def infer(self, texts: list[str]) -> np.ndarray:
        """Run inference and return embeddings."""
        # Tokenize
        inputs = self.tokenizer(
            texts,
            return_tensors="np",
            padding=True,
            truncation=True,
            max_length=128
        )
        
        # Run inference
        outputs = self.session.run(
            None,
            {
                "input_ids": inputs["input_ids"].astype(np.int64),
                "attention_mask": inputs["attention_mask"].astype(np.int64)
            }
        )
        
        # Mean pooling
        last_hidden_state = outputs[0]
        attention_mask = inputs["attention_mask"]
        
        # Expand attention mask for broadcasting
        mask_expanded = np.expand_dims(attention_mask, -1)
        mask_expanded = np.broadcast_to(mask_expanded, last_hidden_state.shape)
        
        # Mean pooling
        sum_embeddings = np.sum(last_hidden_state * mask_expanded, axis=1)
        sum_mask = np.clip(np.sum(mask_expanded, axis=1), a_min=1e-9, a_max=None)
        embeddings = sum_embeddings / sum_mask
        
        return embeddings
    
    def warmup(self, iterations: int = 5) -> None:
        """Warm up the model."""
        sample = ["warmup text for ONNX inference benchmark"]
        for _ in range(iterations):
            self.infer(sample)
        logger.info(f"ONNX warmup complete ({iterations} iterations)")
    
    def get_model_info(self) -> dict:
        """Return model information."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "backend": "onnx",
            "providers": self.providers,
            "optimized": self.optimize,
            "use_coreml": self.use_coreml,
        }

