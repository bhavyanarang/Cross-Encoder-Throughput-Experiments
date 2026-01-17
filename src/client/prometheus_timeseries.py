from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class PrometheusQuery:
    name: str
    query: str


class PrometheusTimeseriesCollector:
    def __init__(
        self,
        base_url: str,
        step_seconds: float = 1.0,
        rate_window_seconds: float = 10.0,
        timeout_seconds: float = 10.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._step_seconds = step_seconds
        self._rate_window_seconds = rate_window_seconds
        self._timeout_seconds = timeout_seconds

    def collect(self, start_time: float, end_time: float) -> dict[str, list[float | None]]:
        start_time = float(start_time)
        end_time = float(end_time)
        if end_time < start_time:
            return {"timestamps": []}
        timestamps = self._build_timestamps(start_time, end_time)
        window = f"{int(self._rate_window_seconds)}s"
        metrics: dict[str, list[float | None]] = {"timestamps": timestamps}
        for query in self._queries(window):
            series = self._query_range(query.query, start_time, end_time)
            metrics[query.name] = self._align_series(series, timestamps)
        return metrics

    def _queries(self, window: str) -> list[PrometheusQuery]:
        return [
            PrometheusQuery("gpu_memory_mb", "avg(gpu_memory_mb)"),
            PrometheusQuery("gpu_utilization_pct", "avg(gpu_utilization_pct)"),
            PrometheusQuery("cpu_percent", "avg(cpu_percent)"),
            PrometheusQuery(
                "latency_ms",
                f"histogram_quantile(0.50, sum(rate(request_latency_seconds_bucket[{window}])) by (le)) * 1000",
            ),
            PrometheusQuery("throughput", f"sum(rate(request_count_total[{window}]))"),
            PrometheusQuery(
                "tokenize_ms",
                f"histogram_quantile(0.50, sum(rate(tokenization_latency_seconds_bucket[{window}])) by (le)) * 1000",
            ),
            PrometheusQuery(
                "inference_ms",
                f"histogram_quantile(0.50, sum(rate(inference_latency_seconds_bucket[{window}])) by (le)) * 1000",
            ),
            PrometheusQuery(
                "queue_wait_ms",
                f"histogram_quantile(0.50, sum(rate(queue_wait_latency_seconds_bucket[{window}])) by (le)) * 1000",
            ),
            PrometheusQuery(
                "tokenizer_queue_wait_ms",
                f"histogram_quantile(0.50, sum(rate(tokenizer_queue_wait_latency_seconds_bucket[{window}])) by (le)) * 1000",
            ),
            PrometheusQuery(
                "model_queue_wait_ms",
                f"histogram_quantile(0.50, sum(rate(model_queue_wait_latency_seconds_bucket[{window}])) by (le)) * 1000",
            ),
            PrometheusQuery("tokenizer_queue_size", "avg(tokenizer_queue_size)"),
            PrometheusQuery("model_queue_size", "avg(model_queue_size)"),
            PrometheusQuery("batch_queue_size", "avg(batch_queue_size)"),
            PrometheusQuery("padding_pct", "avg(padding_ratio) * 100"),
        ]

    def _build_timestamps(self, start_time: float, end_time: float) -> list[float]:
        step = float(self._step_seconds)
        if step <= 0:
            return []
        count = int((end_time - start_time) / step) + 1
        return [start_time + (i * step) for i in range(count)]

    def _query_range(
        self, query: str, start_time: float, end_time: float
    ) -> list[tuple[float, float]]:
        try:
            response = requests.get(
                f"{self._base_url}/api/v1/query_range",
                params={
                    "query": query,
                    "start": f"{start_time:.3f}",
                    "end": f"{end_time:.3f}",
                    "step": f"{self._step_seconds:.3f}",
                },
                timeout=self._timeout_seconds,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception:
            return []
        if payload.get("status") != "success":
            return []
        data = payload.get("data", {}) or {}
        results = data.get("result", []) or []
        if not results:
            return []
        combined: dict[float, float] = {}
        for result in results:
            values = result.get("values", []) or []
            for ts, raw in values:
                try:
                    value = float(raw)
                except Exception:
                    continue
                if value != value:
                    continue
                combined[float(ts)] = combined.get(float(ts), 0.0) + value
        return sorted(combined.items(), key=lambda item: item[0])

    def _align_series(
        self, series: list[tuple[float, float]], timestamps: list[float]
    ) -> list[float | None]:
        if not timestamps:
            return []
        lookup: dict[float, float] = {round(ts, 3): value for ts, value in series}
        return [lookup.get(round(ts, 3)) for ts in timestamps]
