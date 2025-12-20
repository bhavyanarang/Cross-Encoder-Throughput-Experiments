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
            # Apply dynamic quantization for CPU inference
            if self.device == "cpu":
                # Quantize the model's underlying transformer modules
                # SentenceTransformer wraps modules in a Sequential container
                quantized_any = False
                if hasattr(self.model, '_modules'):
                    for module_name, module in self.model._modules.items():
                        if hasattr(module, 'auto_model'):
                            # Quantize the transformer model (AutoModel)
                            self.model._modules[module_name].auto_model = torch.quantization.quantize_dynamic(
                                module.auto_model, {torch.nn.Linear}, dtype=torch.qint8
                            )
                            quantized_any = True
                
                if quantized_any:
                    print(f"Loaded {self.model_name} on {self.device} (QUANTIZED)")
                else:
                    print(f"Warning: Could not find transformer modules to quantize. Running without quantization.")
                    self.quantized = False
            else:
                print(f"Warning: Quantization is only supported on CPU. Running on {self.device} without quantization.")
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

