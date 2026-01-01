import gc
import sys
import threading
import time
import weakref
from pathlib import Path

import pytest

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))


_orchestrator_registry = weakref.WeakSet()


def register_orchestrator(orchestrator):
    """Register an orchestrator for automatic cleanup."""
    _orchestrator_registry.add(orchestrator)


def create_orchestrator(*args, **kwargs):
    """Create and register an orchestrator for automatic cleanup."""
    from src.server.services.orchestrator_service import OrchestratorService

    orchestrator = OrchestratorService(*args, **kwargs)
    register_orchestrator(orchestrator)
    return orchestrator


def ensure_orchestrator_cleanup(orchestrator):
    """Clean up an orchestrator and wait for threads to finish."""
    if orchestrator is None:
        return

    try:
        orchestrator.stop()
    except Exception:
        pass

    if hasattr(orchestrator, "_batch_thread") and orchestrator._batch_thread:
        if orchestrator._batch_thread.is_alive():
            orchestrator._batch_thread.join(timeout=2.0)

    time.sleep(0.05)


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


@pytest.fixture
def minimal_config():
    from src.server.dto import Config, ModelConfig, PoolConfig, TokenizerPoolConfig

    return Config(
        model_pool=PoolConfig(
            instances=[ModelConfig(name="cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")]
        ),
        tokenizer_pool=TokenizerPoolConfig(enabled=True, num_workers=1),
    )


@pytest.fixture
def orchestrator_with_batching(minimal_config):
    from src.server.dto import BatchConfig
    from src.server.services.orchestrator_service import OrchestratorService

    minimal_config.batching = BatchConfig(enabled=True, max_batch_size=8, timeout_ms=100.0)
    orchestrator = OrchestratorService(minimal_config, "test")
    orchestrator.setup()
    yield orchestrator
    ensure_orchestrator_cleanup(orchestrator)


@pytest.fixture
def orchestrator_without_batching(minimal_config):
    from src.server.dto import BatchConfig
    from src.server.services.orchestrator_service import OrchestratorService

    minimal_config.batching = BatchConfig(enabled=False)
    orchestrator = OrchestratorService(minimal_config, "test")
    orchestrator.setup()
    yield orchestrator
    ensure_orchestrator_cleanup(orchestrator)


@pytest.fixture(autouse=True)
def auto_register_orchestrators():
    """Automatically register orchestrators when setup() is called (like @BeforeEach in Java)."""
    from src.server.services.orchestrator_service import OrchestratorService

    original_setup = OrchestratorService.setup

    def setup_with_registration(self):
        result = original_setup(self)
        register_orchestrator(self)
        return result

    OrchestratorService.setup = setup_with_registration
    yield
    OrchestratorService.setup = original_setup


@pytest.fixture(autouse=True)
def ensure_cleanup():
    """Automatically clean up orchestrators and threads after each test (like @AfterEach in Java)."""
    yield

    for orchestrator in list(_orchestrator_registry):
        try:
            ensure_orchestrator_cleanup(orchestrator)
        except Exception:
            pass

    gc.collect()

    try:
        from src.server.services.orchestrator_service import OrchestratorService

        for obj in gc.get_objects():
            if isinstance(obj, OrchestratorService):
                try:
                    if hasattr(obj, "_tokenization_started") and (
                        obj._tokenization_started
                        or hasattr(obj, "_batch_thread")
                        and obj._batch_thread
                    ):
                        ensure_orchestrator_cleanup(obj)
                except Exception:
                    pass
    except Exception:
        pass

    threads = [t for t in threading.enumerate() if t.is_alive() and t != threading.current_thread()]
    if threads:
        for t in threads:
            if hasattr(t, "name") and ("batch" in t.name.lower() or "pool" in t.name.lower()):
                if t.is_alive():
                    t.join(timeout=0.5)

    time.sleep(0.1)
