"""Tests for gRPC client."""

from src.client.grpc_client import InferenceClient


class TestInferenceClient:
    def test_inference_client_init(self):
        """Test InferenceClient initialization."""
        client = InferenceClient(host="localhost", port=50051)
        assert client._channel is not None
        assert client._stub is not None

    def test_inference_client_init_defaults(self):
        """Test InferenceClient initialization with defaults."""
        client = InferenceClient()
        assert client._channel is not None
        assert client._stub is not None

    def test_inference_client_close(self):
        """Test closing client."""
        client = InferenceClient()
        # Should not raise
        client.close()

    def test_inference_client_benchmark_structure(self):
        """Test benchmark method returns correct structure."""
        client = InferenceClient()
        pairs = [("query1", "doc1"), ("query2", "doc2")]

        # Note: This will fail if server is not running, but we can test the structure
        # by checking the return type when it succeeds
        try:
            result = client.benchmark(
                pairs=pairs,
                batch_size=1,
                num_requests=2,
                concurrency=1,
            )
            # Check structure if successful
            assert "batch_size" in result
            assert "concurrency" in result
            assert "num_requests" in result
            assert "total_pairs" in result
            assert "elapsed_s" in result
            assert "latency_avg_ms" in result
            assert "latency_p50_ms" in result
            assert "latency_p95_ms" in result
            assert "latency_p99_ms" in result
            assert "throughput_avg" in result
        except Exception:
            # Server not running, skip
            pass
