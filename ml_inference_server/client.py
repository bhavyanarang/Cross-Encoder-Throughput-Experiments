import grpc
import sys
import os
import argparse
import yaml
import time
import logging
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "proto"))
import inference_pb2
import inference_pb2_grpc

from utils import load_experiment_config


def load_dataset(num_samples: int = 1000, cache_dir: str = None):
    """Load MS MARCO query-passage pairs from HuggingFace datasets with local caching."""
    import json
    
    # Default cache location
    if cache_dir is None:
        cache_dir = os.path.join(os.path.dirname(__file__), ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    
    cache_file = os.path.join(cache_dir, f"msmarco_pairs_{num_samples}.json")
    
    # Check if cached file exists
    if os.path.exists(cache_file):
        logger.info(f"Loading cached pairs from {cache_file}")
        with open(cache_file, "r") as f:
            pairs = json.load(f)
        logger.info(f"Loaded {len(pairs)} cached query-passage pairs from MS MARCO")
        return pairs
    
    # Download and cache
    from datasets import load_dataset as hf_load_dataset
    
    logger.info("Downloading MS MARCO dataset (first time only, will be cached)...")
    dataset = hf_load_dataset("ms_marco", "v1.1", split="train", streaming=True)
    
    pairs = []
    for i, item in enumerate(dataset):
        if i >= num_samples:
            break
        query = item["query"]
        # Get passages from the item
        passages = item.get("passages", {})
        passage_texts = passages.get("passage_text", [])
        
        if passage_texts:
            # Use the first passage as the document
            pairs.append([query, passage_texts[0]])
        else:
            # Fallback: use query as both (for testing)
            pairs.append([query, query])
    
    # Save to cache
    with open(cache_file, "w") as f:
        json.dump(pairs, f)
    logger.info(f"Cached {len(pairs)} query-passage pairs to {cache_file}")
    
    return pairs


def run_inference_timed(stub, pairs: list):
    """Run cross-encoder inference and return (response, latency_ms)."""
    try:
        start = time.perf_counter()
        proto_pairs = [
            inference_pb2.QueryDocPair(query=p[0], document=p[1]) 
            for p in pairs
        ]
        request = inference_pb2.InferRequest(pairs=proto_pairs)
        response = stub.Infer(request)
        latency_ms = (time.perf_counter() - start) * 1000
        return response, latency_ms
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


def benchmark(stub, all_pairs: list, batch_size: int, num_requests: int, concurrency: int = 1):
    """Run benchmark with configurable concurrency, tracking per-request metrics."""
    logger.info(f"Starting benchmark: {num_requests} requests, concurrency={concurrency}, batch_size={batch_size}")
    
    # Prepare batches from real pairs
    batches = []
    for i in range(num_requests):
        start_idx = (i * batch_size) % len(all_pairs)
        batch = all_pairs[start_idx:start_idx + batch_size]
        if len(batch) < batch_size:
            batch = batch + all_pairs[:batch_size - len(batch)]
        batches.append(batch)
    
    # Track per-request latencies and throughputs
    request_latencies = []
    request_throughputs = []  # pairs/second for each request
    
    start = time.perf_counter()
    completed = 0
    
    if concurrency == 1:
        for batch in batches:
            _, latency_ms = run_inference_timed(stub, batch)
            request_latencies.append(latency_ms)
            # Throughput for this request: pairs / time_in_seconds
            request_throughputs.append(batch_size / (latency_ms / 1000))
            completed += 1
            if completed % 100 == 0:
                logger.info(f"Progress: {completed}/{num_requests} requests")
    else:
        from threading import Lock
        lock = Lock()
        
        def run_and_record(batch):
            _, latency_ms = run_inference_timed(stub, batch)
            throughput = batch_size / (latency_ms / 1000)
            with lock:
                request_latencies.append(latency_ms)
                request_throughputs.append(throughput)
            return latency_ms
        
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(run_and_record, batch) for batch in batches]
            for f in as_completed(futures):
                f.result()
                completed += 1
                if completed % 100 == 0:
                    logger.info(f"Progress: {completed}/{num_requests} requests")
    
    elapsed = time.perf_counter() - start
    
    total_pairs = num_requests * batch_size
    avg_throughput = total_pairs / elapsed
    
    # Convert to numpy for percentile calculations
    lat_arr = np.array(request_latencies)
    tp_arr = np.array(request_throughputs)
    
    logger.info(f"Completed: {elapsed:.2f}s | {total_pairs} pairs | {avg_throughput:.2f} pairs/s")
    
    return {
        "batch_size": batch_size,
        "concurrency": concurrency,
        "num_requests": num_requests,
        "total_pairs": total_pairs,
        "total_time_s": elapsed,
        # Latency metrics (ms)
        "latency_avg_ms": float(np.mean(lat_arr)),
        "latency_min_ms": float(np.min(lat_arr)),
        "latency_max_ms": float(np.max(lat_arr)),
        "latency_std_ms": float(np.std(lat_arr)),
        "latency_p50_ms": float(np.percentile(lat_arr, 50)),
        "latency_p90_ms": float(np.percentile(lat_arr, 90)),
        "latency_p95_ms": float(np.percentile(lat_arr, 95)),
        "latency_p99_ms": float(np.percentile(lat_arr, 99)),
        # Throughput metrics (pairs/s)
        "throughput_avg": avg_throughput,
        "throughput_min": float(np.min(tp_arr)),
        "throughput_max": float(np.max(tp_arr)),
        "throughput_std": float(np.std(tp_arr)),
        "throughput_p50": float(np.percentile(tp_arr, 50)),
        "throughput_p90": float(np.percentile(tp_arr, 90)),
        "throughput_p95": float(np.percentile(tp_arr, 95)),
        "throughput_p99": float(np.percentile(tp_arr, 99)),
    }


def save_results_to_markdown(results: list, config: dict, output_file: str = "docs/experiment_results.md"):
    """Save experiment results to markdown file with detailed sub-experiment metrics."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    model_name = config["model"]["name"]
    experiment_name = config.get("_experiment_name", "unnamed")
    backend = config['model'].get('backend', 'pytorch')
    device = config['model']['device']
    batching_enabled = config.get('batching', {}).get('enabled', False)
    batching_config = config.get('batching', {})
    
    # Write to experiment-specific file (overwrite)
    with open(output_file, "w") as f:
        f.write(f"# {experiment_name}\n\n")
        f.write(f"**Timestamp:** {timestamp}\n\n")
        f.write(f"**Model:** `{model_name}`\n\n")
        f.write(f"**Device:** `{device}`\n\n")
        f.write(f"**Backend:** `{backend}`\n\n")
        f.write(f"**Dynamic Batching:** `{batching_enabled}`")
        if batching_enabled:
            f.write(f" (max_batch={batching_config.get('max_batch_size', 'N/A')}, timeout={batching_config.get('timeout_ms', 'N/A')}ms)")
        f.write("\n\n")
        f.write(f"**Model Type:** Cross-Encoder\n\n")
        f.write(f"**Requests per config:** `{config['experiment']['benchmark_requests']}`\n\n")
        
        # Summary table
        f.write("## Results Summary\n\n")
        f.write("| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |\n")
        f.write("|-------|------|-------|---------|---------|---------|---------|--------|--------|\n")
        
        for r in results:
            if 'error' in r:
                f.write(f"| {r['batch_size']} | {r['concurrency']} | ERROR | - | - | - | - | - | - |\n")
            else:
                f.write(f"| {r['batch_size']} | {r['concurrency']} | {r['total_pairs']} | "
                        f"{r['total_time_s']:.2f} | {r['latency_avg_ms']:.1f}ms | {r['latency_p95_ms']:.1f}ms | "
                        f"{r['latency_p99_ms']:.1f}ms | {r['throughput_avg']:.1f} | {r['throughput_p95']:.1f} |\n")
        
        # Detailed sub-experiment metrics
        f.write("\n## Detailed Sub-Experiment Metrics\n\n")
        
        for i, r in enumerate(results, 1):
            if 'error' in r:
                f.write(f"### Config {i}: batch={r['batch_size']}, concurrency={r['concurrency']} - **ERROR**\n\n")
                f.write(f"Error: {r.get('error', 'Unknown')}\n\n")
            else:
                f.write(f"### Config {i}: batch={r['batch_size']}, concurrency={r['concurrency']}\n\n")
                f.write(f"**Total:** {r['total_pairs']} pairs in {r['total_time_s']:.2f}s\n\n")
                
                f.write("#### Latency (ms)\n")
                f.write(f"| Metric | Value |\n")
                f.write(f"|--------|-------|\n")
                f.write(f"| Average | {r['latency_avg_ms']:.2f} |\n")
                f.write(f"| Min | {r['latency_min_ms']:.2f} |\n")
                f.write(f"| Max | {r['latency_max_ms']:.2f} |\n")
                f.write(f"| Std Dev | {r['latency_std_ms']:.2f} |\n")
                f.write(f"| P50 | {r['latency_p50_ms']:.2f} |\n")
                f.write(f"| P90 | {r['latency_p90_ms']:.2f} |\n")
                f.write(f"| P95 | {r['latency_p95_ms']:.2f} |\n")
                f.write(f"| P99 | {r['latency_p99_ms']:.2f} |\n\n")
                
                f.write("#### Throughput (pairs/s)\n")
                f.write(f"| Metric | Value |\n")
                f.write(f"|--------|-------|\n")
                f.write(f"| Average | {r['throughput_avg']:.2f} |\n")
                f.write(f"| Min | {r['throughput_min']:.2f} |\n")
                f.write(f"| Max | {r['throughput_max']:.2f} |\n")
                f.write(f"| Std Dev | {r['throughput_std']:.2f} |\n")
                f.write(f"| P50 | {r['throughput_p50']:.2f} |\n")
                f.write(f"| P90 | {r['throughput_p90']:.2f} |\n")
                f.write(f"| P95 | {r['throughput_p95']:.2f} |\n")
                f.write(f"| P99 | {r['throughput_p99']:.2f} |\n\n")
        
        # Overall summary
        successful = [r for r in results if 'error' not in r]
        if successful:
            best_throughput = max(successful, key=lambda x: x['throughput_avg'])
            best_latency = min(successful, key=lambda x: x['latency_avg_ms'])
            avg_all_throughput = sum(r['throughput_avg'] for r in successful) / len(successful)
            avg_all_latency = sum(r['latency_avg_ms'] for r in successful) / len(successful)
            
            f.write(f"## Overall Summary\n\n")
            f.write(f"| Metric | Value | Config |\n")
            f.write(f"|--------|-------|--------|\n")
            f.write(f"| Best Throughput | {best_throughput['throughput_avg']:.2f} p/s | batch={best_throughput['batch_size']}, conc={best_throughput['concurrency']} |\n")
            f.write(f"| Best Latency | {best_latency['latency_avg_ms']:.2f}ms | batch={best_latency['batch_size']}, conc={best_latency['concurrency']} |\n")
            f.write(f"| Avg Throughput | {avg_all_throughput:.2f} p/s | all configs |\n")
            f.write(f"| Avg Latency | {avg_all_latency:.2f}ms | all configs |\n")
    
    # Also append to combined results file
    combined_file = os.path.join(os.path.dirname(output_file), "all_results.md")
    file_exists = os.path.exists(combined_file)
    
    with open(combined_file, "a") as f:
        if not file_exists:
            f.write("# All Experiment Results\n\n")
            f.write("Combined results from all experiments.\n\n")
            f.write("---\n")
        
        f.write(f"\n## {experiment_name} ({timestamp})\n\n")
        f.write(f"**Backend:** `{backend}` | **Device:** `{device}` | **Dynamic Batching:** `{batching_enabled}`\n\n")
        
        # Full table with comprehensive metrics
        f.write("| Batch | Conc | Pairs | Time | Lat Avg | Lat P50 | Lat P95 | Lat P99 | TP Avg | TP P50 | TP P95 | TP P99 |\n")
        f.write("|-------|------|-------|------|---------|---------|---------|---------|--------|--------|--------|--------|\n")
        
        for r in results:
            if 'error' in r:
                f.write(f"| {r['batch_size']} | {r['concurrency']} | ERROR | - | - | - | - | - | - | - | - | - |\n")
            else:
                f.write(f"| {r['batch_size']} | {r['concurrency']} | {r['total_pairs']} | "
                        f"{r['total_time_s']:.1f}s | {r['latency_avg_ms']:.1f} | {r['latency_p50_ms']:.1f} | "
                        f"{r['latency_p95_ms']:.1f} | {r['latency_p99_ms']:.1f} | {r['throughput_avg']:.1f} | "
                        f"{r['throughput_p50']:.1f} | {r['throughput_p95']:.1f} | {r['throughput_p99']:.1f} |\n")
        
        # Add summary stats
        successful = [r for r in results if 'error' not in r]
        if successful:
            best_tp = max(successful, key=lambda x: x['throughput_avg'])
            avg_tp = sum(r['throughput_avg'] for r in successful) / len(successful)
            avg_lat = sum(r['latency_avg_ms'] for r in successful) / len(successful)
            avg_p99_lat = sum(r['latency_p99_ms'] for r in successful) / len(successful)
            
            f.write(f"\n**Summary:** BestTP={best_tp['throughput_avg']:.1f} | AvgTP={avg_tp:.1f} | AvgLat={avg_lat:.1f}ms | AvgP99Lat={avg_p99_lat:.1f}ms\n")
        
        f.write("\n---\n")
    
    logger.info(f"Results saved to {output_file}")


def run_experiments(stub, config, pairs: list):
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
                result = benchmark(stub, pairs, batch_size, num_requests, concurrency)
                results.append(result)
            except Exception as e:
                logger.error(f"Experiment {current}/{total_experiments} failed: {e}")
                logger.error("Continuing with next experiment...")
                results.append({
                    "batch_size": batch_size,
                    "concurrency": concurrency,
                    "num_requests": num_requests,
                    "total_pairs": num_requests * batch_size,
                    "total_time_s": 0.0,
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
    parser.add_argument("--dataset-size", type=int, default=5000, help="Number of pairs to load from dataset")
    parser.add_argument("--experiment", action="store_true", help="Run full experiment suite from config")
    parser.add_argument("--config", help="Path to experiment config (e.g., experiments/minilm_baseline.yaml)")
    parser.add_argument("--output", default="docs/experiment_results.md", help="Output markdown file")
    args = parser.parse_args()

    channel = grpc.insecure_channel(f"{args.host}:{args.port}")
    stub = inference_pb2_grpc.InferenceServiceStub(channel)

    logger.info("=" * 60)
    logger.info("Cross-Encoder Benchmark Client")
    logger.info("Monitor live metrics at: http://localhost:8080")
    logger.info("=" * 60)

    # Load real query-passage pairs
    pairs = load_dataset(args.dataset_size)

    # Check if server is reachable
    try:
        _ = get_metrics(stub)
        logger.info("Connected to cross-encoder server successfully")
    except Exception as e:
        logger.error(f"Failed to connect to server at {args.host}:{args.port}")
        logger.error(f"Error: {e}")
        logger.error("Make sure the server is running with: ./run_server.sh")
        sys.exit(1)

    if args.experiment:
        try:
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
            
            results = run_experiments(stub, config, pairs)
            
            logger.info(f"\nCompleted {len(results)} experiments")
            
            save_results_to_markdown(results, config, args.output)
            
            # Print summary
            print("\n" + "=" * 120)
            print("EXPERIMENT SUMMARY (Cross-Encoder)")
            print("=" * 120)
            print(f"{'Batch':<6} {'Conc':<5} {'Pairs':<8} {'Time':<8} {'Lat Avg':<10} {'Lat P95':<10} {'Lat P99':<10} {'TP Avg':<12} {'TP P99':<12}")
            print("-" * 120)
            for r in results:
                if 'error' in r:
                    print(f"{r['batch_size']:<6} {r['concurrency']:<5} {'FAILED':<8} {'N/A':<8} {'N/A':<10} {'N/A':<10} {'N/A':<10} {'N/A':<12} {'N/A':<12}")
                else:
                    print(f"{r['batch_size']:<6} {r['concurrency']:<5} {r['total_pairs']:<8} "
                          f"{r['total_time_s']:<8.1f} {r['latency_avg_ms']:<10.1f} {r['latency_p95_ms']:<10.1f} "
                          f"{r['latency_p99_ms']:<10.1f} {r['throughput_avg']:<12.1f} {r['throughput_p99']:<12.1f}")
            print("=" * 120)
            print(f"\nResults saved to: {args.output}")
        except Exception as e:
            logger.error(f"Failed to run experiments: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        try:
            result = benchmark(stub, pairs, args.batch_size, args.requests, args.concurrency)
            print(f"\nLatency: avg={result['latency_avg_ms']:.1f}ms, p95={result['latency_p95_ms']:.1f}ms, p99={result['latency_p99_ms']:.1f}ms")
            print(f"Throughput: avg={result['throughput_avg']:.1f} p/s, p95={result['throughput_p95']:.1f} p/s, p99={result['throughput_p99']:.1f} p/s")
        except Exception as e:
            logger.error(f"Benchmark failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
