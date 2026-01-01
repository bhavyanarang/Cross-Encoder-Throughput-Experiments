import logging
import time

import torch
from sentence_transformers import CrossEncoder

from src.server.backends.device import apply_fp16, sync_device
from src.server.backends.torch_base import TorchBackend
from src.server.dto import InferenceResult

logger = logging.getLogger(__name__)


class CUDABackend(TorchBackend):
    def __init__(
        self,
        model_name: str,
        device: str = "cuda",
        quantization: str = "fp16",
        max_length: int = 512,
        use_amp: bool = True,
    ):
        super().__init__(model_name, device, quantization, max_length)
        self._use_amp = use_amp and quantization == "fp16"

    def load_model(self) -> None:
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is not available. Install CUDA-enabled PyTorch.")

        logger.info(f"Loading {self.model_name} on {self.device} ({self.quantization})")

        device_name = torch.cuda.get_device_name(0)
        total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        logger.info(f"CUDA Device: {device_name}, Memory: {total_memory:.1f} GB")

        self.model = CrossEncoder(self.model_name, device=self.device)

        if self.quantization == "fp16":
            applied, msg = apply_fp16(self.model.model, self.device)
            if applied:
                logger.info(f"Applied {msg}")
        elif self.quantization == "int8":
            self.model.model = torch.quantization.quantize_dynamic(
                self.model.model, {torch.nn.Linear}, dtype=torch.qint8
            )
            logger.info("Applied INT8 dynamic quantization")

        self._is_loaded = True

    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        self._acquire()
        try:
            total_start = time.perf_counter()

            tokenizer = self._get_tokenizer()
            if self._tokenizer_pool:
                tokenized_batch = tokenizer.tokenize(pairs)
                features = {k: v.to(self.device) for k, v in tokenized_batch.features.items()}
            else:
                tokenized_batch = tokenizer.tokenize(pairs, device=self.device)
                features = tokenized_batch.features

            inf_start = time.perf_counter()
            sync_device(self.device)

            with torch.inference_mode():
                if self._use_amp:
                    with torch.cuda.amp.autocast():
                        out = self.model.model(**features, return_dict=True)
                else:
                    out = self.model.model(**features, return_dict=True)

                logits = out.logits
                if self.model.config.num_labels == 1:
                    scores = torch.sigmoid(logits).squeeze(-1)
                else:
                    scores = torch.softmax(logits, dim=-1)[:, 1]

            sync_device(self.device)
            t_inf = (time.perf_counter() - inf_start) * 1000
            scores_np = scores.float().cpu().numpy()

            return InferenceResult(
                scores=scores_np,
                t_tokenize_ms=tokenized_batch.tokenize_time_ms,
                t_model_inference_ms=t_inf,
                total_ms=(time.perf_counter() - total_start) * 1000,
                total_tokens=tokenized_batch.total_tokens,
                real_tokens=tokenized_batch.real_tokens,
                padded_tokens=tokenized_batch.padded_tokens,
                padding_ratio=tokenized_batch.padding_ratio,
                max_seq_length=tokenized_batch.max_seq_length,
                avg_seq_length=tokenized_batch.avg_seq_length,
                batch_size=tokenized_batch.batch_size,
            )
        finally:
            self._release()

    def get_gpu_memory_mb(self) -> float:
        if torch.cuda.is_available():
            return torch.cuda.memory_allocated() / (1024 * 1024)
        return 0.0

    @classmethod
    def from_config(cls, config) -> "CUDABackend":
        return cls(
            model_name=config.name if hasattr(config, "name") else config["name"],
            device="cuda",
            quantization=getattr(config, "quantization", "fp16"),
            max_length=getattr(config, "max_length", 512),
        )
