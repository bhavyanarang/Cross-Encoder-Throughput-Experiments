#!/usr/bin/env python3

import argparse
import logging
import signal
from pathlib import Path

from src.client.collector import DashboardCollector
from src.client.grpc_client import InferenceClient
from src.client.loader import DatasetLoader
from src.client.runner import BenchmarkRunner
from src.client.writer import ResultsWriter
from src.server.dto import BenchmarkState

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Inference Benchmark Client")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=50051, help="Server port")
    parser.add_argument("--experiment", "-e", action="store_true", help="Experiment mode")
    parser.add_argument("--config", "-c", help="Experiment config YAML")
    parser.add_argument("--output", "-o", help="Output file for results")
    parser.add_argument(
        "--timeseries-file", help="Separate file for timeseries data (for sweep consolidation)"
    )
    parser.add_argument(
        "--append", action="store_true", help="Append to output file instead of overwriting"
    )
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--num-requests", type=int, default=100, help="Number of requests")
    parser.add_argument("--concurrency", type=int, default=1, help="Concurrency level")
    parser.add_argument("--dataset-size", type=int, default=50000, help="Number of test pairs")
    args = parser.parse_args()

    state = BenchmarkState()
    signal.signal(signal.SIGINT, state.handle_interrupt)
    signal.signal(signal.SIGTERM, state.handle_interrupt)

    config = {}
    if args.config:
        import yaml

        with open(args.config) as f:
            config = yaml.safe_load(f)
    if not config and args.experiment:
        base_config_path = Path(__file__).parent.parent / "experiments" / "base_config.yaml"
        if base_config_path.exists():
            import yaml

            with open(base_config_path) as f:
                config = yaml.safe_load(f)

    loader = DatasetLoader()
    collector = DashboardCollector(f"http://{args.host}:8080")
    writer = ResultsWriter()

    try:
        pairs = loader.load(args.dataset_size)

        client = InferenceClient(host=args.host, port=args.port)

        runner = BenchmarkRunner(client, state)

        result = runner.run(
            pairs=pairs,
            batch_size=args.batch_size,
            num_requests=args.num_requests,
            concurrency=args.concurrency,
        )

        dashboard_metrics = None
        if args.experiment:
            dashboard_metrics = collector.collect_history()

        if args.output:
            writer.save(
                results=[result],
                config=config,
                output_file=args.output,
                dashboard_metrics=dashboard_metrics,
                append=args.append,
                timeseries_file=args.timeseries_file,
            )

        if "error" in result:
            logger.error(f"Benchmark failed: {result['error']}")
        else:
            logger.info(
                f"Benchmark completed: {result.get('num_requests', 0)} requests processed in {result.get('total_time_s', 0):.2f}s. Check Grafana for metrics."
            )

    except Exception as e:
        logger.error(f"Benchmark failed with exception: {e}", exc_info=True)
        pass


if __name__ == "__main__":
    main()
