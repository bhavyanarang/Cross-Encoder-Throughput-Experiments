# Cross Encoder Inference Server

A high-performance ML inference server for cross-encoder models with support for multiple backends, quantization, and comprehensive benchmarking on Apple Silicon.

![Dashboard Screenshot](images/dashboard_screenshot.png)

## Setup

### Prerequisites

- Python 3.11+
- macOS with Apple Silicon (for MPS backend) or Linux with CUDA (for GPU backend)
- Docker and Docker Compose (for observability stack)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd "cross encoder throughput experiments"

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install MLX for Apple Silicon native inference
pip install mlx mlx-lm
```

### Docker Setup (Observability Stack)

The project uses Docker for running Prometheus and Grafana (observability only). The inference server runs locally to leverage Apple Silicon hardware (MPS, MLX).

```bash
# Pull observability images
./scripts/setup_observability.sh

# Start observability services (Prometheus + Grafana)
./scripts/start_services.sh

# Stop all services and servers
./scripts/stop_all_servers.sh
```

**Services:**
| Service | URL | Description |
|---------|-----|-------------|
| Prometheus | http://localhost:9091 | Metrics collection |
| Grafana | http://localhost:3001 | Dashboard visualization |
| Server Metrics | http://localhost:8000/metrics | Local server metrics endpoint |

### Verify Installation

```bash
# Run linter
./scripts/lint.sh

# Run tests
pytest tests/ -v
```

## Project Structure

```
.
├── src/                          # Source code
│   ├── main.py                   # Server entry point (Hydra config)
│   ├── run_client.py             # Benchmark client entry point
│   ├── screenshot.py             # Screenshot utilities
│   ├── client/                   # gRPC client implementation
│   ├── server/                   # Server implementation
│   │   ├── grpc.py               # gRPC server
│   │   ├── pool/                 # Model and tokenizer pools
│   │   ├── pipeline/             # Queue-based pipeline
│   │   ├── backends/             # Model backends (pytorch, mps, mlx, compiled)
│   │   ├── dto/                  # Data transfer objects
│   │   └── services/             # Server services
│   └── proto/                    # gRPC protocol definitions
├── conf/                         # Hydra configuration
│   ├── config.yaml               # Main config
│   ├── experiment/               # Experiment configs
│   ├── model_pool/               # Model pool configs
│   ├── batching/                 # Batching configs
│   ├── tokenizer_pool/           # Tokenizer pool configs
│   ├── prometheus/               # Prometheus config
│   └── grafana/                  # Grafana provisioning
├── scripts/                      # Shell scripts
│   ├── start_services.sh         # Start Docker observability stack
│   ├── stop_all_servers.sh       # Stop all servers and Docker containers
│   ├── setup_observability.sh    # Pull Docker images
│   ├── run_server.sh             # Start inference server
│   ├── run_client.sh             # Run benchmark client
│   ├── run_experiment.sh         # Run single experiment
│   ├── run_sweep_experiment.sh   # Run sweep experiments (parameter sweeps)
│   ├── run_all_experiments.sh    # Run all experiments
│   └── lint.sh                   # Run linter
├── experiments/                  # Experiment outputs
│   ├── results/                  # Experiment results (Markdown)
│   └── distribution/             # Time-series distribution data
├── tests/                        # Test suite
├── docker-compose.yml            # Docker Compose for observability
├── requirements.txt              # Python dependencies
└── pyproject.toml                # Project configuration
```

## Scripts Reference

| Script | Description |
|--------|-------------|
| `start_services.sh` | Start Prometheus + Grafana via Docker Compose |
| `stop_all_servers.sh` | Stop Python servers and Docker containers, cleanup ports |
| `setup_observability.sh` | Pull required Docker images |
| `run_server.sh <experiment>` | Start server with specified experiment config |
| `run_client.sh [args]` | Run benchmark client with optional arguments |
| `run_experiment.sh <name>` | Run a complete experiment (server + client + metrics) |
| `run_sweep_experiment.sh <config>` | Run parameter sweep experiments |
| `run_all_experiments.sh` | Run all experiments in `conf/experiment/` |
| `lint.sh` | Run code linting |

## Configuration System

The project uses [Hydra](https://hydra.cc/) for configuration management. Configs are in `conf/`.

### Experiment Configuration

Experiments are defined in `conf/experiment/`:

```yaml
# @package _global_

defaults:
  - override /model_pool: default
  - override /batching: default
  - override /tokenizer_pool: default
  - override /server: default

name: "My Experiment"
description: "Description of experiment"

model_pool:
  instances:
    - name: "cross-encoder/ms-marco-MiniLM-L-6-v2"
      backend: mps          # pytorch, mps, mlx, compiled
      device: mps
      quantization: fp16    # fp32, fp16, int8, int4
      max_length: 512

batching:
  enabled: true
  max_batch_size: 32
  timeout_ms: 50.0

experiment:
  batch_sizes: [32, 64, 128]
  concurrency_levels: [1, 2, 4]
```

### Sweep Experiments

Run parameter sweeps by using arrays in config:

```yaml
# Backend comparison sweep
model_pool:
  instances:
    - name: "cross-encoder/ms-marco-MiniLM-L-6-v2"
      backend: ["pytorch", "mps", "mlx", "compiled"]  # Sweeps all backends
      device: mps
      quantization: fp16
```

The sweep system automatically generates and runs all combinations.

### Available Backends

| Backend | Device | Description | Best For |
|---------|--------|-------------|----------|
| `pytorch` | mps/cpu | Standard PyTorch inference | Baseline, debugging |
| `mps` | mps | Optimized Apple Metal Performance Shaders | Apple Silicon production |
| `mlx` | mps | Apple MLX framework | Native Apple Silicon, quantization |
| `compiled` | mps | torch.compile with inductor | Optimized inference |

### Quantization Options

| Quantization | Description | Backends |
|--------------|-------------|----------|
| `fp32` | Full precision | All |
| `fp16` | Half precision | All (recommended for MPS) |
| `int8` | 8-bit quantization | mlx, cpu |
| `int4` | 4-bit quantization | mlx |

## Running Experiments

### Quick Start

```bash
# 1. Start observability stack
./scripts/start_services.sh

# 2. Run a single experiment
./scripts/run_experiment.sh 10_multi_model_pool

# 3. View results
cat experiments/results/10_multi_model_pool_results.md

# 4. View dashboard
open http://localhost:3001
```

### Running All Backends (Apple Silicon)

```bash
# Run backend comparison sweep (pytorch, mps, mlx, compiled)
./scripts/run_experiment.sh 01_backend_comparison

# This will automatically:
# 1. Generate configs for each backend
# 2. Run experiments sequentially
# 3. Collect metrics from Prometheus
# 4. Save results to experiments/results/
```

### Running All Experiments

```bash
./scripts/run_all_experiments.sh
```

### Manual Benchmark

```bash
# Terminal 1: Start server
source venv/bin/activate
python -m src.main experiment=10_multi_model_pool

# Terminal 2: Run benchmark
source venv/bin/activate
python -m src.run_client --experiment --config <config.yaml>
```

## Metrics and Observability

### Prometheus Metrics

The server exposes metrics at `http://localhost:8000/metrics`:

- **Request metrics**: `inference_requests_total`, `inference_request_duration_seconds`
- **Throughput**: `inference_throughput_samples_per_second`
- **Latency**: `inference_latency_seconds` (histogram with percentiles)
- **Queue**: `inference_queue_size`, `inference_queue_wait_time_seconds`
- **Pool**: `model_pool_active_workers`, `tokenizer_pool_queue_size`
- **System**: `process_cpu_percent`, `gpu_memory_bytes`

### Grafana Dashboard

Pre-configured dashboard available at `http://localhost:3001`:

- Real-time throughput and latency graphs
- Queue sizes and wait times
- Worker utilization
- System resource usage

## Results and Analysis

### Experiment Results Ranking (by Throughput)

| Rank | Experiment | Throughput (p/s) | Latency (ms) | Key Insight |
|------|------------|------------------|--------------|-------------|
| 1 | 11: 3x Replicas | 1200.8 | 211.6 | Best throughput |
| 2 | 10: 2x Pool + Tokenizer Pool | 1192.4 | 131.8 | Parallel tokenization + model pool |
| 3 | 10: 2x Pool (opt) | 1011.6 | 126.1 | Best balance |
| 4 | 14: Production | 679.6 | 141.1 | Best stability |
| 5 | 07b: Dynamic Batch | 686.0 | 186.4 | Best single |
| 6 | 10a: Padding Base | 687.4 | 93.0 | Best latency |

## Development

### Linting

```bash
./scripts/lint.sh
```

### Running Tests

```bash
pytest tests/ -v
pytest tests/ -v --cov=src --cov-report=html
```

### Adding New Backends

1. Create a new backend class in `src/server/backends/`
2. Implement: `load_model()`, `infer()`, `warmup()`
3. Register in `src/server/backends/__init__.py`
4. Create experiment configs for the new backend

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
./scripts/stop_all_servers.sh
```

**Docker containers not starting:**
```bash
docker compose down --remove-orphans
./scripts/start_services.sh
```

**MPS not available:**
```python
import torch
print(torch.backends.mps.is_available())  # Should be True on Apple Silicon
```

**MLX not working:**
```bash
pip install mlx mlx-lm
```

## License

MIT
