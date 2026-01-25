# Timeseries Data

**Experiment:** 04b_dynamic_batch_enabled

**Run:** batch_size=32, concurrency=4

**Generated:** 2026-01-25 20:40:02

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue Wait (ms) | Tokenizer Queue Wait (ms) | Model Queue Wait (ms) | Tokenizer Queue Size | Model Queue Size | Batch Queue Size | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1058 | - | 1 | - | 0 | - | - | - | - | - | 0 | 0 | 0 | 0 |
| 1 | 1058 | - | 0.90 | 312 | 29.9 | 15.4 | 64.1 | 19.6 | 19.6 | 4.50 | 0 | 0 | 0 | 39.3 |
| 2 | 1471 | - | 67.8 | 211 | 92.6 | 17.5 | 58.8 | 21.1 | 19.6 | 3.50 | 0 | 3 | 0 | 42.1 |
| 3 | 1855 | - | 64.5 | 201 | 155 | 19.3 | 56.2 | 21.4 | 20.5 | 3.67 | 0 | 3 | 0 | 39.2 |
| 4 | 1855 | - | 63.8 | 195 | 216 | 20.3 | 55 | 22.1 | 21.2 | 3.67 | 0 | 3 | 0 | 34.3 |
| 5 | 2015 | - | 63.8 | 189 | 288 | 21.6 | 51.8 | 23.8 | 22.7 | 3.67 | 0 | 2 | 0 | 41.1 |
