import gc
import sys
import threading
import time
import weakref
from pathlib import Path

import pytest
from prometheus_client import REGISTRY

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))


def _clear_prometheus_registry():
    collectors_to_remove = []
    for collector in REGISTRY._names_to_collectors.values():
        if (
            hasattr(collector, "_name")
            and not collector._name.startswith("python_")
            and not collector._name.startswith("process_")
        ):
            collectors_to_remove.append(collector)
    for collector in collectors_to_remove:
        try:
            REGISTRY.unregister(collector)
        except Exception:
            pass


@pytest.fixture(autouse=True)
def cleanup_prometheus_registry():
    _clear_prometheus_registry()
    yield
    _clear_prometheus_registry()


_orchestrator_registry = weakref.WeakSet()


def register_orchestrator(orchestrator):
    _orchestrator_registry.add(orchestrator)


def create_orchestrator(*args, **kwargs):
    from src.server.services.orchestrator_service import OrchestratorService

    orchestrator = OrchestratorService(*args, **kwargs)
    register_orchestrator(orchestrator)
    return orchestrator


def ensure_orchestrator_cleanup(orchestrator):
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
