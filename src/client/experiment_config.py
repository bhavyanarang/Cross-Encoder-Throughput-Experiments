from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExperimentConfig:
    name: str
    description: str
    batch_sizes: list[int]
    concurrency_levels: list[int]
    benchmark_requests: int
    dataset_size: int

    @staticmethod
    def _listify(value: Any, fallback: list[int]) -> list[int]:
        if value is None:
            return fallback
        if isinstance(value, list):
            return [int(v) for v in value]
        return [int(value)]

    @classmethod
    def from_sources(cls, config: dict | None, args: Any) -> "ExperimentConfig":
        source = config or {}
        experiment = source.get("experiment", {}) or {}
        name = str(source.get("name") or "")
        description = str(source.get("description") or "")
        batch_sizes = cls._listify(experiment.get("batch_sizes"), [int(args.batch_size)])
        concurrency_levels = cls._listify(
            experiment.get("concurrency_levels"), [int(args.concurrency)]
        )
        benchmark_requests = int(experiment.get("benchmark_requests") or args.num_requests)
        dataset_size = int(experiment.get("dataset_size") or args.dataset_size)
        return cls(
            name=name,
            description=description,
            batch_sizes=batch_sizes,
            concurrency_levels=concurrency_levels,
            benchmark_requests=benchmark_requests,
            dataset_size=dataset_size,
        )
