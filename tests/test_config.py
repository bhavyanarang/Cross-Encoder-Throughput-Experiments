"""Tests for configuration loading."""

from ml_inference_server.core.config import ServerConfig
from ml_inference_server.utils.config_loader import load_experiment_config


class TestConfig:
    """Test configuration loading and validation."""

    def test_load_experiment_config(self):
        """Test loading an experiment configuration."""
        config_path = "ml_inference_server/experiments/01_backend_pytorch.yaml"
        config = load_experiment_config(config_path)

        assert config is not None
        assert "name" in config or "_experiment_name" in config
        assert "model" in config

    def test_server_config_validation(self):
        """Test ServerConfig validation."""

        config_data = {
            "server": {
                "host": "localhost",
                "port": 50051,
                "http_port": 8080,
            },
            "model_pool": {
                "instances": [
                    {
                        "name": "cross-encoder/ms-marco-MiniLM-L-6-v2",
                        "backend": "pytorch",
                        "device": "cpu",
                    }
                ]
            },
        }

        config = ServerConfig.model_validate(config_data)
        assert config.server.host == "localhost"
        assert config.server.port == 50051
        assert config.model_pool is not None
        assert len(config.model_pool.instances) == 1
