# Backend Comparison Summary

**Date:** 2023-12-23  
**Model:** cross-encoder/ms-marco-MiniLM-L-6-v2  
**Test Config:** batch_size=32, concurrency=1, 200 requests (6400 pairs total)

## Results

| Backend | Throughput (pairs/s) | Latency Avg (ms) | Latency P99 (ms) | GPU Utilization |
|---------|---------------------|------------------|------------------|-----------------|
| **MPS** | **476.0** | **67.2** | 120.7 | ✅ MPS (Metal) |
| **MLX** | 473.1 | 67.6 | 117.0 | ✅ MPS (Metal) |
| **PyTorch** | 462.1 | 69.2 | 142.6 | ✅ MPS (Metal) |
| Compiled | 189.6 | 168.8 | 256.2 | ⚠️ Inductor overhead |

## Winner: **MPS Backend**

The MPS backend provides the best performance on Apple Silicon:
- **Highest throughput:** 476.0 pairs/second
- **Lowest latency:** 67.2ms average
- **Native GPU acceleration** via Metal Performance Shaders

## Analysis

### Why MPS Wins
1. **Native Metal integration** - MPS uses Apple's Metal Performance Shaders, optimized for Apple Silicon
2. **Low overhead** - Direct GPU access without translation layers
3. **FP16 support** - Efficient half-precision on Apple GPU

### Backend Notes

| Backend | Technology | Notes |
|---------|------------|-------|
| **MPS** | PyTorch + Metal Shaders | Best for Apple Silicon, native GPU |
| **MLX** | Apple MLX + Metal | Very close to MPS, Apple's ML framework |
| **PyTorch** | PyTorch + MPS device | Slightly more overhead than direct MPS |
| **Compiled** | torch.compile + inductor | Inductor optimized for CUDA, not MPS |

### Why Compiled/TensorRT Approach Didn't Help
- `torch.compile` with inductor is optimized for NVIDIA CUDA
- The compilation overhead exceeds benefits on MPS
- Apple Silicon's Metal shaders are already well-optimized
- For Apple Silicon, native backends (MPS/MLX) > compilation

## Recommendation

For subsequent experiments, use **MPS backend** for optimal performance:

```yaml
model:
  backend: "mps"
  mps:
    fp16: true
```

Or equivalently, **MLX** for Apple-native solution:

```yaml
model:
  backend: "mlx"
  mlx:
    bits: 16
```

---

## Next Steps

With MPS/MLX as the chosen backend:
1. **Experiment 05:** Batch size optimization
2. **Experiment 06:** Concurrency optimization  
3. **Experiment 07:** Multi-model simulation
4. **Experiment 08:** Dynamic batching

