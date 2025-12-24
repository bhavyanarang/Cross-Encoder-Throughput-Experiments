"""Tests for backend implementations."""

import numpy as np

from ml_inference_server.backends import create_backend
from ml_inference_server.core.config import ModelInstanceConfig


class TestBackends:
    """Test backend functionality."""

    def test_backend_creation(self):
        """Test that backends can be created from config."""
        config = ModelInstanceConfig(
            name="cross-encoder/ms-marco-MiniLM-L-6-v2",
            backend="pytorch",
            device="cpu",
        )
        backend = create_backend(config)
        assert backend is not None
        assert backend.device == "cpu"
        assert backend.model_name == "cross-encoder/ms-marco-MiniLM-L-6-v2"

    def test_backend_inference(self):
        """Test basic inference functionality."""
        config = ModelInstanceConfig(
            name="cross-encoder/ms-marco-MiniLM-L-6-v2",
            backend="pytorch",
            device="cpu",
        )
        backend = create_backend(config)

        # Load the model before inference
        backend.load_model()

        # Test pairs
        pairs = [
            ("What is Python?", "Python is a programming language"),
            ("What is ML?", "Machine learning is a subset of AI"),
        ]

        # Run inference
        scores = backend.infer(pairs)

        # Check results
        assert isinstance(scores, np.ndarray)
        assert len(scores) == len(pairs)
        assert all(isinstance(s, (float, np.floating)) for s in scores)
