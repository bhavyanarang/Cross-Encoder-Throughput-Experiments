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
    request = inference_pb2.InferRequest(texts=texts)
    response = stub.Infer(request)
    return response


def get_metrics(stub):
    response = stub.GetMetrics(inference_pb2.Empty())
    return response


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
            result = benchmark(stub, queries, batch_size, num_requests, concurrency)
            results.append(result)
    
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

    if args.experiment:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
        
        results = run_experiments(stub, config, queries)
        
        # Save to markdown
        save_results_to_markdown(results, config, args.output)
        
        # Print summary
        print("\n" + "=" * 120)
        print("EXPERIMENT SUMMARY")
        print("=" * 120)
        print(f"{'Batch':<6} {'Conc':<5} {'Requests':<10} {'Pairs':<10} {'Time(s)':<10} {'Avg(ms)':<10} {'P95(ms)':<10} {'Avg Thpt':<12} {'Pairs/s':<10}")
        print("-" * 120)
        for r in results:
            print(f"{r['batch_size']:<6} {r['concurrency']:<5} {r['num_requests']:<10} {r['total_pairs']:<10} "
                  f"{r['total_time_s']:<10.2f} {r['avg_ms']:<10.2f} {r['p95_ms']:<10.2f} {r['throughput_rps']:<12.2f} {r['pairs_per_s']:<10.2f}")
        print("=" * 120)
        print(f"\nResults saved to: {args.output}")
    else:
        benchmark(stub, queries, args.batch_size, args.requests, args.concurrency)


if __name__ == "__main__":
    main()
