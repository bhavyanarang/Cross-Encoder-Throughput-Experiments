# Timeseries Data

**Experiment:** 06_dynamic_batch_max_batch_sweep

**Run:** batch_size=32, concurrency=4

**Generated:** 2026-01-25 20:45:40

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue Wait (ms) | Tokenizer Queue Wait (ms) | Model Queue Wait (ms) | Tokenizer Queue Size | Model Queue Size | Batch Queue Size | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1058 | - | 0.80 | - | 0 | - | - | - | - | - | 0 | 0 | 0 | 0 |
| 1 | 1058 | - | 0.90 | - | 0 | - | - | - | - | - | 0 | 0 | 0 | 0 |
| 2 | 1371 | - | 54.1 | 194 | 56.9 | 17.0 | 62.5 | 18.7 | 18.1 | 3.75 | 0 | 3 | 0 | 44.6 |
| 3 | 1727 | - | 63.8 | 198 | 126 | 17.8 | 57.5 | 19.2 | 18.5 | 3.54 | 0 | 3 | 0 | 47.1 |
| 4 | 1867 | - | 62.3 | 192 | 192 | 19.3 | 56.2 | 20.9 | 20.1 | 3.49 | 0 | 3 | 0 | 56.0 |
| 5 | 2027 | - | 62 | 190 | 257 | 20 | 54.5 | 21.4 | 20.7 | 3.40 | 0 | 2 | 0 | 42.6 |
