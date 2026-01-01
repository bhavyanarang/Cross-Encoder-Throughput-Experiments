"""Integration tests for the frontend dashboard."""

import json
import socket
import time
from http.client import HTTPConnection, HTTPResponse
from unittest.mock import MagicMock

import pytest

from src.frontend.server import (
    DashboardState,
    set_metrics_service,
    start_dashboard,
    stop_dashboard,
)
from src.server.services.metrics_service import MetricsService


def find_free_port():
    """Find a free port for testing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


class TestDashboardHTTPEndpoints:
    """Test HTTP endpoints of the dashboard."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown dashboard server for each test."""
        # Reset dashboard state
        state = DashboardState()
        state.reset()
        state._metrics_service = None
        state._server = None

        # Start dashboard on a free port
        self.port = find_free_port()
        self.server = start_dashboard(port=self.port, host="127.0.0.1")
        time.sleep(0.1)  # Give server time to start
        yield
        # Cleanup
        stop_dashboard()
        if self.server:
            try:
                self.server.shutdown()
                self.server.server_close()
            except Exception:
                pass
        time.sleep(0.2)  # Give server time to shut down

    def _make_request(self, path: str, method: str = "GET") -> HTTPResponse:
        """Make an HTTP request to the dashboard."""
        conn = HTTPConnection("127.0.0.1", self.port, timeout=2)
        try:
            conn.request(method, path)
            response = conn.getresponse()
            return response
        finally:
            conn.close()

    def test_root_endpoint_serves_html(self):
        """Test that GET / serves the HTML dashboard."""
        response = self._make_request("/")
        assert response.status == 200
        assert "text/html" in response.getheader("Content-Type")
        content = response.read().decode("utf-8")
        assert "<!DOCTYPE html>" in content
        assert "ML Inference Dashboard" in content

    def test_index_html_endpoint_serves_html(self):
        """Test that GET /index.html serves the HTML dashboard."""
        response = self._make_request("/index.html")
        assert response.status == 200
        assert "text/html" in response.getheader("Content-Type")
        content = response.read().decode("utf-8")
        assert "<!DOCTYPE html>" in content

    def test_metrics_endpoint_returns_json(self):
        """Test that GET /metrics returns JSON metrics."""
        response = self._make_request("/metrics")
        assert response.status == 200
        assert "application/json" in response.getheader("Content-Type")
        data = json.loads(response.read().decode("utf-8"))
        assert isinstance(data, dict)
        assert "history" in data
        assert "error" in data  # No metrics service set

    def test_metrics_endpoint_with_metrics_service(self):
        """Test that GET /metrics returns metrics when service is set."""
        metrics_service = MetricsService()
        set_metrics_service(metrics_service)
        metrics_service.record(10.5, num_queries=1)

        response = self._make_request("/metrics")
        assert response.status == 200
        data = json.loads(response.read().decode("utf-8"))
        assert "history" in data
        assert "query_count" in data
        assert data["query_count"] == 1

    def test_reset_endpoint(self):
        """Test that GET /reset resets metrics and returns status."""
        metrics_service = MetricsService()
        set_metrics_service(metrics_service)
        metrics_service.record(10.5, num_queries=1)

        # Verify metrics exist
        response = self._make_request("/metrics")
        data = json.loads(response.read().decode("utf-8"))
        assert data["query_count"] == 1

        # Reset
        response = self._make_request("/reset")
        assert response.status == 200
        data = json.loads(response.read().decode("utf-8"))
        assert data["status"] == "reset"

        # Verify metrics are reset
        response = self._make_request("/metrics")
        data = json.loads(response.read().decode("utf-8"))
        assert data["query_count"] == 0

    def test_static_css_files(self):
        """Test that static CSS files are served."""
        response = self._make_request("/static/css/styles.css")
        assert response.status == 200
        assert "text/css" in response.getheader(
            "Content-Type"
        ) or "text/plain" in response.getheader("Content-Type")

    def test_static_js_files(self):
        """Test that static JS files are served."""
        response = self._make_request("/static/js/main.js")
        assert response.status == 200
        content_type = response.getheader("Content-Type")
        assert "javascript" in content_type or "text/plain" in content_type

    def test_nonexistent_endpoint_returns_404(self):
        """Test that nonexistent endpoints return 404."""
        response = self._make_request("/nonexistent")
        assert response.status == 404

    def test_nonexistent_static_file_returns_404(self):
        """Test that nonexistent static files return 404."""
        response = self._make_request("/static/css/nonexistent.css")
        assert response.status == 404


class TestDashboardState:
    """Test dashboard state management."""

    @pytest.fixture(autouse=True)
    def reset_state(self):
        """Reset dashboard state before each test."""
        state = DashboardState()
        state.reset()
        state._metrics_service = None
        state._server = None
        yield
        state.reset()
        state._metrics_service = None
        state._server = None

    def test_dashboard_state_singleton(self):
        """Test that DashboardState is a singleton."""
        state1 = DashboardState()
        state2 = DashboardState()
        assert state1 is state2

    def test_set_metrics_service(self):
        """Test setting metrics service."""
        state = DashboardState()
        metrics_service = MetricsService()
        state.set_metrics_service(metrics_service)
        assert state.metrics_service is metrics_service

    def test_get_metrics_response_without_service(self):
        """Test getting metrics response without metrics service."""
        state = DashboardState()
        response = state.get_metrics_response()
        assert "error" in response
        assert response["error"] == "No metrics available"
        assert "history" in response

    def test_get_metrics_response_with_service(self):
        """Test getting metrics response with metrics service."""
        state = DashboardState()
        metrics_service = MetricsService()
        metrics_service.record(10.5, num_queries=1)
        state.set_metrics_service(metrics_service)

        response = state.get_metrics_response()
        assert "query_count" in response
        assert response["query_count"] == 1
        assert "history" in response

    def test_get_metrics_response_with_service_error(self):
        """Test getting metrics response when service throws error."""
        state = DashboardState()
        metrics_service = MagicMock()
        # Mock get_summary to raise exception
        metrics_service.get_summary.side_effect = Exception("Test error")
        state.set_metrics_service(metrics_service)

        # Patch update_history to not raise, since the exception will be caught
        # in get_metrics_response's try-except block when it calls get_summary()
        original_update_history = state.update_history

        def update_history_no_raise():
            try:
                original_update_history()
            except Exception:
                # Swallow exception from update_history, let get_metrics_response handle it
                pass

        state.update_history = update_history_no_raise

        # Now get_summary will be called in get_metrics_response's try block
        response = state.get_metrics_response()
        assert "error" in response
        assert "Test error" in response["error"]
        assert "history" in response
        assert response["is_running"] is False

    def test_reset(self):
        """Test resetting dashboard state."""
        state = DashboardState()
        metrics_service = MetricsService()
        metrics_service.record(10.5, num_queries=1)
        state.set_metrics_service(metrics_service)

        # Update history to have some data
        state.update_history()
        assert len(state._history.timestamps) > 0

        # Reset
        state.reset()
        assert len(state._history.timestamps) == 0
        assert state._last_request_count == 0

    def test_update_history_without_service(self):
        """Test updating history without metrics service."""
        state = DashboardState()
        state.update_history()
        # Should not crash, just return early
        assert len(state._history.timestamps) == 0

    def test_update_history_with_service(self):
        """Test updating history with metrics service."""
        state = DashboardState()
        metrics_service = MetricsService()
        metrics_service.record(10.5, num_queries=1)
        state.set_metrics_service(metrics_service)

        state.update_history()
        assert len(state._history.timestamps) > 0
        assert len(state._history.latencies) > 0
        assert len(state._history.queries) > 0

    def test_update_history_periodic_updates(self):
        """Test that history updates periodically."""
        state = DashboardState()
        metrics_service = MetricsService()
        metrics_service.record(10.5, num_queries=1)
        state.set_metrics_service(metrics_service)

        # First update
        state.update_history()
        initial_count = len(state._history.timestamps)

        # Wait a bit and update again
        time.sleep(0.3)
        state.update_history()
        assert len(state._history.timestamps) > initial_count


class TestDashboardMetricsIntegration:
    """Test dashboard integration with MetricsService."""

    @pytest.fixture(autouse=True)
    def reset_state(self):
        """Reset dashboard state before each test."""
        state = DashboardState()
        state.reset()
        state._metrics_service = None
        state._server = None
        yield
        state.reset()
        state._metrics_service = None
        state._server = None

    def test_metrics_response_includes_all_fields(self):
        """Test that metrics response includes all expected fields."""
        state = DashboardState()
        metrics_service = MetricsService()
        metrics_service.record(10.5, num_queries=1)
        metrics_service.record_stage_timings(
            t_tokenize=2.0,
            t_model_inference=8.0,
            t_tokenizer_queue_wait=0.5,
            t_model_queue_wait=0.5,
            t_overhead=1.0,
            total_ms=10.5,
        )
        state.set_metrics_service(metrics_service)

        response = state.get_metrics_response()
        assert "query_count" in response
        assert "throughput_qps" in response
        assert "avg_ms" in response
        assert "history" in response
        assert "cpu_percent" in response
        assert "gpu_memory_mb" in response
        assert "queue_sizes" in response
        assert "worker_stats" in response
        assert "tokenizer_worker_stats" in response

    def test_history_structure(self):
        """Test that history has the correct structure."""
        state = DashboardState()
        metrics_service = MetricsService()
        metrics_service.record(10.5, num_queries=1)
        state.set_metrics_service(metrics_service)

        state.update_history()
        history_dict = state._history.to_dict()

        assert "timestamps" in history_dict
        assert "latencies" in history_dict
        assert "throughput" in history_dict
        assert "queries" in history_dict
        assert "cpu_percent" in history_dict
        assert "gpu_memory_mb" in history_dict
        assert "tokenize_ms" in history_dict
        assert "inference_ms" in history_dict

    def test_metrics_with_multiple_recordings(self):
        """Test metrics with multiple recordings."""
        state = DashboardState()
        metrics_service = MetricsService()
        for i in range(5):
            metrics_service.record(10.0 + i, num_queries=1)
        state.set_metrics_service(metrics_service)

        response = state.get_metrics_response()
        assert response["query_count"] == 5
        assert response["avg_ms"] > 0

    def test_metrics_with_stage_breakdown(self):
        """Test metrics with stage breakdown."""
        state = DashboardState()
        metrics_service = MetricsService()
        metrics_service.record(10.5, num_queries=1)
        metrics_service.record_stage_timings(
            t_tokenize=2.0,
            t_model_inference=8.0,
            t_overhead=0.5,
            total_ms=10.5,
        )
        state.set_metrics_service(metrics_service)

        response = state.get_metrics_response()
        assert "last_tokenize_ms" in response
        assert "last_inference_ms" in response
        assert "last_overhead_ms" in response


class TestDashboardCORS:
    """Test CORS headers."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown dashboard server for each test."""
        state = DashboardState()
        state.reset()
        state._metrics_service = None
        state._server = None

        self.port = find_free_port()
        self.server = start_dashboard(port=self.port, host="127.0.0.1")
        time.sleep(0.1)  # Give server time to start
        yield
        stop_dashboard()
        if self.server:
            try:
                self.server.shutdown()
                self.server.server_close()
            except Exception:
                pass
        time.sleep(0.2)  # Give server time to shut down

    def _make_request_with_origin(self, path: str, origin: str) -> HTTPResponse:
        """Make an HTTP request with Origin header."""
        conn = HTTPConnection("127.0.0.1", self.port, timeout=2)
        try:
            conn.request("GET", path, headers={"Origin": origin})
            response = conn.getresponse()
            return response
        finally:
            conn.close()

    def test_cors_allowed_origins(self):
        """Test that CORS headers are set for allowed origins."""
        allowed_origins = [
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            "http://localhost",
            "http://127.0.0.1",
        ]

        for origin in allowed_origins:
            response = self._make_request_with_origin("/metrics", origin)
            cors_header = response.getheader("Access-Control-Allow-Origin")
            assert cors_header == origin, f"CORS header not set for {origin}"

    def test_cors_not_set_for_other_origins(self):
        """Test that CORS headers are not set for other origins."""
        response = self._make_request_with_origin("/metrics", "http://evil.com")
        cors_header = response.getheader("Access-Control-Allow-Origin")
        assert cors_header is None

    def test_cors_methods_header(self):
        """Test that CORS methods header is set."""
        response = self._make_request_with_origin("/metrics", "http://localhost:8080")
        methods_header = response.getheader("Access-Control-Allow-Methods")
        assert methods_header == "GET, POST, OPTIONS"

    def test_cors_headers_header(self):
        """Test that CORS headers header is set."""
        response = self._make_request_with_origin("/metrics", "http://localhost:8080")
        headers_header = response.getheader("Access-Control-Allow-Headers")
        assert headers_header == "Content-Type"


class TestDashboardConcurrency:
    """Test dashboard behavior under concurrent requests."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown dashboard server for each test."""
        state = DashboardState()
        state.reset()
        metrics_service = MetricsService()
        metrics_service.record(10.5, num_queries=1)
        set_metrics_service(metrics_service)

        self.port = find_free_port()
        self.server = start_dashboard(port=self.port, host="127.0.0.1")
        time.sleep(0.1)  # Give server time to start
        yield
        stop_dashboard()
        if self.server:
            try:
                self.server.shutdown()
                self.server.server_close()
            except Exception:
                pass
        time.sleep(0.2)  # Give server time to shut down

    def _make_request(self, path: str) -> HTTPResponse:
        """Make an HTTP request to the dashboard."""
        conn = HTTPConnection("127.0.0.1", self.port, timeout=2)
        try:
            conn.request("GET", path)
            response = conn.getresponse()
            return response
        finally:
            conn.close()

    def test_concurrent_metrics_requests(self):
        """Test that multiple concurrent metrics requests work."""
        import concurrent.futures

        def make_request():
            response = self._make_request("/metrics")
            assert response.status == 200
            data = json.loads(response.read().decode("utf-8"))
            return data

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All requests should succeed
        assert len(results) == 10
        for result in results:
            assert "query_count" in result
            assert "history" in result
