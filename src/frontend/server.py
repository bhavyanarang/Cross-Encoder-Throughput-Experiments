"""HTTP server for metrics dashboard."""

import http.server
import json
import logging
import threading
from pathlib import Path

logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).parent


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for dashboard."""

    metrics_collector = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/metrics":
            self._send_json(self._get_metrics())
        elif self.path == "/" or self.path == "/index.html":
            self._serve_template()
        else:
            super().do_GET()

    def _send_json(self, data: dict):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _serve_template(self):
        template = FRONTEND_DIR / "templates" / "index.html"
        if template.exists():
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(template.read_bytes())
        else:
            self.send_error(404)

    def _get_metrics(self) -> dict:
        if self.metrics_collector is None:
            return {"error": "No metrics collector"}
        return self.metrics_collector.get_json()

    def log_message(self, format, *args):
        pass  # Suppress request logs


def start_dashboard(port: int = 8080, metrics_collector=None):
    """Start dashboard server in background thread."""
    DashboardHandler.metrics_collector = metrics_collector
    server = http.server.HTTPServer(("0.0.0.0", port), DashboardHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"Dashboard at http://localhost:{port}")
    return server


__all__ = ["start_dashboard", "DashboardHandler"]
