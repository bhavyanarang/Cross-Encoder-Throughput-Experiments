# ML Inference Server

A high-performance ML inference server for cross-encoder models with support for multiple backends, quantization, and comprehensive benchmarking on Apple Silicon.

## Setup

### Prerequisites

- Python 3.11+
- macOS with Apple Silicon (for MPS backend) or Linux with CUDA (for GPU backend)

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
│   ├── main.py                   # Server entry point
│   ├── run_client.py             # Benchmark client entry point
│   ├── screenshot.py             # Screenshot utilities
│   ├── test_timing.py            # Timing test utilities
│   ├── client/                   # gRPC client implementation
│   │   └── grpc_client.py
│   ├── frontend/                 # Web dashboard
│   │   ├── server.py             # HTTP server for metrics
│   │   ├── static/               # Static assets
│   │   │   ├── css/
│   │   │   │   └── styles.css    # Dashboard styles
│   │   │   └── js/
│   │   │       ├── charts.js     # Chart rendering
│   │   │       └── main.js       # Dashboard JavaScript
│   │   └── templates/
│   │       └── index.html        # Dashboard HTML template
│   ├── models/                   # Data models and configurations
│   │   ├── benchmark.py          # Benchmark data models
│   │   ├── config.py             # Configuration data models
│   │   ├── config_loader.py      # Configuration loader
│   │   ├── dashboard.py          # Dashboard metrics models
│   │   ├── inference.py          # Inference request/response models
│   │   ├── metrics.py            # Metrics data models
│   │   ├── scheduler.py          # Scheduler models
│   │   ├── server_metrics.py     # Server metrics models
│   │   └── sweep.py              # Sweep experiment models
│   ├── proto/                    # gRPC protocol definitions
│   │   ├── inference.proto       # Protocol buffer definition
│   │   ├── inference_pb2.py      # Generated Python code
│   │   └── inference_pb2_grpc.py  # Generated gRPC code
│   ├── server/                   # Server implementation
│   │   ├── grpc.py               # gRPC server
│   │   ├── metrics.py            # Metrics collection
│   │   ├── orchestrator.py       # Server orchestrator (coordinates components)
│   │   ├── pool.py               # Model pool management
│   │   ├── scheduler.py          # Request scheduler with batching
│   │   ├── tokenizer_pool.py     # Tokenizer pool for parallel tokenization
│   │   ├── backends/             # Model backends
│   │   │   ├── base.py           # Base backend interface
│   │   │   ├── pytorch.py        # PyTorch backend
│   │   │   ├── mps.py            # MPS (Apple Silicon) backend
│   │   │   ├── mlx_backend.py    # MLX backend
│   │   │   ├── compiled.py       # torch.compile backend
│   │   │   ├── cuda.py           # CUDA backend
│   │   │   ├── tensorrt.py       # TensorRT backend
│   │   │   └── device.py         # Device utilities
│   │   └── services/             # Server services
│   │       ├── inference_service.py    # Inference orchestration service
│   │       ├── tokenization_service.py # Tokenization service wrapper
│   │       └── tokenizer.py      # Core tokenization service
├── experiments/                  # Experiment configurations
│   ├── base_config.yaml          # Base configuration (inherited)
│   ├── *.yaml                    # Individual experiment configs
│   ├── distribution/             # Time-series distribution data
│   │   ├── *_timeseries.md       # Time-series data files
│   │   └── *_timeseries.idx      # Time-series index files
│   ├── results/                  # Experiment results (Markdown)
│   ├── EXPERIMENT_PLAN.md        # Experiment planning document
│   └── README.md                 # Experiments documentation
├── scripts/                      # Shell scripts
│   ├── run_server.sh             # Start server
│   ├── run_client.sh             # Run client
│   ├── run_experiment.sh         # Run single experiment
│   ├── run_all_experiments.sh    # Run all experiments
│   ├── run_experiments_from_06.sh # Run experiments from 06 onwards
│   ├── run_sweep_experiment.sh   # Run sweep experiment
│   ├── stop_all_servers.sh       # Stop all running servers
│   ├── check_and_fix_experiment_duration.sh  # Fix experiment duration issues
│   └── lint.sh                   # Run linter
├── tests/                        # Test suite
│   ├── conftest.py               # Pytest fixtures
│   ├── test_backends.py          # Backend tests
│   ├── test_models.py            # Model tests
│   ├── test_scheduler.py         # Scheduler tests
│   └── README.md                 # Test documentation
├── images/                       # Experiment visualization outputs
│   └── *.html                    # HTML dashboard screenshots
├── requirements.txt              # Python dependencies
└── pyproject.toml                # Project configuration
```

## Configuration System

### Base Configuration

All experiments inherit from `experiments/base_config.yaml`:

```yaml
# Model configuration
model:
  name: "cross-encoder/ms-marco-MiniLM-L-6-v2"
  device: "mps"
  backend: "pytorch"
  quantized: false
  mps:
    fp16: true
  mlx:
    bits: 16

# Server settings
server:
  host: "0.0.0.0"
  port: 50051

# Experiment parameters
experiment:
  batch_sizes: [32, 64, 128]
  concurrency_levels: [4, 8]
  warmup_iterations: 10
  benchmark_requests: 500
```

### Creating Custom Experiments

Create a new YAML file in `experiments/` to override base settings:

```yaml
name: "my_experiment"
description: "Description of the experiment"

model:
  backend: "mps"
  mps:
    fp16: true

# Optional: Enable tokenizer pool for parallel tokenization
tokenizer_pool:
  enabled: true
  num_workers: 4

experiment:
  batch_sizes: [32, 64, 96]
  concurrency_levels: [1, 2, 4]
  benchmark_requests: 100
```

### Available Backends

| Backend | Device | Description | Quantization |
|---------|--------|-------------|--------------|
| `pytorch` | mps/cpu | Standard PyTorch inference | FP32, FP16 |
| `mps` | mps | Optimized MPS backend | FP16 |
| `mlx` | mps | Apple MLX framework | FP16, INT8, INT4 |
| `compiled` | mps | torch.compile optimized | FP16 |

### Tokenizer Pool

The tokenizer pool enables parallel CPU-based tokenization using dedicated worker threads, reducing bottlenecks when multiple inference requests arrive concurrently.

**Configuration:**
```yaml
tokenizer_pool:
  enabled: true          # Enable/disable tokenizer pool
  num_workers: 4         # Number of parallel tokenizer workers (recommended: 2-4)
```

**Benefits:**
- **Parallel Tokenization**: Multiple requests can be tokenized simultaneously
- **Reduced Blocking**: Model inference workers don't wait for tokenization
- **Better Concurrency**: Improves throughput at higher concurrency levels (typically +1-3%)
- **CPU Offloading**: Tokenization runs on CPU, freeing GPU/MPS for inference

**When to Use:**
- High concurrency scenarios (4+ concurrent requests)
- Multi-model pools where tokenization could become a bottleneck
- Production deployments requiring maximum throughput

**Performance Impact:**
- Small overhead at low concurrency (< 2 workers)
- Best improvements at higher concurrency (4+ workers): +1-3% throughput, -1-3% latency
- Recommended: 2-4 workers for most use cases

## Benchmarking

### Running a Single Experiment

```bash
# Run a specific experiment
./scripts/run_experiment.sh experiments/02_backend_mps.yaml

# Results are saved to experiments/results/<experiment_name>_results.md
```

### Running All Experiments

```bash
# Run all experiments sequentially
./scripts/run_all_experiments.sh
```

### Manual Benchmark

```bash
# Terminal 1: Start server
source venv/bin/activate
python -m src.main --experiment experiments/02_backend_mps.yaml

# Terminal 2: Run benchmark
source venv/bin/activate
python -m src.run_client --experiment --config experiments/02_backend_mps.yaml
```

### Metrics Dashboard

Real-time metrics are available during experiments:

- **Dashboard**: http://localhost:8080
- **JSON API**: http://localhost:8080/metrics
- **Reset Metrics**: http://localhost:8080/reset

## Results and Analysis

### Experiment Results Ranking (by Throughput)

| Rank | Experiment | Throughput (p/s) | Latency (ms) | Key Insight |
|------|------------|------------------|--------------|-------------|
| 1 | 11: 3x Replicas | 1200.8 | 211.6 | Best throughput |
| 2 | 10: 2x Pool + Tokenizer Pool | 1192.4 | 37.7 | Parallel tokenization + model pool |
| 3 | 10: 2x Pool (opt) | 1011.6 | 126.1 | Best balance |
| 4 | 14: Production | 679.6 | 141.1 | Best stability |
| 5 | 07b: Dynamic Batch | 686.0 | 186.4 | Best single |
| 6 | 10a: Padding Base | 687.4 | 93.0 | Best latency |
| 7 | 12: Max Length 512 | 576.5 | 110.9 | Longer sequences |
| 8 | 11_Quant: INT8 | 572.3 | 167.5 | Quantization |
| 9 | 09: Max Batch 256 | 671.6 | 190.0 | Batch sweep |
| 10 | 08: Timeout 200ms | 670.6 | 190.4 | Timeout sweep |
| 11 | 07a: Static Batch | 647.2 | 197.1 | Baseline |

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
2. Implement the required interface: `load_model()`, `infer()`, `warmup()`
3. Update `src/server/pool.py` to support the new backend type
4. Create experiment configs for the new backend

## License

MIT
