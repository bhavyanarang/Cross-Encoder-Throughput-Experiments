import time
from typing import Any

from src.client.experiment_config import ExperimentConfig
from src.client.runner import BenchmarkRunner


class ExperimentRunner:
    def __init__(
        self,
        benchmark_runner: BenchmarkRunner,
        dataset_loader: Any,
        state: Any,
        timeseries_collector: Any = None,
        timeseries_writer: Any = None,
    ) -> None:
        self._benchmark_runner = benchmark_runner
        self._dataset_loader = dataset_loader
        self._state = state
        self._timeseries_collector = timeseries_collector
        self._timeseries_writer = timeseries_writer

    async def run(
        self,
        config: ExperimentConfig,
        timeseries_file: str | None = None,
        append: bool = False,
    ) -> list[dict]:
        pairs = self._dataset_loader.load(config.dataset_size)
        results: list[dict] = []
        append_next = append
        for batch_size in config.batch_sizes:
            for concurrency in config.concurrency_levels:
                if self._state.interrupted:
                    return results
                start_time = time.time()
                # Await the async benchmark runner
                result = await self._benchmark_runner.run(
                    pairs=pairs,
                    batch_size=batch_size,
                    num_requests=config.benchmark_requests,
                    concurrency=concurrency,
                )
                end_time = time.time()
                result["start_time_s"] = start_time
                result["end_time_s"] = end_time
                results.append(result)
                if (
                    timeseries_file
                    and self._timeseries_collector
                    and self._timeseries_writer
                    and "error" not in result
                ):
                    metrics = self._timeseries_collector.collect(start_time, end_time)
                    run_label = f"batch_size={batch_size}, concurrency={concurrency}"
                    self._timeseries_writer.write(
                        experiment_name=config.name or "experiment",
                        run_label=run_label,
                        metrics=metrics,
                        append=append_next,
                    )
                    append_next = True
        return results
