"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_pairs():
    """Sample query-document pairs for testing."""
    return [
        ("What is Python?", "Python is a programming language"),
        ("What is machine learning?", "Machine learning is a subset of artificial intelligence"),
        ("What is deep learning?", "Deep learning uses neural networks with multiple layers"),
    ]


@pytest.fixture
def model_config():
    """Sample model configuration."""
    from ml_inference_server.core.config import ModelInstanceConfig

    return ModelInstanceConfig(
        name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        backend="pytorch",
        device="cpu",
    )
