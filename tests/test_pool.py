"""Tests for model pool."""

import pytest

from src.models import ModelConfig, PoolConfig
from src.server.pool import ModelPool


class TestModelPool:
    def test_model_pool_init(self):
        """Test ModelPool initialization."""
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
        """Test pool length."""
        config = PoolConfig(
            instances=[
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
            ]
        )
        pool = ModelPool(config)
        assert len(pool) == 1

    def test_model_pool_get_info(self):
        """Test getting pool info."""
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
        """Test get_gpu_memory_mb when pool not started."""
        config = PoolConfig(
            instances=[
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
            ]
        )
        pool = ModelPool(config)
        memory = pool.get_gpu_memory_mb()
        assert memory == 0.0

    def test_model_pool_infer_with_tokenized_not_started(self):
        """Test infer_with_tokenized raises error when pool not started."""
        config = PoolConfig(
            instances=[
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
            ]
        )
        pool = ModelPool(config)

        # Create a mock tokenized batch
        class MockTokenizedBatch:
            pass

        tokenized_batch = MockTokenizedBatch()
        with pytest.raises(RuntimeError, match="not started"):
            pool.infer_with_tokenized(tokenized_batch)

    def test_model_pool_stop_not_started(self):
        """Test stop when pool not started."""
        config = PoolConfig(
            instances=[
                ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu"),
            ]
        )
        pool = ModelPool(config)
        # Should not raise
        pool.stop()
