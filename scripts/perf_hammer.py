#!/usr/bin/env python3

import argparse
import logging
import signal
import sys
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import numpy as np

sys.path.insert(0, str(__file__).replace("/scripts/perf_hammer.py", ""))

import json
from pathlib import Path

from src.client.grpc_client import InferenceClient


class DataLoader:
    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or Path(__file__).parent.parent / ".cache"
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
    ):
        self.client = InferenceClient(host=host, port=port)
        self.concurrency = concurrency
        self.batch_size = batch_size
        self.duration = duration
        self.num_requests = num_requests
        self.running = True
        self.stats_lock = Lock()

        self.latencies: list[float] = []
        self.throughputs: list[float] = []
        self.errors: list[str] = []
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.request_count = 0

        self.recent_latencies = deque(maxlen=100)
        self.recent_throughputs = deque(maxlen=100)

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        logger.info("\nInterrupt received, stopping...")
        self.running = False

    def _load_test_data(self) -> list[tuple[str, str]]:
        logger.info("Loading test data...")
        loader = DataLoader()
        pairs = loader.load(10000)
        logger.info(f"Loaded {len(pairs)} query-document pairs")
        return pairs

    def _create_batch(self, pairs: list[tuple[str, str]], index: int) -> list[tuple[str, str]]:
        start_idx = (index * self.batch_size) % len(pairs)
        batch = pairs[start_idx : start_idx + self.batch_size]
        if len(batch) < self.batch_size:
            batch = batch + pairs[: self.batch_size - len(batch)]
        return batch

    def _send_request(self, batch: list[tuple[str, str]]) -> tuple[bool, float, float]:
        try:
            _, latency_ms = self.client.infer(batch, timeout=120.0)
            throughput = self.batch_size / (latency_ms / 1000.0) if latency_ms > 0 else 0
            return True, latency_ms, throughput
        except Exception:
            return False, 0.0, 0.0

    def _worker(self, pairs: list[tuple[str, str]], request_id: int) -> None:
        while self.running:
            if self.duration and self.start_time:
                if time.perf_counter() - self.start_time >= self.duration:
                    break

            batch = self._create_batch(pairs, request_id)
            success, latency_ms, throughput = self._send_request(batch)

            with self.stats_lock:
                self.request_count += 1
                if success:
                    self.latencies.append(latency_ms)
                    self.throughputs.append(throughput)
                    self.recent_latencies.append(latency_ms)
                    self.recent_throughputs.append(throughput)
                else:
                    self.errors.append(f"Request {request_id} failed")

            request_id += self.concurrency

    def _print_stats(self):
        with self.stats_lock:
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

            lat_array = np.array(self.latencies)
            recent_lat_array = (
                np.array(list(self.recent_latencies)) if self.recent_latencies else lat_array
            )

            logger.info(
                f"Stats: {total_requests} requests ({total_pairs} pairs) | "
                f"QPS: {current_qps:.1f} | Throughput: {current_throughput:.1f} p/s | "
                f"Latency: {np.mean(recent_lat_array):.1f}ms (P50: {np.percentile(recent_lat_array, 50):.1f}ms, "
                f"P95: {np.percentile(recent_lat_array, 95):.1f}ms) | "
                f"Errors: {total_errors}"
            )

    def run(self):
        pairs = self._load_test_data()

        logger.info(
            f"\n{'=' * 80}\n"
            f"Performance Hammer\n"
            f"{'=' * 80}\n"
            f"Concurrency: {self.concurrency}\n"
            f"Batch size: {self.batch_size}\n"
            f"Duration: {self.duration}s\n"
            if self.duration
            else f"Requests: {self.num_requests}\n{'=' * 80}\n"
        )

        self.start_time = time.perf_counter()

        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            futures = []
            for i in range(self.concurrency):
                future = executor.submit(self._worker, pairs, i)
                futures.append(future)

            last_stats_time = time.perf_counter()
            while self.running:
                time.sleep(1.0)

                if self.duration:
                    if time.perf_counter() - self.start_time >= self.duration:
                        self.running = False
                        break
                elif self.num_requests:
                    with self.stats_lock:
                        if len(self.latencies) >= self.num_requests:
                            self.running = False
                            break

                if time.perf_counter() - last_stats_time >= 60.0:
                    self._print_stats()
                    last_stats_time = time.perf_counter()

            logger.info("Waiting for workers to finish...")
            for future in futures:
                future.cancel()

        self.end_time = time.perf_counter()

        self._print_final_stats()

    def _print_final_stats(self):
        if not self.latencies:
            logger.warning("No successful requests completed")
            return

        elapsed = self.end_time - self.start_time if self.end_time and self.start_time else 0
        total_requests = len(self.latencies)
        total_pairs = total_requests * self.batch_size
        total_errors = len(self.errors)

        lat_array = np.array(self.latencies)
        thr_array = np.array(self.throughputs)

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
            f"  Per-request avg: {np.mean(thr_array):.1f} pairs/sec\n"
            f"  Per-request P95: {np.percentile(thr_array, 95):.1f} pairs/sec\n"
            f"\nLatency:\n"
            f"  Average: {np.mean(lat_array):.1f}ms\n"
            f"  Min: {np.min(lat_array):.1f}ms\n"
            f"  Max: {np.max(lat_array):.1f}ms\n"
            f"  P50: {np.percentile(lat_array, 50):.1f}ms\n"
            f"  P95: {np.percentile(lat_array, 95):.1f}ms\n"
            f"  P99: {np.percentile(lat_array, 99):.1f}ms\n"
            f"  Std Dev: {np.std(lat_array):.1f}ms\n"
            f"{'=' * 80}\n"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Performance Hammer - High-concurrency stress testing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run for 60 seconds with 256 concurrent requests
  python scripts/perf_hammer.py --concurrency 256 --batch-size 64 --duration 60

  # Run 1000 requests with 512 concurrent workers
  python scripts/perf_hammer.py --concurrency 512 --batch-size 64 --requests 1000

  # Maximum stress test
  python scripts/perf_hammer.py --concurrency 1024 --batch-size 64 --duration 120
        """,
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Server hostname (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=50051,
        help="Server port (default: 50051)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=256,
        help="Number of concurrent requests (default: 256)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Pairs per request (default: 64)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Run duration in seconds (default: None, use --requests)",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=None,
        help="Total number of requests (default: None, use --duration)",
    )

    args = parser.parse_args()

    if not args.duration and not args.requests:
        args.duration = 60.0
        logger.info("No duration or requests specified, defaulting to 60 seconds")

    if args.duration and args.requests:
        logger.warning("Both duration and requests specified, using duration")

    hammer = PerfHammer(
        host=args.host,
        port=args.port,
        concurrency=args.concurrency,
        batch_size=args.batch_size,
        duration=args.duration,
        num_requests=args.requests,
    )

    try:
        hammer.run()
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        hammer.client.close()


if __name__ == "__main__":
    main()
