# Timeseries Data

**Experiment:** 05_batch_size_sweep

**Generated:** 2026-01-01 20:57:12

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Tokenizer Queue | Model Queue | Batch Queue | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1088.6 | 9.0 | 1.4 | 509.6 | 16 | 4.1 | 47.1 | 4.1 | 0 | 0 | - | 17.3 |
| 1 | 1110.6 | 6.1 | 2.1 | 525.4 | 16 | 14.3 | 60.8 | 14.4 | 0 | 0 | - | 32.4 |
| 2 | 1172.8 | 11.0 | 3.0 | 529.1 | 64 | 15.0 | 39.5 | 15.1 | 0 | 0 | - | 29.2 |
| 3 | 1310.8 | 17.3 | 4.6 | 540.3 | 96 | 28.6 | 87.0 | 28.7 | 0 | 0 | - | 45.7 |
| 4 | 1178.9 | 5.0 | 5.6 | 527.2 | 48 | 14.9 | 49.9 | 15.0 | 0 | 0 | - | 41.1 |

---

### Configuration

**Parameters:** batch_size: 48 | concurrency: 1 | backend: mlx | device: mps | model: cross-encoder/ms-marco-MiniLM-L-6-v2

**Data rows:**

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue (ms) | Tokenizer Queue | Model Queue | Batch Queue | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 5 | 1088.6 | 7.5 | 1.7 | 518.4 | 16 | 6.6 | 53.1 | 6.8 | 0 | 0 | - | 36.4 |
| 6 | 1132.8 | 12.9 | 2.4 | 519.9 | 32 | 9.5 | 62.9 | 9.6 | 0 | 0 | - | 37.2 |
| 7 | 1162.8 | 10.4 | 3.7 | 520.4 | 64 | 11.4 | 40.0 | 11.5 | 0 | 0 | - | 40.5 |
| 8 | 1178.8 | 13.6 | 5.1 | 537.3 | 96 | 22.4 | 49.5 | 22.5 | 0 | 0 | - | 36.4 |
| 9 | 1178.9 | 4.9 | 5.6 | 532.4 | 48 | 21.5 | 49.3 | 21.6 | 0 | 0 | - | 41.1 |
