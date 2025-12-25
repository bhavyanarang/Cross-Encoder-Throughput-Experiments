"""HTTP Server for ML Inference Metrics Dashboard."""

import json
import logging
import mimetypes
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import TYPE_CHECKING

from src.models import DashboardHistory, MetricsCollector

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).parent
TEMPLATES_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR / "static"


class DashboardState:
    """State container for dashboard.

    Uses singleton pattern to share state across HTTP handlers.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._metrics_collector: MetricsCollector | None = None
        self._history = DashboardHistory()
        self._start_time = time.time()
        self._last_request_count = 0

    @property
    def metrics_collector(self) -> MetricsCollector | None:
        return self._metrics_collector

    def set_metrics_collector(self, collector: MetricsCollector) -> None:
        self._metrics_collector = collector

    def reset(self) -> None:
        self._history.reset()
        self._last_request_count = 0
        self._start_time = time.time()
        if self._metrics_collector:
            self._metrics_collector.reset()

    def update_history(self) -> None:
        if not self._metrics_collector:
            return

        summary = self._metrics_collector.summary()
        current_count = summary.get("count", 0)
        is_running = summary.get("is_running", False)

        if is_running and current_count > self._last_request_count:
            elapsed = time.time() - self._start_time
            self._history.timestamps.append(round(elapsed, 1))
            self._history.latencies.append(
                round(summary.get("instant_latency_ms", summary.get("avg_ms", 0)), 2)
            )
            self._history.throughput.append(round(summary.get("throughput_qps", 0), 2))
            self._history.queries.append(summary.get("query_count", 0))
            self._history.cpu_percent.append(round(summary.get("cpu_percent", 0), 1))
            self._history.gpu_memory_mb.append(round(summary.get("gpu_memory_mb", 0), 1))
            self._history.gpu_utilization_pct.append(
                round(summary.get("gpu_utilization_pct", 0), 1)
            )
            self._history.queue_wait_ms.append(round(summary.get("last_queue_wait_ms", 0), 2))
            self._history.tokenize_ms.append(round(summary.get("last_tokenize_ms", 0), 2))
            self._history.inference_ms.append(round(summary.get("last_inference_ms", 0), 2))

            padding = summary.get("padding_analysis", {})
            self._history.padding_pct.append(round(padding.get("last_padding_pct", 0), 1))

            self._last_request_count = current_count

    def get_metrics_response(self) -> dict:
        self.update_history()

        if self._metrics_collector:
            data = self._metrics_collector.summary()
            data["history"] = self._history.to_dict()
        else:
            data = {"error": "No metrics available", "history": self._history.to_dict()}

        return data


class MetricsHandler(BaseHTTPRequestHandler):
    """HTTP request handler for dashboard endpoints."""

    def log_message(self, format, *args):
        pass

    @property
    def state(self) -> DashboardState:
        return DashboardState()

    def _send_response(self, content: bytes, content_type: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, data: dict, status: int = 200):
        content = json.dumps(data, indent=2).encode("utf-8")
        self._send_response(content, "application/json", status)

    def _send_file(self, filepath: Path):
        if not filepath.exists() or not filepath.is_file():
            self._send_response(b"Not Found", "text/plain", 404)
            return

        content_type, _ = mimetypes.guess_type(str(filepath))
        content_type = content_type or "application/octet-stream"

        with open(filepath, "rb") as f:
            content = f.read()
        self._send_response(content, content_type)

    def do_GET(self):
        path = self.path.split("?")[0]

        if path == "/" or path == "/index.html":
            self._send_file(TEMPLATES_DIR / "index.html")
        elif path == "/metrics":
            self._handle_metrics()
        elif path == "/reset":
            self._handle_reset()
        elif path.startswith("/static/"):
            relative = path[8:]
            self._send_file(STATIC_DIR / relative)
        else:
            self._send_response(b"Not Found", "text/plain", 404)

    def _handle_metrics(self):
        data = self.state.get_metrics_response()
        self._send_json(data)

    def _handle_reset(self):
        self.state.reset()
        self._send_json({"status": "reset"})


def set_metrics_collector(collector: MetricsCollector) -> None:
    """Set the metrics collector for the dashboard."""
    DashboardState().set_metrics_collector(collector)


def start_dashboard(port: int = 8080, metrics_collector: MetricsCollector = None) -> HTTPServer:
    """Start the dashboard HTTP server."""
    if metrics_collector:
        set_metrics_collector(metrics_collector)

    server = HTTPServer(("0.0.0.0", port), MetricsHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"Dashboard at http://localhost:{port}")
    return server


__all__ = ["start_dashboard", "set_metrics_collector", "MetricsHandler", "DashboardState"]
