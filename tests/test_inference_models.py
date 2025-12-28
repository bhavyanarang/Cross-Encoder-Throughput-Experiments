"""Tests for inference models."""

import numpy as np

from src.models.inference import InferenceResult, WorkItem, WorkResult


class TestInferenceResult:
    def test_inference_result_basic(self):
        """Test InferenceResult with basic fields."""
        scores = np.array([0.5, 0.8, 0.3])
        result = InferenceResult(scores=scores)
        assert np.array_equal(result.scores, scores)
        assert result.t_tokenize_ms == 0.0
        assert result.total_ms == 0.0

    def test_inference_result_all_fields(self):
        """Test InferenceResult with all fields."""
        scores = np.array([0.5, 0.8])
        result = InferenceResult(
            scores=scores,
            t_tokenize_ms=5.0,
            t_model_inference_ms=10.0,
            t_queue_wait_ms=2.0,
            t_overhead_ms=1.0,
            t_mp_queue_send_ms=0.5,
            t_mp_queue_receive_ms=1.5,
            t_grpc_serialize_ms=0.3,
            t_grpc_deserialize_ms=0.2,
            t_scheduler_ms=0.1,
            total_ms=21.6,
            total_tokens=100,
            real_tokens=80,
            padded_tokens=20,
            padding_ratio=0.2,
            max_seq_length=512,
            avg_seq_length=400.0,
            batch_size=2,
            worker_id=0,
        )
        assert result.t_tokenize_ms == 5.0
        assert result.t_model_inference_ms == 10.0
        assert result.total_ms == 21.6
        assert result.batch_size == 2
        assert result.worker_id == 0


class TestWorkItem:
    def test_work_item_creation(self):
        """Test WorkItem creation."""

        # Mock tokenized batch
        class MockTokenizedBatch:
            pass

        tokenized_batch = MockTokenizedBatch()
        item = WorkItem(req_id=123, tokenized_batch=tokenized_batch)
        assert item.req_id == 123
        assert item.tokenized_batch == tokenized_batch


class TestWorkResult:
    def test_work_result_basic(self):
        """Test WorkResult with basic fields."""
        scores = np.array([0.5, 0.8])
        result = WorkResult(
            req_id=123,
            scores=scores,
            worker_id=0,
        )
        assert result.req_id == 123
        assert np.array_equal(result.scores, scores)
        assert result.worker_id == 0

    def test_work_result_all_fields(self):
        """Test WorkResult with all fields."""
        scores = np.array([0.5, 0.8])
        result = WorkResult(
            req_id=123,
            scores=scores,
            worker_id=0,
            t_tokenize_ms=5.0,
            t_model_inference_ms=10.0,
            t_queue_wait_ms=2.0,
            total_ms=17.0,
            total_tokens=100,
            real_tokens=80,
            padded_tokens=20,
            padding_ratio=0.2,
            max_seq_length=512,
            avg_seq_length=400.0,
            batch_size=2,
        )
        assert result.req_id == 123
        assert result.t_tokenize_ms == 5.0
        assert result.total_ms == 17.0
        assert result.batch_size == 2
