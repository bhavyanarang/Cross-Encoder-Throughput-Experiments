# Systematic Experiment Plan

This document outlines a structured approach to testing all experimentable parameters one at a time.

## Experimentable Parameters

Based on codebase analysis, the following parameters can be varied:

### 1. Backends
- `pytorch`: Standard PyTorch (CPU/MPS)
- `mps`: Optimized MPS backend
- `mlx`: Apple MLX framework
- `compiled`: torch.compile optimized

### 2. Quantization
- `fp32`: Full precision
- `fp16`: Half precision (default)
- `int8`: 8-bit quantization (CPU only)
- `int4`: 4-bit quantization (MLX only)

### 3. Batch Sizes
- Range: 8, 16, 32, 64, 96, 128, 256

### 4. Concurrency Levels
- Range: 1, 2, 4, 6, 8, 12, 16

### 5. Dynamic Batching
- `enabled`: true/false
- `timeout_ms`: 5, 10, 20, 50, 100, 200
- `max_batch_size`: 32, 64, 96, 128, 256
- `length_aware`: true/false

### 6. Max Sequence Length
- Options: 128, 256, 512

### 7. Model Pool Configuration
- Single model (baseline)
- Multi-model: 2, 3, 4 instances
- Routing: round_robin (if implemented)

### 8. Compilation Modes (for compiled backend)
- `default`: Balanced
- `reduce-overhead`: Optimized for overhead
- `max-autotune`: Maximum optimization

## Structured Experiment Phases

### Phase 1: Backend Baseline (01-04)
**Goal**: Establish baseline performance for each backend
**Fixed**: batch_size=32, concurrency=1, no dynamic batching, fp16

| ID | Experiment | Backend | Description |
|----|-----------|---------|-------------|
| 01 | `01_backend_pytorch` | pytorch | PyTorch baseline |
| 02 | `02_backend_mps` | mps | MPS optimized |
| 03 | `03_backend_mlx` | mlx | MLX framework |
| 04 | `04_backend_compiled` | compiled | torch.compile |

### Phase 2: Batch Size Optimization (05)
**Goal**: Find optimal batch size for each backend
**Fixed**: concurrency=1, no dynamic batching, fp16
**Variable**: batch_size

| ID | Experiment | Backend | Batch Sizes |
|----|-----------|---------|-------------|
| 05a | `05a_batch_size_mps` | mps | [8, 16, 32, 64, 96, 128, 256] |
| 05b | `05b_batch_size_mlx` | mlx | [8, 16, 32, 64, 96, 128, 256] |

### Phase 3: Concurrency Optimization (06)
**Goal**: Find optimal concurrency level
**Fixed**: batch_size=96 (optimal from Phase 2), no dynamic batching, fp16
**Variable**: concurrency

| ID | Experiment | Backend | Concurrency Levels |
|----|-----------|---------|-------------------|
| 06a | `06a_concurrency_mps` | mps | [1, 2, 4, 6, 8, 12] |
| 06b | `06b_concurrency_mlx` | mlx | [1, 2, 4, 6, 8, 12] |

### Phase 4: Dynamic Batching - Basic (07)
**Goal**: Compare static vs dynamic batching
**Fixed**: batch_size=32, concurrency=4, fp16
**Variable**: dynamic batching enabled/disabled

| ID | Experiment | Dynamic Batching | Max Batch | Timeout |
|----|-----------|-----------------|-----------|---------|
| 07a | `07a_dynamic_batch_baseline` | disabled | - | - |
| 07b | `07b_dynamic_batch_enabled` | enabled | 96 | 50ms |

### Phase 5: Dynamic Batching - Timeout Sweep (08)
**Goal**: Find optimal timeout for dynamic batching
**Fixed**: batch_size=32, concurrency=4, max_batch_size=96, fp16
**Variable**: timeout_ms

| ID | Experiment | Backend | Timeout Values |
|----|-----------|---------|---------------|
| 08a | `08a_dynamic_batch_timeout_mps` | mps | [5, 10, 20, 50, 100, 200] |
| 08b | `08b_dynamic_batch_timeout_mlx` | mlx | [5, 10, 20, 50, 100, 200] |

### Phase 6: Dynamic Batching - Max Batch Size (09)
**Goal**: Find optimal max_batch_size for dynamic batching
**Fixed**: batch_size=32, concurrency=4, timeout_ms=50, fp16
**Variable**: max_batch_size

| ID | Experiment | Backend | Max Batch Sizes |
|----|-----------|---------|----------------|
| 09a | `09a_dynamic_batch_max_batch_mps` | mps | [32, 64, 96, 128, 256] |
| 09b | `09b_dynamic_batch_max_batch_mlx` | mlx | [32, 64, 96, 128, 256] |

### Phase 7: Length-Aware Batching (10)
**Goal**: Measure impact of length-aware batching on padding waste
**Fixed**: batch_size=64, concurrency=1, dynamic batching enabled, fp16
**Variable**: length_aware

| ID | Experiment | Length Aware | Description |
|----|-----------|--------------|-------------|
| 10a | `10a_padding_baseline` | false | Random ordering |
| 10b | `10b_padding_length_aware` | true | Sorted by length |

### Phase 8: Quantization Comparison (11)
**Goal**: Compare quantization modes
**Fixed**: batch_size=96, concurrency=1, no dynamic batching
**Variable**: quantization

| ID | Experiment | Backend | Quantization |
|----|-----------|---------|-------------|
| 11a | `11a_quantization_fp32` | mps | fp32 |
| 11b | `11b_quantization_fp16` | mps | fp16 (baseline) |
| 11c | `11c_quantization_int8` | pytorch | int8 (CPU) |

### Phase 9: Max Sequence Length (12)
**Goal**: Measure impact of sequence length on performance
**Fixed**: batch_size=64, concurrency=1, fp16
**Variable**: max_length

| ID | Experiment | Backend | Max Lengths |
|----|-----------|---------|-------------|
| 12a | `12a_max_length_mps` | mps | [128, 256, 512] |
| 12b | `12b_max_length_mlx` | mlx | [128, 256, 512] |

### Phase 10: Multi-Model Pool (13)
**Goal**: Measure scaling with multiple model instances
**Fixed**: batch_size=32, concurrency=4, fp16, no dynamic batching
**Variable**: number of instances

| ID | Experiment | Instances | Description |
|----|-----------|-----------|-------------|
| 13a | `13a_multi_model_2x` | 2 | Two model instances |
| 13b | `13b_multi_model_3x` | 3 | Three model instances |
| 13c | `13c_multi_model_4x` | 4 | Four model instances |

### Phase 11: Compilation Modes (14)
**Goal**: Compare torch.compile modes
**Fixed**: batch_size=64, concurrency=1, fp16
**Variable**: compile_mode

| ID | Experiment | Compile Mode | Description |
|----|-----------|--------------|-------------|
| 14a | `14a_compile_default` | default | Balanced compilation |
| 14b | `14b_compile_reduce_overhead` | reduce-overhead | Optimized overhead |
| 14c | `14c_compile_max_autotune` | max-autotune | Maximum optimization |

### Phase 12: Combined Optimizations (15)
**Goal**: Test best settings from previous phases combined
**Fixed**: Optimal settings from previous phases
**Variable**: Combinations

| ID | Experiment | Description |
|----|-----------|-------------|
| 15a | `15a_optimal_mps` | MPS with optimal batch/concurrency/dynamic batching |
| 15b | `15b_optimal_mlx` | MLX with optimal batch/concurrency/dynamic batching |
| 15c | `15c_optimal_compiled` | Compiled with optimal settings |

## Experiment Naming Convention

Format: `{phase}{letter}_{parameter}_{backend_or_variant}.yaml`

Examples:
- `05a_batch_size_mps.yaml` - Phase 5a, batch size sweep, MPS backend
- `08b_dynamic_batch_timeout_mlx.yaml` - Phase 8b, timeout sweep, MLX backend
- `13a_multi_model_2x.yaml` - Phase 13a, multi-model, 2 instances

## Standard Experiment Structure

Each experiment should:
1. Have a clear, single variable being tested
2. Use consistent baseline settings from previous phases
3. Include a description explaining the hypothesis
4. Use `benchmark_requests: 1500` (inherited from base_config) for ~1 min runtime
5. Test a reasonable range of values for the variable

## Experiment Execution

### How Combinations Work

When an experiment specifies multiple `batch_sizes` and/or `concurrency_levels`, the runner will:
1. **Iterate through all combinations** of batch_sizes × concurrency_levels
2. **Each combination gets the full `benchmark_requests`** number of requests (e.g., 1500)
3. **Metrics are reset** before each configuration for clean per-config metrics
4. **All results are collected** and written to a single results file

Example:
```yaml
experiment:
  batch_sizes: [32, 64]
  concurrency_levels: [1, 2, 4]
  benchmark_requests: 1500  # Each of 6 combinations gets 1500 requests
```

This will run:
- Config 1: batch=32, conc=1, 1500 requests
- Config 2: batch=32, conc=2, 1500 requests
- Config 3: batch=32, conc=4, 1500 requests
- Config 4: batch=64, conc=1, 1500 requests
- Config 5: batch=64, conc=2, 1500 requests
- Config 6: batch=64, conc=4, 1500 requests

**Total runtime**: ~6 minutes (1 min per config × 6 configs)

## Running Experiments

Run all experiments in order:
```bash
./scripts/run_all_experiments.sh
```

Run specific phase:
```bash
# Run Phase 5 (batch size optimization)
for exp in experiments/05*.yaml; do
    ./scripts/run_experiment.sh "$exp"
done
```
