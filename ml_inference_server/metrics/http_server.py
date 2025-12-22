"""
HTTP Server for ML Inference Metrics Dashboard.

Serves:
- /          : Dashboard HTML page
- /metrics   : JSON metrics endpoint
- /reset     : Reset metrics endpoint
- /static/*  : Static assets (CSS, JS)
"""

import json
import mimetypes
import os
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Dashboard directory paths
DASHBOARD_DIR = Path(__file__).parent.parent / "dashboard"
TEMPLATES_DIR = DASHBOARD_DIR / "templates"
STATIC_DIR = DASHBOARD_DIR / "static"

_metrics_collector = None

# Metrics history for charts
_history = {
    "timestamps": [],
    "latencies": [],
    "throughput": [],
    "queries": [],
    "cpu_percent": [],
    "gpu_memory_mb": [],
    "queue_wait_ms": [],
    "tokenize_ms": [],
    "inference_ms": [],
}
_start_time = time.time()
_last_request_count = 0


def set_metrics_collector(collector):
    """Set the metrics collector instance for the dashboard."""
    global _metrics_collector
    _metrics_collector = collector


def _reset_history():
    """Reset all history data."""
    global _history, _last_request_count, _start_time
    _history = {
        "timestamps": [],
        "latencies": [],
        "throughput": [],
        "queries": [],
        "cpu_percent": [],
        "gpu_memory_mb": [],
        "queue_wait_ms": [],
        "tokenize_ms": [],
        "inference_ms": [],
    }
    _last_request_count = 0
    _start_time = time.time()


def update_history():
    """Update metrics history for charts - only when new requests are processed."""
    global _last_request_count
    
    if not _metrics_collector:
        return
        
    summary = _metrics_collector.summary()
    current_count = summary.get("count", 0)
    is_running = summary.get("is_running", False)
    
    # Only add data points when experiment is running AND new requests processed
    if is_running and current_count > _last_request_count:
        elapsed = time.time() - _start_time
        _history["timestamps"].append(round(elapsed, 1))
        _history["latencies"].append(round(summary.get("instant_latency_ms", summary.get("avg_ms", 0)), 2))
        _history["throughput"].append(round(summary.get("throughput_qps", 0), 2))
        _history["queries"].append(summary.get("query_count", 0))
        _history["cpu_percent"].append(round(summary.get("cpu_percent", 0), 1))
        _history["gpu_memory_mb"].append(round(summary.get("gpu_memory_mb", 0), 1))
        _history["queue_wait_ms"].append(round(summary.get("last_queue_wait_ms", 0), 2))
        _history["tokenize_ms"].append(round(summary.get("last_tokenize_ms", 0), 2))
        _history["inference_ms"].append(round(summary.get("last_inference_ms", 0), 2))
        _last_request_count = current_count


class MetricsHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the metrics dashboard."""
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def _send_response(self, content: bytes, content_type: str, status: int = 200):
        """Send HTTP response with content."""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        content = json.dumps(data, indent=2).encode("utf-8")
        self._send_response(content, "application/json", status)

    def _send_file(self, filepath: Path):
        """Send static file."""
        if not filepath.exists() or not filepath.is_file():
            self._send_not_found()
            return
            
        # Security: ensure file is within allowed directories
        try:
            filepath.resolve().relative_to(DASHBOARD_DIR.resolve())
        except ValueError:
            self._send_not_found()
            return
        
        content_type, _ = mimetypes.guess_type(str(filepath))
        content_type = content_type or "application/octet-stream"
        
        with open(filepath, "rb") as f:
            content = f.read()
        
        self._send_response(content, content_type)

    def _send_not_found(self):
        """Send 404 response."""
        self._send_response(b"Not Found", "text/plain", 404)

    def do_GET(self):
        """Handle GET requests."""
        path = self.path.split("?")[0]  # Remove query string
        
        if path == "/":
            self._handle_index()
        elif path == "/metrics":
            self._handle_metrics()
        elif path == "/reset":
            self._handle_reset()
        elif path.startswith("/static/"):
            self._handle_static(path)
        else:
            self._send_not_found()

    def _handle_index(self):
        """Serve the dashboard HTML page."""
        template_path = TEMPLATES_DIR / "index.html"
        self._send_file(template_path)

    def _handle_metrics(self):
        """Serve metrics JSON endpoint."""
        update_history()
        
        if _metrics_collector:
            data = _metrics_collector.summary()
            data["history"] = _history.copy()
        else:
            data = {"error": "No metrics available"}
        
        self._send_json(data)

    def _handle_reset(self):
        """Handle metrics reset."""
        _reset_history()
        if _metrics_collector:
            _metrics_collector.reset()
        self._send_json({"status": "reset"})

    def _handle_static(self, path: str):
        """Serve static files (CSS, JS)."""
        # Remove /static/ prefix and construct file path
        relative_path = path[8:]  # len("/static/") = 8
        filepath = STATIC_DIR / relative_path
        self._send_file(filepath)


def start_metrics_server(port: int = 8080) -> HTTPServer:
    """Start the metrics HTTP server in a background thread."""
    server = HTTPServer(("0.0.0.0", port), MetricsHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"Metrics dashboard: http://localhost:{port}")
    return server
