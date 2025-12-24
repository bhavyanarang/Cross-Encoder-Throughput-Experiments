"""
gRPC Server - Cross-Encoder Inference Service.

Provides gRPC endpoints for:
- Infer: Run cross-encoder inference on query-document pairs
- GetMetrics: Get server metrics
"""

import logging
import time
from concurrent import futures
from typing import TYPE_CHECKING

import grpc

# Use relative imports - proto module re-exports pb2 modules
from proto import inference_pb2, inference_pb2_grpc

if TYPE_CHECKING:
    from metrics import MetricsCollector

    from .scheduler import Scheduler

logger = logging.getLogger(__name__)


class InferenceServicer(inference_pb2_grpc.InferenceServiceServicer):
    """gRPC servicer for cross-encoder inference."""

    def __init__(self, scheduler: "Scheduler", metrics: "MetricsCollector" = None):
        self.scheduler = scheduler
        self.metrics = metrics or scheduler.metrics
        logger.info("[TRACE] InferenceServicer initialized")

    def Infer(self, request, context):
        """Handle inference request."""
        logger.debug(f"[TRACE] Infer: received request with {len(request.pairs)} pairs")
        try:
            # Record request arrival time for queue wait analysis
            request_arrival_time = time.perf_counter()

            # Stage: gRPC receive (deserialize request)
            grpc_recv_start = time.perf_counter()
            pairs = [(p.query, p.document) for p in request.pairs]
            t_grpc_recv = (time.perf_counter() - grpc_recv_start) * 1000

            # Run cross-encoder inference
            scores, latency_ms = self.scheduler.schedule(
                pairs, request_arrival_time=request_arrival_time
            )

            # Stage: gRPC send (serialize response)
            grpc_send_start = time.perf_counter()
            response = inference_pb2.InferResponse(
                scores=scores.tolist(),
                num_pairs=len(pairs),
                latency_ms=latency_ms,
            )
            t_grpc_send = (time.perf_counter() - grpc_send_start) * 1000

            # Record gRPC stage timings
            self.metrics.record_stage_timings(
                t_grpc_receive=t_grpc_recv,
                t_grpc_send=t_grpc_send,
            )

            return response

        except Exception as e:
            logger.exception(f"Inference failed: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return inference_pb2.InferResponse()

    def GetMetrics(self, request, context):
        """Handle metrics request."""
        logger.debug("[TRACE] GetMetrics: received request")
        try:
            logger.debug("[TRACE] GetMetrics: calling metrics.summary()...")
            summary = self.scheduler.metrics.summary()
            logger.debug("[TRACE] GetMetrics: summary retrieved")
            return inference_pb2.MetricsResponse(
                count=summary.get("count", 0),
                avg_ms=summary.get("avg_ms", 0),
                p50_ms=summary.get("p50_ms", 0),
                p95_ms=summary.get("p95_ms", 0),
                p99_ms=summary.get("p99_ms", 0),
                throughput_qps=summary.get("throughput_qps", 0),
                query_count=summary.get("query_count", 0),
            )
        except Exception as e:
            logger.exception(f"GetMetrics failed: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return inference_pb2.MetricsResponse()


def serve(
    scheduler: "Scheduler",
    host: str = "0.0.0.0",
    port: int = 50051,
    max_workers: int = 10,
):
    """
    Start the gRPC server.

    Args:
        scheduler: Scheduler instance for handling requests
        host: Server bind address
        port: Server port
        max_workers: Maximum thread pool workers
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    inference_pb2_grpc.add_InferenceServiceServicer_to_server(InferenceServicer(scheduler), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logger.info(f"Cross-encoder server started on {host}:{port}")
    server.wait_for_termination()


__all__ = ["InferenceServicer", "serve"]
