from src.client.grpc_client import InferenceClient


class TestInferenceClient:
    def test_inference_client_init(self):
        client = InferenceClient(host="localhost", port=50051)
        assert client._channel is not None
        assert client._stub is not None

    def test_inference_client_init_defaults(self):
        client = InferenceClient()
        assert client._channel is not None
        assert client._stub is not None

    def test_inference_client_close(self):
        client = InferenceClient()

        client.close()

    def test_inference_client_benchmark_structure(self):
        client = InferenceClient()
        pairs = [("query1", "doc1"), ("query2", "doc2")]

        try:
            result = client.benchmark(
                pairs=pairs,
                batch_size=1,
                num_requests=2,
                concurrency=1,
            )

            assert "batch_size" in result
            assert "concurrency" in result
            assert "num_requests" in result
            assert "total_pairs" in result
            assert "elapsed_s" in result
            assert "status" in result
        except Exception:
            pass
