import json
import logging
import mimetypes
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import TYPE_CHECKING

from src.server.dto import DashboardHistory

if TYPE_CHECKING:
    from src.server.services.metrics_service import MetricsService

logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).parent
TEMPLATES_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR / "static"


class DashboardState:
    """Manages dashboard state. Use get_or_create() instead of direct instantiation."""

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
        self._metrics_service: MetricsService | None = None
        self._history = DashboardHistory()
        self._start_time = time.time()
        self._last_request_count = 0
        self._server: HTTPServer | None = None  # Track the server instance

    @property
    def metrics_service(self) -> "MetricsService | None":
        return self._metrics_service

    def set_metrics_service(self, service: "MetricsService") -> None:
        self._metrics_service = service

    def reset(self) -> None:
        self._history.reset()
        self._last_request_count = 0
        self._start_time = time.time()
        if self._metrics_service:
            self._metrics_service.reset()

    def update_history(self) -> None:
        if not self._metrics_service:
            return

        summary = self._metrics_service.get_summary()
        current_count = summary.get("count", 0)
        query_count = summary.get("query_count", 0)
        summary.get("is_running", False)

        # Update history more frequently for charts to show data
        # Always capture metrics at regular intervals for proper chart visualization
        elapsed = time.time() - self._start_time
        time_since_last_update = elapsed - (
            self._history.timestamps[-1] if self._history.timestamps else 0
        )

        # Update if:
        # 1. First update (no history yet)
        # 2. We have new queries (query_count increased)
        # 3. It's been at least 0.2 seconds since last update AND we have any activity
        has_any_activity = query_count > 0 or self._last_request_count > 0
        should_update = (
            not self._history.timestamps  # First update
            or query_count > self._last_request_count  # New queries
            or (has_any_activity and time_since_last_update >= 0.2)  # Periodic updates when active
        )

        if should_update:
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
            # Queue wait times (separate tracking)
            self._history.tokenizer_queue_wait_ms.append(
                round(summary.get("last_tokenizer_queue_wait_ms", 0), 2)
            )
            self._history.model_queue_wait_ms.append(
                round(summary.get("last_model_queue_wait_ms", 0), 2)
            )
            self._history.queue_wait_ms.append(
                round(summary.get("last_queue_wait_ms", 0), 2)
            )  # Combined for backward compatibility

            # Queue sizes
            queue_sizes = summary.get("queue_sizes", {})
            self._history.tokenizer_queue_size.append(queue_sizes.get("tokenizer_queue_size", 0))
            self._history.model_queue_size.append(queue_sizes.get("model_queue_size", 0))

            self._history.tokenize_ms.append(round(summary.get("last_tokenize_ms", 0), 2))
            self._history.inference_ms.append(round(summary.get("last_inference_ms", 0), 2))
            self._history.overhead_ms.append(round(summary.get("last_overhead_ms", 0), 2))

            padding = summary.get("padding_analysis", {})
            self._history.padding_pct.append(round(padding.get("last_padding_pct", 0), 1))

            tokenizer_worker_stats = summary.get("tokenizer_worker_stats", [])
            if tokenizer_worker_stats:
                avg_latency = sum(ws.get("avg_ms", 0) for ws in tokenizer_worker_stats) / len(
                    tokenizer_worker_stats
                )
                total_requests = sum(ws.get("request_count", 0) for ws in tokenizer_worker_stats)
                self._history.tokenizer_worker_latencies.append(round(avg_latency, 2))
                self._history.tokenizer_worker_requests.append(total_requests)

            # Pipeline throughput metrics (sum of all worker throughputs)
            tokenizer_throughput = (
                sum(ws.get("throughput_qps", 0) for ws in tokenizer_worker_stats)
                if tokenizer_worker_stats
                else 0
            )
            self._history.tokenizer_throughput_qps.append(round(tokenizer_throughput, 2))

            model_worker_stats = summary.get("worker_stats", [])
            inference_throughput = (
                sum(ws.get("throughput_qps", 0) for ws in model_worker_stats)
                if model_worker_stats
                else 0
            )
            self._history.inference_throughput_qps.append(round(inference_throughput, 2))

            # Overall response throughput is the same as system throughput_qps
            overall_throughput = summary.get("throughput_qps", 0)
            self._history.overall_throughput_qps.append(round(overall_throughput, 2))

            self._last_request_count = max(current_count, query_count)

    def get_metrics_response(self) -> dict:
        self.update_history()

        if self._metrics_service:
            try:
                data = self._metrics_service.get_summary()
                pipeline_mode = data.get("pipeline_mode", "full")

                if pipeline_mode == "tokenization_only":
                    filtered_history = self._history.to_dict()
                    filtered_history["inference_throughput_qps"] = []
                    filtered_history["inference_ms"] = []
                    filtered_history["model_queue_wait_ms"] = []
                    filtered_history["model_queue_size"] = []
                    data["history"] = filtered_history
                elif pipeline_mode == "inference_only":
                    filtered_history = self._history.to_dict()
                    filtered_history["tokenizer_throughput_qps"] = []
                    filtered_history["tokenizer_worker_latencies"] = []
                    filtered_history["tokenizer_queue_wait_ms"] = []
                    filtered_history["tokenizer_queue_size"] = []
                    data["history"] = filtered_history
                else:
                    data["history"] = self._history.to_dict()
            except Exception as e:
                logger.error(f"Error getting metrics summary: {e}", exc_info=True)
                data = {
                    "error": f"Error getting metrics: {str(e)}",
                    "history": self._history.to_dict(),
                    "is_running": False,
                }
        else:
            data = {"error": "No metrics available", "history": self._history.to_dict()}

        return data


class MetricsHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    @property
    def state(self) -> DashboardState:
        return DashboardState()

    def _send_response(self, content: bytes, content_type: str, status: int = 200):
        try:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))

            # Only allow CORS from localhost/127.0.0.1 by default for security
            origin = self.headers.get("Origin", "")
            if origin in (
                "http://localhost:8080",
                "http://127.0.0.1:8080",
                "http://localhost",
                "http://127.0.0.1",
            ):
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
            # For non-browser requests, don't send CORS header

            self.end_headers()
            self.wfile.write(content)
        except BrokenPipeError:
            # Client disconnected before response could be sent - ignore
            logger.debug("Client disconnected before response sent")
        except Exception as e:
            logger.error(f"Error sending response: {e}", exc_info=True)

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
            try:
                self._handle_metrics()
            except Exception as e:
                logger.error(f"Error handling metrics request: {e}", exc_info=True)
                error_data = {
                    "error": f"Error getting metrics: {str(e)}",
                    "history": {},
                    "is_running": False,
                }
                self._send_json(error_data, status=500)
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


def set_metrics_service(service: "MetricsService") -> None:
    DashboardState().set_metrics_service(service)


def start_dashboard(
    port: int = 8080, metrics_service: "MetricsService | None" = None, host: str = "0.0.0.0"
) -> HTTPServer:
    """Start the dashboard HTTP server on the specified host and port.

    Args:
        port: HTTP port to listen on (default 8080)
        metrics_service: Optional metrics service to display
        host: Host to bind to (default "0.0.0.0", use "127.0.0.1" for local-only)

    Returns:
        HTTPServer instance that can be shut down with server.shutdown()
    """
    if metrics_service:
        set_metrics_service(metrics_service)

    server = HTTPServer((host, port), MetricsHandler)
    state = DashboardState()
    state._server = server

    # Use non-daemon thread so it doesn't prevent clean shutdown
    thread = threading.Thread(target=server.serve_forever, daemon=False)
    thread.start()
    logger.info(f"Dashboard at http://{host}:{port}")
    return server


def stop_dashboard() -> None:
    """Stop the dashboard server if running."""
    state = DashboardState()
    if state._server:
        try:
            state._server.shutdown()
            state._server.server_close()
            state._server = None
            logger.info("Dashboard stopped")
        except Exception as e:
            logger.warning(f"Error stopping dashboard: {e}")


__all__ = [
    "start_dashboard",
    "stop_dashboard",
    "set_metrics_service",
    "MetricsHandler",
    "DashboardState",
]
