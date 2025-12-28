import numpy as np

from src.server.models import Config, InferenceResult, ModelConfig, PoolConfig


class TestModels:
    def test_inference_result(self):
        result = InferenceResult(scores=np.array([0.5, 0.8]), total_ms=10.0)
        assert len(result.scores) == 2
        assert result.total_ms == 10.0

    def test_model_config(self):
        cfg = ModelConfig(name="test-model", device="cpu")
        assert cfg.name == "test-model"
        assert cfg.device == "cpu"

    def test_pool_config(self):
        cfg = PoolConfig(instances=[ModelConfig(name="test")])
        assert len(cfg.instances) == 1

    def test_config(self):
        cfg = Config()
        assert cfg.server.grpc_port == 50051
