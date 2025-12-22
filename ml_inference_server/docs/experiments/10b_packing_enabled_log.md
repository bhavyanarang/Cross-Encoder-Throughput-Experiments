[0;32m==========================================
Running experiment: 10b_packing_enabled
Config: ml_inference_server/experiments/10b_packing_enabled.yaml
Output: ml_inference_server/docs/experiments/10b_packing_enabled_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 50068
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 03:34:22,862 | INFO | Loading experiment config: ml_inference_server/experiments/10b_packing_enabled.yaml
2025-12-23 03:34:22,867 | INFO | Experiment: 10b_packing_enabled
2025-12-23 03:34:22,867 | INFO | Description: Sequential packing (no padding, block-diagonal attention)
2025-12-23 03:34:22,867 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 03:34:22,867 | INFO | Device: mps
2025-12-23 03:34:22,867 | INFO | Backend: mps
2025-12-23 03:34:22,867 | INFO | Quantization: DISABLED
2025-12-23 03:34:22,883 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 03:34:22,883 | INFO | Device: mps
2025-12-23 03:34:22,883 | INFO | Precision: FP16
  Waiting... 6s
  Waiting... 8s
  Waiting... 10s
  Waiting... 12s
  Waiting... 14s
2025-12-23 03:34:31,762 | INFO | Applied FP16 precision
2025-12-23 03:34:31,762 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 03:34:31,762 | INFO | Warming up MPS backend (10 iterations)...
2025-12-23 03:34:31,912 | INFO | Warmup complete
2025-12-23 03:34:31,912 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mps', 'use_fp16': True, 'actual_dtype': 'float16', 'model_type': 'cross-encoder', 'sync_on_infer': False, 'mps_memory_allocated': 66627840, 'mps_driver_memory': 1101430784}
2025-12-23 03:34:31,912 | INFO | Experiment: 10b_packing_enabled | Backend: mps | Device: mps
2025-12-23 03:34:31,912 | INFO | Sequence packing: ENABLED (no padding, block-diagonal attention)
2025-12-23 03:34:31,912 | INFO | Sequential packing ENABLED - no padding, block-diagonal attention
2025-12-23 03:34:31,916 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 03:34:31,916 | INFO | ==================================================
2025-12-23 03:34:31,916 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 03:34:31,916 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 03:34:31,916 | INFO | ==================================================
  Waiting... 16s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 03:34:34,836 | INFO | ============================================================
2025-12-23 03:34:34,836 | INFO | Cross-Encoder Benchmark Client
2025-12-23 03:34:34,836 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 03:34:34,836 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 03:34:34,836 | INFO | ============================================================
2025-12-23 03:34:34,836 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 03:34:34,842 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 03:34:34,845 | INFO | Connected to cross-encoder server successfully
2025-12-23 03:34:34,845 | INFO | Loading experiment config: ml_inference_server/experiments/10b_packing_enabled.yaml
2025-12-23 03:34:34,847 | INFO | Experiment: 10b_packing_enabled
2025-12-23 03:34:34,847 | INFO | Description: Sequential packing (no padding, block-diagonal attention)
2025-12-23 03:34:34,847 | INFO | Running experiments with 3 batch sizes and 1 concurrency levels
2025-12-23 03:34:34,847 | INFO | Total experiments: 3
2025-12-23 03:34:34,847 | INFO | 
============================================================
2025-12-23 03:34:34,847 | INFO | Experiment 1/3: batch_size=32, concurrency=1
2025-12-23 03:34:34,847 | INFO | ============================================================
2025-12-23 03:34:34,847 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=32
2025-12-23 03:34:35,342 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:35,595 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:35,990 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:36,187 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:36,506 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:36,692 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:36,886 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:37,297 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:37,684 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:37,979 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:38,338 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:39,020 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:39,207 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:39,494 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:39,800 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:40,024 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:40,197 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:40,377 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:40,528 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:40,724 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:40,916 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:41,072 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:41,225 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:41,372 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:41,540 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:41,725 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:41,913 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:42,072 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:42,325 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:42,544 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:43,080 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:43,272 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:43,445 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:43,722 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:43,887 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:44,079 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:44,231 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:44,346 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:44,525 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:44,699 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:44,858 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:45,126 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:45,327 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:45,479 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:45,673 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:45,861 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:46,124 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:46,441 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:46,670 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:46,853 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:47,008 | INFO | Processed 1600 queries (50 requests) | Latency: 193.82ms | QPS: 160.0
2025-12-23 03:34:47,053 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:47,218 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:47,374 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:47,574 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:47,840 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:48,002 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:48,217 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:48,364 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:48,535 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:48,705 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:48,899 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:49,068 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:49,388 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:49,585 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:49,760 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:49,964 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:50,176 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:50,375 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:50,541 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:50,719 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:50,878 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:51,091 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:51,257 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:51,436 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:51,568 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:51,730 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:51,872 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:52,014 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:52,205 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:52,385 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:52,617 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:52,765 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:53,120 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:53,387 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:53,545 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:53,693 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:53,884 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:54,083 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:54,249 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:54,398 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:54,563 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:54,714 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:54,890 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:55,048 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:55,219 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:55,427 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:55,585 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:55,756 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:56,035 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:56,242 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:56,609 | INFO | Processed 3200 queries (100 requests) | Latency: 414.19ms | QPS: 128.0
2025-12-23 03:34:56,610 | INFO | Progress: 100/150 requests
2025-12-23 03:34:56,660 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:56,993 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:57,165 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:57,339 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:57,512 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:57,661 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:57,863 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:58,223 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:58,441 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:58,578 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:58,769 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:59,018 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:59,185 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:59,352 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:59,517 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:59,652 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:34:59,824 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:00,466 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:00,648 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:00,811 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:00,975 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:01,101 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:01,312 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:01,469 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:01,642 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:01,802 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:01,953 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:02,109 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:02,314 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:02,525 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:02,692 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:02,806 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:02,970 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:03,090 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:03,247 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:03,420 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:03,572 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:03,739 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:03,884 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:04,050 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:04,275 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:04,414 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:04,563 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:04,750 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:04,912 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:05,098 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:05,305 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:05,456 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:05,783 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:05,913 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:06,037 | INFO | Processed 4800 queries (150 requests) | Latency: 143.42ms | QPS: 192.0
2025-12-23 03:35:06,037 | INFO | Completed: 31.19s | 4800 pairs | 153.90 pairs/s
2025-12-23 03:35:06,048 | INFO | 
============================================================
2025-12-23 03:35:06,048 | INFO | Experiment 2/3: batch_size=64, concurrency=1
2025-12-23 03:35:06,048 | INFO | ============================================================
2025-12-23 03:35:06,048 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=64
2025-12-23 03:35:06,109 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:07,990 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:08,851 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:09,630 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:10,364 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:11,067 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:12,115 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:12,611 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:13,151 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:13,705 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:14,231 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:14,960 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:15,814 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:16,559 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:17,553 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:18,480 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:19,033 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:19,526 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:20,353 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:21,120 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:22,225 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:23,047 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:23,985 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:24,842 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:25,911 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:26,705 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:27,596 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:28,579 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:29,370 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:30,107 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:31,166 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:31,989 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:33,035 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:34,120 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:34,983 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:35,708 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:37,280 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:38,055 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:38,981 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:40,320 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:41,115 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:41,710 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:42,521 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:43,348 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:44,570 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:45,280 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:45,862 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:47,105 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:47,908 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:48,652 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:49,451 | INFO | Processed 8000 queries (200 requests) | Latency: 855.55ms | QPS: 128.0
2025-12-23 03:35:49,631 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:50,475 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:51,119 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:51,644 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:52,838 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:53,580 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:54,160 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:54,959 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:55,828 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:56,596 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:57,193 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:58,090 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:58,858 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:35:59,370 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:00,310 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:01,198 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:01,963 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:02,952 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:03,664 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:04,466 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:05,197 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:05,763 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:06,524 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:07,955 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
2025-12-23 03:36:08,890 | WARNING | Packed inference failed (too many indices for tensor of dimension 2), falling back to padded
