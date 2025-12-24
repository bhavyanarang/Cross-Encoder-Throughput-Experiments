[0;32m==========================================
Running experiment: 09b_padding_length_aware
Config: ml_inference_server/experiments/09b_padding_length_aware.yaml
Output: ml_inference_server/docs/experiments/09b_padding_length_aware_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 49704
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 03:32:44,019 | INFO | Loading experiment config: ml_inference_server/experiments/09b_padding_length_aware.yaml
2025-12-23 03:32:44,022 | INFO | Experiment: 09b_padding_length_aware
2025-12-23 03:32:44,022 | INFO | Description: Length-aware batching - sorted by token length
2025-12-23 03:32:44,022 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 03:32:44,022 | INFO | Device: mps
2025-12-23 03:32:44,022 | INFO | Backend: mps
2025-12-23 03:32:44,022 | INFO | Quantization: DISABLED
2025-12-23 03:32:44,039 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 03:32:44,039 | INFO | Device: mps
2025-12-23 03:32:44,039 | INFO | Precision: FP16
  Waiting... 6s
  Waiting... 8s
2025-12-23 03:32:48,343 | INFO | Applied FP16 precision
2025-12-23 03:32:48,343 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 03:32:48,343 | INFO | Warming up MPS backend (10 iterations)...
2025-12-23 03:32:48,490 | INFO | Warmup complete
2025-12-23 03:32:48,490 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mps', 'use_fp16': True, 'actual_dtype': 'float16', 'model_type': 'cross-encoder', 'sync_on_infer': False, 'mps_memory_allocated': 66627840, 'mps_driver_memory': 1101430784}
2025-12-23 03:32:48,490 | INFO | Experiment: 09b_padding_length_aware | Backend: mps | Device: mps
2025-12-23 03:32:48,490 | INFO | Length-aware batching: ENABLED (sorting pairs by length)
2025-12-23 03:32:48,490 | INFO | Length-aware batching ENABLED - pairs will be sorted by length
2025-12-23 03:32:48,494 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 03:32:48,494 | INFO | ==================================================
2025-12-23 03:32:48,494 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 03:32:48,494 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 03:32:48,494 | INFO | ==================================================
  Waiting... 10s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 03:32:50,344 | INFO | ============================================================
2025-12-23 03:32:50,344 | INFO | Cross-Encoder Benchmark Client
2025-12-23 03:32:50,344 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 03:32:50,344 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 03:32:50,344 | INFO | ============================================================
2025-12-23 03:32:50,344 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 03:32:50,349 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 03:32:50,352 | INFO | Connected to cross-encoder server successfully
2025-12-23 03:32:50,352 | INFO | Loading experiment config: ml_inference_server/experiments/09b_padding_length_aware.yaml
2025-12-23 03:32:50,357 | INFO | Experiment: 09b_padding_length_aware
2025-12-23 03:32:50,357 | INFO | Description: Length-aware batching - sorted by token length
2025-12-23 03:32:50,357 | INFO | Running experiments with 3 batch sizes and 1 concurrency levels
2025-12-23 03:32:50,357 | INFO | Total experiments: 3
2025-12-23 03:32:50,357 | INFO |
============================================================
2025-12-23 03:32:50,357 | INFO | Experiment 1/3: batch_size=32, concurrency=1
2025-12-23 03:32:50,357 | INFO | ============================================================
2025-12-23 03:32:50,357 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=32
2025-12-23 03:32:53,560 | INFO | Processed 1600 queries (50 requests) | Latency: 37.18ms | QPS: 576.0
2025-12-23 03:32:56,339 | INFO | Processed 3200 queries (100 requests) | Latency: 88.06ms | QPS: 576.0
2025-12-23 03:32:56,340 | INFO | Progress: 100/150 requests
2025-12-23 03:32:58,846 | INFO | Processed 4800 queries (150 requests) | Latency: 40.29ms | QPS: 704.0
2025-12-23 03:32:58,847 | INFO | Completed: 8.49s | 4800 pairs | 565.37 pairs/s
2025-12-23 03:32:58,857 | INFO |
============================================================
2025-12-23 03:32:58,857 | INFO | Experiment 2/3: batch_size=64, concurrency=1
2025-12-23 03:32:58,857 | INFO | ============================================================
2025-12-23 03:32:58,857 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=64
2025-12-23 03:33:04,017 | INFO | Processed 8000 queries (200 requests) | Latency: 114.43ms | QPS: 640.0
2025-12-23 03:33:08,753 | INFO | Processed 11200 queries (250 requests) | Latency: 100.26ms | QPS: 832.0
2025-12-23 03:33:08,754 | INFO | Progress: 100/150 requests
2025-12-23 03:33:12,945 | INFO | Processed 14400 queries (300 requests) | Latency: 74.47ms | QPS: 832.0
2025-12-23 03:33:12,946 | INFO | Completed: 14.09s | 9600 pairs | 681.38 pairs/s
2025-12-23 03:33:12,946 | INFO |
============================================================
2025-12-23 03:33:12,946 | INFO | Experiment 3/3: batch_size=96, concurrency=1
2025-12-23 03:33:12,946 | INFO | ============================================================
2025-12-23 03:33:12,946 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=96
2025-12-23 03:33:21,112 | INFO | Processed 19200 queries (350 requests) | Latency: 127.07ms | QPS: 768.0
2025-12-23 03:33:27,331 | INFO | Processed 24000 queries (400 requests) | Latency: 112.80ms | QPS: 864.0
2025-12-23 03:33:27,331 | INFO | Progress: 100/150 requests
2025-12-23 03:33:33,675 | INFO | Processed 28800 queries (450 requests) | Latency: 109.32ms | QPS: 864.0
2025-12-23 03:33:33,676 | INFO | Completed: 20.73s | 14400 pairs | 694.64 pairs/s
2025-12-23 03:33:33,677 | INFO | Completed 3 experiments
2025-12-23 03:33:33,678 | INFO | Results saved to ml_inference_server/docs/experiments/09b_padding_length_aware_results.md

========================================================================================================================
EXPERIMENT SUMMARY (Cross-Encoder)
========================================================================================================================
Batch  Conc  Pairs    Time     Lat Avg    Lat P95    Lat P99    TP Avg       TP P99
------------------------------------------------------------------------------------------------------------------------
32     1     4800     8.5      56.6       90.5       112.1      565.4        914.6
64     1     9600     14.1     93.9       145.5      163.9      681.4        908.3
96     1     14400    20.7     138.2      211.7      296.9      694.6        915.9
========================================================================================================================

Results saved to: ml_inference_server/docs/experiments/09b_padding_length_aware_results.md

Capturing dashboard screenshot...
2025-12-23 03:33:35,333 | INFO | Navigating to http://localhost:8080 (attempt 1/3)...
2025-12-23 03:33:35,595 | INFO | Waiting for page to be fully loaded...
2025-12-23 03:33:35,869 | INFO | Metrics frozen - experiment stopped
2025-12-23 03:34:04,110 | INFO | Waiting 1.5s for charts to render...
2025-12-23 03:34:05,614 | INFO | Taking screenshot: ml_inference_server/docs/experiments/screenshots/09b_padding_length_aware_20251223_033333.png
2025-12-23 03:34:05,822 | INFO | Dashboard screenshot saved: ml_inference_server/docs/experiments/screenshots/09b_padding_length_aware_20251223_033333.png

[0;32m==========================================
Experiment completed successfully!
Results: ml_inference_server/docs/experiments/09b_padding_length_aware_results.md
Screenshot: ml_inference_server/docs/experiments/screenshots/09b_padding_length_aware_20251223_033333.png
==========================================[0m
Stopping server (PID: 49704)...
/Users/bnarang/.pyenv/versions/3.11.4/lib/python3.11/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
