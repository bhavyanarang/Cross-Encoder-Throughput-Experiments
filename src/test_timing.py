import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import threading

from src.client.grpc_client import InferenceClient
from src.run_client import DatasetLoader
from src.server.dto import Config
from src.server.dto.config import ModelConfig, PoolConfig, TokenizerPoolConfig
from src.server.grpc import serve
from src.server.services.metrics_service import MetricsService
from src.server.services.orchestrator_service import OrchestratorService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def run_test(num_samples: int = 500, batch_size: int = 1, concurrency: int = 1):
    logger.info(
        f"Starting timing test: {num_samples} samples, batch_size={batch_size}, concurrency={concurrency}"
    )

    model_config = ModelConfig(
        name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        device="mps",
        quantization="fp16",
        max_length=512,
    )

    pool_config = PoolConfig(instances=[model_config])

    config = Config(
        model_pool=pool_config,
        tokenizer_pool=TokenizerPoolConfig(
            enabled=True,
            num_workers=2,
            model_name=model_config.name,
        ),
        description="Timing test",
    )

    orchestrator = OrchestratorService(config, experiment_name="timing_test")
    orchestrator.setup()
    orchestrator.start()

    metrics: MetricsService = orchestrator.get_metrics()

    server_thread = threading.Thread(
        target=serve,
        args=(orchestrator, "localhost", 50051, 10, metrics),
        daemon=True,
    )
    server_thread.start()

    time.sleep(3)

    client = InferenceClient(host="localhost", port=50051)

    logger.info("Loading MS MARCO dataset...")
    loader = DatasetLoader()

    test_pairs = loader.load(max(num_samples * batch_size, 1000))
    logger.info(f"Loaded {len(test_pairs)} query-document pairs from dataset")

    logger.info(f"Running {num_samples} requests...")
    start_time = time.perf_counter()

    for i in range(num_samples):
        batch_start = (i * batch_size) % len(test_pairs)
        batch = test_pairs[batch_start : batch_start + batch_size]
        if len(batch) < batch_size:
            batch = batch + test_pairs[: batch_size - len(batch)]

        try:
            client.infer(batch)
            if (i + 1) % 50 == 0:
                logger.info(f"Completed {i + 1}/{num_samples} requests")
        except Exception as e:
            logger.error(f"Error on request {i}: {e}")

    elapsed = time.perf_counter() - start_time

    logger.info(f"Timing run complete: {num_samples} requests in {elapsed:.2f}s")
    logger.info("Use Prometheus/Grafana for latency percentiles and stage timings")

    client.close()
    orchestrator.stop()

    return {"requests": num_samples, "elapsed_s": elapsed}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test timing with detailed measurements")
    parser.add_argument("--num-samples", type=int, default=500, help="Number of samples to test")
    parser.add_argument("--batch-size", type=int, default=1, help="Batch size per request")
    parser.add_argument("--concurrency", type=int, default=1, help="Concurrency level")

    args = parser.parse_args()

    run_test(
        num_samples=args.num_samples,
        batch_size=args.batch_size,
        concurrency=args.concurrency,
    )
