import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import deque
import logging
from prometheus_client import CONTENT_TYPE_LATEST

logger = logging.getLogger(__name__)

_metrics_collector = None
_history = {
    "timestamps": deque(maxlen=200),
    "latencies": deque(maxlen=200),
    "throughput": deque(maxlen=200),
    "requests": deque(maxlen=200),
    "cpu_percent": deque(maxlen=200),
    "gpu_memory_mb": deque(maxlen=200),
}
_start_time = time.time()
_last_request_count = 0


def set_metrics_collector(collector):
    global _metrics_collector
    _metrics_collector = collector


def update_history():
    """Update metrics history for charts - only when new requests are processed."""
    global _last_request_count
    
    if _metrics_collector:
        summary = _metrics_collector.summary()
        current_count = summary.get("count", 0)
        is_running = summary.get("is_running", False)
        
        # Only add data points when experiment is running AND new requests processed
        if is_running and current_count > _last_request_count:
            elapsed = time.time() - _start_time
            _history["timestamps"].append(round(elapsed, 1))
            _history["latencies"].append(round(summary.get("avg_ms", 0), 2))
            _history["throughput"].append(round(summary.get("throughput_rps", 0), 2))
            _history["requests"].append(current_count)
            _history["cpu_percent"].append(round(summary.get("cpu_percent", 0), 1))
            _history["gpu_memory_mb"].append(round(summary.get("gpu_memory_mb", 0), 1))
            _last_request_count = current_count


class MetricsHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            update_history()
            
            if _metrics_collector:
                data = _metrics_collector.summary()
                data["history"] = {
                    "timestamps": list(_history["timestamps"]),
                    "latencies": list(_history["latencies"]),
                    "throughput": list(_history["throughput"]),
                    "requests": list(_history["requests"]),
                    "cpu_percent": list(_history["cpu_percent"]),
                    "gpu_memory_mb": list(_history["gpu_memory_mb"]),
                }
            else:
                data = {"error": "No metrics available"}
            
            self.wfile.write(json.dumps(data, indent=2).encode())
        
        elif self.path == "/prometheus":
            # Prometheus format metrics
            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.end_headers()
            if _metrics_collector:
                self.wfile.write(_metrics_collector.get_prometheus_metrics())
            else:
                self.wfile.write(b"")
        
        elif self.path == "/reset":
            global _last_request_count
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            for key in _history:
                _history[key].clear()
            _last_request_count = 0
            if _metrics_collector:
                _metrics_collector.reset()
            self.wfile.write(json.dumps({"status": "reset"}).encode())
        
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = """
<!DOCTYPE html>
<html>
<head>
    <title>ML Inference Metrics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', system-ui, sans-serif; 
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            color: #eee; 
            min-height: 100vh;
            padding: 20px;
        }
        .header { 
            text-align: center; 
            padding: 15px;
            margin-bottom: 20px;
        }
        h1 { color: #00d9ff; font-size: 1.8em; margin-bottom: 5px; }
        .subtitle { color: #666; font-size: 0.85em; }
        .endpoints { color: #444; font-size: 0.75em; margin-top: 5px; }
        .endpoints a { color: #00d9ff; text-decoration: none; }
        .status { 
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            margin-top: 10px;
        }
        .status.running { background: #00c853; color: #000; animation: pulse 2s infinite; }
        .status.idle { background: #444; color: #888; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .metrics-row { 
            display: flex; 
            gap: 15px; 
            margin-bottom: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .metric-card {
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            padding: 15px 25px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.08);
            min-width: 140px;
        }
        .metric-label { color: #666; font-size: 0.75em; text-transform: uppercase; letter-spacing: 1px; }
        .metric-value { 
            font-size: 2em; 
            font-weight: 600;
            color: #00d9ff;
            margin: 5px 0;
        }
        .metric-unit { color: #444; font-size: 0.75em; }
        
        .charts-container {
            max-width: 900px;
            margin: 0 auto;
        }
        .chart-container {
            background: rgba(255,255,255,0.02);
            border-radius: 10px;
            padding: 15px 20px;
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.05);
        }
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .chart-title {
            color: #888;
            font-size: 0.9em;
            font-weight: 500;
        }
        .chart-value {
            color: #00d9ff;
            font-size: 1.1em;
            font-weight: 600;
        }
        canvas { height: 120px !important; }
    </style>
</head>
<body>
    <div class="header">
        <h1>ML Inference Dashboard</h1>
        <div class="subtitle">Real-time metrics • sentence-transformers/all-MiniLM-L6-v2 • MPS</div>
        <div class="endpoints">
            Endpoints: <a href="/metrics">/metrics</a> (JSON) | 
            <a href="/prometheus">/prometheus</a> (Prometheus) |
            <a href="/reset">/reset</a>
        </div>
        <div class="status idle" id="status">Idle</div>
    </div>
    
    <div class="metrics-row">
        <div class="metric-card">
            <div class="metric-label">Requests</div>
            <div class="metric-value" id="count">0</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Avg Latency</div>
            <div class="metric-value" id="avg_ms">0</div>
            <div class="metric-unit">ms</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">P95</div>
            <div class="metric-value" id="p95_ms">0</div>
            <div class="metric-unit">ms</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Throughput</div>
            <div class="metric-value" id="throughput_rps">0</div>
            <div class="metric-unit">req/s</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">CPU</div>
            <div class="metric-value" id="cpu_percent">0</div>
            <div class="metric-unit">%</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">GPU Memory</div>
            <div class="metric-value" id="gpu_memory_mb">0</div>
            <div class="metric-unit">MB</div>
        </div>
    </div>
    
    <div class="charts-container">
        <div class="chart-container">
            <div class="chart-header">
                <span class="chart-title">Latency (ms)</span>
                <span class="chart-value" id="latency_live">0 ms</span>
            </div>
            <canvas id="latencyChart"></canvas>
        </div>
        
        <div class="chart-container">
            <div class="chart-header">
                <span class="chart-title">Throughput (req/s)</span>
                <span class="chart-value" id="throughput_live">0 req/s</span>
            </div>
            <canvas id="throughputChart"></canvas>
        </div>
        
        <div class="chart-container">
            <div class="chart-header">
                <span class="chart-title">Requests Processed</span>
                <span class="chart-value" id="requests_live">0</span>
            </div>
            <canvas id="requestsChart"></canvas>
        </div>
        
        <div class="chart-container" style="border-color: rgba(255,159,64,0.3);">
            <div class="chart-header">
                <span class="chart-title">CPU Usage (%)</span>
                <span class="chart-value" id="cpu_live">0%</span>
            </div>
            <canvas id="cpuChart"></canvas>
        </div>
        
        <div class="chart-container" style="border-color: rgba(153,102,255,0.3);">
            <div class="chart-header">
                <span class="chart-title">GPU Memory (MB) - MPS</span>
                <span class="chart-value" id="gpu_live">0 MB</span>
            </div>
            <canvas id="gpuChart"></canvas>
        </div>
    </div>

    <script>
        const chartConfig = (color, fillColor) => ({
            type: 'line',
            data: { labels: [], datasets: [{ data: [], borderColor: color, backgroundColor: fillColor, fill: true, tension: 0.3, pointRadius: 0, borderWidth: 2 }] },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 0 },
                scales: {
                    x: { display: false },
                    y: { 
                        grid: { color: 'rgba(255,255,255,0.03)' },
                        ticks: { color: '#444', font: { size: 10 } },
                        beginAtZero: true
                    }
                },
                plugins: { legend: { display: false } }
            }
        });

        const latencyChart = new Chart(document.getElementById('latencyChart'), chartConfig('#ff6384', 'rgba(255,99,132,0.1)'));
        const throughputChart = new Chart(document.getElementById('throughputChart'), chartConfig('#36a2eb', 'rgba(54,162,235,0.1)'));
        const requestsChart = new Chart(document.getElementById('requestsChart'), chartConfig('#4bc0c0', 'rgba(75,192,192,0.1)'));
        const cpuChart = new Chart(document.getElementById('cpuChart'), chartConfig('#ff9f40', 'rgba(255,159,64,0.1)'));
        const gpuChart = new Chart(document.getElementById('gpuChart'), chartConfig('#9966ff', 'rgba(153,102,255,0.1)'));

        function updateChart(chart, labels, data) {
            chart.data.labels = labels;
            chart.data.datasets[0].data = data;
            chart.update('none');
        }

        async function update() {
            try {
                const res = await fetch('/metrics');
                const data = await res.json();
                
                document.getElementById('count').textContent = data.count || 0;
                document.getElementById('avg_ms').textContent = (data.avg_ms || 0).toFixed(1);
                document.getElementById('p95_ms').textContent = (data.p95_ms || 0).toFixed(1);
                document.getElementById('throughput_rps').textContent = (data.throughput_rps || 0).toFixed(1);
                document.getElementById('cpu_percent').textContent = (data.cpu_percent || 0).toFixed(0);
                document.getElementById('gpu_memory_mb').textContent = (data.gpu_memory_mb || 0).toFixed(0);
                
                document.getElementById('latency_live').textContent = (data.avg_ms || 0).toFixed(1) + ' ms';
                document.getElementById('throughput_live').textContent = (data.throughput_rps || 0).toFixed(1) + ' req/s';
                document.getElementById('requests_live').textContent = data.count || 0;
                document.getElementById('cpu_live').textContent = (data.cpu_percent || 0).toFixed(0) + '%';
                document.getElementById('gpu_live').textContent = (data.gpu_memory_mb || 0).toFixed(0) + ' MB';
                
                const status = document.getElementById('status');
                if (data.is_running) {
                    status.textContent = 'Running';
                    status.className = 'status running';
                } else {
                    status.textContent = 'Idle';
                    status.className = 'status idle';
                }

                if (data.history) {
                    const labels = data.history.timestamps.map(t => t + 's');
                    updateChart(latencyChart, labels, data.history.latencies);
                    updateChart(throughputChart, labels, data.history.throughput);
                    updateChart(requestsChart, labels, data.history.requests);
                    updateChart(cpuChart, labels, data.history.cpu_percent);
                    updateChart(gpuChart, labels, data.history.gpu_memory_mb);
                }
            } catch (e) {
                document.getElementById('status').textContent = 'Disconnected';
                document.getElementById('status').className = 'status';
            }
        }
        
        update();
        setInterval(update, 500);
    </script>
</body>
</html>
"""
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()


def start_metrics_server(port: int = 8080):
    server = HTTPServer(("0.0.0.0", port), MetricsHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"Metrics dashboard: http://localhost:{port}")
    logger.info(f"Prometheus metrics: http://localhost:{port}/prometheus")
    return server
