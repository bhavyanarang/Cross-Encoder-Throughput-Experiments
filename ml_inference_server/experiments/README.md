# Experiment Configurations

This directory contains experiment configurations for different model variants and optimizations.

## Structure

- `base_config.yaml` - Base configuration with common settings
- Individual experiment configs - Specific model variants to test

## Available Experiments

### 1. `minilm_baseline.yaml`
Baseline experiment with MiniLM-L6-v2 on MPS without any optimizations.

### 2. `minilm_quantized.yaml`
MiniLM-L6-v2 with INT8 dynamic quantization on CPU.

### 3. `minilm_onnx.yaml`
MiniLM-L6-v2 with ONNX Runtime optimization (to be implemented).

## Running Experiments

### Run a specific experiment:
```bash
./run_server.sh --experiment experiments/minilm_baseline.yaml
# In another terminal:
./run_client.sh --experiment --config experiments/minilm_baseline.yaml
```

### Run all experiments sequentially:
```bash
python run_all_experiments.py
```

## Adding New Experiments

1. Create a new YAML file in this directory
2. Specify the model configuration and any overrides
3. The experiment inherits settings from `base_config.yaml`
4. Run the experiment using the commands above

## Configuration Schema

```yaml
name: "experiment_name"
description: "Description of the experiment"

model:
  name: "model-name"
  device: "cpu|mps|cuda"
  quantized: true|false
  backend: "pytorch|onnx"
  # Backend-specific options
  onnx:
    optimize: true
    use_gpu: false

# Optional: override base experiment parameters
experiment:
  batch_sizes: [1, 4, 8]
  concurrency_levels: [1, 4]
  benchmark_requests: 100
```

