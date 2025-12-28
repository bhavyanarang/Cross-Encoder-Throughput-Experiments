import logging
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import grpc
import numpy as np

from src.proto import inference_pb2, inference_pb2_grpc

logger = logging.getLogger(__name__)


class InferenceClient:
    def __init__(self, host: str = "localhost", port: int = 50051):
        self._channel = grpc.insecure_channel(f"{host}:{port}")
        self._stub = inference_pb2_grpc.InferenceServiceStub(self._channel)

    def infer(
        self, pairs: list[tuple[str, str]], timeout: float = 60.0
    ) -> tuple[list[float], float]:
        start = time.perf_counter()
        proto_pairs = [inference_pb2.QueryDocPair(query=p[0], document=p[1]) for p in pairs]
        request = inference_pb2.InferRequest(pairs=proto_pairs)
        response = self._stub.Infer(request, timeout=timeout)
        latency = (time.perf_counter() - start) * 1000
        return list(response.scores), latency

    def get_metrics(self, timeout: float = 10.0) -> dict:
        response = self._stub.GetMetrics(inference_pb2.Empty(), timeout=timeout)
        return {"qps": response.qps, "latency_avg_ms": response.latency_avg_ms}

    def benchmark(
        self,
        pairs: list[tuple[str, str]],
        batch_size: int,
        num_requests: int,
        concurrency: int = 1,
    ) -> dict:
        batches = []
        for i in range(num_requests):
            start = (i * batch_size) % len(pairs)
            batch = pairs[start : start + batch_size]
            if len(batch) < batch_size:
                batch = batch + pairs[: batch_size - len(batch)]
            batches.append(batch)

        latencies = []
        lock = Lock()
        start = time.perf_counter()

        def run_batch(batch):
            _, lat = self.infer(batch)
            with lock:
                latencies.append(lat)
            return lat

        if concurrency == 1:
            for batch in batches:
                run_batch(batch)
        else:
            with ThreadPoolExecutor(max_workers=concurrency) as ex:
                list(ex.map(run_batch, batches))

        elapsed = time.perf_counter() - start
        total_pairs = len(latencies) * batch_size
        lat = np.array(latencies)

        return {
            "batch_size": batch_size,
            "concurrency": concurrency,
            "num_requests": len(latencies),
            "total_pairs": total_pairs,
            "elapsed_s": elapsed,
            "latency_avg_ms": float(np.mean(lat)),
            "latency_p50_ms": float(np.percentile(lat, 50)),
            "latency_p95_ms": float(np.percentile(lat, 95)),
            "latency_p99_ms": float(np.percentile(lat, 99)),
            "throughput_avg": total_pairs / elapsed if elapsed > 0 else 0,
        }

    def close(self):
        self._channel.close()
