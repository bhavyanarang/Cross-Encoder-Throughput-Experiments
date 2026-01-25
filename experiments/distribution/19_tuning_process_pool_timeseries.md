# Timeseries Data

**Experiment:** 19_tuning_process_pool

**Run:** batch_size=32, concurrency=8

**Generated:** 2026-01-25 21:10:10

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue Wait (ms) | Tokenizer Queue Wait (ms) | Model Queue Wait (ms) | Tokenizer Queue Size | Model Queue Size | Batch Queue Size | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1058 | - | 1.30 | - | 0 | - | - | - | - | - | 0 | 0 | 0 | 0 |
| 1 | 1056 | - | 1.60 | - | 0 | - | - | - | - | - | 0 | 0 | 0 | 0 |
| 2 | 1056 | - | 27 | 571 | 43.6 | 18.2 | 175 | 125 | 125 | 4.29 | 0 | 0 | 0 | 36.5 |
| 3 | 1479 | - | 27 | 429 | 108 | 17.8 | 138 | 21.2 | 20.2 | 4.17 | 0 | 0 | 0 | 30.7 |
| 4 | 1623 | - | 27.3 | 430 | 174 | 17.7 | 131 | 19.9 | 19.2 | 4.54 | 0 | 0 | 0 | 42.6 |
| 5 | 1623 | - | 26.1 | 422 | 234 | 17.6 | 132 | 19.3 | 18.7 | 4.85 | 0 | 0 | 0 | 39.6 |
| 6 | 1771 | - | 26.1 | 436 | 290 | 17.6 | 136 | 18.9 | 18.4 | 4.66 | 0 | 0 | 0 | 40.8 |
