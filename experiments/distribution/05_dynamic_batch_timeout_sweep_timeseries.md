# Timeseries Data

**Experiment:** 05_dynamic_batch_timeout_sweep

**Run:** batch_size=32, concurrency=4

**Generated:** 2026-01-25 20:40:36

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue Wait (ms) | Tokenizer Queue Wait (ms) | Model Queue Wait (ms) | Tokenizer Queue Size | Model Queue Size | Batch Queue Size | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1058 | - | 0.80 | - | 0 | - | - | - | - | - | 0 | 0 | 0 | 0 |
| 1 | 1058 | - | 0.90 | - | 0 | - | - | - | - | - | 0 | 0 | 0 | 0 |
| 2 | 1251 | - | 36.6 | 212 | 57.2 | 13.8 | 63.5 | 18.7 | 17.5 | 3.75 | 0 | 3 | 0 | 44.6 |
| 3 | 1587 | - | 67.5 | 201 | 130 | 17.5 | 58.1 | 20.3 | 19.2 | 3.65 | 0 | 2 | 0 | 40.6 |
| 4 | 1855 | - | 63.1 | 200 | 189 | 18.4 | 56.5 | 21.7 | 20 | 3.51 | 0 | 3 | 0 | 37.0 |
| 5 | 2015 | - | 63.6 | 195 | 254 | 20.4 | 55.4 | 22.6 | 21.5 | 3.48 | 0 | 2 | 0 | 52.0 |
