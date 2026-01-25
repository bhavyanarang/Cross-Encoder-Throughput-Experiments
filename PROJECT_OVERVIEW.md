# Cross Encoder Inference Server - Project Overview

## Purpose

This project is a **high-performance ML inference server** specifically designed for **cross-encoder models**. Cross-encoders are transformer models that take a query-document pair as input and output a relevance score, commonly used in semantic search and reranking tasks.

The server is optimized for **Apple Silicon** (M1/M2/M3 chips) but also supports CUDA GPUs on Linux.

## Core Goals

1. **High Throughput**: Maximize the number of query-document pairs processed per second
2. **Low Latency**: Minimize response time for inference requests
3. **Comprehensive Benchmarking**: Systematically compare different configurations to find optimal settings
4. **Production Observability**: Full metrics collection via Prometheus and visualization via Grafana

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      gRPC Server                            │
│  (receives query-document pairs, returns relevance scores)  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Orchestrator Service                        │
│    (coordinates tokenization, batching, and inference)       │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌───────────────────┐     ┌───────────────────┐
│  Tokenizer Pool   │     │    Model Pool     │
│ (parallel text    │     │ (parallel model   │
│  preprocessing)   │     │  inference)       │
└───────────────────┘     └───────────────────┘
        │                           │
        ▼                           ▼
┌───────────────────┐     ┌───────────────────┐
│ Tokenizer Workers │     │  Model Workers    │
└───────────────────┘     └───────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              ┌──────────┐   ┌──────────┐   ┌──────────┐
              │ PyTorch  │   │   MPS    │   │   MLX    │
              │ Backend  │   │ Backend  │   │ Backend  │
              └──────────┘   └──────────┘   └──────────┘
```

## Key Features

### 1. Multiple Inference Backends
- **PyTorch**: Standard inference (baseline)
- **MPS**: Apple Metal Performance Shaders (optimized for Apple Silicon)
- **MLX**: Apple's native ML framework (best for quantization)
- **Compiled**: torch.compile with inductor optimization

### 2. Dynamic Batching
- Automatically groups incoming requests into batches
- Configurable max batch size and timeout
- Improves GPU utilization and throughput

### 3. Quantization Support
- FP32 (full precision)
- FP16 (half precision - recommended for MPS)
- INT8/INT4 (for MLX backend)

### 4. Resource Pooling
- **Model Pool**: Multiple model instances for parallel inference
- **Tokenizer Pool**: Parallel text tokenization to avoid CPU bottlenecks

### 5. Comprehensive Metrics
- Request latency histograms
- Throughput (samples/second)
- Queue sizes and wait times
- Per-worker statistics
- Padding efficiency
- CPU/GPU utilization

## Experiment System

The project includes a sophisticated experiment framework using **Hydra** configuration:

- **29+ predefined experiments** covering:
  - Backend comparisons
  - Batch size sweeps
  - Concurrency testing
  - Dynamic batching tuning
  - Quantization comparisons
  - Multi-model pooling strategies
  - Production optimization profiles

- **Automated sweeps**: Test multiple parameter combinations automatically
- **Results persistence**: All results saved as Markdown reports with time-series data

## Use Cases

1. **Semantic Search Reranking**: Rerank search results using cross-encoder relevance scores
2. **Question-Answer Matching**: Score query-answer pairs for QA systems
3. **Document Similarity**: Compute pairwise document similarity scores
4. **Performance Research**: Benchmark different ML serving configurations on Apple Silicon

## Tech Stack

- **Python 3.11+**
- **gRPC**: High-performance RPC for client-server communication
- **Hydra**: Configuration management
- **Prometheus**: Metrics collection
- **Grafana**: Dashboard visualization
- **PyTorch/MLX**: ML inference frameworks
- **Docker**: Observability stack deployment

---

## Prometheus Metrics Integration

### How It Works

The server exposes metrics via an HTTP endpoint at `http://localhost:8000/metrics` using the `prometheus_client` Python library. Prometheus (running in Docker) scrapes this endpoint every 1 second.

```
┌─────────────────┐    scrape /metrics    ┌─────────────────┐
│  Inference      │ ◄──────────────────── │   Prometheus    │
│  Server :8000   │      every 1s         │   :9091         │
└─────────────────┘                       └─────────────────┘
```

### Metrics Collected

The `MetricsService` class (`src/server/services/metrics_service.py`) exposes these Prometheus metric types:

| Metric Type | Metrics | Purpose |
|-------------|---------|---------|
| **Counter** | `request_count`, `padded_tokens_total`, `total_tokens_total`, `worker_request_count`, `worker_tokens` | Cumulative counts |
| **Gauge** | `gpu_memory_mb`, `cpu_percent`, `tokenizer_queue_size`, `model_queue_size`, `padding_ratio` | Current values |
| **Histogram** | `request_latency_seconds`, `inference_latency_seconds`, `tokenization_latency_seconds`, `queue_wait_latency_seconds` | Latency distributions with percentiles |

### Key Metrics

```
# Request metrics
request_count                      # Total requests processed
request_latency_seconds            # End-to-end latency histogram

# Pipeline stage latencies
inference_latency_seconds          # Model inference time
tokenization_latency_seconds       # Tokenization time
tokenizer_queue_wait_latency_seconds  # Time waiting in tokenizer queue
model_queue_wait_latency_seconds   # Time waiting in model queue

# Resource metrics
gpu_memory_mb                      # GPU memory usage
cpu_percent                        # CPU utilization
tokenizer_queue_size               # Current tokenizer queue depth
model_queue_size                   # Current model queue depth

# Per-worker metrics (labeled by worker_id)
worker_latency_ms{worker_id, worker_type}    # Per-worker latency
worker_request_count{worker_id, worker_type} # Per-worker request count

# Padding efficiency
padding_ratio                      # Ratio of padding tokens to total
padded_tokens_total               # Total padding tokens (waste)
total_tokens_total                # Total tokens processed
```

### Prometheus Configuration

Located at `conf/prometheus/prometheus.yml`:

```yaml
global:
  scrape_interval: 1s      # High-frequency scraping for benchmarks
  evaluation_interval: 1s

scrape_configs:
  - job_name: 'cross_encoder_server'
    static_configs:
      - targets: ['host.docker.internal:8000']  # Server metrics endpoint
    metrics_path: /metrics
```

---

## Grafana Dashboard

### How It Works

Grafana connects to Prometheus as a data source and provides real-time visualization of all collected metrics.

```
┌─────────────────┐    query PromQL    ┌─────────────────┐
│    Grafana      │ ─────────────────► │   Prometheus    │
│    :3001        │                    │   :9091         │
└─────────────────┘                    └─────────────────┘
```

### Pre-configured Dashboard

The dashboard is auto-provisioned via `conf/grafana/provisioning/`:

- **Datasource**: `conf/grafana/provisioning/datasources/datasource.yaml` - Connects Grafana to Prometheus
- **Dashboard**: `conf/grafana/provisioning/dashboards/default_dashboard.json` - Pre-built panels

### Dashboard Panels

The Grafana dashboard displays:

1. **Throughput Panel**: Requests per second over time
2. **Latency Panels**: P50, P95, P99 latency histograms
3. **Queue Monitoring**: Tokenizer and model queue depths
4. **Resource Usage**: CPU and GPU memory utilization
5. **Worker Stats**: Per-worker latency and request distribution
6. **Padding Efficiency**: Token padding waste metrics

### Access

- URL: `http://localhost:3001`
- Default credentials: `admin` / `admin`
- Anonymous access enabled for convenience

---

## Hydra Experiment Configuration

### How It Works

[Hydra](https://hydra.cc/) is a configuration framework that enables:

1. **Composable configs**: Mix and match config fragments
2. **Parameter sweeps**: Test multiple values automatically
3. **Override from CLI**: Change any config value at runtime

```
conf/
├── config.yaml              # Main config (composes defaults)
├── experiment/              # Experiment definitions (50+ configs)
├── model_pool/              # Model pool settings
├── tokenizer_pool/          # Tokenizer pool settings
├── batching/                # Dynamic batching settings
├── server/                  # Server settings (ports, workers)
└── pipeline/                # Pipeline configuration
```

### Configuration Hierarchy

```yaml
# conf/config.yaml - Main entry point
defaults:
  - model_pool: default
  - tokenizer_pool: default
  - batching: default
  - pipeline: default
  - server: default
  - experiment: default      # Can be overridden via CLI
```

### Experiment Configuration Example

```yaml
# conf/experiment/01_backend_comparison.yaml
# @package _global_

defaults:
  - override /model_pool: default
  - override /batching: default

name: "01_backend_comparison"
description: "Compare all backends on Apple Silicon"

model_pool:
  instances:
    - name: "cross-encoder/ms-marco-MiniLM-L-6-v2"
      backend: ["pytorch", "mps", "mlx", "compiled"]  # SWEEP: tests all 4
      device: "mps"
      quantization: "fp16"
      max_length: 512

experiment:
  batch_sizes: [32]
  concurrency_levels: [1]
```

### Running Experiments

```bash
# Run specific experiment
python -m src.main experiment=01_backend_comparison

# Override config values at runtime
python -m src.main experiment=default model_pool.instances[0].backend=mps

# Run via script (handles server lifecycle + metrics collection)
./scripts/run_experiment.sh 01_backend_comparison
```

### Sweep Experiments

When a config value is a list (e.g., `backend: ["pytorch", "mps"]`), the system automatically:

1. Generates separate configs for each combination
2. Runs experiments sequentially
3. Collects metrics for each configuration
4. Saves consolidated results

### Available Experiments (50+ configs)

| Category | Examples |
|----------|----------|
| **Backend Comparison** | `01_backend_comparison` - Compare PyTorch, MPS, MLX, Compiled |
| **Batch Size Tuning** | `02_batch_size_sweep` - Find optimal batch size |
| **Concurrency Testing** | `03a_concurrency_sweep` - Test parallel request handling |
| **Dynamic Batching** | `04a_dynamic_batch_baseline`, `04b_dynamic_batch_enabled` |
| **Quantization** | `07_quantization_sweep` - FP32, FP16, INT8, INT4 |
| **Multi-Model Pool** | `12_multi_model_pool`, `13a_multi_model_2x` |
| **Production Configs** | `22_production_optimal`, `23_optimized_production` |

### Results Storage

Experiment results are automatically saved to:

- `experiments/results/` - Markdown summary reports
- `experiments/distribution/` - Time-series data for analysis

---

## Summary

This project provides a production-ready, highly optimized inference server for cross-encoder models with extensive benchmarking capabilities. It's particularly valuable for:
- Teams deploying cross-encoders on Apple Silicon hardware
- Researchers comparing ML serving optimizations
- Production systems requiring low-latency semantic similarity scoring
