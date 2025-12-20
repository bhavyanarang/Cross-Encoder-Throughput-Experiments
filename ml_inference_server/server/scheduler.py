import time
import threading
from queue import Queue, Empty
from typing import Tuple
import numpy as np

from backends import PyTorchBackend
from metrics import MetricsCollector


class Scheduler:
    def __init__(
        self,
        backend: PyTorchBackend,
        metrics: MetricsCollector,
        batching_enabled: bool = False,
        max_batch_size: int = 8,
        timeout_ms: float = 100,
    ):
        self.backend = backend
        self.metrics = metrics
        self.batching_enabled = batching_enabled
        self.max_batch_size = max_batch_size
        self.timeout_ms = timeout_ms

    def schedule(self, texts: list[str]) -> Tuple[np.ndarray, float]:
        start = time.perf_counter()
        embeddings = self.backend.infer(texts)
        elapsed_ms = (time.perf_counter() - start) * 1000
        self.metrics.record(elapsed_ms)
        return embeddings, elapsed_ms

