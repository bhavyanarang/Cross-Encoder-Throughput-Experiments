import logging
import time
from concurrent import futures
from typing import TYPE_CHECKING, Optional

import grpc
import numpy as np

from src.proto import inference_pb2, inference_pb2_grpc

if TYPE_CHECKING:
    from src.server.services.metrics_service import MetricsService
    from src.server.services.orchestrator_service import InferenceInterface

logger = logging.getLogger(__name__)


class InferenceServicer(inference_pb2_grpc.InferenceServiceServicer):
    def __init__(
        self, inference_handler: "InferenceInterface", metrics: Optional["MetricsService"] = None
    ):
        self._inference_handler = inference_handler
        self._metrics = metrics

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
        status_code = getattr(result, "status_code", 200)
        response = inference_pb2.InferResponse(scores=scores, status_code=status_code)
        t_grpc_serialize_ms = (time.perf_counter() - grpc_serialize_start) * 1000

        total_latency = (time.perf_counter() - total_start) * 1000

        result.t_grpc_deserialize_ms = t_grpc_deserialize_ms
        result.t_grpc_serialize_ms = t_grpc_serialize_ms

        result.t_scheduler_ms = 0.0

        if self._metrics:
            self._metrics.record(total_latency, len(pairs))

            self._metrics.record_stage_timings(
                t_tokenize=getattr(result, "t_tokenize_ms", 0),
                t_tokenizer_queue_wait=getattr(result, "t_tokenizer_queue_wait_ms", 0),
                t_model_queue_wait=getattr(result, "t_model_queue_wait_ms", 0),
                t_model_inference=getattr(result, "t_model_inference_ms", 0),
                t_overhead=getattr(result, "t_overhead_ms", 0),
                t_mp_queue_send=getattr(result, "t_mp_queue_send_ms", 0),
                t_mp_queue_receive=getattr(result, "t_mp_queue_receive_ms", 0),
                t_grpc_serialize=t_grpc_serialize_ms,
                t_grpc_deserialize=t_grpc_deserialize_ms,
                t_scheduler=getattr(result, "t_scheduler_ms", 0),
                total_ms=total_latency,
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
                    num_queries=len(pairs),
                )

        return response


def serve(
    inference_handler: "InferenceInterface",
    host: str = "127.0.0.1",
    port: int = 50051,
    max_workers: int = 10,
    metrics: Optional["MetricsService"] = None,
    use_ssl: bool = False,
    ssl_cert_path: str | None = None,
    ssl_key_path: str | None = None,
) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    inference_pb2_grpc.add_InferenceServiceServicer_to_server(
        InferenceServicer(inference_handler, metrics), server
    )

    if use_ssl:
        if not ssl_cert_path or not ssl_key_path:
            raise ValueError("ssl_cert_path and ssl_key_path required when use_ssl=True")

        try:
            with open(ssl_key_path, "rb") as f:
                private_key = f.read()
            with open(ssl_cert_path, "rb") as f:
                certificate_chain = f.read()
        except FileNotFoundError as e:
            raise ValueError(f"SSL certificate or key file not found: {e}") from e

        credentials = grpc.ssl_server_credentials(
            [(private_key, certificate_chain)], require_client_auth=False
        )
        server.add_secure_port(f"{host}:{port}", credentials)
        logger.info(f"gRPC server listening on {host}:{port} (SSL/TLS enabled)")
    else:
        server.add_insecure_port(f"{host}:{port}")
        logger.warning(f"gRPC server listening on {host}:{port} (insecure, no SSL/TLS)")

    server.start()
    logger.info("gRPC server started")
    server.wait_for_termination()
    return server


__all__ = ["serve", "InferenceServicer"]
