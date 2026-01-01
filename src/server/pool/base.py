"""Base worker pool class for managing pools of workers."""

import logging
import queue
import threading
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


class BaseWorkerPool(ABC, Generic[T, R]):
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self._is_started = False
        self._inference_queue: queue.Queue | None = None

        # Metrics handling
        self._metrics_queue = None  # Should be set by subclass (likely mp.Queue)
        self._metrics_thread: threading.Thread | None = None
        self._worker_metrics: dict[int, dict] = {}
        self._metrics_lock = threading.Lock()
        self._shutdown_event = threading.Event()

    @abstractmethod
    def start(self, timeout_s: float = 120.0) -> None:
        pass

    @abstractmethod
    def stop(self, timeout_s: float = 30.0) -> None:
        pass

    def submit(self, work_item: T) -> R:
        if not self._is_started:
            raise RuntimeError(f"{self.__class__.__name__} not started")
        raise NotImplementedError("Subclass must implement submit() or override with custom logic")

    def set_inference_queue(self, inference_queue: queue.Queue) -> None:
        self._inference_queue = inference_queue

    @property
    def is_loaded(self) -> bool:
        return self._is_started

    def get_info(self) -> dict:
        return {
            "num_workers": self.num_workers,
            "is_loaded": self._is_started,
        }

    def _metrics_loop(self) -> None:
        """Common loop for collecting metrics from workers."""
        if self._metrics_queue is None:
            logger.warning("Metrics queue not initialized, skipping metrics loop")
            return

        while not self._shutdown_event.is_set():
            try:
                # Use a short timeout to check shutdown event frequently
                try:
                    worker_id, metrics_stats = self._metrics_queue.get(timeout=0.5)
                except (queue.Empty, EOFError, OSError):
                    continue

                with self._metrics_lock:
                    self._worker_metrics[worker_id] = metrics_stats
            except Exception as e:
                logger.error(f"Metrics loop error: {e}", exc_info=True)
                continue

    def start_metrics_thread(self) -> None:
        """Start the metrics collection thread."""
        if self._metrics_queue:
            self._metrics_thread = threading.Thread(target=self._metrics_loop, daemon=True)
            self._metrics_thread.start()

    def stop_metrics_thread(self, timeout_s: float = 1.0) -> None:
        """Stop the metrics collection thread."""
        if self._metrics_thread:
            self._metrics_thread.join(timeout=timeout_s)
            if self._metrics_thread.is_alive():
                logger.warning("Metrics thread did not exit cleanly")

    def get_worker_metrics(self) -> list[dict]:
        """Get cached worker metrics."""
        with self._metrics_lock:
            return [self._worker_metrics.get(i, {}) for i in range(self.num_workers)]

    def get_worker_metrics_by_id(self, worker_id: int) -> dict:
        if not self._is_started or worker_id >= self.num_workers:
            return {}

        with self._metrics_lock:
            return self._worker_metrics.get(worker_id, {})

    def reset_worker_metrics(self) -> None:
        with self._metrics_lock:
            self._worker_metrics.clear()

    def get_aggregate_throughput_qps(self) -> float:
        worker_metrics = self.get_worker_metrics()
        if not worker_metrics:
            return 0.0

        total_throughput = sum(ws.get("throughput_qps", 0) for ws in worker_metrics)
        return total_throughput

    def __len__(self) -> int:
        return self.num_workers
