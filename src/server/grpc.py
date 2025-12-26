"""gRPC server for inference."""

import logging
import time
from concurrent import futures

import grpc
import numpy as np

from src.proto import inference_pb2, inference_pb2_grpc

logger = logging.getLogger(__name__)


class InferenceServicer(inference_pb2_grpc.InferenceServiceServicer):
    """gRPC servicer for inference requests."""

    def __init__(self, scheduler, metrics=None):
        self._scheduler = scheduler
        self._metrics = metrics
        self._request_count = 0

    def Infer(self, request, context):
        pairs = [(p.query, p.document) for p in request.pairs]

        start = time.perf_counter()
        result = self._scheduler.schedule(pairs)
        latency = (time.perf_counter() - start) * 1000

        self._request_count += 1

        if self._metrics:
            # Record overall latency
            self._metrics.record(latency, len(pairs))

            # Record stage timings if available (including queue wait)
            self._metrics.record_stage_timings(
                t_tokenize=getattr(result, "t_tokenize_ms", 0),
                t_queue_wait=getattr(result, "t_queue_wait_ms", 0),
                t_model_inference=getattr(result, "t_model_inference_ms", 0),
            )

            # Record padding stats if available (use >= 0 to catch 0.0 padding ratios)
            padding_ratio = getattr(result, "padding_ratio", -1)
            if padding_ratio >= 0:
                self._metrics.record_padding_stats(
                    padding_ratio=padding_ratio,
                    padded_tokens=getattr(result, "padded_tokens", 0),
                    total_tokens=getattr(result, "total_tokens", 0),
                    max_seq_length=getattr(result, "max_seq_length", 0),
                    avg_seq_length=getattr(result, "avg_seq_length", 0),
                )

            # Record per-worker/per-model stats if available
            worker_id = getattr(result, "worker_id", -1)
            if worker_id >= 0:
                self._metrics.record_worker_stats(
                    worker_id=worker_id,
                    latency_ms=latency,
                    num_queries=len(pairs),
                )

        scores = (
            result.scores.tolist() if isinstance(result.scores, np.ndarray) else list(result.scores)
        )
        return inference_pb2.InferResponse(scores=scores)

    def GetMetrics(self, request, context):
        if self._metrics:
            summary = self._metrics.summary()
            return inference_pb2.MetricsResponse(
                qps=summary.get("throughput_qps", 0),
                latency_avg_ms=summary.get("avg_ms", 0),
                total_requests=self._request_count,
            )
        return inference_pb2.MetricsResponse(total_requests=self._request_count)


def serve(scheduler, host: str = "0.0.0.0", port: int = 50051, max_workers: int = 10, metrics=None):
    """Start gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    inference_pb2_grpc.add_InferenceServiceServicer_to_server(
        InferenceServicer(scheduler, metrics), server
    )
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logger.info(f"gRPC server listening on {host}:{port}")
    server.wait_for_termination()


__all__ = ["serve", "InferenceServicer"]
