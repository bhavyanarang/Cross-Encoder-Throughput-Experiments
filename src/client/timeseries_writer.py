from datetime import datetime
from pathlib import Path


class TimeseriesWriter:
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def write(
        self,
        experiment_name: str,
        run_label: str,
        metrics: dict[str, list[float | None]],
        append: bool = False,
    ) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append and self._path.exists() else "w"
        with self._path.open(mode, encoding="utf-8") as f:
            if mode == "w":
                f.write("# Timeseries Data\n\n")
            f.write(f"**Experiment:** {experiment_name}\n\n")
            if run_label:
                f.write(f"**Run:** {run_label}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            headers = [
                "Index",
                "GPU Mem (MB)",
                "GPU Util (%)",
                "CPU (%)",
                "Latency (ms)",
                "Throughput",
                "Tokenize (ms)",
                "Inference (ms)",
                "Queue Wait (ms)",
                "Tokenizer Queue Wait (ms)",
                "Model Queue Wait (ms)",
                "Tokenizer Queue Size",
                "Model Queue Size",
                "Batch Queue Size",
                "Padding (%)",
            ]
            f.write("| " + " | ".join(headers) + " |\n")
            f.write("|" + "|".join(["-----"] * len(headers)) + "|\n")
            length = len(metrics.get("timestamps", []))
            for idx in range(length):
                row = [
                    str(idx),
                    self._fmt(metrics.get("gpu_memory_mb", []), idx),
                    self._fmt(metrics.get("gpu_utilization_pct", []), idx),
                    self._fmt(metrics.get("cpu_percent", []), idx),
                    self._fmt(metrics.get("latency_ms", []), idx),
                    self._fmt(metrics.get("throughput", []), idx),
                    self._fmt(metrics.get("tokenize_ms", []), idx),
                    self._fmt(metrics.get("inference_ms", []), idx),
                    self._fmt(metrics.get("queue_wait_ms", []), idx),
                    self._fmt(metrics.get("tokenizer_queue_wait_ms", []), idx),
                    self._fmt(metrics.get("model_queue_wait_ms", []), idx),
                    self._fmt(metrics.get("tokenizer_queue_size", []), idx),
                    self._fmt(metrics.get("model_queue_size", []), idx),
                    self._fmt(metrics.get("batch_queue_size", []), idx),
                    self._fmt(metrics.get("padding_pct", []), idx),
                ]
                f.write("| " + " | ".join(row) + " |\n")
            f.write("\n")

    def _fmt(self, series: list[float | None], idx: int) -> str:
        if idx >= len(series):
            return "-"
        value = series[idx]
        if value is None:
            return "-"
        if abs(value) >= 100 or float(value).is_integer():
            return f"{value:.0f}"
        if abs(value) >= 10:
            return f"{value:.1f}"
        return f"{value:.2f}"
