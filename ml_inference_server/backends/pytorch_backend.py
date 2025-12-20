import torch
import numpy as np
from sentence_transformers import SentenceTransformer


class PyTorchBackend:
    def __init__(self, model_name: str, device: str = "mps", quantized: bool = False):
        self.model_name = model_name
        self.device = device if torch.backends.mps.is_available() else "cpu"
        self.quantized = quantized
        self.model = None

    def load_model(self):
        self.model = SentenceTransformer(self.model_name, device=self.device)
        
        if self.quantized:
            # Apply dynamic quantization
            # Note: PyTorch dynamic quantization works on CPU. For MPS/GPU, we use half precision (FP16)
            quantized_any = False
            
            if self.device == "cpu":
                # INT8 quantization for CPU
                if hasattr(self.model, '_modules'):
                    for module_name, module in self.model._modules.items():
                        if hasattr(module, 'auto_model'):
                            # Quantize the transformer model (AutoModel)
                            self.model._modules[module_name].auto_model = torch.quantization.quantize_dynamic(
                                module.auto_model, {torch.nn.Linear}, dtype=torch.qint8
                            )
                            quantized_any = True
                
                if quantized_any:
                    print(f"Loaded {self.model_name} on {self.device} (INT8 QUANTIZED)")
                else:
                    print(f"Warning: Could not find transformer modules to quantize. Running without quantization.")
                    self.quantized = False
            else:
                # For MPS/CUDA, use FP16 (half precision) as a form of quantization
                try:
                    if hasattr(self.model, '_modules'):
                        for module_name, module in self.model._modules.items():
                            if hasattr(module, 'auto_model'):
                                # Convert to half precision
                                self.model._modules[module_name].auto_model = module.auto_model.half()
                                quantized_any = True
                    
                    if quantized_any:
                        print(f"Loaded {self.model_name} on {self.device} (FP16 QUANTIZED)")
                    else:
                        print(f"Warning: Could not apply FP16 quantization. Running in FP32.")
                        self.quantized = False
                except Exception as e:
                    print(f"Warning: FP16 quantization failed on {self.device}: {e}")
                    print(f"Running in FP32 mode.")
                    self.quantized = False
        else:
            print(f"Loaded {self.model_name} on {self.device}")

    def infer(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings

    def warmup(self, iterations: int = 5):
        sample = ["warmup text"]
        for _ in range(iterations):
            self.infer(sample)
        print(f"Warmup complete ({iterations} iterations)")

