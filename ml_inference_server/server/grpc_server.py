import grpc
import time
from concurrent import futures
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "proto"))
import inference_pb2
import inference_pb2_grpc


class InferenceServicer(inference_pb2_grpc.InferenceServiceServicer):
    def __init__(self, scheduler, metrics=None):
        self.scheduler = scheduler
        self.metrics = metrics or scheduler.metrics

    def Infer(self, request, context):
        # Record request arrival time for queue wait analysis
        request_arrival_time = time.perf_counter()
        
        # Stage: gRPC receive (deserialize request)
        grpc_recv_start = time.perf_counter()
        pairs = [(p.query, p.document) for p in request.pairs]
        t_grpc_recv = (time.perf_counter() - grpc_recv_start) * 1000
        
        # Run cross-encoder inference (includes tokenization + model stages)
        # Pass arrival time for queue wait calculation
        scores, latency_ms = self.scheduler.schedule(pairs, request_arrival_time=request_arrival_time)
        
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
