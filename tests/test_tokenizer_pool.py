import pytest

from src.server.pool.tokenizer_pool import TokenizerPool


class TestTokenizerPool:
    def test_tokenizer_pool_init(self):
        pool = TokenizerPool(
            model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
            num_workers=2,
            max_length=512,
        )
        assert pool.model_name == "cross-encoder/ms-marco-MiniLM-L-6-v2"
        assert pool.num_workers == 2
        assert pool.max_length == 512
        assert pool.is_loaded is False

    def test_tokenizer_pool_get_info(self):
        pool = TokenizerPool(
            model_name="test-model",
            num_workers=3,
            max_length=256,
        )
        info = pool.get_info()
        assert info["model_name"] == "test-model"
        assert info["num_workers"] == 3
        assert info["is_loaded"] is False
        assert len(info["queue_sizes"]) == 3
        assert info["total_queue_size"] == 0

    def test_tokenizer_pool_len(self):
        pool = TokenizerPool(
            model_name="test-model",
            num_workers=5,
            max_length=512,
        )
        assert len(pool) == 5

    def test_tokenizer_pool_submit_not_started(self):
        from src.server.dto.pipeline import TokenizationQueueItem

        pool = TokenizerPool(
            model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
            num_workers=1,
            max_length=512,
        )

        class MockRequest:
            pass

        tokenization_item = TokenizationQueueItem(
            request=MockRequest(),
            pairs=[("query", "document")],
        )

        with pytest.raises(RuntimeError, match="not started"):
            pool.submit(tokenization_item)
