# Timeseries Data

**Experiment:** 14_multi_model_tokenizer_pool

**Run:** batch_size=16, concurrency=2

**Generated:** 2026-01-25 21:02:42

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue Wait (ms) | Tokenizer Queue Wait (ms) | Model Queue Wait (ms) | Tokenizer Queue Size | Model Queue Size | Batch Queue Size | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1058 | - | 1.10 | - | 0 | - | - | - | - | - | 0 | 0 | 0 | 0 |
| 1 | 1056 | - | 1.10 | 292 | 8.32 | 7.50 | 125 | 156 | 156 | 3.12 | 0 | 0 | 0 | 41.3 |
| 2 | 1207 | - | 2.70 | 86.5 | 51.3 | 7.50 | 63.2 | 17.2 | 7.87 | 2.98 | 0 | 0 | 0 | 30.5 |
| 3 | 1327 | - | 4.50 | 81.0 | 95.6 | 7.46 | 61.7 | 15.9 | 7.74 | 2.74 | 0 | 0 | 0 | 44.4 |
| 4 | 1391 | - | 4.40 | 78.4 | 140 | 7.47 | 60.4 | 15.0 | 7.66 | 2.69 | 0 | 0 | 0 | 38.3 |

**Experiment:** 14_multi_model_tokenizer_pool

**Run:** batch_size=16, concurrency=4

**Generated:** 2026-01-25 21:02:44

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue Wait (ms) | Tokenizer Queue Wait (ms) | Model Queue Wait (ms) | Tokenizer Queue Size | Model Queue Size | Batch Queue Size | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1391 | - | 4.40 | 78.4 | 144 | 7.47 | 60.4 | 15.0 | 7.66 | 2.69 | 0 | 0 | 0 | 38.3 |
| 1 | 1391 | - | 4.60 | 73.3 | 210 | 7.48 | 54.9 | 14.9 | 7.61 | 2.74 | 0 | 0 | 0 | 30.4 |

**Experiment:** 14_multi_model_tokenizer_pool

**Run:** batch_size=32, concurrency=2

**Generated:** 2026-01-25 21:02:50

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue Wait (ms) | Tokenizer Queue Wait (ms) | Model Queue Wait (ms) | Tokenizer Queue Size | Model Queue Size | Batch Queue Size | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1391 | - | 6.60 | 69.0 | 310 | 7.46 | 45.9 | 15.2 | 7.57 | 2.84 | 0 | 0 | 0 | 40.5 |
| 1 | 1391 | - | 7.70 | 72.1 | 358 | 7.54 | 47.2 | 15.4 | 7.67 | 2.80 | 0 | 0 | 0 | 39.4 |
| 2 | 1779 | - | 4 | 74.6 | 423 | 7.78 | 49.6 | 15.7 | 7.91 | 2.80 | 0 | 0 | 0 | 41.6 |
| 3 | 1563 | - | 3.40 | 76.9 | 480 | 7.99 | 51.9 | 15.9 | 8.13 | 2.78 | 0 | 0 | 0 | 42.0 |
| 4 | 1624 | - | 3.40 | 79.6 | 537 | 8.21 | 54.1 | 16.0 | 8.35 | 2.77 | 0 | 0 | 0 | 40.5 |
| 5 | 1784 | - | 3.30 | 81.4 | 570 | 8.60 | 54.5 | 16.0 | 8.69 | 2.73 | 0 | 0 | 0 | 35.1 |

**Experiment:** 14_multi_model_tokenizer_pool

**Run:** batch_size=32, concurrency=4

**Generated:** 2026-01-25 21:02:55

| Index | GPU Mem (MB) | GPU Util (%) | CPU (%) | Latency (ms) | Throughput | Tokenize (ms) | Inference (ms) | Queue Wait (ms) | Tokenizer Queue Wait (ms) | Model Queue Wait (ms) | Tokenizer Queue Size | Model Queue Size | Batch Queue Size | Padding (%) |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 1592 | - | 3.40 | 85.3 | 583 | 9.12 | 56.4 | 16.3 | 9.20 | 2.77 | 0 | 0 | 0 | 34.9 |
| 1 | 1592 | - | 3.60 | 92.5 | 596 | 9.89 | 59.4 | 16.7 | 9.98 | 2.77 | 0 | 0 | 0 | 41.9 |
| 2 | 1592 | - | 3.30 | 112 | 583 | 13 | 73.6 | 17.1 | 13.2 | 2.76 | 0 | 0 | 0 | 41.6 |
| 3 | 1592 | - | 3.30 | 158 | 545 | 16.7 | 92.5 | 17.5 | 16.8 | 2.68 | 0 | 0 | 0 | 31.9 |
| 4 | 1592 | - | 3.30 | 166 | 558 | 17.5 | 98.0 | 17.6 | 17.5 | 2.71 | 0 | 0 | 0 | 47.6 |
| 5 | 1592 | - | 3.60 | 175 | 547 | 17.5 | 109 | 17.5 | 17.5 | 2.71 | 0 | 0 | 0 | 37.6 |
