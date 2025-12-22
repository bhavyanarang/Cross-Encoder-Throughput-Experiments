[0;32m==========================================
Running experiment: 02_backend_mps
Config: ml_inference_server/experiments/02_backend_mps.yaml
Output: ml_inference_server/docs/experiments/02_backend_mps_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 32791
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 02:21:41,379 | INFO | Loading experiment config: ml_inference_server/experiments/02_backend_mps.yaml
2025-12-23 02:21:41,381 | INFO | Experiment: 02_backend_mps
2025-12-23 02:21:41,382 | INFO | Description: MPS backend with FP16 optimization
2025-12-23 02:21:41,382 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:21:41,382 | INFO | Device: mps
2025-12-23 02:21:41,382 | INFO | Backend: mps
2025-12-23 02:21:41,382 | INFO | Quantization: DISABLED
2025-12-23 02:21:41,399 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:21:41,399 | INFO | Device: mps
2025-12-23 02:21:41,399 | INFO | Precision: FP16
  Waiting... 6s
  Waiting... 8s
2025-12-23 02:21:45,503 | INFO | Applied FP16 precision
2025-12-23 02:21:45,503 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 02:21:45,503 | INFO | Warming up MPS backend (10 iterations)...
2025-12-23 02:21:45,649 | INFO | Warmup complete
2025-12-23 02:21:45,649 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mps', 'use_fp16': True, 'actual_dtype': 'float16', 'model_type': 'cross-encoder', 'sync_on_infer': False, 'mps_memory_allocated': 66627840, 'mps_driver_memory': 1101430784}
2025-12-23 02:21:45,649 | INFO | Experiment: 02_backend_mps | Backend: mps | Device: mps
2025-12-23 02:21:45,653 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 02:21:45,653 | INFO | ==================================================
2025-12-23 02:21:45,653 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 02:21:45,653 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 02:21:45,653 | INFO | ==================================================
  Waiting... 10s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 02:21:46,284 | INFO | ============================================================
2025-12-23 02:21:46,284 | INFO | Cross-Encoder Benchmark Client
2025-12-23 02:21:46,284 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 02:21:46,284 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 02:21:46,284 | INFO | ============================================================
2025-12-23 02:21:46,286 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 02:21:46,292 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 02:21:46,297 | INFO | Connected to cross-encoder server successfully
2025-12-23 02:21:46,297 | INFO | Loading experiment config: ml_inference_server/experiments/02_backend_mps.yaml
2025-12-23 02:21:46,299 | INFO | Experiment: 02_backend_mps
2025-12-23 02:21:46,299 | INFO | Description: MPS backend with FP16 optimization
2025-12-23 02:21:46,299 | INFO | Running experiments with 1 batch sizes and 1 concurrency levels
2025-12-23 02:21:46,299 | INFO | Total experiments: 1
2025-12-23 02:21:46,299 | INFO | 
============================================================
2025-12-23 02:21:46,299 | INFO | Experiment 1/1: batch_size=32, concurrency=1
2025-12-23 02:21:46,299 | INFO | ============================================================
2025-12-23 02:21:46,299 | INFO | Starting benchmark: 200 requests, concurrency=1, batch_size=32
2025-12-23 02:21:49,406 | INFO | Processed 1600 queries (50 requests) | Latency: 39.05ms | QPS: 608.0
2025-12-23 02:21:52,151 | INFO | Processed 3200 queries (100 requests) | Latency: 73.89ms | QPS: 608.0
2025-12-23 02:21:52,152 | INFO | Progress: 100/200 requests
2025-12-23 02:21:54,628 | INFO | Processed 4800 queries (150 requests) | Latency: 43.77ms | QPS: 672.0
2025-12-23 02:21:56,841 | INFO | Processed 6400 queries (200 requests) | Latency: 45.34ms | QPS: 736.0
2025-12-23 02:21:56,842 | INFO | Progress: 200/200 requests
2025-12-23 02:21:56,842 | INFO | Completed: 10.54s | 6400 pairs | 607.06 pairs/s
2025-12-23 02:21:56,851 | INFO | Completed 1 experiments
2025-12-23 02:21:56,852 | INFO | Results saved to ml_inference_server/docs/experiments/02_backend_mps_results.md

========================================================================================================================
EXPERIMENT SUMMARY (Cross-Encoder)
========================================================================================================================
Batch  Conc  Pairs    Time     Lat Avg    Lat P95    Lat P99    TP Avg       TP P99      
------------------------------------------------------------------------------------------------------------------------
32     1     6400     10.5     52.7       80.5       101.8      607.1        917.8       
========================================================================================================================

Results saved to: ml_inference_server/docs/experiments/02_backend_mps_results.md

Capturing dashboard screenshot...
2025-12-23 02:21:59,076 | INFO | Metrics frozen - experiment stopped
2025-12-23 02:22:00,368 | INFO | Dashboard screenshot saved: ml_inference_server/docs/experiments/screenshots/02_backend_mps_20251223_022156.png

[0;32m==========================================
Experiment completed successfully!
Results: ml_inference_server/docs/experiments/02_backend_mps_results.md
Screenshot: ml_inference_server/docs/experiments/screenshots/02_backend_mps_20251223_022156.png
==========================================[0m
Stopping server (PID: 32791)...
/Users/bnarang/.pyenv/versions/3.11.4/lib/python3.11/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
[0;32m==========================================
Running experiment: 03_backend_mlx
Config: ml_inference_server/experiments/03_backend_mlx.yaml
Output: ml_inference_server/docs/experiments/03_backend_mlx_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 33045
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 02:22:28,882 | INFO | Loading experiment config: ml_inference_server/experiments/03_backend_mlx.yaml
2025-12-23 02:22:28,884 | INFO | Experiment: 03_backend_mlx
2025-12-23 02:22:28,884 | INFO | Description: MLX backend with 16-bit quantization
2025-12-23 02:22:28,884 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:22:28,884 | INFO | Device: mps
2025-12-23 02:22:28,884 | INFO | Backend: mlx
2025-12-23 02:22:28,884 | INFO | Quantization: DISABLED
2025-12-23 02:22:28,900 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:22:28,900 | INFO | Device: mps
2025-12-23 02:22:28,900 | INFO | Requested precision: 16 bits
  Waiting... 6s
  Waiting... 8s
2025-12-23 02:22:32,598 | INFO | Applied FP16 precision
2025-12-23 02:22:32,598 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 02:22:32,598 | INFO | Warming up MLX backend (10 iterations)...
2025-12-23 02:22:32,745 | INFO | Warmup complete
2025-12-23 02:22:32,745 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mlx', 'quantization_bits': 16, 'actual_dtype': 'float16', 'group_size': 64, 'model_type': 'cross-encoder', 'note': 'Uses PyTorch/MPS with MLX-style config'}
2025-12-23 02:22:32,746 | INFO | Experiment: 03_backend_mlx | Backend: mlx | Device: mps
2025-12-23 02:22:32,749 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 02:22:32,749 | INFO | ==================================================
2025-12-23 02:22:32,749 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 02:22:32,749 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 02:22:32,749 | INFO | ==================================================
  Waiting... 10s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 02:22:34,151 | INFO | ============================================================
2025-12-23 02:22:34,151 | INFO | Cross-Encoder Benchmark Client
2025-12-23 02:22:34,151 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 02:22:34,151 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 02:22:34,151 | INFO | ============================================================
2025-12-23 02:22:34,154 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 02:22:34,160 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 02:22:34,163 | INFO | Connected to cross-encoder server successfully
2025-12-23 02:22:34,163 | INFO | Loading experiment config: ml_inference_server/experiments/03_backend_mlx.yaml
2025-12-23 02:22:34,165 | INFO | Experiment: 03_backend_mlx
2025-12-23 02:22:34,165 | INFO | Description: MLX backend with 16-bit quantization
2025-12-23 02:22:34,165 | INFO | Running experiments with 1 batch sizes and 1 concurrency levels
2025-12-23 02:22:34,165 | INFO | Total experiments: 1
2025-12-23 02:22:34,165 | INFO | 
============================================================
2025-12-23 02:22:34,165 | INFO | Experiment 1/1: batch_size=32, concurrency=1
2025-12-23 02:22:34,165 | INFO | ============================================================
2025-12-23 02:22:34,165 | INFO | Starting benchmark: 200 requests, concurrency=1, batch_size=32
2025-12-23 02:22:37,267 | INFO | Processed 1600 queries (50 requests) | Latency: 40.74ms | QPS: 608.0
2025-12-23 02:22:39,985 | INFO | Processed 3200 queries (100 requests) | Latency: 71.63ms | QPS: 608.0
2025-12-23 02:22:39,985 | INFO | Progress: 100/200 requests
2025-12-23 02:22:42,428 | INFO | Processed 4800 queries (150 requests) | Latency: 41.20ms | QPS: 704.0
2025-12-23 02:22:44,637 | INFO | Processed 6400 queries (200 requests) | Latency: 45.27ms | QPS: 736.0
2025-12-23 02:22:44,637 | INFO | Progress: 200/200 requests
2025-12-23 02:22:44,638 | INFO | Completed: 10.47s | 6400 pairs | 611.15 pairs/s
2025-12-23 02:22:44,648 | INFO | Completed 1 experiments
2025-12-23 02:22:44,650 | INFO | Results saved to ml_inference_server/docs/experiments/03_backend_mlx_results.md

========================================================================================================================
EXPERIMENT SUMMARY (Cross-Encoder)
========================================================================================================================
Batch  Conc  Pairs    Time     Lat Avg    Lat P95    Lat P99    TP Avg       TP P99      
------------------------------------------------------------------------------------------------------------------------
32     1     6400     10.5     52.3       79.0       97.4       611.1        927.8       
========================================================================================================================

Results saved to: ml_inference_server/docs/experiments/03_backend_mlx_results.md

Capturing dashboard screenshot...
2025-12-23 02:22:47,016 | INFO | Metrics frozen - experiment stopped
2025-12-23 02:23:03,703 | INFO | Dashboard screenshot saved: ml_inference_server/docs/experiments/screenshots/03_backend_mlx_20251223_022244.png

[0;32m==========================================
Experiment completed successfully!
Results: ml_inference_server/docs/experiments/03_backend_mlx_results.md
Screenshot: ml_inference_server/docs/experiments/screenshots/03_backend_mlx_20251223_022244.png
==========================================[0m
Stopping server (PID: 33045)...
/Users/bnarang/.pyenv/versions/3.11.4/lib/python3.11/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
[0;32m==========================================
Running experiment: 05a_batch_size_mps
Config: ml_inference_server/experiments/05a_batch_size_mps.yaml
Output: ml_inference_server/docs/experiments/05a_batch_size_mps_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 33275
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 02:23:18,144 | INFO | Loading experiment config: ml_inference_server/experiments/05a_batch_size_mps.yaml
2025-12-23 02:23:18,146 | INFO | Experiment: 05a_batch_size_mps
2025-12-23 02:23:18,146 | INFO | Description: Sweep batch sizes on MPS backend
2025-12-23 02:23:18,146 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:23:18,147 | INFO | Device: mps
2025-12-23 02:23:18,147 | INFO | Backend: mps
2025-12-23 02:23:18,147 | INFO | Quantization: DISABLED
2025-12-23 02:23:18,163 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:23:18,163 | INFO | Device: mps
2025-12-23 02:23:18,163 | INFO | Precision: FP16
  Waiting... 6s
  Waiting... 8s
  Waiting... 10s
2025-12-23 02:23:23,338 | INFO | Applied FP16 precision
2025-12-23 02:23:23,338 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 02:23:23,338 | INFO | Warming up MPS backend (10 iterations)...
2025-12-23 02:23:23,489 | INFO | Warmup complete
2025-12-23 02:23:23,489 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mps', 'use_fp16': True, 'actual_dtype': 'float16', 'model_type': 'cross-encoder', 'sync_on_infer': False, 'mps_memory_allocated': 66627840, 'mps_driver_memory': 1101430784}
2025-12-23 02:23:23,489 | INFO | Experiment: 05a_batch_size_mps | Backend: mps | Device: mps
2025-12-23 02:23:23,501 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 02:23:23,502 | INFO | ==================================================
2025-12-23 02:23:23,502 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 02:23:23,502 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 02:23:23,502 | INFO | ==================================================
  Waiting... 12s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 02:23:25,508 | INFO | ============================================================
2025-12-23 02:23:25,508 | INFO | Cross-Encoder Benchmark Client
2025-12-23 02:23:25,508 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 02:23:25,508 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 02:23:25,508 | INFO | ============================================================
2025-12-23 02:23:25,511 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 02:23:25,517 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 02:23:25,520 | INFO | Connected to cross-encoder server successfully
2025-12-23 02:23:25,520 | INFO | Loading experiment config: ml_inference_server/experiments/05a_batch_size_mps.yaml
2025-12-23 02:23:25,522 | INFO | Experiment: 05a_batch_size_mps
2025-12-23 02:23:25,523 | INFO | Description: Sweep batch sizes on MPS backend
2025-12-23 02:23:25,523 | INFO | Running experiments with 9 batch sizes and 1 concurrency levels
2025-12-23 02:23:25,523 | INFO | Total experiments: 9
2025-12-23 02:23:25,523 | INFO | 
============================================================
2025-12-23 02:23:25,523 | INFO | Experiment 1/9: batch_size=8, concurrency=1
2025-12-23 02:23:25,523 | INFO | ============================================================
2025-12-23 02:23:25,523 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=8
2025-12-23 02:23:27,538 | INFO | Processed 400 queries (50 requests) | Latency: 54.02ms | QPS: 240.0
2025-12-23 02:23:29,115 | INFO | Processed 800 queries (100 requests) | Latency: 16.76ms | QPS: 256.0
2025-12-23 02:23:29,116 | INFO | Progress: 100/150 requests
2025-12-23 02:23:30,595 | INFO | Processed 1200 queries (150 requests) | Latency: 26.63ms | QPS: 280.0
2025-12-23 02:23:30,595 | INFO | Completed: 5.07s | 1200 pairs | 236.56 pairs/s
2025-12-23 02:23:30,603 | INFO | 
============================================================
2025-12-23 02:23:30,603 | INFO | Experiment 2/9: batch_size=16, concurrency=1
2025-12-23 02:23:30,603 | INFO | ============================================================
2025-12-23 02:23:30,603 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=16
2025-12-23 02:23:33,031 | INFO | Processed 2000 queries (200 requests) | Latency: 52.81ms | QPS: 352.0
2025-12-23 02:23:35,280 | INFO | Processed 2800 queries (250 requests) | Latency: 24.05ms | QPS: 352.0
2025-12-23 02:23:35,280 | INFO | Progress: 100/150 requests
2025-12-23 02:23:37,023 | INFO | Processed 3600 queries (300 requests) | Latency: 22.34ms | QPS: 512.0
2025-12-23 02:23:37,023 | INFO | Completed: 6.42s | 2400 pairs | 373.83 pairs/s
2025-12-23 02:23:37,024 | INFO | 
============================================================
2025-12-23 02:23:37,024 | INFO | Experiment 3/9: batch_size=32, concurrency=1
2025-12-23 02:23:37,024 | INFO | ============================================================
2025-12-23 02:23:37,024 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=32
2025-12-23 02:23:40,287 | INFO | Processed 5200 queries (350 requests) | Latency: 38.59ms | QPS: 544.0
2025-12-23 02:23:43,216 | INFO | Processed 6800 queries (400 requests) | Latency: 84.59ms | QPS: 576.0
2025-12-23 02:23:43,217 | INFO | Progress: 100/150 requests
2025-12-23 02:23:45,862 | INFO | Processed 8400 queries (450 requests) | Latency: 56.89ms | QPS: 608.0
2025-12-23 02:23:45,863 | INFO | Completed: 8.84s | 4800 pairs | 543.05 pairs/s
2025-12-23 02:23:45,863 | INFO | 
============================================================
2025-12-23 02:23:45,863 | INFO | Experiment 4/9: batch_size=48, concurrency=1
2025-12-23 02:23:45,863 | INFO | ============================================================
2025-12-23 02:23:45,863 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=48
2025-12-23 02:23:50,123 | INFO | Processed 10800 queries (500 requests) | Latency: 60.80ms | QPS: 672.0
2025-12-23 02:23:54,036 | INFO | Processed 13200 queries (550 requests) | Latency: 90.17ms | QPS: 624.0
2025-12-23 02:23:54,037 | INFO | Progress: 100/150 requests
2025-12-23 02:23:57,237 | INFO | Processed 15600 queries (600 requests) | Latency: 53.51ms | QPS: 768.0
2025-12-23 02:23:57,237 | INFO | Completed: 11.37s | 7200 pairs | 633.05 pairs/s
2025-12-23 02:23:57,238 | INFO | 
============================================================
2025-12-23 02:23:57,238 | INFO | Experiment 5/9: batch_size=64, concurrency=1
2025-12-23 02:23:57,238 | INFO | ============================================================
2025-12-23 02:23:57,238 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=64
2025-12-23 02:24:02,542 | INFO | Processed 18800 queries (650 requests) | Latency: 130.97ms | QPS: 640.0
2025-12-23 02:24:07,429 | INFO | Processed 22000 queries (700 requests) | Latency: 92.71ms | QPS: 832.0
2025-12-23 02:24:07,430 | INFO | Progress: 100/150 requests
2025-12-23 02:24:11,845 | INFO | Processed 25200 queries (750 requests) | Latency: 77.91ms | QPS: 832.0
2025-12-23 02:24:11,845 | INFO | Completed: 14.61s | 9600 pairs | 657.19 pairs/s
2025-12-23 02:24:11,846 | INFO | 
============================================================
2025-12-23 02:24:11,846 | INFO | Experiment 6/9: batch_size=96, concurrency=1
2025-12-23 02:24:11,846 | INFO | ============================================================
2025-12-23 02:24:11,846 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=96
2025-12-23 02:24:19,550 | INFO | Processed 30000 queries (800 requests) | Latency: 138.06ms | QPS: 768.0
2025-12-23 02:24:25,741 | INFO | Processed 34800 queries (850 requests) | Latency: 113.41ms | QPS: 864.0
2025-12-23 02:24:25,742 | INFO | Progress: 100/150 requests
2025-12-23 02:24:32,152 | INFO | Processed 39600 queries (900 requests) | Latency: 108.55ms | QPS: 864.0
2025-12-23 02:24:32,153 | INFO | Completed: 20.31s | 14400 pairs | 709.13 pairs/s
2025-12-23 02:24:32,153 | INFO | 
============================================================
2025-12-23 02:24:32,153 | INFO | Experiment 7/9: batch_size=128, concurrency=1
2025-12-23 02:24:32,153 | INFO | ============================================================
2025-12-23 02:24:32,153 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=128
2025-12-23 02:24:41,505 | INFO | Processed 46000 queries (950 requests) | Latency: 170.48ms | QPS: 896.0
2025-12-23 02:24:49,866 | INFO | Processed 52400 queries (1000 requests) | Latency: 151.08ms | QPS: 768.0
2025-12-23 02:24:49,867 | INFO | Progress: 100/150 requests
2025-12-23 02:24:58,112 | INFO | Processed 58800 queries (1050 requests) | Latency: 149.25ms | QPS: 896.0
2025-12-23 02:24:58,112 | INFO | Completed: 25.96s | 19200 pairs | 739.63 pairs/s
2025-12-23 02:24:58,113 | INFO | 
============================================================
2025-12-23 02:24:58,113 | INFO | Experiment 8/9: batch_size=192, concurrency=1
2025-12-23 02:24:58,113 | INFO | ============================================================
2025-12-23 02:24:58,113 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=192
2025-12-23 02:25:12,812 | INFO | Processed 68400 queries (1100 requests) | Latency: 210.32ms | QPS: 960.0
2025-12-23 02:25:25,501 | INFO | Processed 78000 queries (1150 requests) | Latency: 254.59ms | QPS: 960.0
2025-12-23 02:25:25,501 | INFO | Progress: 100/150 requests
2025-12-23 02:25:39,385 | INFO | Processed 87600 queries (1200 requests) | Latency: 241.25ms | QPS: 768.0
2025-12-23 02:25:39,387 | INFO | Completed: 41.27s | 28800 pairs | 697.79 pairs/s
2025-12-23 02:25:39,392 | INFO | 
============================================================
2025-12-23 02:25:39,392 | INFO | Experiment 9/9: batch_size=256, concurrency=1
2025-12-23 02:25:39,392 | INFO | ============================================================
2025-12-23 02:25:39,392 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=256
2025-12-23 02:25:57,677 | INFO | Processed 100400 queries (1250 requests) | Latency: 342.29ms | QPS: 768.0
2025-12-23 02:26:14,651 | INFO | Processed 113200 queries (1300 requests) | Latency: 330.48ms | QPS: 1024.0
2025-12-23 02:26:14,652 | INFO | Progress: 100/150 requests
2025-12-23 02:26:31,290 | INFO | Processed 126000 queries (1350 requests) | Latency: 336.69ms | QPS: 1024.0
2025-12-23 02:26:31,290 | INFO | Completed: 51.90s | 38400 pairs | 739.91 pairs/s
2025-12-23 02:26:31,291 | INFO | Completed 9 experiments
2025-12-23 02:26:31,294 | INFO | Results saved to ml_inference_server/docs/experiments/05a_batch_size_mps_results.md

========================================================================================================================
EXPERIMENT SUMMARY (Cross-Encoder)
========================================================================================================================
Batch  Conc  Pairs    Time     Lat Avg    Lat P95    Lat P99    TP Avg       TP P99      
------------------------------------------------------------------------------------------------------------------------
8      1     1200     5.1      33.8       57.4       62.3       236.6        524.7       
16     1     2400     6.4      42.8       70.3       76.5       373.8        731.3       
32     1     4800     8.8      58.9       89.3       123.5      543.1        926.1       
48     1     7200     11.4     75.8       108.0      171.4      633.0        900.1       
64     1     9600     14.6     97.4       132.5      194.5      657.2        907.0       
96     1     14400    20.3     135.3      165.6      231.0      709.1        935.5       
128    1     19200    26.0     173.0      215.9      283.4      739.6        945.7       
192    1     28800    41.3     275.1      409.3      486.6      697.8        906.6       
256    1     38400    51.9     345.9      417.7      506.8      739.9        921.2       
========================================================================================================================

Results saved to: ml_inference_server/docs/experiments/05a_batch_size_mps_results.md

Capturing dashboard screenshot...
2025-12-23 02:26:33,575 | INFO | Metrics frozen - experiment stopped
2025-12-23 02:27:03,308 | ERROR | Failed to capture screenshot: Timeout 30000ms exceeded.
2025-12-23 02:27:03,308 | INFO | Created dashboard link: ml_inference_server/docs/experiments/screenshots/05a_batch_size_mps_20251223_022631.html
[1;33mNote: Screenshot capture requires playwright. Install with:[0m
  uv pip install playwright && playwright install chromium

[0;32m==========================================
Experiment completed successfully!
Results: ml_inference_server/docs/experiments/05a_batch_size_mps_results.md
==========================================[0m
Stopping server (PID: 33275)...
/Users/bnarang/.pyenv/versions/3.11.4/lib/python3.11/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
[0;32m==========================================
Running experiment: 06a_concurrency_mps
Config: ml_inference_server/experiments/06a_concurrency_mps.yaml
Output: ml_inference_server/docs/experiments/06a_concurrency_mps_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 37581
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 02:49:26,390 | INFO | Loading experiment config: ml_inference_server/experiments/06a_concurrency_mps.yaml
2025-12-23 02:49:26,392 | INFO | Experiment: 06a_concurrency_mps
2025-12-23 02:49:26,392 | INFO | Description: Sweep concurrency levels on MPS backend
2025-12-23 02:49:26,392 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:49:26,392 | INFO | Device: mps
2025-12-23 02:49:26,392 | INFO | Backend: mps
2025-12-23 02:49:26,392 | INFO | Quantization: DISABLED
2025-12-23 02:49:26,408 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:49:26,408 | INFO | Device: mps
2025-12-23 02:49:26,408 | INFO | Precision: FP16
  Waiting... 6s
  Waiting... 8s
  Waiting... 10s
2025-12-23 02:49:31,139 | INFO | Applied FP16 precision
2025-12-23 02:49:31,139 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 02:49:31,139 | INFO | Warming up MPS backend (10 iterations)...
2025-12-23 02:49:31,307 | INFO | Warmup complete
2025-12-23 02:49:31,308 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mps', 'use_fp16': True, 'actual_dtype': 'float16', 'model_type': 'cross-encoder', 'sync_on_infer': False, 'mps_memory_allocated': 66627840, 'mps_driver_memory': 1101430784}
2025-12-23 02:49:31,308 | INFO | Experiment: 06a_concurrency_mps | Backend: mps | Device: mps
2025-12-23 02:49:31,312 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 02:49:31,312 | INFO | ==================================================
2025-12-23 02:49:31,312 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 02:49:31,312 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 02:49:31,312 | INFO | ==================================================
  Waiting... 12s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 02:49:33,030 | INFO | ============================================================
2025-12-23 02:49:33,030 | INFO | Cross-Encoder Benchmark Client
2025-12-23 02:49:33,030 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 02:49:33,030 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 02:49:33,030 | INFO | ============================================================
2025-12-23 02:49:33,033 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 02:49:33,039 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 02:49:33,042 | INFO | Connected to cross-encoder server successfully
2025-12-23 02:49:33,042 | INFO | Loading experiment config: ml_inference_server/experiments/06a_concurrency_mps.yaml
2025-12-23 02:49:33,044 | INFO | Experiment: 06a_concurrency_mps
2025-12-23 02:49:33,044 | INFO | Description: Sweep concurrency levels on MPS backend
2025-12-23 02:49:33,044 | INFO | Running experiments with 1 batch sizes and 7 concurrency levels
2025-12-23 02:49:33,044 | INFO | Total experiments: 7
2025-12-23 02:49:33,044 | INFO | 
============================================================
2025-12-23 02:49:33,044 | INFO | Experiment 1/7: batch_size=96, concurrency=1
2025-12-23 02:49:33,044 | INFO | ============================================================
2025-12-23 02:49:33,044 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=96
2025-12-23 02:49:40,575 | INFO | Processed 4800 queries (50 requests) | Latency: 119.43ms | QPS: 864.0
2025-12-23 02:49:46,825 | INFO | Processed 9600 queries (100 requests) | Latency: 110.51ms | QPS: 864.0
2025-12-23 02:49:46,825 | INFO | Progress: 100/150 requests
2025-12-23 02:49:53,136 | INFO | Processed 14400 queries (150 requests) | Latency: 108.31ms | QPS: 864.0
2025-12-23 02:49:53,137 | INFO | Completed: 20.09s | 14400 pairs | 716.69 pairs/s
2025-12-23 02:49:53,147 | INFO | 
============================================================
2025-12-23 02:49:53,147 | INFO | Experiment 2/7: batch_size=96, concurrency=2
2025-12-23 02:49:53,147 | INFO | ============================================================
2025-12-23 02:49:53,147 | INFO | Starting benchmark: 150 requests, concurrency=2, batch_size=96
2025-12-23 02:49:54,239 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - Socket closed
2025-12-23 02:49:54,239 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - Socket closed
2025-12-23 02:49:54,240 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,240 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,240 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,240 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,241 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,241 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,241 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,241 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,242 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,242 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,242 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,242 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,242 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,243 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,243 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,243 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,243 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,243 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,244 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,244 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,244 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,244 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,244 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,245 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,245 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,245 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,245 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,245 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,246 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,246 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,246 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,246 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,247 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,247 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,247 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,247 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,247 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,248 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,248 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,248 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,248 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,248 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,249 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,249 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,249 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,250 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,250 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,250 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,250 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,250 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,251 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,251 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,251 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,251 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,251 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,252 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,252 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,252 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,252 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,253 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,253 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,253 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,253 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,253 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,254 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,254 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,254 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,254 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,255 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,255 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,255 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,256 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,256 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,256 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,256 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,257 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,257 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,257 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,257 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
/Users/bnarang/.pyenv/versions/3.11.4/lib/python3.11/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
2025-12-23 02:49:54,257 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,258 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,258 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,258 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,258 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,259 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,260 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,260 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,260 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,260 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,261 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,261 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,261 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,262 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,262 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,262 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,263 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,263 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,263 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,263 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,263 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,264 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,264 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,264 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,265 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,265 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,265 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,265 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,266 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,266 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,267 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,267 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,267 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,267 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,268 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,268 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,268 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,268 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,269 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,269 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,269 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,269 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,270 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,270 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,270 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,270 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,271 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,271 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,271 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,271 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,271 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,272 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,272 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,273 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,273 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,273 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,273 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,274 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,274 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,274 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,274 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,274 | ERROR | Experiment 2/7 failed: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "Socket closed"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"Socket closed"}"
>
2025-12-23 02:49:54,274 | ERROR | Continuing with next experiment...
2025-12-23 02:49:54,274 | INFO | 
============================================================
2025-12-23 02:49:54,274 | INFO | Experiment 3/7: batch_size=96, concurrency=3
2025-12-23 02:49:54,274 | INFO | ============================================================
2025-12-23 02:49:54,274 | INFO | Starting benchmark: 150 requests, concurrency=3, batch_size=96
2025-12-23 02:49:54,275 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,275 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,275 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,276 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,276 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,276 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,277 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,277 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,277 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,278 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,278 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,278 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,279 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,279 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,280 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,280 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,280 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,280 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,281 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,291 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,291 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,291 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,292 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,292 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,292 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,292 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,293 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,293 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,293 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,293 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,293 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,294 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,294 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,294 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,294 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,295 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,295 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,295 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,295 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,295 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,296 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,296 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,296 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,296 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,297 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,297 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,297 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,297 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,297 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,298 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,298 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,298 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,298 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,299 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,299 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,299 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,299 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,300 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,300 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,300 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,300 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,300 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,301 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,301 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,301 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,301 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,302 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,302 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,302 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,302 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,302 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,303 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,303 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,303 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,303 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,303 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,303 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,304 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,304 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,304 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,304 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,304 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,305 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,305 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,305 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,305 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,306 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,306 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,306 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,306 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,306 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,307 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,307 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,307 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,307 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,307 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,307 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,308 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,308 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,308 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,308 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,308 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,308 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,309 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,309 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,309 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,309 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,309 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,309 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,310 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,310 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,310 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,310 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,310 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,310 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,311 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,311 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,311 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,311 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,311 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,312 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,312 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,312 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,312 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,312 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,313 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,313 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,313 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,313 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,313 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,314 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,314 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,314 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,314 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,314 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,314 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,315 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,315 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,315 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,315 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,315 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,315 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,316 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,316 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,316 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,316 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,316 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,317 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,317 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,317 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,317 | ERROR | Experiment 3/7 failed: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>
2025-12-23 02:49:54,317 | ERROR | Continuing with next experiment...
2025-12-23 02:49:54,317 | INFO | 
============================================================
2025-12-23 02:49:54,317 | INFO | Experiment 4/7: batch_size=96, concurrency=4
2025-12-23 02:49:54,317 | INFO | ============================================================
2025-12-23 02:49:54,317 | INFO | Starting benchmark: 150 requests, concurrency=4, batch_size=96
2025-12-23 02:49:54,318 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,318 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,319 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,319 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,320 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,320 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,320 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,320 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,320 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,321 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,321 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,321 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,321 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,322 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,322 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,322 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,322 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,322 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,322 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,323 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,323 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,323 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,323 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,323 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,324 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,324 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,324 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,324 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,324 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,325 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,325 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,325 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,325 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,325 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,326 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,326 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,326 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,326 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,327 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,327 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,327 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,328 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,328 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,328 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,328 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,328 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,329 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,329 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,329 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,330 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,330 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,330 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,330 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,330 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,331 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,331 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,331 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,331 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,331 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,332 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,332 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,332 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,332 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,332 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,333 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,333 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,333 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,333 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,333 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,334 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,334 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,334 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,334 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,334 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,335 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,335 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,335 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,336 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,336 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,336 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,336 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,336 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,336 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,337 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,337 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,337 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,337 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,338 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,338 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,338 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,338 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,339 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,339 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,339 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,339 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,339 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,340 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,340 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,340 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,340 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,341 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,341 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,341 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,341 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,341 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,342 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,342 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,342 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,343 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,343 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,343 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,343 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,343 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,344 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,344 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,344 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,344 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,344 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,345 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,345 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,345 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,345 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,345 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,346 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,346 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,346 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,346 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,346 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,347 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,347 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,347 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,347 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,347 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,348 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,348 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,348 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,348 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,348 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,349 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,349 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,349 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,349 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,350 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,350 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,350 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,350 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,350 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,351 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,351 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,351 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,351 | ERROR | Experiment 4/7 failed: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)", grpc_status:14}"
>
2025-12-23 02:49:54,351 | ERROR | Continuing with next experiment...
2025-12-23 02:49:54,351 | INFO | 
============================================================
2025-12-23 02:49:54,351 | INFO | Experiment 5/7: batch_size=96, concurrency=6
2025-12-23 02:49:54,351 | INFO | ============================================================
2025-12-23 02:49:54,351 | INFO | Starting benchmark: 150 requests, concurrency=6, batch_size=96
2025-12-23 02:49:54,351 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,351 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,352 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,352 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,352 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,353 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,353 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,354 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,355 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,355 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,355 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,356 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,356 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,356 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,356 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,356 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,357 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,357 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,357 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,357 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,357 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,358 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,358 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,358 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,358 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,359 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,359 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,359 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,359 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,359 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,359 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,360 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,360 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,360 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,360 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,361 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,361 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,361 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,361 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,361 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,362 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,362 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,362 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,362 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,362 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,363 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,363 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,363 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,363 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,363 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,363 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,364 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,364 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,364 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,364 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,364 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,364 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,364 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,364 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,364 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,365 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,365 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,365 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,366 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,367 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,367 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,367 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,367 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,368 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,368 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,368 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,368 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,368 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,369 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,369 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,369 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,369 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,369 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,370 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,370 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,370 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,370 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,371 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,371 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,371 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,371 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,371 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,372 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,372 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,372 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,372 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,372 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,373 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,373 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,373 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,373 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,373 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,374 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,374 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,374 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,374 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,375 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,375 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,375 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,375 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,375 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,375 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,376 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,376 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,376 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,376 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,376 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,377 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,377 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,377 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,377 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,377 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,378 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,378 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,378 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,378 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,378 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,379 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,379 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,379 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,379 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,380 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,380 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,380 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,380 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,380 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,381 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,381 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,381 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,381 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,381 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,382 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,382 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,382 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,382 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,383 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,383 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,383 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,383 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,383 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,384 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,384 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,384 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,384 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,384 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,384 | ERROR | Experiment 5/7 failed: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>
2025-12-23 02:49:54,384 | ERROR | Continuing with next experiment...
2025-12-23 02:49:54,384 | INFO | 
============================================================
2025-12-23 02:49:54,384 | INFO | Experiment 6/7: batch_size=96, concurrency=8
2025-12-23 02:49:54,384 | INFO | ============================================================
2025-12-23 02:49:54,384 | INFO | Starting benchmark: 150 requests, concurrency=8, batch_size=96
2025-12-23 02:49:54,385 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,385 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,385 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,385 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,386 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,386 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,386 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,386 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,386 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,387 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,387 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,387 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,387 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,387 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,387 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,388 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,388 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,388 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,389 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,389 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,391 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,391 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,391 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,391 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,392 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,392 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,392 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,393 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,393 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,393 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,393 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,393 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,394 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,394 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,394 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,394 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,395 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,395 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,395 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,395 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,395 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,396 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,396 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,396 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,396 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,396 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,397 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,397 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,397 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,397 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,397 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,398 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,398 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,398 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,398 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,398 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,398 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,399 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,399 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,399 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,399 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,399 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,400 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,400 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,400 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,400 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,400 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,401 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,401 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,401 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,401 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,401 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,402 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,402 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,402 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,402 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,402 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,402 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,403 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,403 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,403 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,403 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,404 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,404 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,404 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,405 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,405 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,405 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,405 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,405 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,406 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,406 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,406 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,406 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,407 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,407 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,407 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,407 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,407 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,408 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,408 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,408 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,408 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,408 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,409 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,409 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,409 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,409 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,409 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,410 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,410 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,410 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,410 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,410 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,410 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,411 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,411 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,411 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,411 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,412 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,412 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,412 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,412 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,412 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,413 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,413 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,413 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,413 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,413 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,414 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,414 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,414 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,414 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,414 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,415 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,416 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,416 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,416 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,416 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,416 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,416 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,417 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,417 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,417 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,417 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,417 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,417 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,417 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,417 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,417 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,418 | ERROR | Experiment 6/7 failed: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"}"
>
2025-12-23 02:49:54,418 | ERROR | Continuing with next experiment...
2025-12-23 02:49:54,418 | INFO | 
============================================================
2025-12-23 02:49:54,418 | INFO | Experiment 7/7: batch_size=96, concurrency=12
2025-12-23 02:49:54,418 | INFO | ============================================================
2025-12-23 02:49:54,418 | INFO | Starting benchmark: 150 requests, concurrency=12, batch_size=96
2025-12-23 02:49:54,418 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,419 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,420 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,420 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,420 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,421 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,422 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,422 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,422 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,423 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,423 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,424 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,424 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,424 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,424 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,425 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,425 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,425 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,425 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,425 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,426 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,426 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,426 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,426 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,426 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,427 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,427 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,427 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,427 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,427 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,428 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,428 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,428 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,428 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,428 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,428 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,429 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,429 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,429 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,430 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,430 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,430 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,461 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,461 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,461 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,462 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,462 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,462 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,462 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,462 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,463 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,463 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,463 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,463 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,463 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,463 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,464 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,464 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,464 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,464 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,465 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,465 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,465 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,465 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,465 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,466 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,466 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,466 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,466 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,466 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,467 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,467 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,467 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,467 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,467 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,468 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,468 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,468 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,468 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,468 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,469 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,469 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,469 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,469 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,470 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,470 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,470 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,470 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,470 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,471 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,471 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,471 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,471 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,471 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,471 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,472 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,472 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,472 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,472 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,473 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,473 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,473 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,473 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,473 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,474 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,474 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,474 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,475 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,475 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,475 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,475 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,476 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,476 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,476 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,476 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,476 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,477 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,477 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,477 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,477 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,477 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,477 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,478 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,478 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,478 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,478 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,478 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,479 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,479 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,479 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,479 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,479 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,480 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,480 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,480 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,480 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,480 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,481 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,481 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,481 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,481 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,481 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,481 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,481 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,481 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,481 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,481 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,482 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,482 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,482 | ERROR | gRPC error during inference: StatusCode.UNAVAILABLE - failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)
2025-12-23 02:49:54,482 | ERROR | Experiment 7/7 failed: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)"
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"failed to connect to all addresses; last error: UNKNOWN: ipv4:127.0.0.1:50051: Failed to connect to remote host: connect: Connection refused (61)", grpc_status:14}"
>
2025-12-23 02:49:54,482 | ERROR | Continuing with next experiment...
2025-12-23 02:49:54,482 | INFO | Completed 7 experiments
2025-12-23 02:49:54,484 | INFO | Results saved to ml_inference_server/docs/experiments/06a_concurrency_mps_results.md

========================================================================================================================
EXPERIMENT SUMMARY (Cross-Encoder)
========================================================================================================================
Batch  Conc  Pairs    Time     Lat Avg    Lat P95    Lat P99    TP Avg       TP P99      
------------------------------------------------------------------------------------------------------------------------
96     1     14400    20.1     133.9      171.8      198.5      716.7        919.9       
96     2     FAILED   N/A      N/A        N/A        N/A        N/A          N/A         
96     3     FAILED   N/A      N/A        N/A        N/A        N/A          N/A         
96     4     FAILED   N/A      N/A        N/A        N/A        N/A          N/A         
96     6     FAILED   N/A      N/A        N/A        N/A        N/A          N/A         
96     8     FAILED   N/A      N/A        N/A        N/A        N/A          N/A         
96     12    FAILED   N/A      N/A        N/A        N/A        N/A          N/A         
========================================================================================================================

Results saved to: ml_inference_server/docs/experiments/06a_concurrency_mps_results.md
./run_experiment.sh: line 151: 37581 Segmentation fault: 11  python ml_inference_server/main.py --experiment "$EXPERIMENT_CONFIG"

Capturing dashboard screenshot...
2025-12-23 02:49:55,741 | ERROR | Failed to capture screenshot: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8080/
Call log:
  - navigating to "http://localhost:8080/", waiting until "load"

2025-12-23 02:49:55,741 | INFO | Created dashboard link: ml_inference_server/docs/experiments/screenshots/06a_concurrency_mps_20251223_024954.html
[1;33mNote: Screenshot capture requires playwright. Install with:[0m
  uv pip install playwright && playwright install chromium

[0;32m==========================================
Experiment completed successfully!
Results: ml_inference_server/docs/experiments/06a_concurrency_mps_results.md
==========================================[0m
