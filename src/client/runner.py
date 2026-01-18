import asyncio
import logging
import time
from collections.abc import Callable

from tqdm import tqdm

from src.client.grpc_client import AsyncInferenceClient
from src.server.dto import BenchmarkState

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    def __init__(self, client: AsyncInferenceClient, state: BenchmarkState):
        self.client = client
        self.state = state

    async def run(
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

        # Async semaphore to limit concurrency
        semaphore = asyncio.Semaphore(concurrency)

        async def run_batch(batch):
            if self.state.interrupted:
                return None

            async with semaphore:
                # Double check interruption
                if self.state.interrupted:
                    return None

                await self.client.infer(batch)
                completed[0] += 1
            return 1

        await self._execute_batches(batches, run_batch, num_requests, start, completed)

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

    async def _execute_batches(
        self,
        batches: list,
        run_batch: Callable,
        num_requests: int,
        start_time: float,
        completed: list,
    ):
        pbar = tqdm(total=num_requests, desc="Benchmarking", unit="req", ncols=80, leave=False)
        last_completed = 0

        # Create tasks
        tasks = [asyncio.create_task(run_batch(batch)) for batch in batches]

        try:
            # We want to update progress bar as tasks complete
            # asyncio.as_completed is good, but we also want to support interruption and timeouts

            for f in asyncio.as_completed(tasks):
                await f

                if self.state.interrupted:
                    break

                if time.perf_counter() - start_time > 60.0:
                    # Soft timeout to prevent hangs
                    break

                current = completed[0]
                if current > last_completed:
                    pbar.update(current - last_completed)
                    last_completed = current

        finally:
            # Cancel any pending tasks if we exited early
            for t in tasks:
                if not t.done():
                    t.cancel()

            # Wait for cancellations to propagate
            await asyncio.gather(*tasks, return_exceptions=True)

            final = completed[0]
            if final > last_completed:
                pbar.update(final - last_completed)
            pbar.close()
