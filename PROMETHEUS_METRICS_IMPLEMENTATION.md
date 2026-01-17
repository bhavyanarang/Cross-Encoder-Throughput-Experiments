# Prometheus-Native Metrics Implementation Guide

## Overview

This document describes the complete migration from custom metrics tracking to a Prometheus-native architecture. All metrics are now exposed via Prometheus, and Grafana queries Prometheus directly instead of relying on application-level aggregations.

## Architecture

```
Worker/Service
    ↓ (calls MetricsService.record_*())
MetricsService
    ↓ (increments Prometheus metrics)
Prometheus Metrics (Counter, Gauge, Histogram)
    ↓ (scrapes /metrics endpoint)
Prometheus Server (port 9091)
    ↓ (queries)
Grafana Dashboard
    ↓ (displays visualizations)
User
```

## Metrics Exposed

### 1. System Metrics (Gauges)

Gauges represent instantaneous values and should be scraped regularly.

| Metric | Type | Description | Labels | Units |
|--------|------|-------------|--------|-------|
| `gpu_memory_mb` | Gauge | GPU Memory Usage | - | MB |
| `gpu_utilization_pct` | Gauge | GPU Utilization | - | % |
| `cpu_percent` | Gauge | CPU Usage Percentage | - | % |
| `tokenizer_queue_size` | Gauge | Tokenizer Queue Depth | - | count |
| `model_queue_size` | Gauge | Model Queue Depth | - | count |
| `batch_queue_size` | Gauge | Batch Queue Depth | - | count |
| `padding_ratio` | Gauge | Padding Ratio | - | 0-1 |
| `max_seq_length` | Gauge | Maximum Sequence Length | - | tokens |
| `avg_seq_length` | Gauge | Average Sequence Length | - | tokens |

**Recording Locations:**
- `gpu_memory_mb`: `MetricsService._update_system_metrics()`
- `gpu_utilization_pct`: `record_gpu_utilization()`
- `cpu_percent`: `MetricsService._update_system_metrics()`
- Queue sizes: `MetricsService._update_system_metrics()`
- Padding stats: `record_padding_stats()`

### 2. Request Counters

Counters monotonically increase and are used for rates.

| Metric | Type | Description | Labels | Units |
|--------|------|-------------|--------|-------|
| `request_count_total` | Counter | Total Requests Processed | - | count |
| `padded_tokens_total` | Counter | Total Padded Tokens | - | tokens |
| `total_tokens_total` | Counter | Total Tokens Processed | - | tokens |
| `worker_request_count_total` | Counter | Per-Worker Request Count | `worker_id`, `worker_type` | count |

**Recording Locations:**
- `request_count_total`: `MetricsService.record()` increments
- Token counters: `record_padding_stats()`
- `worker_request_count_total`: `record_worker_stats()` and `record_tokenizer_worker_stats()`

### 3. Latency Histograms

Histograms track distribution of latencies with configurable buckets.

| Metric | Type | Description | Labels | Units |
|--------|------|-------------|--------|-------|
| `request_latency_seconds` | Histogram | End-to-End Request Latency | - | seconds |
| `tokenization_latency_seconds` | Histogram | Tokenization Latency | - | seconds |
| `inference_latency_seconds` | Histogram | Model Inference Latency | - | seconds |
| `queue_wait_latency_seconds` | Histogram | Total Queue Wait | - | seconds |
| `tokenizer_queue_wait_latency_seconds` | Histogram | Tokenizer Queue Wait | - | seconds |
| `model_queue_wait_latency_seconds` | Histogram | Model Queue Wait | - | seconds |
| `mp_queue_send_latency_seconds` | Histogram | Multiprocessing Queue Send | - | seconds |
| `mp_queue_receive_latency_seconds` | Histogram | Multiprocessing Queue Receive | - | seconds |
| `grpc_serialize_latency_seconds` | Histogram | gRPC Serialization | - | seconds |
| `grpc_deserialize_latency_seconds` | Histogram | gRPC Deserialization | - | seconds |
| `scheduler_latency_seconds` | Histogram | Scheduler Latency | - | seconds |
| `overhead_latency_seconds` | Histogram | Pipeline Overhead | - | seconds |
| `pipeline_overhead_latency_seconds` | Histogram | Pipeline Overhead (detailed) | - | seconds |

**Recording Locations:**
- `request_latency_seconds`: `MetricsService.record()`
- Stage latencies: `MetricsService.record_stage_timings()`

### 4. Throughput Gauges

Gauges for QPS (queries per second) metrics.

| Metric | Type | Description | Labels | Units |
|--------|------|-------------|--------|-------|
| `tokenizer_throughput_qps` | Gauge | Tokenizer Throughput | - | QPS |
| `inference_throughput_qps` | Gauge | Inference Throughput | - | QPS |
| `overall_throughput_qps` | Gauge | Overall System Throughput | - | QPS |
| `worker_throughput_qps` | Gauge | Per-Worker Throughput | `worker_id`, `worker_type` | QPS |

**Recording Locations:**
- Throughput gauges: `record_throughput_stats()`
- Worker throughput: `record_worker_stats()` (implicitly via metrics service)

### 5. Worker Metrics

Metrics with worker identification labels.

| Metric | Type | Description | Labels | Units |
|--------|------|-------------|--------|-------|
| `worker_latency_ms` | Gauge | Worker Request Latency | `worker_id`, `worker_type` | ms |
| `worker_request_count_total` | Counter | Worker Request Count | `worker_id`, `worker_type` | count |
| `worker_throughput_qps` | Gauge | Worker Throughput | `worker_id`, `worker_type` | QPS |

**Recording Locations:**
- Model workers: `MetricsService.record_worker_stats()`
- Tokenizer workers: `MetricsService.record_tokenizer_worker_stats()`

## Implementation Details

### MetricsService Initialization

All Prometheus metrics are initialized in `MetricsService.__init__()`:

```python
def __init__(self, collection_interval_seconds: float = 5.0, prometheus_port: int = 8000):
    # Counters
    self.prom_request_count = Counter("request_count", "Total number of requests")

    # Gauges
    self.prom_gpu_memory = Gauge("gpu_memory_mb", "GPU Memory Usage in MB")

    # Histograms with custom buckets
    self.prom_request_latency = Histogram(
        "request_latency_seconds",
        "Request latency in seconds",
        buckets=[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]
    )
```

### Recording Metrics

Metrics are recorded at various points in the request flow:

#### 1. Request Recording
```python
# In gRPC Infer endpoint
def record(self, duration_ms: float, num_queries: int = 1):
    self._collector.record(duration_ms, num_queries)
    self.prom_request_count.inc(num_queries)
    self.prom_request_latency.observe(duration_ms / 1000.0)
```

#### 2. Stage Timing Recording
```python
def record_stage_timings(self,
    t_tokenize: float = 0.0,
    t_tokenizer_queue_wait: float = 0.0,
    t_model_queue_wait: float = 0.0,
    t_model_inference: float = 0.0,
    # ... other stages
):
    # Record to collector (for internal tracking)
    self._collector.record_stage_timings(...)

    # Record to Prometheus histograms
    if t_tokenize > 0:
        self.prom_tokenization_latency.observe(t_tokenize / 1000.0)
    if t_model_inference > 0:
        self.prom_inference_latency.observe(t_model_inference / 1000.0)
    # ... etc for all stages
```

#### 3. System Metrics Collection Loop
```python
def _update_system_metrics(self) -> None:
    # GPU and CPU
    cpu_pct = self._process_monitor_service.get_cpu_percent()
    self.prom_cpu_percent.set(cpu_pct)

    gpu_mem = self.get_gpu_memory_mb()
    self.prom_gpu_memory.set(gpu_mem)

    # Queue sizes
    queue_info = self._get_queue_sizes(self._collector)
    self.prom_tokenizer_queue_size.set(queue_info.get("tokenizer_queue_size", 0))
    self.prom_model_queue_size.set(queue_info.get("model_queue_size", 0))
    self.prom_batch_queue_size.set(queue_info.get("batch_queue_size", 0))
```

#### 4. Worker Metrics Recording
```python
def record_worker_stats(self, worker_id: int, latency_ms: float, num_queries: int = 1):
    self.prom_worker_latency.labels(
        worker_id=str(worker_id),
        worker_type="model"
    ).set(latency_ms)

    self.prom_worker_requests.labels(
        worker_id=str(worker_id),
        worker_type="model"
    ).inc(num_queries)
```

#### 5. Padding Statistics Recording
```python
def record_padding_stats(self,
    padding_ratio: float = 0.0,
    padded_tokens: int = 0,
    total_tokens: int = 0,
    max_seq_length: int = 0,
    avg_seq_length: float = 0.0,
):
    if padding_ratio >= 0:
        self.prom_padding_ratio.set(padding_ratio)
    if padded_tokens > 0:
        self.prom_padded_tokens.inc(padded_tokens)
    if total_tokens > 0:
        self.prom_total_tokens.inc(total_tokens)
    if max_seq_length > 0:
        self.prom_max_seq_length.set(max_seq_length)
    if avg_seq_length > 0:
        self.prom_avg_seq_length.set(avg_seq_length)
```

## Prometheus Queries for Grafana

Instead of using `DashboardMetrics.get_summary()`, Grafana should use these Prometheus queries:

### Latency Statistics

```promql
# Average latency (all time)
avg(request_latency_seconds_sum) / avg(request_latency_seconds_count)

# Latency percentiles (over 5 minute window)
histogram_quantile(0.50, rate(request_latency_seconds_bucket[5m]))  # P50
histogram_quantile(0.95, rate(request_latency_seconds_bucket[5m]))  # P95
histogram_quantile(0.99, rate(request_latency_seconds_bucket[5m]))  # P99

# Min/Max latency (over time window)
min(rate(request_latency_seconds_bucket{le="+Inf"}[5m]))
max(request_latency_seconds)
```

### Throughput

```promql
# Requests per second (current window)
rate(request_count_total[1m])

# Tokenizer QPS
tokenizer_throughput_qps

# Inference QPS
inference_throughput_qps

# Overall system QPS
overall_throughput_qps

# Per-worker QPS
worker_throughput_qps{worker_type="model"}
```

### Stage Breakdown Percentages

```promql
# Tokenization percentage of total latency
(rate(tokenization_latency_seconds_sum[5m]) / rate(request_latency_seconds_sum[5m])) * 100

# Inference percentage
(rate(inference_latency_seconds_sum[5m]) / rate(request_latency_seconds_sum[5m])) * 100

# Queue wait percentage
(rate(queue_wait_latency_seconds_sum[5m]) / rate(request_latency_seconds_sum[5m])) * 100
```

### Queue Metrics

```promql
# Current queue sizes
tokenizer_queue_size
model_queue_size
batch_queue_size

# Total queue size
tokenizer_queue_size + model_queue_size + batch_queue_size
```

### System Resources

```promql
# GPU memory
gpu_memory_mb

# GPU utilization
gpu_utilization_pct

# CPU usage
cpu_percent
```

### Padding Statistics

```promql
# Padding ratio
padding_ratio

# Tokens padded (rate)
rate(padded_tokens_total[1m])

# Total tokens (rate)
rate(total_tokens_total[1m])

# Max/Avg sequence length
max_seq_length
avg_seq_length
```

## Migration Checklist

- [x] Add all Prometheus metrics to MetricsService
- [x] Record metrics at all relevant points in code
- [x] Remove self-tracking lists from workers
- [x] Remove self-tracking from MetricsCollector
- [x] Remove `get_metrics_stats()` from workers
- [x] Update tests to verify Prometheus recording
- [ ] Create Grafana dashboard with Prometheus queries
- [ ] Replace DashboardMetrics.get_summary() usage with Grafana queries
- [ ] Remove DashboardMetrics (or deprecate it)
- [ ] Update documentation to reference Prometheus queries

## Code Locations

### Key Files Changed

| File | Changes |
|------|---------|
| `src/server/services/metrics_service.py` | Added all Prometheus metrics initialization and recording |
| `src/server/worker/base.py` | Removed self-tracking, kept only recording callback |
| `src/server/worker/tokenizer_worker.py` | Removed self-tracking |
| `src/server/dto/metrics/collector.py` | Removed internal latency lists and counters |
| `src/server/grpc.py` | Removed manual request counting |
| `src/server/pipeline/base.py` | Removed request tracking |
| `src/server/pool/model_pool.py` | Removed `get_metrics_stats()` calls |
| `src/server/pool/tokenizer_pool.py` | Removed `get_metrics_stats()` calls |

### Test Files

- `tests/test_prometheus_metrics.py` - Verifies all Prometheus metrics are initialized and recording

## Benefits of This Architecture

1. **Stateless Application** - No metrics state stored in memory
2. **Single Source of Truth** - Prometheus is the only metrics store
3. **Industry Standard** - Follows Prometheus best practices
4. **Scalability** - Easy to add/remove workers without metric concerns
5. **Flexibility** - Grafana can compute any metric combination via queries
6. **Memory Efficient** - No bounded lists or custom time-series storage
7. **Observability** - All metrics available for alerting and dashboarding

## Prometheus Configuration

The application exposes metrics on `http://localhost:8000/metrics`.

Prometheus scrape config in `conf/prometheus/prometheus.yml`:
```yaml
global:
  scrape_interval: 1s

scrape_configs:
  - job_name: 'cross_encoder_server'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /metrics
```

## Troubleshooting

### Metrics Not Appearing in Prometheus

1. Check that MetricsService is started: `service.start()`
2. Verify metrics endpoint: `curl http://localhost:8000/metrics`
3. Check Prometheus targets: `http://localhost:9091/targets`
4. Look at `MetricsService._collection_loop()` for collection errors

### Missing Metric Type

Ensure the correct Prometheus type is used:
- **Counter**: Use for continuously increasing values (requests, tokens)
- **Gauge**: Use for instantaneous values (memory, queue size)
- **Histogram**: Use for latency/distribution measurements

### Per-Worker Metrics

Use labels to distinguish workers:
```promql
worker_throughput_qps{worker_id="0", worker_type="model"}
worker_throughput_qps{worker_id="1", worker_type="model"}
```

## Future Enhancements

1. Add custom Prometheus exporters for application-specific metrics
2. Implement metric retention policies in Prometheus
3. Add alerting rules for SLO violations
4. Create service-level dashboards for different teams
5. Implement metric cardinality monitoring
