import logging
import time
from abc import ABC

import numpy as np
import torch

from src.server.backends.base import BaseBackend
from src.server.backends.device import sync_device
from src.server.dto import InferenceResult

logger = logging.getLogger(__name__)


class TorchBackend(BaseBackend, ABC):
    """
    Base backend for PyTorch-based implementations (CPU, MPS, CUDA, etc.).
    Provides common inference implementations.
    """

    def _get_tokenizer(self):
        if self._tokenizer_pool is not None:
            return self._tokenizer_pool

        if not hasattr(self, "_tokenizer"):
            from src.server.utils.tokenizer import TokenizerService

            self._tokenizer = TokenizerService(self.model_name, self.max_length)
        return self._tokenizer

    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        self._acquire()
        try:
            return self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
        finally:
            self._release()

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
                out = self.model.model(**features, return_dict=True)
                logits = out.logits
                if self.model.config.num_labels == 1:
                    scores = torch.sigmoid(logits).squeeze(-1)
                else:
                    scores = torch.softmax(logits, dim=-1)[:, 1]

            sync_device(self.device)
            t_inf = (time.perf_counter() - inf_start) * 1000
            scores_np = scores.cpu().numpy()

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

    def infer_with_tokenized(self, tokenized_batch) -> InferenceResult:
        self._acquire()
        try:
            features = {k: v.to(self.device) for k, v in tokenized_batch.features.items()}

            inf_start = time.perf_counter()
            sync_device(self.device)

            with torch.inference_mode():
                out = self.model.model(**features, return_dict=True)
                logits = out.logits
                if self.model.config.num_labels == 1:
                    scores = torch.sigmoid(logits).squeeze(-1)
                else:
                    scores = torch.softmax(logits, dim=-1)[:, 1]

            sync_device(self.device)
            t_inf = (time.perf_counter() - inf_start) * 1000
            scores_np = scores.cpu().numpy()

            return InferenceResult(
                scores=scores_np,
                t_tokenize_ms=0.0,
                t_model_inference_ms=t_inf,
                total_ms=t_inf,
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
