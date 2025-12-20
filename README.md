# ML Inference Server with Dynamic Batching

A high-performance ML inference server with support for multiple model variants, quantization, and comprehensive benchmarking.

## Features

- **gRPC-based inference server** with sentence transformer models
- **Multiple experiment configurations** for different model variants
- **Quantization support**: INT8 (CPU) and FP16 (MPS/GPU)
- **Dynamic batching** with configurable parameters
- **Real-time metrics** via HTTP endpoint
- **Comprehensive benchmarking** with MS MARCO dataset
- **Extensible architecture** for adding new backends (PyTorch, ONNX, etc.)

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run a Single Experiment

```bash
# Start server with specific experiment config
./run_server.sh --experiment ml_inference_server/experiments/minilm_baseline.yaml

# In another terminal, run benchmark
./run_client.sh --experiment --config ml_inference_server/experiments/minilm_baseline.yaml
```

Or use the convenience script:
```bash
./run_experiment.sh ml_inference_server/experiments/minilm_baseline.yaml
```

### 3. Run All Experiments

```bash
python run_all_experiments.py
```

This will run all experiments sequentially and save results to `ml_inference_server/docs/experiments/`.

## Available Experiments

| Experiment | Description | Device | Quantization |
|------------|-------------|--------|--------------|
| `minilm_baseline.yaml` | Baseline MiniLM-L6-v2 | MPS | None (FP32) |
| `minilm_quantized.yaml` | MiniLM with FP16 quantization | MPS | FP16 |
| `minilm_onnx.yaml` | MiniLM with ONNX Runtime | MPS | None (planned) |

## Project Structure

```
.
├── ml_inference_server/
│   ├── backends/           # Model backends (PyTorch, ONNX, etc.)
│   ├── experiments/        # Experiment configurations
│   │   ├── base_config.yaml
│   │   ├── minilm_baseline.yaml
│   │   ├── minilm_quantized.yaml
│   │   └── minilm_onnx.yaml
│   ├── metrics/            # Metrics collection and HTTP server
│   ├── proto/              # gRPC protocol definitions
│   ├── server/             # gRPC server and scheduler
│   ├── utils/              # Config loader and utilities
│   ├── client.py           # Benchmark client
│   ├── main.py             # Server entry point
│   └── config.yaml         # Legacy config (deprecated)
├── run_server.sh           # Start server
├── run_client.sh           # Run client
├── run_experiment.sh       # Run single experiment
├── run_all_experiments.py  # Run all experiments
└── lint.sh                 # Run linter

```

## Configuration System

### Base Configuration (`experiments/base_config.yaml`)
Contains common settings shared across all experiments:
- Server settings (host, port)
- Experiment parameters (batch sizes, concurrency levels, etc.)
- Batching configuration

### Experiment Configurations
Individual experiment files that override base settings:
- Model name and device
- Quantization settings
- Backend-specific options
- Custom experiment parameters

### Creating New Experiments

1. Create a new YAML file in `ml_inference_server/experiments/`:

```yaml
name: "my_experiment"
description: "Description of the experiment"

model:
  name: "sentence-transformers/all-MiniLM-L6-v2"
  device: "mps"
  quantized: false
  backend: "pytorch"

# Optional: override experiment parameters
experiment:
  batch_sizes: [1, 4, 8]
  benchmark_requests: 100
```

2. Run the experiment:
```bash
./run_experiment.sh ml_inference_server/experiments/my_experiment.yaml
```

## Benchmarking

The client supports two modes:

### 1. Single Benchmark
```bash
./run_client.sh --batch-size 4 --concurrency 8 --requests 100
```

### 2. Full Experiment Suite
```bash
./run_client.sh --experiment --config ml_inference_server/experiments/minilm_baseline.yaml
```

This runs all combinations of batch sizes and concurrency levels defined in the config.

## Metrics

Real-time metrics are available at:
- **Dashboard**: http://localhost:8080
- **JSON API**: http://localhost:8080/metrics

Metrics include:
- Request latency (avg, p50, p95, p99)
- Throughput (requests/sec, pairs/sec)
- CPU and GPU memory usage

## Development

### Linting
```bash
./lint.sh
```

### Adding New Backends

1. Create a new backend class in `ml_inference_server/backends/`
2. Implement the required interface (load_model, infer, warmup)
3. Update `main.py` to support the new backend type
4. Create experiment configs for the new backend

## Results

Experiment results are saved to:
- Single experiment: `ml_inference_server/docs/experiment_results.md`
- All experiments: `ml_inference_server/docs/experiments/<experiment_name>_results.md`

## License

MIT

