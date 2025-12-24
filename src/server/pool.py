"""Process-based model pool for parallel inference."""

import concurrent.futures
import logging
import multiprocessing as mp
import os
import threading
import time

from src.models import InferenceResult, PoolConfig, WorkItem, WorkResult

logger = logging.getLogger(__name__)

_STOP = "__STOP__"


def _worker_main(
    worker_id: int,
    config_dict: dict,
    input_queue: mp.Queue,
    output_queue: mp.Queue,
    ready_event: mp.Event,
):
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    from src.models import ModelConfig
    from src.server.backends import create_backend

    cfg = ModelConfig(**config_dict)
    backend = create_backend(cfg)
    backend.load_model()
    backend.warmup(3)

    ready_event.set()
    logger.info(f"Worker {worker_id} ready")

    while True:
        try:
            item = input_queue.get()
            if item == _STOP:
                break

            result = backend.infer_with_timing(item.pairs)
            output_queue.put(
                WorkResult(
                    req_id=item.req_id,
                    scores=result.scores,
                    worker_id=worker_id,
                    t_tokenize_ms=result.t_tokenize_ms,
                    t_model_inference_ms=result.t_model_inference_ms,
                    total_ms=result.total_ms,
                    total_tokens=result.total_tokens,
                    real_tokens=result.real_tokens,
                    padded_tokens=result.padded_tokens,
                    padding_ratio=result.padding_ratio,
                    max_seq_length=result.max_seq_length,
                    avg_seq_length=result.avg_seq_length,
                    batch_size=result.batch_size,
                )
            )
        except Exception as e:
            logger.error(f"Worker {worker_id} error: {e}")


class ModelPool:
    def __init__(self, config: PoolConfig):
        self.config = config
        self.num_workers = len(config.instances)
        self._processes: list[mp.Process] = []
        self._input_queue = mp.Queue()
        self._output_queue = mp.Queue()
        self._ready_events: list[mp.Event] = []
        self._is_started = False
        self._next_req_id = 0
        self._pending: dict[int, concurrent.futures.Future] = {}
        self._result_thread: threading.Thread | None = None
        self._request_counts: dict[int, int] = {}

    def start(self, timeout_s: float = 120.0) -> None:
        if self._is_started:
            return

        for i, inst in enumerate(self.config.instances):
            ready = mp.Event()
            self._ready_events.append(ready)

            p = mp.Process(
                target=_worker_main,
                args=(i, inst.model_dump(), self._input_queue, self._output_queue, ready),
                daemon=True,
            )
            p.start()
            self._processes.append(p)

        for i, ev in enumerate(self._ready_events):
            if not ev.wait(timeout_s):
                raise RuntimeError(f"Worker {i} failed to start")

        self._result_thread = threading.Thread(target=self._result_loop, daemon=True)
        self._result_thread.start()
        self._is_started = True
        logger.info(f"Pool ready with {self.num_workers} workers")

    def stop(self, timeout_s: float = 30.0) -> None:
        if not self._is_started:
            return

        for _ in range(self.num_workers):
            self._input_queue.put(_STOP)

        deadline = time.time() + timeout_s
        for p in self._processes:
            remaining = max(0, deadline - time.time())
            p.join(timeout=remaining)
            if p.is_alive():
                p.terminate()

        self._processes.clear()
        self._is_started = False
        logger.info("Pool stopped")

    def _result_loop(self) -> None:
        while True:
            try:
                result = self._output_queue.get()
                if not isinstance(result, WorkResult):
                    continue

                self._request_counts[result.worker_id] = (
                    self._request_counts.get(result.worker_id, 0) + 1
                )

                future = self._pending.pop(result.req_id, None)
                if future and not future.cancelled():
                    future.set_result(result)
            except Exception as e:
                logger.error(f"Result loop error: {e}")
                time.sleep(0.1)

    def infer(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        if not self._is_started:
            raise RuntimeError("Pool not started")

        req_id = self._next_req_id
        self._next_req_id += 1

        future = concurrent.futures.Future()
        self._pending[req_id] = future

        self._input_queue.put(WorkItem(req_id=req_id, pairs=pairs))

        try:
            result = future.result()
            return InferenceResult(
                scores=result.scores,
                t_tokenize_ms=result.t_tokenize_ms,
                t_model_inference_ms=result.t_model_inference_ms,
                total_ms=result.total_ms,
                total_tokens=result.total_tokens,
                real_tokens=result.real_tokens,
                padded_tokens=result.padded_tokens,
                padding_ratio=result.padding_ratio,
                max_seq_length=result.max_seq_length,
                avg_seq_length=result.avg_seq_length,
                batch_size=result.batch_size,
            )
        except Exception:
            self._pending.pop(req_id, None)
            raise

    def infer_with_timing(self, pairs: list[tuple[str, str]]) -> InferenceResult:
        return self.infer(pairs)

    def get_info(self) -> dict:
        return {
            "num_instances": self.num_workers,
            "is_loaded": self._is_started,
            "request_counts": dict(self._request_counts),
        }

    @property
    def is_loaded(self) -> bool:
        return self._is_started

    def __len__(self) -> int:
        return self.num_workers
