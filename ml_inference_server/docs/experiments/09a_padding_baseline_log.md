[0;32m==========================================
Running experiment: 09a_padding_baseline
Config: ml_inference_server/experiments/09a_padding_baseline.yaml
Output: ml_inference_server/docs/experiments/09a_padding_baseline_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 43206
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 03:07:50,862 | INFO | Loading experiment config: ml_inference_server/experiments/09a_padding_baseline.yaml
2025-12-23 03:07:50,864 | INFO | Experiment: 09a_padding_baseline
2025-12-23 03:07:50,864 | INFO | Description: Baseline padding analysis - random ordering
2025-12-23 03:07:50,864 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 03:07:50,864 | INFO | Device: mps
2025-12-23 03:07:50,864 | INFO | Backend: mps
2025-12-23 03:07:50,864 | INFO | Quantization: DISABLED
2025-12-23 03:07:50,880 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 03:07:50,880 | INFO | Device: mps
2025-12-23 03:07:50,880 | INFO | Precision: FP16
  Waiting... 6s
  Waiting... 8s
  Waiting... 10s
2025-12-23 03:07:55,721 | INFO | Applied FP16 precision
2025-12-23 03:07:55,722 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 03:07:55,722 | INFO | Warming up MPS backend (10 iterations)...
2025-12-23 03:07:55,872 | INFO | Warmup complete
2025-12-23 03:07:55,872 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mps', 'use_fp16': True, 'actual_dtype': 'float16', 'model_type': 'cross-encoder', 'sync_on_infer': False, 'mps_memory_allocated': 66627840, 'mps_driver_memory': 1101430784}
2025-12-23 03:07:55,872 | INFO | Experiment: 09a_padding_baseline | Backend: mps | Device: mps
2025-12-23 03:07:55,876 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 03:07:55,876 | INFO | ==================================================
2025-12-23 03:07:55,876 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 03:07:55,876 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 03:07:55,876 | INFO | ==================================================
  Waiting... 12s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 03:07:57,876 | INFO | ============================================================
2025-12-23 03:07:57,876 | INFO | Cross-Encoder Benchmark Client
2025-12-23 03:07:57,876 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 03:07:57,876 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 03:07:57,876 | INFO | ============================================================
2025-12-23 03:07:57,879 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 03:07:57,885 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 03:07:57,888 | INFO | Connected to cross-encoder server successfully
2025-12-23 03:07:57,888 | INFO | Loading experiment config: ml_inference_server/experiments/09a_padding_baseline.yaml
2025-12-23 03:07:57,890 | INFO | Experiment: 09a_padding_baseline
2025-12-23 03:07:57,890 | INFO | Description: Baseline padding analysis - random ordering
2025-12-23 03:07:57,890 | INFO | Running experiments with 3 batch sizes and 1 concurrency levels
2025-12-23 03:07:57,890 | INFO | Total experiments: 3
2025-12-23 03:07:57,890 | INFO | 
============================================================
2025-12-23 03:07:57,890 | INFO | Experiment 1/3: batch_size=32, concurrency=1
2025-12-23 03:07:57,890 | INFO | ============================================================
2025-12-23 03:07:57,890 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=32
2025-12-23 03:08:00,980 | INFO | Processed 1600 queries (50 requests) | Latency: 37.21ms | QPS: 576.0
2025-12-23 03:08:03,968 | INFO | Processed 3200 queries (100 requests) | Latency: 71.71ms | QPS: 608.0
2025-12-23 03:08:03,968 | INFO | Progress: 100/150 requests
2025-12-23 03:08:06,897 | INFO | Processed 4800 queries (150 requests) | Latency: 39.59ms | QPS: 704.0
2025-12-23 03:08:06,898 | INFO | Completed: 9.01s | 4800 pairs | 532.87 pairs/s
2025-12-23 03:08:06,906 | INFO | 
============================================================
2025-12-23 03:08:06,906 | INFO | Experiment 2/3: batch_size=64, concurrency=1
2025-12-23 03:08:06,906 | INFO | ============================================================
2025-12-23 03:08:06,906 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=64
2025-12-23 03:08:12,026 | INFO | Processed 8000 queries (200 requests) | Latency: 114.07ms | QPS: 640.0
2025-12-23 03:08:16,404 | INFO | Processed 11200 queries (250 requests) | Latency: 91.75ms | QPS: 768.0
2025-12-23 03:08:16,405 | INFO | Progress: 100/150 requests
2025-12-23 03:08:20,659 | INFO | Processed 14400 queries (300 requests) | Latency: 73.13ms | QPS: 832.0
2025-12-23 03:08:20,659 | INFO | Completed: 13.75s | 9600 pairs | 698.03 pairs/s
2025-12-23 03:08:20,660 | INFO | 
============================================================
2025-12-23 03:08:20,660 | INFO | Experiment 3/3: batch_size=96, concurrency=1
2025-12-23 03:08:20,660 | INFO | ============================================================
2025-12-23 03:08:20,660 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=96
2025-12-23 03:08:27,969 | INFO | Processed 19200 queries (350 requests) | Latency: 124.95ms | QPS: 768.0
2025-12-23 03:08:34,227 | INFO | Processed 24000 queries (400 requests) | Latency: 112.93ms | QPS: 864.0
2025-12-23 03:08:34,227 | INFO | Progress: 100/150 requests
2025-12-23 03:08:40,549 | INFO | Processed 28800 queries (450 requests) | Latency: 106.35ms | QPS: 864.0
2025-12-23 03:08:40,550 | INFO | Completed: 19.89s | 14400 pairs | 723.98 pairs/s
2025-12-23 03:08:40,550 | INFO | Completed 3 experiments
2025-12-23 03:08:40,553 | INFO | Results saved to ml_inference_server/docs/experiments/09a_padding_baseline_results.md

========================================================================================================================
EXPERIMENT SUMMARY (Cross-Encoder)
========================================================================================================================
Batch  Conc  Pairs    Time     Lat Avg    Lat P95    Lat P99    TP Avg       TP P99      
------------------------------------------------------------------------------------------------------------------------
32     1     4800     9.0      60.0       90.2       201.5      532.9        914.0       
64     1     9600     13.8     91.7       121.6      160.9      698.0        899.6       
96     1     14400    19.9     132.6      161.1      178.1      724.0        914.3       
========================================================================================================================

Results saved to: ml_inference_server/docs/experiments/09a_padding_baseline_results.md

Capturing dashboard screenshot...
2025-12-23 03:08:41,798 | INFO | Navigating to http://localhost:8080 (attempt 1/3)...
2025-12-23 03:08:42,123 | INFO | Waiting for page to be fully loaded...
2025-12-23 03:08:42,583 | INFO | Metrics frozen - experiment stopped
2025-12-23 03:09:08,134 | INFO | Waiting 1.5s for charts to render...
2025-12-23 03:09:09,639 | INFO | Taking screenshot: ml_inference_server/docs/experiments/screenshots/09a_padding_baseline_20251223_030840.png
2025-12-23 03:09:09,746 | INFO | Dashboard screenshot saved: ml_inference_server/docs/experiments/screenshots/09a_padding_baseline_20251223_030840.png

[0;32m==========================================
Experiment completed successfully!
Results: ml_inference_server/docs/experiments/09a_padding_baseline_results.md
Screenshot: ml_inference_server/docs/experiments/screenshots/09a_padding_baseline_20251223_030840.png
==========================================[0m
Stopping server (PID: 43206)...
/Users/bnarang/.pyenv/versions/3.11.4/lib/python3.11/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
