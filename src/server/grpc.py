import logging
import time
from concurrent import futures
from typing import TYPE_CHECKING

import grpc
import numpy as np

from src.proto import inference_pb2, inference_pb2_grpc

if TYPE_CHECKING:
    from src.server.services.metrics_service import MetricsService
    from src.server.services.orchestrator_service import InferenceInterface

logger = logging.getLogger(__name__)


class InferenceServicer(inference_pb2_grpc.InferenceServiceServicer):
    def __init__(
        self, inference_handler: "InferenceInterface", metrics: "MetricsService | None" = None
    ):
        self._inference_handler = inference_handler
        self._metrics = metrics
        self._request_count = 0

    def Infer(self, request, context):
        total_start = time.perf_counter()

        grpc_deserialize_start = time.perf_counter()
        pairs = [(p.query, p.document) for p in request.pairs]
        t_grpc_deserialize_ms = (time.perf_counter() - grpc_deserialize_start) * 1000

        result = self._inference_handler.schedule(pairs)

        grpc_serialize_start = time.perf_counter()
        scores = (
            result.scores.tolist() if isinstance(result.scores, np.ndarray) else list(result.scores)
        )
        response = inference_pb2.InferResponse(scores=scores)
        t_grpc_serialize_ms = (time.perf_counter() - grpc_serialize_start) * 1000

        total_latency = (time.perf_counter() - total_start) * 1000

        self._request_count += 1

        result.t_grpc_deserialize_ms = t_grpc_deserialize_ms
        result.t_grpc_serialize_ms = t_grpc_serialize_ms

        result.t_scheduler_ms = 0.0

        if self._metrics:
            self._metrics.record(total_latency, len(pairs))

            self._metrics.record_stage_timings(
                t_tokenize=getattr(result, "t_tokenize_ms", 0),
                t_queue_wait=getattr(result, "t_queue_wait_ms", 0),
                t_model_inference=getattr(result, "t_model_inference_ms", 0),
                t_overhead=getattr(result, "t_overhead_ms", 0),
                t_mp_queue_send=getattr(result, "t_mp_queue_send_ms", 0),
                t_mp_queue_receive=getattr(result, "t_mp_queue_receive_ms", 0),
                t_grpc_serialize=t_grpc_serialize_ms,
                t_grpc_deserialize=t_grpc_deserialize_ms,
                t_scheduler=getattr(result, "t_scheduler_ms", 0),
            )

            padding_ratio = getattr(result, "padding_ratio", -1)
            if padding_ratio >= 0:
                self._metrics.record_padding_stats(
                    padding_ratio=padding_ratio,
                    padded_tokens=getattr(result, "padded_tokens", 0),
                    total_tokens=getattr(result, "total_tokens", 0),
                    max_seq_length=getattr(result, "max_seq_length", 0),
                    avg_seq_length=getattr(result, "avg_seq_length", 0),
                )

            worker_id = getattr(result, "worker_id", -1)
            if worker_id >= 0:
                self._metrics.record_worker_stats(
                    worker_id=worker_id,
                    latency_ms=total_latency,
                    num_queries=len(pairs),
                )

            tokenizer_worker_id = getattr(result, "tokenizer_worker_id", -1)
            t_tokenize_ms = getattr(result, "t_tokenize_ms", 0)
            total_tokens = getattr(result, "total_tokens", 0)
            if tokenizer_worker_id >= 0 and t_tokenize_ms > 0:
                self._metrics.record_tokenizer_worker_stats(
                    worker_id=tokenizer_worker_id,
                    latency_ms=t_tokenize_ms,
                    total_tokens=total_tokens,
                )

        return response

    def GetMetrics(self, request, context):
        if self._metrics:
            summary = self._metrics.get_summary()
            return inference_pb2.MetricsResponse(
                qps=summary.get("throughput_qps", 0),
                latency_avg_ms=summary.get("avg_ms", 0),
                total_requests=self._request_count,
            )
        return inference_pb2.MetricsResponse(total_requests=self._request_count)


def serve(
    inference_handler: "InferenceInterface",
    host: str = "0.0.0.0",
    port: int = 50051,
    max_workers: int = 10,
    metrics: "MetricsService | None" = None,
):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    inference_pb2_grpc.add_InferenceServiceServicer_to_server(
        InferenceServicer(inference_handler, metrics), server
    )
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logger.info(f"gRPC server listening on {host}:{port}")
    server.wait_for_termination()


__all__ = ["serve", "InferenceServicer"]
