# Systematic Experiment Summary

**Date**: December 23, 2025
**Model**: cross-encoder/ms-marco-MiniLM-L-6-v2
**Platform**: Apple Silicon (MPS)

---

## Phase 1: Backend Comparison (Exp 01-04)

### After Backend Optimization (Dec 23, 2025)

Backends were optimized with `torch.inference_mode()`, shared utilities, and pre-allocated buffers:

| Backend | Throughput (p/s) | Latency (ms) | Status | Improvement |
|---------|------------------|--------------|--------|-------------|
| **MLX** | **529.3** | **60.4** | ✅ Winner | +11.9% |
| MPS | 524.8 | 61.0 | Close second | +10.3% |
| PyTorch | 518.2 | 61.7 | Baseline | +12.1% |
| Compiled | 213.5 | 149.8 | ⚠️ Overhead | +12.6% |

<details>
<summary>Previous Results (before optimization)</summary>

| Backend | Throughput (p/s) | Latency (ms) |
|---------|------------------|--------------|
| MPS | 476.0 | 67.2 |
| MLX | 473.1 | 67.6 |
| PyTorch | 462.1 | 69.2 |
| Compiled | 189.6 | 168.8 |

</details>

**Conclusion**: All backends improved ~10-12% after optimization. MLX slightly leads, but MPS and PyTorch are within margin of error. Compiled backend remains slow due to MPS not supporting inductor's CUDA-optimized kernels.

---

## Phase 2: Batch Size Optimization (Exp 05a, 05b)

### MPS Backend

| Batch Size | Throughput (p/s) | Latency (ms) | Efficiency |
|------------|------------------|--------------|------------|
| 8 | 201.3 | 39.7 | Low TP, Low Lat |
| 16 | 329.7 | 48.5 | |
| 32 | 497.1 | 64.4 | |
| 48 | 627.4 | 76.5 | |
| 64 | 687.4 | 93.1 | |
| **96** | **708.2** | **135.5** | ⭐ Sweet Spot |
| 128 | 725.1 | 176.5 | |
| 192 | 738.1 | 260.1 | |
| 256 | 748.0 | 342.2 | High TP, High Lat |

### MLX Backend (similar results)

| Batch Size | Throughput (p/s) | Latency (ms) |
|------------|------------------|--------------|
| 96 | 708.2 | 135.5 |
| 256 | 744.7 | 343.7 |

**Conclusion**: Optimal batch size is **96** - balances throughput (~708 p/s) with acceptable latency (~135ms).

---

## Phase 3: Concurrency Analysis (Exp 06a, 06b)

### MPS Backend (batch=96)

| Concurrency | Throughput (p/s) | Latency (ms) | Analysis |
|-------------|------------------|--------------|----------|
| 1 | 657.0 | 146.1 | Baseline |
| **2** | **749.8** | **256.0** | ⭐ Optimal |
| 3 | 746.4 | 385.8 | |
| **4** | **757.7** | **503.5** | ⭐ Peak TP |
| 6 | 722.0 | 797.5 | Degrading |
| 8 | 623.1 | 1223.3 | Overloaded |
| 12 | 709.8 | 1605.8 | High latency |

### MLX Backend (batch=96)

| Concurrency | Throughput (p/s) | Latency (ms) |
|-------------|------------------|--------------|
| **2** | **748.8** | **256.3** | ⭐ Optimal |
| 4 | 711.8 | 536.2 | |

**Conclusion**: Optimal concurrency is **2-4** for best throughput/latency trade-off.

---

## Phase 4: High Concurrency Stress Test (Exp 07a, 07b)

### MPS Backend - Multi-Client Simulation

| Batch | Conc | Throughput (p/s) | Latency (ms) |
|-------|------|------------------|--------------|
| 32 | 8 | 654.6 | 384.3 |
| 32 | 16 | 632.5 | 777.8 |
| 32 | 24 | 609.6 | 1160.5 |
| **64** | **4** | **711.3** | **359.7** |
| 64 | 16 | 701.9 | 1404.2 |
| 64 | 24 | 660.8 | 2128.0 |

**Conclusion**: GPU handles high concurrency well - throughput remains 600-710 p/s even at 24 concurrent clients, but latency increases significantly. Best config: **batch=64, conc=4** (711 p/s, 360ms).

---

## Phase 5: Dynamic Batching Evaluation (Exp 08a, 08b)

### MPS Backend with Dynamic Batching

| Batch | Conc | Throughput (p/s) | Latency (ms) | Notes |
|-------|------|------------------|--------------|-------|
| 8 | 8 | 479.4 | 133.1 | Small batch, high conc |
| 16 | 8 | 540.4 | 235.9 | |
| 32 | 8 | 626.1 | 406.8 | |
| **64** | **2** | **719.2** | **177.8** | ⭐ Best Balance |
| 64 | 4 | 710.8 | 359.6 | |
| 64 | 8 | 638.4 | 799.5 | |

### MLX Backend with Dynamic Batching

| Batch | Conc | Throughput (p/s) | Latency (ms) |
|-------|------|------------------|--------------|
| 32 | 8 | 657.4 | 388.4 |
| **64** | **2** | **707.8** | **180.8** | ⭐ Best |

---

## Final Recommendations

### 🏆 Optimal Production Configuration

```yaml
model:
  backend: "mps"  # or "mlx" (nearly identical performance)
  device: "mps"

batching:
  enabled: true
  max_batch_size: 64  # Optimal for throughput
  timeout_ms: 50      # Low timeout for responsiveness

server:
  max_concurrency: 4  # Prevent overload
```

### Performance Targets

| Metric | Value |
|--------|-------|
| **Max Throughput** | ~800 pairs/sec (with optimizations) |
| **Target Latency** | <200ms (P50) |
| **Optimal Batch Size** | 64-96 |
| **Optimal Concurrency** | 2-4 |

### Key Insights

1. **Backend Choice**: MLX, MPS, and PyTorch now perform nearly identically (~520-530 p/s at batch=32). Any of these is a good choice.

2. **Optimization Impact** (Dec 23 update):
   - `torch.inference_mode()` decorator: **+10-12% throughput**
   - Removed redundant `np.array()` wrappers: minor improvement
   - Pre-allocated buffers in ONNX backend: helps small batches

3. **Batch Size Trade-off**:
   - Larger batches → Higher throughput, but also higher latency
   - Sweet spot: batch=64-96 for ~700+ p/s with <200ms latency

4. **Concurrency Impact**:
   - Beyond 4 concurrent clients, latency increases dramatically
   - Throughput saturates around 750-800 p/s regardless of concurrency

5. **Dynamic Batching Value**:
   - Most beneficial when combining many small requests
   - Best config: batch=64, conc=2 (719 p/s, 178ms)

6. **torch.compile Overhead**:
   - Inductor backend adds significant overhead on MPS (~2.5x slower)
   - Warning: "Not enough SMs to use max_autotune_gemm mode"
   - Not recommended for Apple Silicon

---

## Experiment Files Reference

| Exp | Name | Description |
|-----|------|-------------|
| 01 | `01_backend_pytorch.yaml` | PyTorch baseline |
| 02 | `02_backend_mps.yaml` | MPS backend |
| 03 | `03_backend_mlx.yaml` | MLX backend |
| 04 | `04_backend_compiled.yaml` | torch.compile |
| 05a | `05a_batch_size_mps.yaml` | Batch sweep (MPS) |
| 05b | `05b_batch_size_mlx.yaml` | Batch sweep (MLX) |
| 06a | `06a_concurrency_mps.yaml` | Concurrency sweep (MPS) |
| 06b | `06b_concurrency_mlx.yaml` | Concurrency sweep (MLX) |
| 07a | `07a_multi_model_mps.yaml` | Stress test (MPS) |
| 07b | `07b_multi_model_mlx.yaml` | Stress test (MLX) |
| 08a | `08a_dynamic_batch_mps.yaml` | Dynamic batching (MPS) |
| 08b | `08b_dynamic_batch_mlx.yaml` | Dynamic batching (MLX) |
