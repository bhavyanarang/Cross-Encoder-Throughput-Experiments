import threading
import time

import numpy as np

from src.server.models import InferenceResult
from src.server.models.scheduler import PendingRequest
from src.server.services.scheduler_service import SchedulerService


class TestPendingRequest:
    def test_pending_request_creation(self):
        event = threading.Event()
        pairs = [("query", "document")]
        req = PendingRequest(pairs=pairs, result_future=event, submit_time=time.perf_counter())
        assert req.pairs == pairs
        assert req.result_future == event
        assert req.result is None


class TestScheduler:
    def test_scheduler_creation(self):
        class MockPool:
            pass

        class MockTokenizationService:
            pass

        class MockInferenceService:
            pass

        scheduler = SchedulerService(MockTokenizationService(), MockInferenceService())
        assert scheduler is not None

    def test_scheduler_info(self):
        class MockPool:
            pass

        class MockTokenizationService:
            pass

        class MockInferenceService:
            pass

        scheduler = SchedulerService(
            MockTokenizationService(),
            MockInferenceService(),
            batching_enabled=True,
            max_batch_size=16,
            timeout_ms=100,
            length_aware=True,
        )
        info = scheduler.get_info()
        assert info["batching_enabled"] is True
        assert info["max_batch_size"] == 16
        assert info["timeout_ms"] == 100
        assert info["length_aware"] is True

    def test_scheduler_non_batching(self):
        class MockPool:
            pass

        class MockTokenizationService:
            def tokenize_sync(self, pairs):
                from src.server.models.inference import TokenizedBatch

                class MockTokenizedBatch(TokenizedBatch):
                    def __init__(self):
                        self.features = {}
                        self.tokenize_time_ms = 5.0
                        self.total_tokens = 100
                        self.real_tokens = 100
                        self.padded_tokens = 0
                        self.padding_ratio = 0.0
                        self.max_seq_length = 512
                        self.avg_seq_length = 256.0

                return MockTokenizedBatch()

        class MockInferenceService:
            def infer_sync(self, tokenized_batch):
                return InferenceResult(
                    scores=np.array([0.5, 0.8]),
                    t_model_inference_ms=10.0,
                    total_ms=15.0,
                )

        scheduler = SchedulerService(
            MockTokenizationService(),
            MockInferenceService(),
            batching_enabled=False,
        )
        result = scheduler.schedule([("query", "document")])
        assert isinstance(result, InferenceResult)
        assert len(result.scores) == 2

    def test_scheduler_stop(self):
        class MockPool:
            pass

        class MockTokenizationService:
            pass

        class MockInferenceService:
            pass

        scheduler = SchedulerService(
            MockTokenizationService(),
            MockInferenceService(),
            batching_enabled=True,
        )

        scheduler.stop()
