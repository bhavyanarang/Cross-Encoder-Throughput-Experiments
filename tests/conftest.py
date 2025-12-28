import sys
from pathlib import Path

import pytest

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))


@pytest.fixture
def sample_pairs():
    return [
        ("What is Python?", "Python is a programming language"),
        ("What is ML?", "Machine learning is AI"),
    ]


@pytest.fixture
def model_config():
    from src.server.dto import ModelConfig

    return ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", backend="pytorch", device="cpu")
