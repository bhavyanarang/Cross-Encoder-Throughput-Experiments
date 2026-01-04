import logging
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from src.server.dto.metrics.padding import PaddingTracker
from src.server.dto.metrics.stage import StageTrackerManager

if TYPE_CHECKING:
    from src.server.pool.model_pool import ModelPool
    from src.server.pool.tokenizer_pool import TokenizerPool

logger = logging.getLogger(__name__)


@dataclass
class MetricsCollector:
    latencies: list = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    request_count: int = 0
    query_count: int = 0
    last_update_time: float = field(default_factory=time.time)

    experiment_name: str = ""
    experiment_description: str = ""
    backend_type: str = ""
    device: str = ""

    recent_queries: deque = field(default_factory=lambda: deque(maxlen=200))
    recent_latencies: deque = field(default_factory=lambda: deque(maxlen=200))

    _lock: threading.Lock = field(default_factory=threading.Lock)

    _stage_tracker_manager: StageTrackerManager = field(default_factory=StageTrackerManager)
    _padding_tracker: PaddingTracker = field(default_factory=PaddingTracker)

    _model_pool: Optional["ModelPool"] = field(default=None)
    _tokenizer_pool: Optional["TokenizerPool"] = field(default=None)

    def __post_init__(self):
        self._stage_tracker_manager.register("tokenize", track_recent=True)
        self._stage_tracker_manager.register("pipeline_overhead", track_recent=True)
        self._stage_tracker_manager.register("tokenizer_queue_wait", track_recent=True)
        self._stage_tracker_manager.register("model_queue_wait", track_recent=True)
        self._stage_tracker_manager.register("model_inference", track_recent=True)
        self._stage_tracker_manager.register("overhead")
        self._stage_tracker_manager.register("mp_queue_send")
        self._stage_tracker_manager.register("mp_queue_receive")
        self._stage_tracker_manager.register("grpc_serialize")
        self._stage_tracker_manager.register("grpc_deserialize")
        self._stage_tracker_manager.register("scheduler")

    def set_pipeline_mode(self, mode: str):
        if mode == "tokenization_only":
            self._stage_tracker_manager.unregister("model_queue_wait")
            self._stage_tracker_manager.unregister("model_inference")
        elif mode == "inference_only":
            self._stage_tracker_manager.unregister("tokenize")
            self._stage_tracker_manager.unregister("tokenizer_queue_wait")

    def set_pool(self, pool: "ModelPool") -> None:
        self._model_pool = pool

    def set_tokenizer_pool(self, pool: "TokenizerPool") -> None:
        self._tokenizer_pool = pool

    def set_experiment_info(
        self, name: str = "", description: str = "", backend: str = "", device: str = ""
    ) -> None:
        self.experiment_name = name
        self.experiment_description = description
        self.backend_type = backend
        self.device = device
        logger.info(f"Experiment: {name} | Backend: {backend} | Device: {device}")

    @property
    def last_latency_ms(self) -> float:
        if self.recent_latencies:
            _, last_lat = self.recent_latencies[-1]
            return last_lat
        return 0.0

    def record(self, duration_ms: float, num_queries: int = 1):
        now = time.time()
        self.latencies.append(duration_ms)
        self.recent_queries.append((now, num_queries))
        self.recent_latencies.append((now, duration_ms))
        with self._lock:
            self.request_count += 1
            self.query_count += num_queries
            self.last_update_time = now

    def record_stage_timings(
        self,
        t_tokenize: float = 0.0,
        t_tokenizer_queue_wait: float = 0.0,
        t_model_queue_wait: float = 0.0,
        t_model_inference: float = 0.0,
        t_overhead: float = 0.0,
        t_mp_queue_send: float = 0.0,
        t_mp_queue_receive: float = 0.0,
        t_grpc_serialize: float = 0.0,
        t_grpc_deserialize: float = 0.0,
        t_scheduler: float = 0.0,
        total_ms: float = 0.0,
    ) -> None:
        now = time.time()
        stage_values = {
            "tokenize": t_tokenize,
            "tokenizer_queue_wait": t_tokenizer_queue_wait,
            "model_queue_wait": t_model_queue_wait,
            "model_inference": t_model_inference,
            "overhead": t_overhead,
            "mp_queue_send": t_mp_queue_send,
            "mp_queue_receive": t_mp_queue_receive,
            "grpc_serialize": t_grpc_serialize,
            "grpc_deserialize": t_grpc_deserialize,
            "scheduler": t_scheduler,
        }

        if total_ms > 0:
            measured_sum = sum(stage_values.values())
            pipeline_overhead = max(0, total_ms - measured_sum)
            stage_values["pipeline_overhead"] = pipeline_overhead

        with self._lock:
            for name, value in stage_values.items():
                try:
                    tracker = self._stage_tracker_manager.get(name)
                    tracker.record(value, now if tracker.recent_history is not None else None)
                except KeyError:
                    pass

    def record_padding_stats(
        self,
        padding_ratio: float = 0.0,
        padded_tokens: int = 0,
        total_tokens: int = 0,
        max_seq_length: int = 0,
        avg_seq_length: float = 0.0,
    ) -> None:
        with self._lock:
            self._padding_tracker.record(
                padding_ratio, padded_tokens, total_tokens, max_seq_length, avg_seq_length
            )

    def reset(self):
        logger.info("Metrics reset")
        now = time.time()

        with self._lock:
            self.latencies = []
            self.start_time = now
            self.request_count = 0
            self.query_count = 0
            self.last_update_time = now

            self.recent_queries.clear()
            self.recent_latencies.clear()

            self._stage_tracker_manager.reset_all()
            self._padding_tracker.reset()
