# Timeseries Data

**Experiment:** 04a_dynamic_batch_baseline

**Run:** batch_size=32, concurrency=4

**Generated:** 2026-01-25 20:39:26

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue Wait (ms) | Tokenizer Queue Wait (ms) | Model Queue Wait (ms) | Tokenizer Queue Size | Model Queue Size | Batch Queue Size | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1058 | - | 0.70 | - | 0 | - | - | - | - | - | 0 | 0 | 0 | 0 |
| 1 | 1239 | - | 24.6 | 250 | 7.08 | 25 | 100 | 25 | 25 | 5 | 0 | 3 | 0 | 41.8 |
| 2 | 1679 | - | 66.1 | 312 | 62.8 | 17.5 | 66.7 | 19.6 | 19.2 | 5 | 0 | 3 | 0 | 32.9 |
| 3 | 1735 | - | 64 | 224 | 131 | 20.9 | 58.3 | 21.9 | 21.7 | 3.96 | 0 | 3 | 0 | 40.3 |
| 4 | 1895 | - | 68.4 | 211 | 188 | 21.3 | 56.9 | 22.4 | 22.3 | 3.93 | 0 | 3 | 0 | 46.7 |
| 5 | 1383 | - | 61.6 | 201 | 253 | 21.6 | 55 | 22.9 | 22.4 | 3.85 | 0 | 2 | 0 | 42.1 |
