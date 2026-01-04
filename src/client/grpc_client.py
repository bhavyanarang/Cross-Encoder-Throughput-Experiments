import logging
import time
from concurrent.futures import ThreadPoolExecutor

import grpc
import numpy as np

from src.proto import inference_pb2, inference_pb2_grpc

logger = logging.getLogger(__name__)


class InferenceClient:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 50051,
        use_ssl: bool = False,
        ssl_ca_cert_path: str | None = None,
    ):
        if use_ssl:
            if ssl_ca_cert_path:
                try:
                    with open(ssl_ca_cert_path, "rb") as f:
                        ca_cert = f.read()
                except FileNotFoundError as e:
                    raise ValueError(f"CA certificate file not found: {e}") from e
                credentials = grpc.ssl_channel_credentials(root_certificates=ca_cert)
            else:
                credentials = grpc.ssl_channel_credentials()
            self._channel = grpc.secure_channel(f"{host}:{port}", credentials)
            logger.info(f"Connected to {host}:{port} (SSL/TLS)")
        else:
            self._channel = grpc.insecure_channel(f"{host}:{port}")
            logger.warning(f"Connected to {host}:{port} (insecure)")

        self._stub = inference_pb2_grpc.InferenceServiceStub(self._channel)

    def infer(
        self, pairs: list[tuple[str, str]], timeout: float = 60.0
    ) -> tuple[list[float], float]:
        start = time.perf_counter()
        proto_pairs = [inference_pb2.QueryDocPair(query=p[0], document=p[1]) for p in pairs]
        request = inference_pb2.InferRequest(pairs=proto_pairs)
        response = self._stub.Infer(request, timeout=timeout)
        latency = (time.perf_counter() - start) * 1000
        status_code = getattr(response, "status_code", 200)
        if status_code == 204:
            return [], latency
        return list(response.scores), latency

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
        start = time.perf_counter()

        def run_batch(batch):
            _, lat = self.infer(batch)
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
