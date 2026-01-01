import pytest

from src.server.dto import ModelConfig, PoolConfig
from src.server.pool.model_pool import ModelPool


class TestModelPool:
    def test_model_pool_init(self):
        config = PoolConfig(
            instances=[
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
            ]
        )
        pool = ModelPool(config)
        assert pool.config == config
        assert pool.num_workers == 2
        assert pool.is_loaded is False

    def test_model_pool_len(self):
        config = PoolConfig(
            instances=[
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
            ]
        )
        pool = ModelPool(config)
        assert len(pool) == 1

    def test_model_pool_get_info(self):
        config = PoolConfig(
            instances=[
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
            ]
        )
        pool = ModelPool(config)
        info = pool.get_info()
        assert info["num_instances"] == 1
        assert info["is_loaded"] is False
        assert isinstance(info["request_counts"], dict)

    def test_model_pool_get_gpu_memory_not_started(self):
        config = PoolConfig(
            instances=[
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
            ]
        )
        pool = ModelPool(config)
        memory = pool.get_gpu_memory_mb()
        assert memory == 0.0

    def test_model_pool_submit_not_started(self):
        config = PoolConfig(
            instances=[
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
            ]
        )
        pool = ModelPool(config)

        class MockWorkItem:
            pass

        work_item = MockWorkItem()
        with pytest.raises(RuntimeError, match="not started"):
            pool.submit(work_item)

    def test_model_pool_stop_not_started(self):
        config = PoolConfig(
            instances=[
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
            ]
        )
        pool = ModelPool(config)

        pool.stop()
