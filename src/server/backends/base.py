import logging
import threading
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal, Optional

import numpy as np

from src.server.backends.device import clear_memory, resolve_device, sync_device
from src.server.dto import InferenceResult

if TYPE_CHECKING:
    from src.server.pool.tokenizer_pool import TokenizerPool

logger = logging.getLogger(__name__)

QuantizationType = Literal["fp32", "fp16", "int8", "int4"]


class BaseBackend(ABC):
    def __init__(
        self,
        model_name: str,
        device: str = "mps",
        quantization: QuantizationType = "fp16",
        max_length: int = 512,
        tokenizer_pool: Optional["TokenizerPool"] = None,
    ):
        self.model_name = model_name
        self.device = resolve_device(device)
        self.quantization = quantization
        self.max_length = max_length
        self.model = None
        self._is_loaded = False
        self._lock = threading.Lock()
        self._is_busy = False
        self._pending = 0
        self._pending_lock = threading.Lock()
        self._tokenizer_pool = tokenizer_pool

    @abstractmethod
    def load_model(self) -> None:
        pass

    @abstractmethod
    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        pass

    def _get_tokenizer(self):
        if self._tokenizer_pool is not None:
            return self._tokenizer_pool

        if not hasattr(self, "_tokenizer"):
            from src.server.utils.tokenizer import TokenizerService

            self._tokenizer = TokenizerService(self.model_name, self.max_length)
        return self._tokenizer

    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        self._acquire()
        try:
            tokenizer = self._get_tokenizer()
            tokenize_start = time.perf_counter()

            if self._tokenizer_pool is not None:
                tokenized_batch = tokenizer.tokenize(pairs)
                features = tokenized_batch.features
            else:
                # Local tokenizer
                tokenized_batch = tokenizer.tokenize(pairs, device=self.device)
                features = tokenized_batch.features

            t_tokenize_ms = (time.perf_counter() - tokenize_start) * 1000

            # Common metadata from tokenized batch
            batch_size = tokenized_batch.batch_size
            max_seq_length = tokenized_batch.max_seq_length
            total_tokens = tokenized_batch.total_tokens
            real_tokens = tokenized_batch.real_tokens
            padded_tokens = tokenized_batch.padded_tokens
            padding_ratio = tokenized_batch.padding_ratio
            avg_seq_length = tokenized_batch.avg_seq_length

            if self._tokenizer_pool is not None:
                features = {k: v.to(self.device) for k, v in features.items()}

            start = time.perf_counter()
            sync_device(self.device)
            scores = self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
            sync_device(self.device)
            t_model_inference_ms = (time.perf_counter() - start) * 1000

            total_ms = t_tokenize_ms + t_model_inference_ms

            return InferenceResult(
                scores=scores,
                t_tokenize_ms=t_tokenize_ms,
                t_model_inference_ms=t_model_inference_ms,
                total_ms=total_ms,
                batch_size=batch_size,
                max_seq_length=max_seq_length,
                total_tokens=total_tokens,
                real_tokens=real_tokens,
                padded_tokens=padded_tokens,
                padding_ratio=padding_ratio,
                avg_seq_length=avg_seq_length,
            )
        finally:
            self._release()

    def infer_with_tokenized(self, tokenized_batch) -> InferenceResult:
        self._acquire()
        try:
            features = {k: v.to(self.device) for k, v in tokenized_batch.features.items()}

            start = time.perf_counter()
            sync_device(self.device)

            import torch

            with torch.inference_mode():
                outputs = self.model.model(**features, return_dict=True)
                logits = outputs.logits

                if hasattr(self.model, "config") and self.model.config.num_labels == 1:
                    scores = torch.sigmoid(logits).squeeze(-1)
                else:
                    scores = (
                        torch.softmax(logits, dim=-1)[:, 1]
                        if logits.shape[1] > 1
                        else torch.sigmoid(logits).squeeze(-1)
                    )

            sync_device(self.device)
            t_model_inference_ms = (time.perf_counter() - start) * 1000
            scores_np = scores.cpu().numpy()

            return InferenceResult(
                scores=scores_np,
                t_tokenize_ms=0.0,
                t_model_inference_ms=t_model_inference_ms,
                total_ms=t_model_inference_ms,
                batch_size=tokenized_batch.batch_size,
                max_seq_length=tokenized_batch.max_seq_length,
                total_tokens=tokenized_batch.total_tokens,
                real_tokens=tokenized_batch.real_tokens,
                padded_tokens=tokenized_batch.padded_tokens,
                padding_ratio=tokenized_batch.padding_ratio,
                avg_seq_length=tokenized_batch.avg_seq_length,
            )
        finally:
            self._release()

    def warmup(self, iterations: int = 5) -> None:
        dummy = [("warmup query", "warmup document")]
        for _ in range(iterations):
            self.infer(dummy)
        logger.info(f"Warmup complete: {iterations} iterations")

    def get_model_info(self) -> dict:
        return {
            "name": self.model_name,
            "device": self.device,
            "quantization": self.quantization,
            "max_length": self.max_length,
            "loaded": self._is_loaded,
        }

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @property
    def is_busy(self) -> bool:
        return self._is_busy

    @property
    def pending_requests(self) -> int:
        return self._pending

    def _acquire(self) -> None:
        # Optimize: Acquire lock first, then update pending counter
        # This reduces the critical section and lock acquisitions
        self._lock.acquire()
        self._is_busy = True
        with self._pending_lock:
            self._pending += 1

    def _release(self) -> None:
        # Optimize: Release pending counter first, then release lock
        with self._pending_lock:
            self._pending -= 1
        self._is_busy = False
        self._lock.release()

    def sync(self) -> None:
        sync_device(self.device)

    def clear_cache(self) -> None:
        clear_memory(self.device)

    @classmethod
    def from_config(cls, config) -> "BaseBackend":
        raise NotImplementedError("Subclass must implement from_config")
