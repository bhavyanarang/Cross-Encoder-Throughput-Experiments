"""
HTTP Server for ML Inference Metrics Dashboard.

Serves:
- /          : Dashboard HTML page
- /metrics   : JSON metrics endpoint
- /reset     : Reset metrics endpoint
- /static/*  : Static assets (CSS, JS)

Refactored to use dependency injection instead of global state.
"""

import json
import mimetypes
import threading
import time
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from .collector import MetricsCollector

logger = logging.getLogger(__name__)

# Dashboard directory paths
DASHBOARD_DIR = Path(__file__).parent.parent / "dashboard"
TEMPLATES_DIR = DASHBOARD_DIR / "templates"
STATIC_DIR = DASHBOARD_DIR / "static"


@dataclass
class MetricsHistory:
    """Stores history data for dashboard charts."""
    
    timestamps: list = field(default_factory=list)
    latencies: list = field(default_factory=list)
    throughput: list = field(default_factory=list)
    queries: list = field(default_factory=list)
    cpu_percent: list = field(default_factory=list)
    gpu_memory_mb: list = field(default_factory=list)
    queue_wait_ms: list = field(default_factory=list)
    tokenize_ms: list = field(default_factory=list)
    inference_ms: list = field(default_factory=list)
    
    start_time: float = field(default_factory=time.time)
    last_request_count: int = 0
    
    def reset(self) -> None:
        """Reset all history data."""
        self.timestamps = []
        self.latencies = []
        self.throughput = []
        self.queries = []
        self.cpu_percent = []
        self.gpu_memory_mb = []
        self.queue_wait_ms = []
        self.tokenize_ms = []
        self.inference_ms = []
        self.start_time = time.time()
        self.last_request_count = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamps": self.timestamps,
            "latencies": self.latencies,
            "throughput": self.throughput,
            "queries": self.queries,
            "cpu_percent": self.cpu_percent,
            "gpu_memory_mb": self.gpu_memory_mb,
            "queue_wait_ms": self.queue_wait_ms,
            "tokenize_ms": self.tokenize_ms,
            "inference_ms": self.inference_ms,
        }


class MetricsServer:
    """
    HTTP server for metrics dashboard with dependency injection.
    
    Usage:
        collector = MetricsCollector()
        server = MetricsServer(collector, port=8080)
        server.start()
    """
    
    def __init__(self, collector: "MetricsCollector", port: int = 8080):
        self.collector = collector
        self.port = port
        self.history = MetricsHistory()
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None
    
    def start(self) -> None:
        """Start the HTTP server in a background thread."""
        handler = self._create_handler()
        self._server = HTTPServer(("0.0.0.0", self.port), handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        logger.info(f"Metrics dashboard: http://localhost:{self.port}")
    
    def stop(self) -> None:
        """Stop the HTTP server."""
        if self._server:
            self._server.shutdown()
    
    def update_history(self) -> None:
        """Update metrics history for charts."""
        summary = self.collector.summary()
        current_count = summary.get("count", 0)
        is_running = summary.get("is_running", False)
        
        # Only add data points when experiment is running AND new requests processed
        if is_running and current_count > self.history.last_request_count:
            elapsed = time.time() - self.history.start_time
            self.history.timestamps.append(round(elapsed, 1))
            self.history.latencies.append(round(summary.get("instant_latency_ms", summary.get("avg_ms", 0)), 2))
            self.history.throughput.append(round(summary.get("throughput_qps", 0), 2))
            self.history.queries.append(summary.get("query_count", 0))
            self.history.cpu_percent.append(round(summary.get("cpu_percent", 0), 1))
            self.history.gpu_memory_mb.append(round(summary.get("gpu_memory_mb", 0), 1))
            self.history.queue_wait_ms.append(round(summary.get("last_queue_wait_ms", 0), 2))
            self.history.tokenize_ms.append(round(summary.get("last_tokenize_ms", 0), 2))
            self.history.inference_ms.append(round(summary.get("last_inference_ms", 0), 2))
            self.history.last_request_count = current_count
    
    def reset_history(self) -> None:
        """Reset history and collector."""
        self.history.reset()
        self.collector.reset()
    
    def _create_handler(self) -> type:
        """Create a handler class with access to server instance."""
        server_instance = self
        
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
                path = self.path.split("?")[0]
                
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
                server_instance.update_history()
                
                data = server_instance.collector.summary()
                data["history"] = server_instance.history.to_dict()
                
                self._send_json(data)
            
            def _handle_reset(self):
                """Handle metrics reset."""
                server_instance.reset_history()
                self._send_json({"status": "reset"})
            
            def _handle_static(self, path: str):
                """Serve static files (CSS, JS)."""
                relative_path = path[8:]  # Remove "/static/"
                filepath = STATIC_DIR / relative_path
                self._send_file(filepath)
        
        return MetricsHandler


# Legacy compatibility functions
_metrics_server: Optional[MetricsServer] = None


def set_metrics_collector(collector: "MetricsCollector") -> None:
    """
    Set the metrics collector for legacy compatibility.
    
    Deprecated: Use MetricsServer class directly instead.
    """
    global _metrics_server
    _metrics_server = MetricsServer(collector)


def start_metrics_server(port: int = 8080) -> HTTPServer:
    """
    Start the metrics HTTP server (legacy compatibility).
    
    Deprecated: Use MetricsServer class directly instead.
    """
    global _metrics_server
    
    if _metrics_server is None:
        raise RuntimeError("Call set_metrics_collector first")
    
    _metrics_server.port = port
    _metrics_server.start()
    return _metrics_server._server


__all__ = [
    "MetricsServer",
    "MetricsHistory",
    # Legacy compatibility
    "set_metrics_collector",
    "start_metrics_server",
]
