"""
ONNX Backend - Cross-Encoder for Query-Document Scoring.

Uses ONNX Runtime for optimized cross-encoder inference.
Supports CoreML acceleration on Apple Silicon with fixed batch sizes.
"""

import time
import numpy as np
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from .base_backend import BaseBackend, InferenceResult

if TYPE_CHECKING:
    from core.config import ModelInstanceConfig

logger = logging.getLogger(__name__)

# CoreML flags for ONNX Runtime
COREML_FLAG_USE_CPU_ONLY = 0x001
COREML_FLAG_ENABLE_ON_SUBGRAPH = 0x002
COREML_FLAG_ONLY_ENABLE_DEVICE_WITH_ANE = 0x004
COREML_FLAG_ONLY_ALLOW_STATIC_INPUT_SHAPES = 0x008
COREML_FLAG_CREATE_MLPROGRAM = 0x010


class ONNXBackend(BaseBackend):
    """ONNX Runtime cross-encoder backend for query-document scoring."""
    
    COREML_BATCH_SIZE = 32
    MAX_SEQ_LENGTH = 128
    
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
        self._fixed_batch_size = self.COREML_BATCH_SIZE if self.use_coreml else None
        self._pad_pair = ("", "")
        self._input_ids_buffer = None
        self._attention_mask_buffer = None
    
    @classmethod
    def from_config(cls, config: "ModelInstanceConfig") -> "ONNXBackend":
        """Create ONNXBackend from configuration."""
        return cls(
            model_name=config.name,
            device=config.device,
            optimize=config.onnx_optimize,
            use_coreml=config.onnx_use_coreml,
        )
    
    def load_model(self) -> None:
        """Load cross-encoder model with ONNX Runtime."""
        try:
            import onnxruntime as ort
            from transformers import AutoTokenizer
        except ImportError as e:
            logger.error("ONNX Runtime not installed. Install with: pip install onnxruntime")
            raise ImportError("onnxruntime is required for ONNX backend") from e
        
        logger.info(f"Loading ONNX cross-encoder: {self.model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._tokenizer = self.tokenizer  # For compatibility
        self._max_length = self.MAX_SEQ_LENGTH
        
        onnx_path = self._get_or_export_onnx_model()
        self.providers = self._get_providers(ort)
        
        sess_options = ort.SessionOptions()
        if self.optimize:
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        self.session = ort.InferenceSession(
            onnx_path, 
            sess_options=sess_options,
            providers=self.providers
        )
        
        self._is_loaded = True
        logger.info(f"Loaded ONNX cross-encoder on {[p[0] if isinstance(p, tuple) else p for p in self.providers]}")
    
    def _get_providers(self, ort) -> list:
        """Get available execution providers with CoreML configuration."""
        available = ort.get_available_providers()
        logger.info(f"Available ONNX providers: {available}")
        
        providers = []
        
        if self.use_coreml and "CoreMLExecutionProvider" in available:
            coreml_options = {
                "coreml_flags": COREML_FLAG_CREATE_MLPROGRAM,
                "MLComputeUnits": 2,
            }
            providers.append(("CoreMLExecutionProvider", coreml_options))
            logger.info(f"Using CoreML with ALL compute units (CPU+GPU+ANE), batch={self._fixed_batch_size}")
        
        if "CPUExecutionProvider" in available:
            providers.append("CPUExecutionProvider")
        
        return providers if providers else ["CPUExecutionProvider"]
    
    def _get_or_export_onnx_model(self) -> str:
        """Get ONNX model path, exporting if necessary."""
        cache_dir = Path.home() / ".cache" / "onnx_models"
        model_safe_name = self.model_name.replace("/", "_")
        
        if self.use_coreml:
            onnx_path = cache_dir / f"{model_safe_name}_cross_encoder_batch{self._fixed_batch_size}.onnx"
        else:
            onnx_path = cache_dir / f"{model_safe_name}_cross_encoder_dynamic.onnx"
        
        if onnx_path.exists():
            logger.info(f"Using cached ONNX model: {onnx_path}")
            return str(onnx_path)
        
        logger.info("Exporting cross-encoder to ONNX format...")
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        return self._export_cross_encoder(onnx_path)
    
    def _export_cross_encoder(self, onnx_path: Path) -> str:
        """Export cross-encoder to ONNX with fixed or dynamic batch size."""
        import torch
        from transformers import AutoModelForSequenceClassification
        
        model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        model.eval()
        
        if self.use_coreml:
            logger.info(f"Exporting for CoreML with fixed batch size {self._fixed_batch_size}...")
            
            dummy_queries = ["sample query"] * self._fixed_batch_size
            dummy_docs = ["sample document for export"] * self._fixed_batch_size
            
            dummy_input = self.tokenizer(
                dummy_queries,
                dummy_docs,
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=128
            )
            
            with torch.no_grad():
                torch.onnx.export(
                    model,
                    (dummy_input["input_ids"], dummy_input["attention_mask"]),
                    str(onnx_path),
                    input_names=["input_ids", "attention_mask"],
                    output_names=["logits"],
                    opset_version=14,
                    do_constant_folding=True,
                    dynamo=False
                )
        else:
            logger.info("Exporting with dynamic batch size for CPU...")
            
            dummy_input = self.tokenizer(
                ["sample query", "another query"],
                ["sample document", "another doc"],
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            with torch.no_grad():
                torch.onnx.export(
                    model,
                    (dummy_input["input_ids"], dummy_input["attention_mask"]),
                    str(onnx_path),
                    input_names=["input_ids", "attention_mask"],
                    output_names=["logits"],
                    dynamic_axes={
                        "input_ids": {0: "batch_size", 1: "sequence"},
                        "attention_mask": {0: "batch_size", 1: "sequence"},
                        "logits": {0: "batch_size"}
                    },
                    opset_version=14,
                    do_constant_folding=True,
                    dynamo=False
                )
        
        logger.info(f"Exported ONNX cross-encoder to: {onnx_path}")
        return str(onnx_path)
    
    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        """Run cross-encoder inference on query-document pairs."""
        self._acquire_for_inference()
        try:
            if self.use_coreml and self._fixed_batch_size:
                return self._infer_fixed_batch(pairs)
            else:
                return self._infer_dynamic(pairs)
        finally:
            self._release_after_inference()
    
    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """Run inference with timing breakdown."""
        self._acquire_for_inference()
        try:
            total_start = time.perf_counter()
            
            # Tokenization stage
            tokenize_start = time.perf_counter()
            
            if self.use_coreml and self._fixed_batch_size:
                batch_size = len(pairs)
                fixed_size = self._fixed_batch_size
                
                queries = [None] * fixed_size
                documents = [None] * fixed_size
                
                for j, (q, d) in enumerate(pairs[:fixed_size]):
                    queries[j] = q
                    documents[j] = d
                
                for j in range(batch_size, fixed_size):
                    queries[j] = ""
                    documents[j] = ""
                
                inputs = self.tokenizer(
                    queries,
                    documents,
                    return_tensors="np",
                    padding="max_length",
                    truncation=True,
                    max_length=self.MAX_SEQ_LENGTH
                )
            else:
                queries, documents = zip(*pairs) if pairs else ([], [])
                inputs = self.tokenizer(
                    list(queries),
                    list(documents),
                    return_tensors="np",
                    padding=True,
                    truncation=True,
                    max_length=512
                )
            
            # Padding analysis
            attention_mask = inputs["attention_mask"]
            actual_batch_size = len(pairs)
            max_seq_length = attention_mask.shape[1]
            total_real_tokens = int(attention_mask[:actual_batch_size].sum())
            total_tokens = actual_batch_size * max_seq_length
            padded_tokens = total_tokens - total_real_tokens
            padding_ratio = padded_tokens / total_tokens if total_tokens > 0 else 0.0
            avg_seq_length = float(attention_mask[:actual_batch_size].sum(axis=1).mean())
            
            input_ids = inputs["input_ids"]
            if input_ids.dtype != np.int64:
                input_ids = input_ids.astype(np.int64)
            if attention_mask.dtype != np.int64:
                attention_mask = attention_mask.astype(np.int64)
            
            t_tokenize_ms = (time.perf_counter() - tokenize_start) * 1000
            
            # Inference stage
            inference_start = time.perf_counter()
            
            outputs = self.session.run(
                None,
                {"input_ids": input_ids, "attention_mask": attention_mask}
            )
            
            logits = outputs[0]
            
            if logits.shape[-1] == 1:
                scores = logits.squeeze(-1)[:actual_batch_size]
            else:
                scores = 1.0 / (1.0 + np.exp(-logits[:actual_batch_size, 1]))
            
            t_model_inference_ms = (time.perf_counter() - inference_start) * 1000
            total_ms = (time.perf_counter() - total_start) * 1000
            
            return InferenceResult(
                scores=scores,
                t_tokenize_ms=t_tokenize_ms,
                t_model_inference_ms=t_model_inference_ms,
                total_ms=total_ms,
                total_tokens=total_tokens,
                real_tokens=total_real_tokens,
                padded_tokens=padded_tokens,
                padding_ratio=padding_ratio,
                max_seq_length=max_seq_length,
                avg_seq_length=avg_seq_length,
                batch_size=actual_batch_size,
            )
        finally:
            self._release_after_inference()
    
    def _infer_fixed_batch(self, pairs: list) -> np.ndarray:
        """Inference with fixed batch size for CoreML."""
        batch_size = len(pairs)
        fixed_size = self._fixed_batch_size
        
        all_scores = np.empty(batch_size, dtype=np.float32)
        
        result_idx = 0
        for i in range(0, batch_size, fixed_size):
            chunk = pairs[i:i + fixed_size]
            chunk_size = len(chunk)
            
            queries = [None] * fixed_size
            documents = [None] * fixed_size
            
            for j, (q, d) in enumerate(chunk):
                queries[j] = q
                documents[j] = d
            
            for j in range(chunk_size, fixed_size):
                queries[j] = ""
                documents[j] = ""
            
            inputs = self.tokenizer(
                queries,
                documents,
                return_tensors="np",
                padding="max_length",
                truncation=True,
                max_length=self.MAX_SEQ_LENGTH
            )
            
            input_ids = inputs["input_ids"]
            attention_mask = inputs["attention_mask"]
            
            if input_ids.dtype != np.int64:
                input_ids = input_ids.astype(np.int64)
            if attention_mask.dtype != np.int64:
                attention_mask = attention_mask.astype(np.int64)
            
            outputs = self.session.run(
                None,
                {"input_ids": input_ids, "attention_mask": attention_mask}
            )
            
            logits = outputs[0]
            
            if logits.shape[-1] == 1:
                all_scores[result_idx:result_idx + chunk_size] = logits.squeeze(-1)[:chunk_size]
            else:
                all_scores[result_idx:result_idx + chunk_size] = (
                    1.0 / (1.0 + np.exp(-logits[:chunk_size, 1]))
                )
            
            result_idx += chunk_size
        
        return all_scores
    
    def _infer_dynamic(self, pairs: list) -> np.ndarray:
        """Inference with dynamic batch size for CPU."""
        queries, documents = zip(*pairs) if pairs else ([], [])
        
        inputs = self.tokenizer(
            list(queries),
            list(documents),
            return_tensors="np",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
        
        if input_ids.dtype != np.int64:
            input_ids = input_ids.astype(np.int64)
        if attention_mask.dtype != np.int64:
            attention_mask = attention_mask.astype(np.int64)
        
        outputs = self.session.run(
            None,
            {"input_ids": input_ids, "attention_mask": attention_mask}
        )
        
        logits = outputs[0]
        
        if logits.shape[-1] == 1:
            return logits.squeeze(-1)
        else:
            return 1.0 / (1.0 + np.exp(-logits[:, 1]))
    
    def warmup(self, iterations: int = 5) -> None:
        """Warm up the model."""
        logger.info(f"Warming up ONNX backend ({iterations} iterations)...")
        if self.use_coreml:
            sample_pairs = [("warmup query", "warmup document")] * self._fixed_batch_size
        else:
            sample_pairs = [("warmup query", "warmup document")]
        
        for _ in range(iterations):
            self.infer(sample_pairs)
        logger.info(f"ONNX warmup complete ({iterations} iterations)")
    
    def get_model_info(self) -> dict:
        """Return model information."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "backend": "onnx",
            "providers": [p[0] if isinstance(p, tuple) else p for p in self.providers],
            "optimized": self.optimize,
            "use_coreml": self.use_coreml,
            "fixed_batch_size": self._fixed_batch_size,
            "model_type": "cross-encoder",
        }
