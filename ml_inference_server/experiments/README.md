# Systematic Experiment Suite

Experiments comparing MPS and MLX backends on Apple Silicon.

## Experiment Progression

### Phase 1: Backend Comparison (01-04)
| # | Experiment | Purpose | Result |
|---|------------|---------|--------|
| 01 | `01_backend_pytorch` | PyTorch baseline | 462.1 p/s |
| 02 | `02_backend_mps` | MPS backend | **476.0 p/s** ✓ |
| 03 | `03_backend_mlx` | MLX backend | **473.1 p/s** ✓ |
| 04 | `04_backend_compiled` | torch.compile | 189.6 p/s |

**Winners:** MPS and MLX (comparable performance)

### Phase 2: Optimization (05-08)
Using both MPS and MLX backends:

| # | Experiment | MPS Config | MLX Config |
|---|------------|------------|------------|
| 05 | Batch Size Sweep | `05a_batch_size_mps` | `05b_batch_size_mlx` |
| 06 | Concurrency Sweep | `06a_concurrency_mps` | `06b_concurrency_mlx` |
| 07 | Multi-Model Sim | `07a_multi_model_mps` | `07b_multi_model_mlx` |
| 08 | Dynamic Batching | `08a_dynamic_batch_mps` | `08b_dynamic_batch_mlx` |

## Running Experiments

### Run individual experiment:
```bash
# Terminal 1: Start server
./run_server.sh --experiment experiments/05a_batch_size_mps.yaml

# Terminal 2: Run benchmark
./run_client.sh --experiment --config experiments/05a_batch_size_mps.yaml
```

### Run all experiments:
```bash
python run_systematic_experiments.py
```

## Backend Configuration

### MPS Backend (PyTorch + Metal)
```yaml
model:
  backend: "mps"
  mps:
    fp16: true
```

### MLX Backend (Apple MLX)
```yaml
model:
  backend: "mlx"
  mlx:
    bits: 16
    group_size: 64
```

## Results

Results are saved to `docs/experiments/` with:
- Full experiment configuration
- Performance metrics table
- Key findings summary
