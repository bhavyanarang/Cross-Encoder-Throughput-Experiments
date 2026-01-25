# Timeseries Data

**Experiment:** 13a_multi_model_2x

**Run:** batch_size=32, concurrency=4

**Generated:** 2026-01-25 21:00:24

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue Wait (ms) | Tokenizer Queue Wait (ms) | Model Queue Wait (ms) | Tokenizer Queue Size | Model Queue Size | Batch Queue Size | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1058 | - | 1.50 | - | 0 | - | - | - | - | - | 0 | 0 | 0 | 0 |
| 1 | 1058 | - | 7.10 | 375 | 10.5 | 21.2 | 138 | 138 | 138 | 2.50 | 0 | 0 | 0 | 40.2 |
| 2 | 1263 | - | 7.10 | 184 | 99.9 | 16.6 | 76.2 | 18.4 | 17.2 | 3.45 | 0 | 0 | 0 | 49.8 |
| 3 | 1623 | - | 31 | 175 | 188 | 16.2 | 74.4 | 17.9 | 16.8 | 3.72 | 0 | 0 | 0 | 50.1 |
| 4 | 1771 | - | 34.1 | 169 | 274 | 16.0 | 72.9 | 17.7 | 16.5 | 3.97 | 0 | 1 | 0 | 52.7 |
