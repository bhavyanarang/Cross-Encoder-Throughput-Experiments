"""Tests for scheduler."""


class TestScheduler:
    def test_scheduler_creation(self):
        from src.server.scheduler import Scheduler

        # Mock pool
        class MockPool:
            def infer(self, pairs):
                import numpy as np

                from src.models import InferenceResult

                return InferenceResult(scores=np.zeros(len(pairs)))

        scheduler = Scheduler(MockPool())
        assert scheduler is not None

    def test_scheduler_info(self):
        from src.server.scheduler import Scheduler

        class MockPool:
            pass

        scheduler = Scheduler(MockPool(), batching_enabled=True, max_batch_size=16)
        info = scheduler.get_info()
        assert info["batching_enabled"] is True
        assert info["max_batch_size"] == 16
