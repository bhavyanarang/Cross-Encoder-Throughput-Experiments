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
from src.server.dto.metrics import MetricsCollector
from src.server.grpc import serve
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

    metrics = MetricsCollector()
    metrics.set_inference_service(orchestrator)
    metrics.set_experiment_info(
        name="timing_test",
        description="Detailed timing analysis",
        backend="mps",
        device="mps",
    )

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

    all_timings = []
    for i in range(num_samples):
        batch_start = (i * batch_size) % len(test_pairs)
        batch = test_pairs[batch_start : batch_start + batch_size]
        if len(batch) < batch_size:
            batch = batch + test_pairs[: batch_size - len(batch)]

        try:
            scores, latency = client.infer(batch)
            all_timings.append(latency)
            if (i + 1) % 50 == 0:
                logger.info(f"Completed {i + 1}/{num_samples} requests")
        except Exception as e:
            logger.error(f"Error on request {i}: {e}")

    elapsed = time.perf_counter() - start_time

    summary = metrics.summary()

    print("\n" + "=" * 80)
    print("TIMING ANALYSIS RESULTS")
    print("=" * 80)
    print(f"\nTotal requests: {num_samples}")
    print(f"Total elapsed time: {elapsed:.2f}s")
    print(f"Average latency: {summary['avg_ms']:.2f}ms")
    print(f"P50 latency: {summary['p50_ms']:.2f}ms")
    print(f"P95 latency: {summary['p95_ms']:.2f}ms")
    print(f"P99 latency: {summary['p99_ms']:.2f}ms")

    print("\n" + "-" * 80)
    print("STAGE BREAKDOWN (Average times)")
    print("-" * 80)
    stage_breakdown = summary.get("stage_breakdown", {})
    stage_percentages = summary.get("stage_percentages", {})

    print(
        f"Tokenization:        {stage_breakdown.get('tokenize', {}).get('avg_ms', 0):.2f}ms ({stage_percentages.get('tokenize_pct', 0):.1f}%)"
    )
    print(
        f"Queue Wait:          {stage_breakdown.get('queue_wait', {}).get('avg_ms', 0):.2f}ms ({stage_percentages.get('queue_wait_pct', 0):.1f}%)"
    )
    print(
        f"Model Inference:     {stage_breakdown.get('model_inference', {}).get('avg_ms', 0):.2f}ms ({stage_percentages.get('inference_pct', 0):.1f}%)"
    )
    print(
        f"Tokenizer Overhead:  {stage_breakdown.get('overhead', {}).get('avg_ms', 0):.2f}ms ({stage_percentages.get('overhead_pct', 0):.1f}%)"
    )
    print(
        f"MP Queue Send:       {stage_breakdown.get('mp_queue_send', {}).get('avg_ms', 0):.2f}ms ({stage_percentages.get('mp_queue_send_pct', 0):.1f}%)"
    )
    print(
        f"MP Queue Receive:    {stage_breakdown.get('mp_queue_receive', {}).get('avg_ms', 0):.2f}ms ({stage_percentages.get('mp_queue_receive_pct', 0):.1f}%)"
    )
    print(
        f"gRPC Serialize:      {stage_breakdown.get('grpc_serialize', {}).get('avg_ms', 0):.2f}ms ({stage_percentages.get('grpc_serialize_pct', 0):.1f}%)"
    )
    print(
        f"gRPC Deserialize:    {stage_breakdown.get('grpc_deserialize', {}).get('avg_ms', 0):.2f}ms ({stage_percentages.get('grpc_deserialize_pct', 0):.1f}%)"
    )
    print(
        f"Scheduler:           {stage_breakdown.get('scheduler', {}).get('avg_ms', 0):.2f}ms ({stage_percentages.get('scheduler_pct', 0):.1f}%)"
    )
    print(f"Other/gRPC:          {stage_percentages.get('other_pct', 0):.1f}%")

    print("\n" + "-" * 80)
    print("VERIFICATION")
    print("-" * 80)
    total_tracked = (
        stage_breakdown.get("tokenize", {}).get("avg_ms", 0)
        + stage_breakdown.get("queue_wait", {}).get("avg_ms", 0)
        + stage_breakdown.get("model_inference", {}).get("avg_ms", 0)
        + stage_breakdown.get("overhead", {}).get("avg_ms", 0)
        + stage_breakdown.get("mp_queue_send", {}).get("avg_ms", 0)
        + stage_breakdown.get("mp_queue_receive", {}).get("avg_ms", 0)
        + stage_breakdown.get("grpc_serialize", {}).get("avg_ms", 0)
        + stage_breakdown.get("grpc_deserialize", {}).get("avg_ms", 0)
        + stage_breakdown.get("scheduler", {}).get("avg_ms", 0)
    )
    other_ms = summary["avg_ms"] - total_tracked
    print(f"Total tracked time:  {total_tracked:.2f}ms")
    print(f"Average latency:      {summary['avg_ms']:.2f}ms")
    print(f"Unaccounted (Other): {other_ms:.2f}ms ({stage_percentages.get('other_pct', 0):.1f}%)")

    print("\n" + "=" * 80)

    client.close()
    orchestrator.stop()

    return summary


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
