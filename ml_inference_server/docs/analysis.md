# Experiment Results Analysis

## Executive Summary

| Experiment | Device | Backend | Peak Throughput | Latency (batch=1) | Status |
|------------|--------|---------|-----------------|-------------------|--------|
| **MLX INT8** | MPS | MLX | **22,200 pairs/s** | **0.46ms** | ✅ **BEST** |
| **MLX INT4** | MPS | MLX | **22,119 pairs/s** | **0.50ms** | ✅ **BEST** |
| Baseline (FP32) | MPS | PyTorch | 3,300 pairs/s | 8.64ms | ✅ Working |
| FP16 Quantized | MPS | PyTorch | 3,138 pairs/s | 9.13ms | ✅ Working |
| Dynamic Batching | MPS | PyTorch | 3,058 pairs/s | 9.34ms | ✅ Working |
| ONNX Runtime | CPU | ONNX | 1,025 pairs/s | 2.38ms | ⚠️ batch=1 only |

---

## 🚀 MLX - The Game Changer

**MLX (Apple's ML framework) is 7x faster than PyTorch on Apple Silicon!**

### Performance Comparison

| Metric | PyTorch (FP32) | MLX | Improvement |
|--------|----------------|-----|-------------|
| **Peak Throughput** | 3,300 pairs/s | 22,200 pairs/s | **6.7x faster** |
| **Single Request** | 8.64ms | 0.46ms | **18.8x faster** |
| **Batch=32, Conc=8** | 3,087 pairs/s | 22,200 pairs/s | **7.2x faster** |

### Why MLX is So Fast

1. **Unified Memory**: No CPU↔GPU data transfer
2. **Native Apple Silicon**: Optimized for M1/M2/M3 chips
3. **Lazy Evaluation**: Efficient computation graph
4. **Metal Backend**: Direct GPU access

---

## Detailed Results

### MLX INT8 (Best Performance)

```
Batch  Conc  Throughput    Latency
1      1     1,265 pairs/s  0.46ms
4      4     5,445 pairs/s  2.10ms
8      8     9,045 pairs/s  2.98ms
16     8     14,834 pairs/s 3.31ms
32     8     22,200 pairs/s 3.73ms  ← PEAK
```

### PyTorch Baseline (for comparison)

```
Batch  Conc  Throughput    Latency
1      1     108 pairs/s    8.64ms
4      4     504 pairs/s    26.98ms
8      8     1,003 pairs/s  32.82ms
16     8     1,777 pairs/s  34.33ms
32     8     3,077 pairs/s  36.29ms
```

---

## Platform Support

### Quantization Support by Platform

| Platform | FP32 | FP16 | INT8 | INT4 | MLX |
|----------|:----:|:----:|:----:|:----:|:---:|
| **Apple Silicon (MPS)** | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Intel Mac (CPU)** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Linux x86** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **NVIDIA GPU** | ✅ | ✅ | ✅ | ✅ | ❌ |

### Recommended Backend by Platform

| Platform | Best Backend | Expected Throughput |
|----------|--------------|---------------------|
| **Apple Silicon** | **MLX** | ~22,000 pairs/s |
| Intel Mac | PyTorch (INT8) | ~1,000 pairs/s |
| Linux x86 + GPU | PyTorch (FP16) | ~10,000+ pairs/s |

---

## How to Run MLX Experiments

### Install MLX
```bash
pip install mlx
```

### Run MLX INT8 Experiment
```bash
./run_experiment.sh ml_inference_server/experiments/minilm_mlx_int8.yaml
```

### Run MLX INT4 Experiment
```bash
./run_experiment.sh ml_inference_server/experiments/minilm_mlx_int4.yaml
```

---

## All Available Experiments

```
experiments/
├── minilm_baseline.yaml        # PyTorch FP32 (baseline)
├── minilm_quantized.yaml       # PyTorch FP16
├── minilm_int8_cpu.yaml        # PyTorch INT8 (x86 only)
├── minilm_dynamic_batching.yaml # Server-side batching
├── minilm_onnx.yaml            # ONNX Runtime
├── minilm_mlx_int8.yaml        # MLX INT8 ← RECOMMENDED
└── minilm_mlx_int4.yaml        # MLX INT4 ← RECOMMENDED
```

---

## Recommendations

### For Apple Silicon Users

1. **Use MLX backend** - 7x faster than PyTorch
2. **Use INT8 or INT4** - Same performance, lower memory
3. **Batch size 32, concurrency 8** - Optimal throughput

### For Production

```yaml
# Recommended config for Apple Silicon
model:
  name: "sentence-transformers/all-MiniLM-L6-v2"
  device: "mps"
  backend: "mlx"
  mlx:
    bits: 8
```

### Expected Performance

- **Single request**: < 1ms
- **Throughput**: > 20,000 pairs/s
- **Memory**: ~100MB

---

## Technical Notes

### MLX Thread Safety

MLX operations are not thread-safe by default. The backend uses a `threading.Lock()` to ensure safe concurrent access:

```python
def infer(self, texts):
    with self._inference_lock:
        return self._mlx_infer(texts)
```

### Fallback Mechanism

If MLX fails, the backend automatically falls back to PyTorch FP16:

```python
except Exception as e:
    logger.warning("Using PyTorch fallback")
    return self._pytorch_fallback.infer(texts)
```

---

## Conclusion

**MLX is the clear winner for Apple Silicon:**

- ✅ **22,200 pairs/s** peak throughput
- ✅ **0.46ms** single request latency
- ✅ **7x faster** than PyTorch
- ✅ Native quantization support
- ✅ Unified memory (no transfer overhead)

For any ML inference workload on Apple Silicon, **use MLX**.
