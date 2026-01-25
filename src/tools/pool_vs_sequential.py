#!/usr/bin/env python3

import argparse
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _create_batch(
    pairs: list[tuple[str, str]], batch_size: int, index: int
) -> list[tuple[str, str]]:
    start_idx = (index * batch_size) % len(pairs)
    batch = pairs[start_idx : start_idx + batch_size]
    if len(batch) < batch_size:
        batch = batch + pairs[: batch_size - len(batch)]
    return batch


def _load_pairs(dataset_size: int, logger: logging.Logger) -> list[tuple[str, str]]:
    from src.client.loader import DatasetLoader

    loader = DatasetLoader()
    pairs = loader.load(dataset_size)
    if not pairs:
        raise RuntimeError("No pairs loaded for benchmark")
    logger.info(f"Loaded {len(pairs)} pairs")
    return pairs


def _run_sequential(
    pairs: list[tuple[str, str]],
    model_name: str,
    backend: str,
    device: str,
    quantization: str,
    max_length: int,
    batch_size: int,
    num_requests: int,
    warmup: int,
    tokenizers_parallelism: bool,
    logger: logging.Logger,
) -> dict:
    from src.server.backends import create_backend
    from src.server.dto.config import ModelConfig
    from src.server.utils.tokenizer import TokenizerService
    from src.server.worker.base import setup_worker_environment

    setup_worker_environment(tokenizers_parallelism)
    model_config = ModelConfig(
        name=model_name,
        device=device,
        backend=backend,
        quantization=quantization,
        max_length=max_length,
    )
    backend_instance = create_backend(model_config)
    backend_instance.load_model()
    if warmup > 0:
        backend_instance.warmup(warmup)

    tokenizer = TokenizerService(model_name, max_length)

    tokenize_times = []
    inference_times = []
    total_times = []

    start = time.perf_counter()
    for i in range(num_requests):
        batch = _create_batch(pairs, batch_size, i)
        t0 = time.perf_counter()
        tokenized = tokenizer.tokenize(batch, device="cpu")
        result = backend_instance.infer_with_tokenized(tokenized)
        total_times.append((time.perf_counter() - t0) * 1000)
        tokenize_times.append(tokenized.tokenize_time_ms)
        inference_times.append(result.t_model_inference_ms)
        if (i + 1) % max(1, num_requests // 10) == 0:
            logger.info(f"Sequential progress: {i + 1}/{num_requests}")

    elapsed = time.perf_counter() - start
    total_pairs = num_requests * batch_size

    return {
        "mode": "sequential",
        "requests": num_requests,
        "pairs": total_pairs,
        "elapsed_s": elapsed,
        "throughput_pairs_s": total_pairs / elapsed if elapsed > 0 else 0.0,
        "avg_total_ms": _mean(total_times),
        "avg_tokenize_ms": _mean(tokenize_times),
        "avg_infer_ms": _mean(inference_times),
    }


def _run_pool(
    pairs: list[tuple[str, str]],
    model_name: str,
    backend: str,
    device: str,
    quantization: str,
    max_length: int,
    batch_size: int,
    num_requests: int,
    warmup: int,
    concurrency: int,
    tokenizer_workers: int,
    model_workers: int,
    tokenizers_parallelism: bool,
    logger: logging.Logger,
) -> dict:
    from src.server.dto import Config
    from src.server.dto.config import ModelConfig, PoolConfig, TokenizerPoolConfig
    from src.server.services.orchestrator_service import OrchestratorService

    instances = []
    for _ in range(model_workers):
        instances.append(
            ModelConfig(
                name=model_name,
                device=device,
                backend=backend,
                quantization=quantization,
                max_length=max_length,
            )
        )

    config = Config(
        model_pool=PoolConfig(instances=instances),
        tokenizer_pool=TokenizerPoolConfig(
            enabled=True,
            num_workers=tokenizer_workers,
            model_name=model_name,
            tokenizers_parallelism=tokenizers_parallelism,
        ),
    )

    orchestrator = OrchestratorService(config, "pool_vs_sequential")
    orchestrator.setup()
    orchestrator.start()

    try:
        for i in range(warmup):
            batch = _create_batch(pairs, batch_size, i)
            orchestrator.schedule(batch)

        def worker(worker_id: int) -> tuple[list[float], list[float], list[float]]:
            local_tokenize = []
            local_infer = []
            local_total = []
            idx = worker_id
            while idx < num_requests:
                batch = _create_batch(pairs, batch_size, idx)
                t0 = time.perf_counter()
                result = orchestrator.schedule(batch)
                local_total.append((time.perf_counter() - t0) * 1000)
                local_tokenize.append(result.t_tokenize_ms)
                local_infer.append(result.t_model_inference_ms)
                idx += concurrency
            return local_tokenize, local_infer, local_total

        start = time.perf_counter()
        tokenize_times = []
        inference_times = []
        total_times = []

        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(worker, i) for i in range(concurrency)]
            for fut in futures:
                local_tokenize, local_infer, local_total = fut.result()
                tokenize_times.extend(local_tokenize)
                inference_times.extend(local_infer)
                total_times.extend(local_total)

        elapsed = time.perf_counter() - start
        total_pairs = num_requests * batch_size

        return {
            "mode": "pool",
            "requests": num_requests,
            "pairs": total_pairs,
            "elapsed_s": elapsed,
            "throughput_pairs_s": total_pairs / elapsed if elapsed > 0 else 0.0,
            "avg_total_ms": _mean(total_times),
            "avg_tokenize_ms": _mean(tokenize_times),
            "avg_infer_ms": _mean(inference_times),
        }
    finally:
        orchestrator.stop()


def _log_results(results: dict, logger: logging.Logger) -> None:
    logger.info(
        f"{results['mode']} | "
        f"pairs={results['pairs']} | "
        f"elapsed={results['elapsed_s']:.2f}s | "
        f"throughput={results['throughput_pairs_s']:.1f} pairs/s | "
        f"avg_total={results['avg_total_ms']:.1f}ms | "
        f"avg_tokenize={results['avg_tokenize_ms']:.1f}ms | "
        f"avg_infer={results['avg_infer_ms']:.1f}ms"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare sequential vs pooled throughput")
    parser.add_argument("--model-name", default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    parser.add_argument("--backend", default="mps")
    parser.add_argument("--device", default="mps")
    parser.add_argument("--quantization", default="fp16")
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--num-requests", type=int, default=200)
    parser.add_argument("--dataset-size", type=int, default=2000)
    parser.add_argument("--warmup", type=int, default=3)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--tokenizer-workers", type=int, default=1)
    parser.add_argument("--model-workers", type=int, default=1)
    parser.add_argument("--tokenizers-parallelism", action="store_true")
    parser.add_argument("--mode", choices=["sequential", "pool", "both"], default="both")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logger = logging.getLogger(__name__)

    try:
        import torch

        logger.info(f"MPS available: {torch.backends.mps.is_available()}")
    except Exception:
        logger.info("MPS available: False")

    pairs = _load_pairs(args.dataset_size, logger)

    if args.mode in ["sequential", "both"]:
        logger.info("Running sequential benchmark")
        seq_results = _run_sequential(
            pairs=pairs,
            model_name=args.model_name,
            backend=args.backend,
            device=args.device,
            quantization=args.quantization,
            max_length=args.max_length,
            batch_size=args.batch_size,
            num_requests=args.num_requests,
            warmup=args.warmup,
            tokenizers_parallelism=args.tokenizers_parallelism,
            logger=logger,
        )
        _log_results(seq_results, logger)

    if args.mode in ["pool", "both"]:
        logger.info("Running pool benchmark")
        pool_results = _run_pool(
            pairs=pairs,
            model_name=args.model_name,
            backend=args.backend,
            device=args.device,
            quantization=args.quantization,
            max_length=args.max_length,
            batch_size=args.batch_size,
            num_requests=args.num_requests,
            warmup=args.warmup,
            concurrency=args.concurrency,
            tokenizer_workers=args.tokenizer_workers,
            model_workers=args.model_workers,
            tokenizers_parallelism=args.tokenizers_parallelism,
            logger=logger,
        )
        _log_results(pool_results, logger)


if __name__ == "__main__":
    main()
