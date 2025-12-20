import grpc
from concurrent import futures
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "proto"))
import inference_pb2
import inference_pb2_grpc


class InferenceServicer(inference_pb2_grpc.InferenceServiceServicer):
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def Infer(self, request, context):
        texts = list(request.texts)
        embeddings, latency_ms = self.scheduler.schedule(texts)
        
        flat_embeddings = embeddings.flatten().tolist()
        return inference_pb2.InferResponse(
            embeddings=flat_embeddings,
            embedding_dim=embeddings.shape[1],
            num_texts=embeddings.shape[0],
            latency_ms=latency_ms,
        )

    def GetMetrics(self, request, context):
        summary = self.scheduler.metrics.summary()
        return inference_pb2.MetricsResponse(
            count=summary.get("count", 0),
            avg_ms=summary.get("avg_ms", 0),
            p50_ms=summary.get("p50_ms", 0),
            p95_ms=summary.get("p95_ms", 0),
            p99_ms=summary.get("p99_ms", 0),
            throughput_rps=summary.get("throughput_rps", 0),
        )


def serve(scheduler, host: str, port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inference_pb2_grpc.add_InferenceServiceServicer_to_server(
        InferenceServicer(scheduler), server
    )
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    print(f"Server started on {host}:{port}")
    server.wait_for_termination()

