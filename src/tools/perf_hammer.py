#!/usr/bin/env python3

import argparse
import asyncio
import logging
import math
import signal
import sys
import threading
import time
from collections import deque
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import json

from src.client.grpc_client import AsyncInferenceClient


class DataLoader:
    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or Path(__file__).resolve().parents[2] / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load(self, num_samples: int = 1000) -> list:
        cache_file = self.cache_dir / f"msmarco_pairs_{num_samples}.json"

        if cache_file.exists():
            with open(cache_file) as f:
                pairs = json.load(f)
            return [(p[0], p[1]) for p in pairs]

        return self._create_synthetic(num_samples)

    def _create_synthetic(self, num_samples: int) -> list:
        return [(f"query {i}", f"document {i} with some text content") for i in range(num_samples)]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class PerfHammer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 50051,
        concurrency: int = 256,
        batch_size: int = 64,
        duration: float | None = None,
        num_requests: int | None = None,
        target_rps: float | None = None,
    ):
        self.host = host
        self.port = port
        self.concurrency = concurrency
        self.batch_size = batch_size
        self.duration = duration
        self.num_requests = num_requests
        self.target_rps = target_rps
        self.running = True

        self.latencies: list[float] = []
        self.throughputs: list[float] = []
        self.errors: list[str] = []
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.request_count = 0

        self.recent_latencies = deque(maxlen=100)
        self.recent_throughputs = deque(maxlen=100)

        # Signal handling setup in run()
        self.loop = None

    def _create_batch(self, pairs: list[tuple[str, str]], index: int) -> list[tuple[str, str]]:
        start_idx = (index * self.batch_size) % len(pairs)
        batch = pairs[start_idx : start_idx + self.batch_size]
        if len(batch) < self.batch_size:
            batch = batch + pairs[: self.batch_size - len(batch)]
        return batch

    async def _send_request(
        self, client: AsyncInferenceClient, batch: list[tuple[str, str]]
    ) -> tuple[bool, float, float]:
        try:
            _, latency_ms = await client.infer(batch, timeout=120.0)
            throughput = self.batch_size / (latency_ms / 1000.0) if latency_ms > 0 else 0
            return True, latency_ms, throughput
        except Exception:
            return False, 0.0, 0.0

    async def _worker(
        self, client: AsyncInferenceClient, pairs: list[tuple[str, str]], worker_id: int
    ) -> None:
        request_idx = worker_id
        while self.running:
            loop_start = time.perf_counter()
            if self.duration and self.start_time:
                if time.perf_counter() - self.start_time >= self.duration:
                    break

            if self.num_requests:
                if self.request_count >= self.num_requests:
                    break

            batch = self._create_batch(pairs, request_idx)

            # Fire the request
            # In target_rps mode, we wait for response too (to measure latency),
            # but we use sleep to maintain rate if we are too fast.
            # If we are too slow (server overload), we fall behind.
            # To strictly force rate, we would need to fire-and-forget, but then we lose tracking.
            # For "Incoming RPS", if we have enough concurrency, we can sustain rate even if individual requests are slow.

            success, latency_ms, throughput = await self._send_request(client, batch)

            self.request_count += 1
            if success:
                self.latencies.append(latency_ms)
                self.throughputs.append(throughput)
                self.recent_latencies.append(latency_ms)
                self.recent_throughputs.append(throughput)
            else:
                self.errors.append(f"Request {request_idx} failed")

            request_idx += self.concurrency

            # Rate limiting logic per worker
            if self.target_rps:
                # Target RPS is total, so per worker it is target_rps / concurrency
                rps_per_worker = self.target_rps / self.concurrency
                interval = 1.0 / rps_per_worker
                elapsed = time.perf_counter() - loop_start
                if elapsed < interval:
                    await asyncio.sleep(interval - elapsed)

            # Yield to event loop
            await asyncio.sleep(0)

    async def _monitor(self):
        last_stats_time = time.perf_counter()
        while self.running:
            await asyncio.sleep(0.5)

            if self.duration:
                if time.perf_counter() - self.start_time >= self.duration:
                    self.running = False
                    break
            elif self.num_requests:
                if self.request_count >= self.num_requests:
                    self.running = False
                    break

            if time.perf_counter() - last_stats_time >= 10.0:
                self._print_stats()
                last_stats_time = time.perf_counter()

    def _get_percentile(self, data, p):
        if not data:
            return 0.0
        data = sorted(data)
        k = (len(data) - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return data[int(k)]
        d0 = data[int(f)] * (c - k)
        d1 = data[int(c)] * (k - f)
        return d0 + d1

    def _mean(self, data):
        if not data:
            return 0.0
        return sum(data) / len(data)

    def _print_stats(self):
        if not self.latencies:
            return

        elapsed = time.perf_counter() - self.start_time if self.start_time else 0
        total_requests = len(self.latencies)
        total_pairs = total_requests * self.batch_size
        total_errors = len(self.errors)

        if elapsed > 0:
            current_qps = total_requests / elapsed
            current_throughput = total_pairs / elapsed
        else:
            current_qps = 0
            current_throughput = 0

        recent_lat = list(self.recent_latencies) if self.recent_latencies else self.latencies

        logger.info(
            f"Stats: {total_requests} requests ({total_pairs} pairs) | "
            f"QPS: {current_qps:.1f} | Throughput: {current_throughput:.1f} p/s | "
            f"Latency: {self._mean(recent_lat):.1f}ms (P50: {self._get_percentile(recent_lat, 50):.1f}ms) | "
            f"Errors: {total_errors}"
        )

    async def run_async(self):
        pairs = self._load_test_data()

        logger.info(
            f"\n{'=' * 80}\n"
            f"Performance Hammer (Async)\n"
            f"{'=' * 80}\n"
            f"Concurrency: {self.concurrency}\n"
            f"Batch size: {self.batch_size}\n"
            f"Target RPS: {self.target_rps or 'Unlimited'}\n"
            f"Duration: {self.duration}s\n"
            if self.duration
            else f"Requests: {self.num_requests}\n{'=' * 80}\n"
        )

        self.start_time = time.perf_counter()

        # Setup Async Client
        async with AsyncInferenceClient(host=self.host, port=self.port) as client:
            tasks = []
            for i in range(self.concurrency):
                tasks.append(asyncio.create_task(self._worker(client, pairs, i)))

            monitor_task = asyncio.create_task(self._monitor())

            try:
                # Wait for monitor to finish
                await monitor_task
            except asyncio.CancelledError:
                pass
            finally:
                self.running = False

            # Cancel workers
            for t in tasks:
                t.cancel()

            # Wait for workers to clean up
            await asyncio.gather(*tasks, return_exceptions=True)

        self.end_time = time.perf_counter()
        self._print_final_stats()

    def _load_test_data(self) -> list[tuple[str, str]]:
        logger.info("Loading test data...")
        loader = DataLoader()
        pairs = loader.load(10000)
        logger.info(f"Loaded {len(pairs)} query-document pairs")
        return pairs

    def _print_final_stats(self):
        if not self.latencies:
            logger.warning("No successful requests completed")
            return

        elapsed = self.end_time - self.start_time if self.end_time and self.start_time else 0
        total_requests = len(self.latencies)
        total_pairs = total_requests * self.batch_size
        total_errors = len(self.errors)

        logger.info(
            f"\n{'=' * 80}\n"
            f"Final Statistics\n"
            f"{'=' * 80}\n"
            f"Duration: {elapsed:.2f}s\n"
            f"Total requests: {total_requests}\n"
            f"Total pairs: {total_pairs}\n"
            f"Errors: {total_errors}\n"
            f"\nThroughput:\n"
            f"  Average: {total_pairs / elapsed:.1f} pairs/sec\n"
            f"  Per-request avg: {self._mean(self.throughputs):.1f} pairs/sec\n"
            f"  Per-request P95: {self._get_percentile(self.throughputs, 95):.1f} pairs/sec\n"
            f"\nLatency:\n"
            f"  Average: {self._mean(self.latencies):.1f}ms\n"
            f"  Min: {min(self.latencies):.1f}ms\n"
            f"  Max: {max(self.latencies):.1f}ms\n"
            f"  P50: {self._get_percentile(self.latencies, 50):.1f}ms\n"
            f"  P95: {self._get_percentile(self.latencies, 95):.1f}ms\n"
            f"  P99: {self._get_percentile(self.latencies, 99):.1f}ms\n"
            f"{'=' * 80}\n"
        )

    def stats_snapshot(self) -> dict | None:
        if not self.start_time:
            return None

        now = self.end_time or time.perf_counter()
        elapsed = max(now - self.start_time, 0.0)
        total_requests = len(self.latencies)
        total_pairs = total_requests * self.batch_size
        total_errors = len(self.errors)

        if elapsed > 0:
            current_qps = total_requests / elapsed
            current_throughput = total_pairs / elapsed
        else:
            current_qps = 0.0
            current_throughput = 0.0

        recent_lat = list(self.recent_latencies) if self.recent_latencies else self.latencies

        return {
            "elapsed_s": elapsed,
            "total_requests": total_requests,
            "total_pairs": total_pairs,
            "errors": total_errors,
            "qps": current_qps,
            "throughput": current_throughput,
            "lat_avg_ms": self._mean(recent_lat),
            "lat_p50_ms": self._get_percentile(recent_lat, 50),
            "lat_p95_ms": self._get_percentile(recent_lat, 95),
            "lat_p99_ms": self._get_percentile(recent_lat, 99),
            "running": self.running,
        }

    def stop(self) -> None:
        self.running = False

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        def signal_handler():
            logger.info("\nInterrupt received, stopping...")
            self.running = False
            for task in asyncio.all_tasks(self.loop):
                task.cancel()

        if threading.current_thread() is threading.main_thread():
            try:
                self.loop.add_signal_handler(signal.SIGINT, signal_handler)
                self.loop.add_signal_handler(signal.SIGTERM, signal_handler)
            except (NotImplementedError, RuntimeError, ValueError):
                try:
                    signal.signal(signal.SIGINT, lambda s, f: signal_handler())
                    signal.signal(signal.SIGTERM, lambda s, f: signal_handler())
                except ValueError:
                    pass

        try:
            self.loop.run_until_complete(self.run_async())
        except KeyboardInterrupt:
            signal_handler()
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
        finally:
            try:
                pending = asyncio.all_tasks(self.loop)
                for task in pending:
                    task.cancel()
                self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                self.loop.close()
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser(
        description="Performance Hammer - High-concurrency stress testing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--host", default="localhost", help="Server hostname")
    parser.add_argument("--port", type=int, default=50051, help="Server port")
    parser.add_argument("--concurrency", type=int, default=256, help="Concurrency")
    parser.add_argument("--batch-size", type=int, default=64, help="Pairs per request")
    parser.add_argument("--duration", type=float, default=None, help="Run duration in seconds")
    parser.add_argument("--requests", type=int, default=None, help="Total number of requests")
    parser.add_argument("--target-rps", type=float, default=None, help="Target RPS (total)")

    args = parser.parse_args()

    if not args.duration and not args.requests:
        args.duration = 60.0
        logger.info("No duration or requests specified, defaulting to 60 seconds")

    hammer = PerfHammer(
        host=args.host,
        port=args.port,
        concurrency=args.concurrency,
        batch_size=args.batch_size,
        duration=args.duration,
        num_requests=args.requests,
        target_rps=args.target_rps,
    )

    hammer.run()


if __name__ == "__main__":
    main()
