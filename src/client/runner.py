import logging
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

from src.client.grpc_client import InferenceClient
from src.server.dto import BenchmarkState

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    def __init__(self, client: InferenceClient, state: BenchmarkState):
        self.client = client
        self.state = state

    def run(
        self,
        pairs: list,
        batch_size: int,
        num_requests: int,
        concurrency: int = 1,
    ) -> dict:
        logger.info(
            f"Starting benchmark: {num_requests} requests, "
            f"concurrency={concurrency}, batch_size={batch_size}"
        )

        batches = self._prepare_batches(pairs, batch_size, num_requests)

        start = time.perf_counter()
        completed = [0]

        def run_batch(batch):
            if self.state.interrupted:
                return None

            _, _ = self.client.infer(batch)
            completed[0] += 1
            return 1

        self._execute_batches(batches, run_batch, concurrency, completed, num_requests, start)

        elapsed = time.perf_counter() - start

        if completed[0] == 0:
            return {"error": "No requests completed", "interrupted": True}

        return {
            "batch_size": batch_size,
            "concurrency": concurrency,
            "num_requests": completed[0],
            "total_pairs": completed[0] * batch_size,
            "total_time_s": elapsed,
            "status": "completed",
            "interrupted": self.state.interrupted,
        }

    def _prepare_batches(self, pairs: list, batch_size: int, num_requests: int) -> list:
        batches = []
        for i in range(num_requests):
            start_idx = (i * batch_size) % len(pairs)
            batch = pairs[start_idx : start_idx + batch_size]
            if len(batch) < batch_size:
                batch = batch + pairs[: batch_size - len(batch)]
            batches.append(batch)
        return batches

    def _execute_batches(
        self,
        batches: list,
        run_batch: Callable,
        concurrency: int,
        completed: list,
        num_requests: int,
        start_time: float = None,
    ):
        if start_time is None:
            start_time = time.perf_counter()

        pbar = tqdm(total=num_requests, desc="Benchmarking", unit="req", ncols=80, leave=False)
        last_completed = 0

        try:
            if concurrency == 1:
                for batch in batches:
                    if self.state.interrupted:
                        break

                    if time.perf_counter() - start_time > 60.0:
                        break
                    run_batch(batch)

                    current = completed[0]
                    if current > last_completed:
                        pbar.update(current - last_completed)
                        last_completed = current
            else:
                with ThreadPoolExecutor(max_workers=concurrency) as executor:
                    futures = [executor.submit(run_batch, batch) for batch in batches]
                    for _f in as_completed(futures):
                        if self.state.interrupted:
                            break

                        if time.perf_counter() - start_time > 60.0:
                            break

                        current = completed[0]
                        if current > last_completed:
                            pbar.update(current - last_completed)
                            last_completed = current
        finally:
            final = completed[0]
            if final > last_completed:
                pbar.update(final - last_completed)
            pbar.close()
