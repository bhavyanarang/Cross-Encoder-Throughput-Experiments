"""Base backend interface."""

import logging
import threading
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal

import numpy as np

from src.models import InferenceResult
from src.server.backends.device import clear_memory, resolve_device, sync_device

if TYPE_CHECKING:
    from src.server.tokenizer_pool import TokenizerPool

logger = logging.getLogger(__name__)

QuantizationType = Literal["fp32", "fp16", "int8", "int4"]


class BaseBackend(ABC):
    def __init__(
        self,
        model_name: str,
        device: str = "mps",
        quantization: QuantizationType = "fp16",
        max_length: int = 512,
        tokenizer_pool: "TokenizerPool | None" = None,
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

    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        """Run inference with timing, optionally using tokenizer pool."""
        self._acquire()
        try:
            # Tokenize using pool if available, otherwise inline
            if self._tokenizer_pool is not None:
                tokenize_start = time.perf_counter()
                tokenized_batch = self._tokenizer_pool.tokenize(pairs)
                t_tokenize_ms = (time.perf_counter() - tokenize_start) * 1000
                features = tokenized_batch.features
                batch_size = tokenized_batch.batch_size
                max_seq_length = tokenized_batch.max_seq_length
                total_tokens = tokenized_batch.total_tokens
                real_tokens = tokenized_batch.real_tokens
                padded_tokens = tokenized_batch.padded_tokens
                padding_ratio = tokenized_batch.padding_ratio
                avg_seq_length = tokenized_batch.avg_seq_length
            else:
                # Fallback: inline tokenization (backward compatible)
                from src.server.services.tokenizer import TokenizerService

                if not hasattr(self, "_tokenizer"):
                    self._tokenizer = TokenizerService(self.model_name, self.max_length)

                tokenize_start = time.perf_counter()
                tokenized_batch = self._tokenizer.tokenize(pairs, device=self.device)
                t_tokenize_ms = (time.perf_counter() - tokenize_start) * 1000
                features = tokenized_batch.features
                batch_size = tokenized_batch.batch_size
                max_seq_length = tokenized_batch.max_seq_length
                total_tokens = tokenized_batch.total_tokens
                real_tokens = tokenized_batch.real_tokens
                padded_tokens = tokenized_batch.padded_tokens
                padding_ratio = tokenized_batch.padding_ratio
                avg_seq_length = tokenized_batch.avg_seq_length

            # Move features to device if using tokenizer pool (which tokenizes on CPU)
            if self._tokenizer_pool is not None:
                features = {k: v.to(self.device) for k, v in features.items()}

            # Run model inference
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
        """Run inference with pre-tokenized batch (no tokenization).

        Args:
            tokenized_batch: TokenizedBatch with features already tokenized

        Returns:
            InferenceResult with scores and timing (t_tokenize_ms will be 0)
        """
        self._acquire()
        try:
            # Move features to device (tokenizer pool tokenizes on CPU)
            features = {k: v.to(self.device) for k, v in tokenized_batch.features.items()}

            # Run model inference directly with features
            start = time.perf_counter()
            sync_device(self.device)

            # Use the model's forward pass directly with features
            import torch

            with torch.inference_mode():
                # Extract input_ids and attention_mask from features
                outputs = self.model.model(**features, return_dict=True)
                logits = outputs.logits
                # Handle different model configurations
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
                t_tokenize_ms=0.0,  # Tokenization already done
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
        with self._pending_lock:
            self._pending += 1
        self._lock.acquire()
        self._is_busy = True

    def _release(self) -> None:
        self._is_busy = False
        self._lock.release()
        with self._pending_lock:
            self._pending -= 1

    def sync(self) -> None:
        sync_device(self.device)

    def clear_cache(self) -> None:
        clear_memory(self.device)

    @classmethod
    def from_config(cls, config) -> "BaseBackend":
        raise NotImplementedError("Subclass must implement from_config")
