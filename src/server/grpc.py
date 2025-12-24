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
            self._metrics.record(latency, len(pairs))

        scores = (
            result.scores.tolist() if isinstance(result.scores, np.ndarray) else list(result.scores)
        )
        return inference_pb2.InferResponse(scores=scores)

    def GetMetrics(self, request, context):
        if self._metrics:
            stats = self._metrics.get_stats()
            return inference_pb2.MetricsResponse(
                qps=stats.get("qps", 0),
                latency_avg_ms=stats.get("latency_avg_ms", 0),
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
