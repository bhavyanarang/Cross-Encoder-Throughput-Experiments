"""Tests for backends."""

import numpy as np

from src.server.backends import create_backend


class TestBackends:
    def test_backend_creation(self, model_config):
        backend = create_backend(model_config)
        assert backend is not None
        assert backend.model_name == model_config.name

    def test_backend_inference(self, model_config, sample_pairs):
        backend = create_backend(model_config)
        backend.load_model()
        scores = backend.infer(sample_pairs)
        assert isinstance(scores, np.ndarray)
        assert scores.shape == (len(sample_pairs),)
