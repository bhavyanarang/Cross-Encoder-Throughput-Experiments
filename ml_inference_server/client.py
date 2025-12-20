import grpc
import sys
import os
import argparse
import yaml
import time
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "proto"))
import inference_pb2
import inference_pb2_grpc

from utils import load_experiment_config


def load_dataset(num_samples: int = 1000):
    """Load MS MARCO queries from HuggingFace datasets."""
    from datasets import load_dataset
    
    logger.info("Loading MS MARCO dataset...")
    dataset = load_dataset("ms_marco", "v1.1", split="train", streaming=True)
    
    queries = []
    for i, item in enumerate(dataset):
        if i >= num_samples:
            break
        queries.append(item["query"])
    
    logger.info(f"Loaded {len(queries)} queries from MS MARCO")
    return queries


def run_inference(stub, texts):
    try:
        request = inference_pb2.InferRequest(texts=texts)
        response = stub.Infer(request)
        return response
    except grpc.RpcError as e:
        logger.error(f"gRPC error during inference: {e.code()} - {e.details()}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during inference: {e}")
        raise


def get_metrics(stub):
    try:
        response = stub.GetMetrics(inference_pb2.Empty())
        return response
    except grpc.RpcError as e:
        logger.error(f"gRPC error getting metrics: {e.code()} - {e.details()}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting metrics: {e}")
        raise


def benchmark(stub, all_texts: list, batch_size: int, num_requests: int, concurrency: int = 1):
    """Run benchmark with configurable concurrency using real queries."""
    logger.info(f"Starting benchmark: {num_requests} requests, concurrency={concurrency}, batch_size={batch_size}")
    
    # Prepare batches from real queries
    batches = []
    for i in range(num_requests):
        start_idx = (i * batch_size) % len(all_texts)
        batch = all_texts[start_idx:start_idx + batch_size]
        if len(batch) < batch_size:
            batch = batch + all_texts[:batch_size - len(batch)]
        batches.append(batch)
    
    start = time.perf_counter()
    completed = 0
    
    if concurrency == 1:
        for batch in batches:
            run_inference(stub, batch)
            completed += 1
            if completed % 100 == 0:
                logger.info(f"Progress: {completed}/{num_requests} requests")
    else:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(run_inference, stub, batch) for batch in batches]
            for f in as_completed(futures):
                f.result()
                completed += 1
                if completed % 100 == 0:
                    logger.info(f"Progress: {completed}/{num_requests} requests")
    
    elapsed = time.perf_counter() - start
    metrics = get_metrics(stub)
    
    total_pairs = num_requests * batch_size
    logger.info(f"Completed: {elapsed:.2f}s | {total_pairs} pairs | {total_pairs/elapsed:.2f} pairs/s")
    
    return {
        "batch_size": batch_size,
        "concurrency": concurrency,
        "num_requests": num_requests,
        "total_pairs": total_pairs,
        "total_time_s": elapsed,
        "avg_ms": metrics.avg_ms,
        "p50_ms": metrics.p50_ms,
        "p95_ms": metrics.p95_ms,
        "p99_ms": metrics.p99_ms,
        "throughput_rps": metrics.throughput_rps,
        "pairs_per_s": total_pairs / elapsed,
    }


def save_results_to_markdown(results: list, config: dict, output_file: str = "docs/experiment_results.md"):
    """Save experiment results to markdown file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    model_name = config["model"]["name"]
    
    # Check if file exists to append or create
    file_exists = os.path.exists(output_file)
    
    with open(output_file, "a") as f:
        f.write(f"\n## Experiment Run: {timestamp}\n\n")
        f.write(f"**Model:** `{model_name}`\n\n")
        f.write(f"**Device:** `{config['model']['device']}`\n\n")
        quantized = config['model'].get('quantized', False)
        f.write(f"**Quantized:** `{quantized}`\n\n")
        f.write(f"**Requests per config:** `{config['experiment']['benchmark_requests']}`\n\n")
        
        # Table header
        f.write("| Batch | Conc | Requests | Pairs | Time(s) | Avg(ms) | P50(ms) | P95(ms) | P99(ms) | Avg Throughput | Pairs/s |\n")
        f.write("|-------|------|----------|-------|---------|---------|---------|---------|---------|----------------|--------|\n")
        
        for r in results:
            f.write(f"| {r['batch_size']} | {r['concurrency']} | {r['num_requests']} | {r['total_pairs']} | "
                    f"{r['total_time_s']:.2f} | {r['avg_ms']:.2f} | {r['p50_ms']:.2f} | {r['p95_ms']:.2f} | "
                    f"{r['p99_ms']:.2f} | {r['throughput_rps']:.2f} req/s | {r['pairs_per_s']:.2f} |\n")
        
        # Summary
        best_throughput = max(results, key=lambda x: x['pairs_per_s'])
        best_latency = min(results, key=lambda x: x['avg_ms'])
        
        f.write(f"\n**Best Throughput:** batch={best_throughput['batch_size']}, conc={best_throughput['concurrency']} → {best_throughput['pairs_per_s']:.2f} pairs/s\n\n")
        f.write(f"**Best Latency:** batch={best_latency['batch_size']}, conc={best_latency['concurrency']} → {best_latency['avg_ms']:.2f}ms avg\n\n")
        f.write("---\n")
    
    logger.info(f"Results saved to {output_file}")


def run_experiments(stub, config, queries: list):
    """Run experiments with different batch sizes and concurrency levels."""
    results = []
    
    batch_sizes = config["experiment"]["batch_sizes"]
    concurrency_levels = config["experiment"]["concurrency_levels"]
    num_requests = config["experiment"]["benchmark_requests"]
    
    total_experiments = len(batch_sizes) * len(concurrency_levels)
    current = 0
    
    for batch_size in batch_sizes:
        for concurrency in concurrency_levels:
            current += 1
            logger.info(f"\n{'='*60}")
            logger.info(f"Experiment {current}/{total_experiments}: batch_size={batch_size}, concurrency={concurrency}")
            logger.info(f"{'='*60}")
            try:
                result = benchmark(stub, queries, batch_size, num_requests, concurrency)
                results.append(result)
            except Exception as e:
                logger.error(f"Experiment {current}/{total_experiments} failed: {e}")
                logger.error("Continuing with next experiment...")
                # Add a failed result entry
                results.append({
                    "batch_size": batch_size,
                    "concurrency": concurrency,
                    "num_requests": num_requests,
                    "total_pairs": num_requests * batch_size,
                    "total_time_s": 0.0,
                    "avg_ms": 0.0,
                    "p50_ms": 0.0,
                    "p95_ms": 0.0,
                    "p99_ms": 0.0,
                    "throughput_rps": 0.0,
                    "pairs_per_s": 0.0,
                    "error": str(e)
                })
    
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=50051)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--requests", type=int, default=50)
    parser.add_argument("--dataset-size", type=int, default=500, help="Number of queries to load from dataset")
    parser.add_argument("--experiment", action="store_true", help="Run full experiment suite from config")
    parser.add_argument("--config", help="Path to experiment config (e.g., experiments/minilm_baseline.yaml)")
    parser.add_argument("--output", default="docs/experiment_results.md", help="Output markdown file")
    args = parser.parse_args()

    channel = grpc.insecure_channel(f"{args.host}:{args.port}")
    stub = inference_pb2_grpc.InferenceServiceStub(channel)

    logger.info("=" * 60)
    logger.info("ML Inference Benchmark Client")
    logger.info("Monitor live metrics at: http://localhost:8080")
    logger.info("=" * 60)

    # Load real queries
    queries = load_dataset(args.dataset_size)

    # Check if server is reachable
    try:
        # Try to get metrics to verify connection
        _ = get_metrics(stub)
        logger.info("Connected to inference server successfully")
    except Exception as e:
        logger.error(f"Failed to connect to inference server at {args.host}:{args.port}")
        logger.error(f"Error: {e}")
        logger.error("Make sure the server is running with: ./run_server.sh")
        sys.exit(1)

    if args.experiment:
        try:
            # Load config - either experiment or legacy config
            if args.config:
                logger.info(f"Loading experiment config: {args.config}")
                config = load_experiment_config(args.config)
                logger.info(f"Experiment: {config.get('_experiment_name', 'unnamed')}")
                logger.info(f"Description: {config.get('_experiment_description', 'N/A')}")
            else:
                logger.info("Loading legacy config.yaml")
                config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
                with open(config_path) as f:
                    config = yaml.safe_load(f)
            
            logger.info(f"Running experiments with {len(config['experiment']['batch_sizes'])} batch sizes and {len(config['experiment']['concurrency_levels'])} concurrency levels")
            logger.info(f"Total experiments: {len(config['experiment']['batch_sizes']) * len(config['experiment']['concurrency_levels'])}")
            
            results = run_experiments(stub, config, queries)
            
            logger.info(f"\nCompleted {len(results)} experiments")
            
            # Save to markdown
            save_results_to_markdown(results, config, args.output)
            
            # Print summary
            print("\n" + "=" * 120)
            print("EXPERIMENT SUMMARY")
            print("=" * 120)
            print(f"{'Batch':<6} {'Conc':<5} {'Requests':<10} {'Pairs':<10} {'Time(s)':<10} {'Avg(ms)':<10} {'P95(ms)':<10} {'Avg Thpt':<12} {'Pairs/s':<10}")
            print("-" * 120)
            for r in results:
                if 'error' in r:
                    print(f"{r['batch_size']:<6} {r['concurrency']:<5} {'FAILED':<10} {'N/A':<10} {'N/A':<10} {'N/A':<10} {'N/A':<10} {'N/A':<12} {'N/A':<10}")
                else:
                    print(f"{r['batch_size']:<6} {r['concurrency']:<5} {r['num_requests']:<10} {r['total_pairs']:<10} "
                          f"{r['total_time_s']:<10.2f} {r['avg_ms']:<10.2f} {r['p95_ms']:<10.2f} {r['throughput_rps']:<12.2f} {r['pairs_per_s']:<10.2f}")
            print("=" * 120)
            print(f"\nResults saved to: {args.output}")
        except Exception as e:
            logger.error(f"Failed to run experiments: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        try:
            benchmark(stub, queries, args.batch_size, args.requests, args.concurrency)
        except Exception as e:
            logger.error(f"Benchmark failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
