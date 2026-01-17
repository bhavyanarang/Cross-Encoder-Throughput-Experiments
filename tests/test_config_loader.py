import tempfile
from pathlib import Path

import pytest
import yaml

from src.server.utils.config_loader import (
    get_experiment_name,
    load_config,
)


class TestConfigLoader:
    def test_load_config_single_model(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "test.yaml"
            config_data = {
                "model": {
                    "name": "test-model",
                    "device": "cpu",
                    "backend": "pytorch",
                }
            }
            with open(config_path, "w") as f:
                yaml.dump(config_data, f)

            config = load_config(str(config_path))
            assert len(config.model_pool.instances) == 1
            assert config.model_pool.instances[0].name == "test-model"
            assert config.model_pool.instances[0].device == "cpu"
            assert config.model_pool.instances[0].backend == "pytorch"

    def test_load_config_multi_model(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "test.yaml"
            config_data = {
                "model_pool": {
                    "instances": [
                        {"name": "model1", "device": "cpu"},
                        {"name": "model2", "device": "mps"},
                    ]
                }
            }
            with open(config_path, "w") as f:
                yaml.dump(config_data, f)

            config = load_config(str(config_path))
            assert len(config.model_pool.instances) == 2
            assert config.model_pool.instances[0].name == "model1"
            assert config.model_pool.instances[1].name == "model2"

    def test_load_config_with_base_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_config_path = Path(tmpdir) / "base_config.yaml"
            config_path = Path(tmpdir) / "test.yaml"

            base_config = {
                "model": {"name": "base-model", "device": "mps"},
                "server": {"grpc_port": 50051},
            }
            exp_config = {
                "model": {"name": "override-model"},
                "name": "test-experiment",
            }

            with open(base_config_path, "w") as f:
                yaml.dump(base_config, f)
            with open(config_path, "w") as f:
                yaml.dump(exp_config, f)

            config = load_config(str(config_path))
            assert config.model_pool.instances[0].name == "override-model"
            assert config.server.grpc_port == 50051
            assert config.name == "test-experiment"

    def test_load_config_batching(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "test.yaml"
            config_data = {
                "batching": {
                    "enabled": True,
                    "max_batch_size": 16,
                    "timeout_ms": 200,
                    "length_aware": True,
                }
            }
            with open(config_path, "w") as f:
                yaml.dump(config_data, f)

            config = load_config(str(config_path))
            assert config.batching.enabled is True
            assert config.batching.max_batch_size == 16
            assert config.batching.timeout_ms == 200
            assert config.batching.length_aware is True

    def test_load_config_tokenizer_pool(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "test.yaml"
            config_data = {
                "tokenizer_pool": {
                    "enabled": True,
                    "num_workers": 3,
                    "model_name": "tokenizer-model",
                }
            }
            with open(config_path, "w") as f:
                yaml.dump(config_data, f)

            config = load_config(str(config_path))
            assert config.tokenizer_pool.enabled is True
            assert config.tokenizer_pool.num_workers == 3
            assert config.tokenizer_pool.model_name == "tokenizer-model"

    def test_load_config_server(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "test.yaml"
            config_data = {
                "server": {
                    "host": "127.0.0.1",
                    "grpc_port": 60000,
                    "http_port": 9000,
                    "grpc_workers": 20,
                }
            }
            with open(config_path, "w") as f:
                yaml.dump(config_data, f)

            config = load_config(str(config_path))
            assert config.server.host == "127.0.0.1"
            assert config.server.grpc_port == 60000
            assert config.server.http_port == 9000
            assert config.server.grpc_workers == 20

    def test_load_config_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_config("nonexistent.yaml")

    def test_get_experiment_name_from_config(self):
        from src.server.dto.config import Config

        config = Config(name="my-experiment")
        name = get_experiment_name(config, "path/to/config.yaml")
        assert name == "my-experiment"

    def test_get_experiment_name_from_filename(self):
        from src.server.dto.config import Config

        config = Config()
        name = get_experiment_name(config, "experiments/07a_test.yaml")
        assert name == "07a_test"

    def test_load_config_defaults(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "test.yaml"
            config_data = {}
            with open(config_path, "w") as f:
                yaml.dump(config_data, f)

            config = load_config(str(config_path))

            assert len(config.model_pool.instances) == 1
            assert config.batching.enabled is False
            assert config.server.grpc_port == 50051
