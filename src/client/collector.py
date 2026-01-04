import logging

import requests

from src.server.dto import DashboardMetrics

logger = logging.getLogger(__name__)


class DashboardCollector:
    def __init__(self, dashboard_url: str = "http://localhost:8080"):
        self.dashboard_url = dashboard_url

    def fetch_metrics(self) -> dict:
        try:
            response = requests.get(f"{self.dashboard_url}/metrics", timeout=2)
            return response.json()
        except Exception:
            return {}

    def collect_history(self) -> DashboardMetrics:
        try:
            data = self.fetch_metrics()
            history = data.get("history", {})
            return DashboardMetrics(
                gpu_memory_mb=history.get("gpu_memory_mb", []),
                gpu_utilization_pct=history.get("gpu_utilization_pct", []),
                cpu_percent=history.get("cpu_percent", []),
                latencies=history.get("latencies", []),
                throughput=history.get("throughput", []),
                tokenize_ms=history.get("tokenize_ms", []),
                inference_ms=history.get("inference_ms", []),
                queue_wait_ms=history.get("queue_wait_ms", []),
                tokenizer_queue_wait_ms=history.get("tokenizer_queue_wait_ms", []),
                model_queue_wait_ms=history.get("model_queue_wait_ms", []),
                tokenizer_queue_size=history.get("tokenizer_queue_size", []),
                model_queue_size=history.get("model_queue_size", []),
                batch_queue_size=history.get("batch_queue_size", []),
                padding_pct=history.get("padding_pct", []),
                worker_stats=data.get("worker_stats", []),
                stage_percentages=data.get("stage_percentages", {}),
                tokenizer_throughput_qps=history.get("tokenizer_throughput_qps", []),
                inference_throughput_qps=history.get("inference_throughput_qps", []),
                overall_throughput_qps=history.get("overall_throughput_qps", []),
            )
        except Exception as e:
            logger.warning(f"Failed to collect dashboard metrics: {e}")
            return DashboardMetrics()
