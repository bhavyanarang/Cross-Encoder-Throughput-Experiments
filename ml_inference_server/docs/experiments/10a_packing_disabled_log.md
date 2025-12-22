[0;32m==========================================
Running experiment: 10a_packing_disabled
Config: ml_inference_server/experiments/10a_packing_disabled.yaml
Output: ml_inference_server/docs/experiments/10a_packing_disabled_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 47038
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 03:22:24,848 | INFO | Loading experiment config: ml_inference_server/experiments/10a_packing_disabled.yaml
2025-12-23 03:22:24,851 | INFO | Experiment: 10a_packing_disabled
2025-12-23 03:22:24,851 | INFO | Description: Standard padded inference (baseline for packing comparison)
2025-12-23 03:22:24,851 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 03:22:24,851 | INFO | Device: mps
2025-12-23 03:22:24,851 | INFO | Backend: mps
2025-12-23 03:22:24,851 | INFO | Quantization: DISABLED
2025-12-23 03:22:24,870 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 03:22:24,870 | INFO | Device: mps
2025-12-23 03:22:24,870 | INFO | Precision: FP16
  Waiting... 6s
  Waiting... 8s
2025-12-23 03:22:28,925 | INFO | Applied FP16 precision
2025-12-23 03:22:28,925 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 03:22:28,925 | INFO | Warming up MPS backend (10 iterations)...
2025-12-23 03:22:29,080 | INFO | Warmup complete
2025-12-23 03:22:29,080 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mps', 'use_fp16': True, 'actual_dtype': 'float16', 'model_type': 'cross-encoder', 'sync_on_infer': False, 'mps_memory_allocated': 66627840, 'mps_driver_memory': 1101430784}
2025-12-23 03:22:29,080 | INFO | Experiment: 10a_packing_disabled | Backend: mps | Device: mps
2025-12-23 03:22:29,085 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 03:22:29,085 | INFO | ==================================================
2025-12-23 03:22:29,085 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 03:22:29,085 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 03:22:29,085 | INFO | ==================================================
  Waiting... 10s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 03:22:30,662 | INFO | ============================================================
2025-12-23 03:22:30,662 | INFO | Cross-Encoder Benchmark Client
2025-12-23 03:22:30,662 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 03:22:30,662 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 03:22:30,662 | INFO | ============================================================
2025-12-23 03:22:30,663 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 03:22:30,668 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 03:22:30,672 | INFO | Connected to cross-encoder server successfully
2025-12-23 03:22:30,672 | INFO | Loading experiment config: ml_inference_server/experiments/10a_packing_disabled.yaml
2025-12-23 03:22:30,674 | INFO | Experiment: 10a_packing_disabled
2025-12-23 03:22:30,674 | INFO | Description: Standard padded inference (baseline for packing comparison)
2025-12-23 03:22:30,674 | INFO | Running experiments with 3 batch sizes and 1 concurrency levels
2025-12-23 03:22:30,674 | INFO | Total experiments: 3
2025-12-23 03:22:30,674 | INFO | 
============================================================
2025-12-23 03:22:30,674 | INFO | Experiment 1/3: batch_size=32, concurrency=1
2025-12-23 03:22:30,674 | INFO | ============================================================
2025-12-23 03:22:30,674 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=32
2025-12-23 03:22:33,963 | INFO | Processed 1600 queries (50 requests) | Latency: 38.71ms | QPS: 544.0
2025-12-23 03:22:37,354 | INFO | Processed 3200 queries (100 requests) | Latency: 78.63ms | QPS: 480.0
2025-12-23 03:22:37,355 | INFO | Progress: 100/150 requests
2025-12-23 03:22:39,995 | INFO | Processed 4800 queries (150 requests) | Latency: 40.07ms | QPS: 608.0
2025-12-23 03:22:39,995 | INFO | Completed: 9.32s | 4800 pairs | 514.97 pairs/s
2025-12-23 03:22:40,005 | INFO | 
============================================================
2025-12-23 03:22:40,005 | INFO | Experiment 2/3: batch_size=64, concurrency=1
2025-12-23 03:22:40,005 | INFO | ============================================================
2025-12-23 03:22:40,005 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=64
2025-12-23 03:22:45,136 | INFO | Processed 8000 queries (200 requests) | Latency: 135.92ms | QPS: 640.0
2025-12-23 03:22:49,546 | INFO | Processed 11200 queries (250 requests) | Latency: 89.33ms | QPS: 768.0
2025-12-23 03:22:49,546 | INFO | Progress: 100/150 requests
2025-12-23 03:22:53,787 | INFO | Processed 14400 queries (300 requests) | Latency: 75.72ms | QPS: 832.0
2025-12-23 03:22:53,787 | INFO | Completed: 13.78s | 9600 pairs | 696.57 pairs/s
2025-12-23 03:22:53,788 | INFO | 
============================================================
2025-12-23 03:22:53,788 | INFO | Experiment 3/3: batch_size=96, concurrency=1
2025-12-23 03:22:53,788 | INFO | ============================================================
2025-12-23 03:22:53,788 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=96
2025-12-23 03:23:01,241 | INFO | Processed 19200 queries (350 requests) | Latency: 128.90ms | QPS: 768.0
2025-12-23 03:23:07,676 | INFO | Processed 24000 queries (400 requests) | Latency: 115.10ms | QPS: 864.0
2025-12-23 03:23:07,676 | INFO | Progress: 100/150 requests
2025-12-23 03:23:14,072 | INFO | Processed 28800 queries (450 requests) | Latency: 109.51ms | QPS: 864.0
2025-12-23 03:23:14,072 | INFO | Completed: 20.28s | 14400 pairs | 709.91 pairs/s
2025-12-23 03:23:14,073 | INFO | Completed 3 experiments
2025-12-23 03:23:14,075 | INFO | Results saved to ml_inference_server/docs/experiments/10a_packing_disabled_results.md

========================================================================================================================
EXPERIMENT SUMMARY (Cross-Encoder)
========================================================================================================================
Batch  Conc  Pairs    Time     Lat Avg    Lat P95    Lat P99    TP Avg       TP P99      
------------------------------------------------------------------------------------------------------------------------
32     1     4800     9.3      62.1       99.5       136.2      515.0        908.7       
64     1     9600     13.8     91.9       121.8      146.8      696.6        908.8       
96     1     14400    20.3     135.2      170.3      182.5      709.9        907.1       
========================================================================================================================

Results saved to: ml_inference_server/docs/experiments/10a_packing_disabled_results.md

Capturing dashboard screenshot...
2025-12-23 03:23:15,593 | INFO | Navigating to http://localhost:8080 (attempt 1/3)...
2025-12-23 03:23:15,957 | INFO | Waiting for page to be fully loaded...
2025-12-23 03:23:16,362 | INFO | Metrics frozen - experiment stopped
2025-12-23 03:24:25,966 | INFO | Waiting 1.5s for charts to render...
2025-12-23 03:24:27,469 | INFO | Taking screenshot: ml_inference_server/docs/experiments/screenshots/10a_packing_disabled_20251223_032314.png
2025-12-23 03:24:27,575 | INFO | Dashboard screenshot saved: ml_inference_server/docs/experiments/screenshots/10a_packing_disabled_20251223_032314.png

[0;32m==========================================
Experiment completed successfully!
Results: ml_inference_server/docs/experiments/10a_packing_disabled_results.md
Screenshot: ml_inference_server/docs/experiments/screenshots/10a_packing_disabled_20251223_032314.png
==========================================[0m
Stopping server (PID: 47038)...
/Users/bnarang/.pyenv/versions/3.11.4/lib/python3.11/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
