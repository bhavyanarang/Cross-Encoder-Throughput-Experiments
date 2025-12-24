[0;32m==========================================
Running experiment: 02_backend_mps
Config: ml_inference_server/experiments/02_backend_mps.yaml
Output: ml_inference_server/docs/experiments/02_backend_mps_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 48279
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 03:29:15,766 | INFO | Loading experiment config: ml_inference_server/experiments/02_backend_mps.yaml
2025-12-23 03:29:15,769 | INFO | Experiment: 02_backend_mps
2025-12-23 03:29:15,769 | INFO | Description: MPS backend with FP16 optimization
2025-12-23 03:29:15,769 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 03:29:15,769 | INFO | Device: mps
2025-12-23 03:29:15,769 | INFO | Backend: mps
2025-12-23 03:29:15,769 | INFO | Quantization: DISABLED
2025-12-23 03:29:15,786 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 03:29:15,786 | INFO | Device: mps
2025-12-23 03:29:15,786 | INFO | Precision: FP16
  Waiting... 6s
  Waiting... 8s
  Waiting... 10s
  Waiting... 12s
2025-12-23 03:29:23,794 | INFO | Applied FP16 precision
2025-12-23 03:29:23,794 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 03:29:23,794 | INFO | Warming up MPS backend (10 iterations)...
2025-12-23 03:29:23,948 | INFO | Warmup complete
2025-12-23 03:29:23,948 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mps', 'use_fp16': True, 'actual_dtype': 'float16', 'model_type': 'cross-encoder', 'sync_on_infer': False, 'mps_memory_allocated': 66627840, 'mps_driver_memory': 1101430784}
2025-12-23 03:29:23,948 | INFO | Experiment: 02_backend_mps | Backend: mps | Device: mps
2025-12-23 03:29:23,952 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 03:29:23,952 | INFO | ==================================================
2025-12-23 03:29:23,952 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 03:29:23,952 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 03:29:23,952 | INFO | ==================================================
  Waiting... 14s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 03:29:25,601 | INFO | ============================================================
2025-12-23 03:29:25,601 | INFO | Cross-Encoder Benchmark Client
2025-12-23 03:29:25,601 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 03:29:25,601 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 03:29:25,601 | INFO | ============================================================
2025-12-23 03:29:25,602 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 03:29:25,607 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 03:29:25,610 | INFO | Connected to cross-encoder server successfully
2025-12-23 03:29:25,610 | INFO | Loading experiment config: ml_inference_server/experiments/02_backend_mps.yaml
2025-12-23 03:29:25,612 | INFO | Experiment: 02_backend_mps
2025-12-23 03:29:25,612 | INFO | Description: MPS backend with FP16 optimization
2025-12-23 03:29:25,612 | INFO | Running experiments with 1 batch sizes and 1 concurrency levels
2025-12-23 03:29:25,612 | INFO | Total experiments: 1
2025-12-23 03:29:25,612 | INFO |
============================================================
2025-12-23 03:29:25,612 | INFO | Experiment 1/1: batch_size=32, concurrency=1
2025-12-23 03:29:25,612 | INFO | ============================================================
2025-12-23 03:29:25,612 | INFO | Starting benchmark: 200 requests, concurrency=1, batch_size=32
2025-12-23 03:29:28,692 | INFO | Processed 1600 queries (50 requests) | Latency: 42.80ms | QPS: 544.0
2025-12-23 03:29:31,473 | INFO | Processed 3200 queries (100 requests) | Latency: 88.74ms | QPS: 576.0
2025-12-23 03:29:31,474 | INFO | Progress: 100/200 requests
2025-12-23 03:29:34,671 | INFO | Processed 4800 queries (150 requests) | Latency: 39.58ms | QPS: 608.0
2025-12-23 03:29:36,906 | INFO | Processed 6400 queries (200 requests) | Latency: 48.48ms | QPS: 736.0
2025-12-23 03:29:36,907 | INFO | Progress: 200/200 requests
2025-12-23 03:29:36,907 | INFO | Completed: 11.30s | 6400 pairs | 566.61 pairs/s
2025-12-23 03:29:36,917 | INFO | Completed 1 experiments
2025-12-23 03:29:36,918 | INFO | Results saved to ml_inference_server/docs/experiments/02_backend_mps_results.md

========================================================================================================================
EXPERIMENT SUMMARY (Cross-Encoder)
========================================================================================================================
Batch  Conc  Pairs    Time     Lat Avg    Lat P95    Lat P99    TP Avg       TP P99
------------------------------------------------------------------------------------------------------------------------
32     1     6400     11.3     56.5       86.4       155.7      566.6        928.1
========================================================================================================================

Results saved to: ml_inference_server/docs/experiments/02_backend_mps_results.md

Capturing dashboard screenshot...
2025-12-23 03:29:38,210 | INFO | Navigating to http://localhost:8080 (attempt 1/3)...
2025-12-23 03:29:38,449 | INFO | Waiting for page to be fully loaded...
2025-12-23 03:29:38,952 | INFO | Metrics frozen - experiment stopped
2025-12-23 03:30:23,958 | INFO | Waiting 1.5s for charts to render...
2025-12-23 03:30:25,463 | INFO | Taking screenshot: ml_inference_server/docs/experiments/screenshots/02_backend_mps_20251223_032937.png
2025-12-23 03:30:25,646 | INFO | Dashboard screenshot saved: ml_inference_server/docs/experiments/screenshots/02_backend_mps_20251223_032937.png

[0;32m==========================================
Experiment completed successfully!
Results: ml_inference_server/docs/experiments/02_backend_mps_results.md
Screenshot: ml_inference_server/docs/experiments/screenshots/02_backend_mps_20251223_032937.png
==========================================[0m
Stopping server (PID: 48279)...
/Users/bnarang/.pyenv/versions/3.11.4/lib/python3.11/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
