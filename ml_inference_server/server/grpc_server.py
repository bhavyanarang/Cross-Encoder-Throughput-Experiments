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
        # Convert proto pairs to list of tuples
        pairs = [(p.query, p.document) for p in request.pairs]
        
        # Run cross-encoder inference
        scores, latency_ms = self.scheduler.schedule(pairs)
        
        return inference_pb2.InferResponse(
            scores=scores.tolist(),
            num_pairs=len(pairs),
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
            throughput_qps=summary.get("throughput_qps", 0),
            query_count=summary.get("query_count", 0),
        )


def serve(scheduler, host: str, port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inference_pb2_grpc.add_InferenceServiceServicer_to_server(
        InferenceServicer(scheduler), server
    )
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    print(f"Cross-encoder server started on {host}:{port}")
    server.wait_for_termination()
