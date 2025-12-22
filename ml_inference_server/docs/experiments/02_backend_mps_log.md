[0;32m==========================================
Running experiment: 02_backend_mps
Config: ml_inference_server/experiments/02_backend_mps.yaml
Output: ml_inference_server/docs/experiments/02_backend_mps_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 39003
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 02:52:14,178 | INFO | Loading experiment config: ml_inference_server/experiments/02_backend_mps.yaml
2025-12-23 02:52:14,181 | INFO | Experiment: 02_backend_mps
2025-12-23 02:52:14,181 | INFO | Description: MPS backend with FP16 optimization
2025-12-23 02:52:14,181 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:52:14,181 | INFO | Device: mps
2025-12-23 02:52:14,181 | INFO | Backend: mps
2025-12-23 02:52:14,181 | INFO | Quantization: DISABLED
2025-12-23 02:52:14,199 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:52:14,199 | INFO | Device: mps
2025-12-23 02:52:14,199 | INFO | Precision: FP16
  Waiting... 6s
  Waiting... 8s
2025-12-23 02:52:18,731 | INFO | Applied FP16 precision
2025-12-23 02:52:18,731 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 02:52:18,731 | INFO | Warming up MPS backend (10 iterations)...
2025-12-23 02:52:18,880 | INFO | Warmup complete
2025-12-23 02:52:18,880 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mps', 'use_fp16': True, 'actual_dtype': 'float16', 'model_type': 'cross-encoder', 'sync_on_infer': False, 'mps_memory_allocated': 66627840, 'mps_driver_memory': 1101430784}
2025-12-23 02:52:18,880 | INFO | Experiment: 02_backend_mps | Backend: mps | Device: mps
2025-12-23 02:52:18,884 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 02:52:18,884 | INFO | ==================================================
2025-12-23 02:52:18,884 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 02:52:18,884 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 02:52:18,884 | INFO | ==================================================
  Waiting... 10s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 02:52:19,719 | INFO | ============================================================
2025-12-23 02:52:19,719 | INFO | Cross-Encoder Benchmark Client
2025-12-23 02:52:19,719 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 02:52:19,719 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 02:52:19,720 | INFO | ============================================================
2025-12-23 02:52:19,722 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 02:52:19,727 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 02:52:19,730 | INFO | Connected to cross-encoder server successfully
2025-12-23 02:52:19,730 | INFO | Loading experiment config: ml_inference_server/experiments/02_backend_mps.yaml
2025-12-23 02:52:19,732 | INFO | Experiment: 02_backend_mps
2025-12-23 02:52:19,732 | INFO | Description: MPS backend with FP16 optimization
2025-12-23 02:52:19,732 | INFO | Running experiments with 1 batch sizes and 1 concurrency levels
2025-12-23 02:52:19,732 | INFO | Total experiments: 1
2025-12-23 02:52:19,732 | INFO | 
============================================================
2025-12-23 02:52:19,732 | INFO | Experiment 1/1: batch_size=32, concurrency=1
2025-12-23 02:52:19,732 | INFO | ============================================================
2025-12-23 02:52:19,732 | INFO | Starting benchmark: 200 requests, concurrency=1, batch_size=32
2025-12-23 02:52:22,771 | INFO | Processed 1600 queries (50 requests) | Latency: 37.82ms | QPS: 608.0
2025-12-23 02:52:25,568 | INFO | Processed 3200 queries (100 requests) | Latency: 79.64ms | QPS: 576.0
2025-12-23 02:52:25,568 | INFO | Progress: 100/200 requests
2025-12-23 02:52:28,179 | INFO | Processed 4800 queries (150 requests) | Latency: 40.32ms | QPS: 640.0
2025-12-23 02:52:30,392 | INFO | Processed 6400 queries (200 requests) | Latency: 46.19ms | QPS: 736.0
2025-12-23 02:52:30,392 | INFO | Progress: 200/200 requests
2025-12-23 02:52:30,392 | INFO | Completed: 10.66s | 6400 pairs | 600.39 pairs/s
2025-12-23 02:52:30,404 | INFO | Completed 1 experiments
2025-12-23 02:52:30,404 | INFO | Results saved to ml_inference_server/docs/experiments/02_backend_mps_results.md

========================================================================================================================
EXPERIMENT SUMMARY (Cross-Encoder)
========================================================================================================================
Batch  Conc  Pairs    Time     Lat Avg    Lat P95    Lat P99    TP Avg       TP P99      
------------------------------------------------------------------------------------------------------------------------
32     1     6400     10.7     53.3       83.8       107.6      600.4        918.5       
========================================================================================================================

Results saved to: ml_inference_server/docs/experiments/02_backend_mps_results.md

Capturing dashboard screenshot...
2025-12-23 02:52:31,481 | INFO | Navigating to http://localhost:8080 (attempt 1/3)...
2025-12-23 02:52:31,722 | INFO | Waiting for page to be fully loaded...
2025-12-23 02:52:32,597 | INFO | Metrics frozen - experiment stopped
2025-12-23 02:52:39,733 | INFO | Waiting 1.5s for charts to render...
2025-12-23 02:52:41,234 | INFO | Taking screenshot: ml_inference_server/docs/experiments/screenshots/02_backend_mps_20251223_025230.png
2025-12-23 02:52:41,347 | INFO | Dashboard screenshot saved: ml_inference_server/docs/experiments/screenshots/02_backend_mps_20251223_025230.png

[0;32m==========================================
Experiment completed successfully!
Results: ml_inference_server/docs/experiments/02_backend_mps_results.md
Screenshot: ml_inference_server/docs/experiments/screenshots/02_backend_mps_20251223_025230.png
==========================================[0m
Stopping server (PID: 39003)...
/Users/bnarang/.pyenv/versions/3.11.4/lib/python3.11/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
