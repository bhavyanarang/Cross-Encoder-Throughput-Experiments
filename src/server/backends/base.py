"""Base backend interface."""

import logging
import threading
import time
from abc import ABC, abstractmethod
from typing import Literal

import numpy as np

from src.models import InferenceResult
from src.server.backends.device import clear_memory, resolve_device, sync_device

logger = logging.getLogger(__name__)

QuantizationType = Literal["fp32", "fp16", "int8", "int4"]


class BaseBackend(ABC):
    def __init__(
        self,
        model_name: str,
        device: str = "mps",
        quantization: QuantizationType = "fp16",
        max_length: int = 512,
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

    @abstractmethod
    def load_model(self) -> None:
        pass

    @abstractmethod
    def infer(self, pairs: list[tuple[str, str]]) -> np.ndarray:
        pass

    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        self._acquire()
        try:
            start = time.perf_counter()
            sync_device(self.device)
            scores = self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
            sync_device(self.device)
            total_ms = (time.perf_counter() - start) * 1000
            return InferenceResult(scores=scores, total_ms=total_ms, batch_size=len(pairs))
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
