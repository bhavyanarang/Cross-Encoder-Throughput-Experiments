[0;32m==========================================
Running experiment: 06a_concurrency_mps
Config: ml_inference_server/experiments/06a_concurrency_mps.yaml
Output: ml_inference_server/docs/experiments/06a_concurrency_mps_results.md
==========================================[0m

Press Ctrl+C to interrupt (results will be saved if possible)

Starting server...
Server PID: 39794
Waiting for server to initialize (up to 60s)...
  Waiting... 2s
  Waiting... 4s
2025-12-23 02:56:54,576 | INFO | Loading experiment config: ml_inference_server/experiments/06a_concurrency_mps.yaml
2025-12-23 02:56:54,579 | INFO | Experiment: 06a_concurrency_mps
2025-12-23 02:56:54,579 | INFO | Description: Sweep concurrency levels on MPS backend
2025-12-23 02:56:54,579 | INFO | Loading model: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:56:54,579 | INFO | Device: mps
2025-12-23 02:56:54,579 | INFO | Backend: mps
2025-12-23 02:56:54,579 | INFO | Quantization: DISABLED
2025-12-23 02:56:54,598 | INFO | Loading cross-encoder: cross-encoder/ms-marco-MiniLM-L-6-v2
2025-12-23 02:56:54,598 | INFO | Device: mps
2025-12-23 02:56:54,598 | INFO | Precision: FP16
  Waiting... 6s
  Waiting... 8s
2025-12-23 02:56:58,468 | INFO | Applied FP16 precision
2025-12-23 02:56:58,468 | INFO | Loaded cross-encoder/ms-marco-MiniLM-L-6-v2 on mps (FLOAT16)
2025-12-23 02:56:58,468 | INFO | Warming up MPS backend (10 iterations)...
2025-12-23 02:56:58,617 | INFO | Warmup complete
2025-12-23 02:56:58,617 | INFO | Model info: {'model_name': 'cross-encoder/ms-marco-MiniLM-L-6-v2', 'device': 'mps', 'backend': 'mps', 'use_fp16': True, 'actual_dtype': 'float16', 'model_type': 'cross-encoder', 'sync_on_infer': False, 'mps_memory_allocated': 66627840, 'mps_driver_memory': 1101430784}
2025-12-23 02:56:58,617 | INFO | Experiment: 06a_concurrency_mps | Backend: mps | Device: mps
2025-12-23 02:56:58,623 | INFO | Metrics dashboard: http://localhost:8080
2025-12-23 02:56:58,623 | INFO | ==================================================
2025-12-23 02:56:58,623 | INFO | Monitor metrics at: http://localhost:8080
2025-12-23 02:56:58,623 | INFO | JSON endpoint: http://localhost:8080/metrics
2025-12-23 02:56:58,623 | INFO | ==================================================
  Waiting... 10s
[0;32mServer is ready![0m

Running benchmark...
2025-12-23 02:56:59,446 | INFO | ============================================================
2025-12-23 02:56:59,446 | INFO | Cross-Encoder Benchmark Client
2025-12-23 02:56:59,447 | INFO | Monitor live metrics at: http://localhost:8080
2025-12-23 02:56:59,447 | INFO | Press Ctrl+C to interrupt (partial results will be saved)
2025-12-23 02:56:59,447 | INFO | ============================================================
2025-12-23 02:56:59,449 | INFO | Loading cached pairs from /Users/bnarang/Desktop/ML_dynamic batching/ml_inference_server/.cache/msmarco_pairs_5000.json
2025-12-23 02:56:59,454 | INFO | Loaded 5000 cached query-passage pairs from MS MARCO
2025-12-23 02:56:59,458 | INFO | Connected to cross-encoder server successfully
2025-12-23 02:56:59,458 | INFO | Loading experiment config: ml_inference_server/experiments/06a_concurrency_mps.yaml
2025-12-23 02:56:59,460 | INFO | Experiment: 06a_concurrency_mps
2025-12-23 02:56:59,460 | INFO | Description: Sweep concurrency levels on MPS backend
2025-12-23 02:56:59,460 | INFO | Running experiments with 1 batch sizes and 7 concurrency levels
2025-12-23 02:56:59,460 | INFO | Total experiments: 7
2025-12-23 02:56:59,460 | INFO |
============================================================
2025-12-23 02:56:59,460 | INFO | Experiment 1/7: batch_size=96, concurrency=1
2025-12-23 02:56:59,460 | INFO | ============================================================
2025-12-23 02:56:59,460 | INFO | Starting benchmark: 150 requests, concurrency=1, batch_size=96
2025-12-23 02:57:07,203 | INFO | Processed 4800 queries (50 requests) | Latency: 127.27ms | QPS: 768.0
2025-12-23 02:57:13,456 | INFO | Processed 9600 queries (100 requests) | Latency: 118.02ms | QPS: 864.0
2025-12-23 02:57:13,457 | INFO | Progress: 100/150 requests
2025-12-23 02:57:19,648 | INFO | Processed 14400 queries (150 requests) | Latency: 107.33ms | QPS: 864.0
2025-12-23 02:57:19,648 | INFO | Completed: 20.19s | 14400 pairs | 713.29 pairs/s
2025-12-23 02:57:19,662 | INFO |
============================================================
2025-12-23 02:57:19,663 | INFO | Experiment 2/7: batch_size=96, concurrency=2
2025-12-23 02:57:19,663 | INFO | ============================================================
2025-12-23 02:57:19,663 | INFO | Starting benchmark: 150 requests, concurrency=2, batch_size=96
2025-12-23 02:57:25,839 | INFO | Processed 19200 queries (200 requests) | Latency: 107.55ms | QPS: 864.0
2025-12-23 02:57:32,089 | INFO | Processed 24000 queries (250 requests) | Latency: 108.83ms | QPS: 864.0
2025-12-23 02:57:32,092 | INFO | Progress: 100/150 requests
2025-12-23 02:57:38,381 | INFO | Processed 28800 queries (300 requests) | Latency: 108.83ms | QPS: 864.0
2025-12-23 02:57:38,381 | INFO | Completed: 18.72s | 14400 pairs | 769.29 pairs/s
2025-12-23 02:57:38,382 | INFO |
============================================================
2025-12-23 02:57:38,382 | INFO | Experiment 3/7: batch_size=96, concurrency=3
2025-12-23 02:57:38,382 | INFO | ============================================================
2025-12-23 02:57:38,382 | INFO | Starting benchmark: 150 requests, concurrency=3, batch_size=96
2025-12-23 02:57:44,620 | INFO | Processed 33600 queries (350 requests) | Latency: 112.14ms | QPS: 864.0
2025-12-23 02:57:50,746 | INFO | Processed 38400 queries (400 requests) | Latency: 111.15ms | QPS: 864.0
2025-12-23 02:57:50,750 | INFO | Progress: 100/150 requests
2025-12-23 02:57:56,926 | INFO | Processed 43200 queries (450 requests) | Latency: 107.27ms | QPS: 864.0
2025-12-23 02:57:56,927 | INFO | Completed: 18.54s | 14400 pairs | 776.52 pairs/s
2025-12-23 02:57:56,927 | INFO |
============================================================
2025-12-23 02:57:56,928 | INFO | Experiment 4/7: batch_size=96, concurrency=4
2025-12-23 02:57:56,928 | INFO | ============================================================
2025-12-23 02:57:56,928 | INFO | Starting benchmark: 150 requests, concurrency=4, batch_size=96
2025-12-23 02:58:03,080 | INFO | Processed 48000 queries (500 requests) | Latency: 105.11ms | QPS: 864.0
2025-12-23 02:58:09,415 | INFO | Processed 52800 queries (550 requests) | Latency: 116.45ms | QPS: 864.0
2025-12-23 02:58:09,419 | INFO | Progress: 100/150 requests
2025-12-23 02:58:15,581 | INFO | Processed 57600 queries (600 requests) | Latency: 107.78ms | QPS: 864.0
2025-12-23 02:58:15,582 | INFO | Completed: 18.65s | 14400 pairs | 771.94 pairs/s
2025-12-23 02:58:15,582 | INFO |
============================================================
2025-12-23 02:58:15,582 | INFO | Experiment 5/7: batch_size=96, concurrency=6
2025-12-23 02:58:15,582 | INFO | ============================================================
2025-12-23 02:58:15,582 | INFO | Starting benchmark: 150 requests, concurrency=6, batch_size=96
2025-12-23 02:58:21,743 | INFO | Processed 62400 queries (650 requests) | Latency: 110.52ms | QPS: 864.0
2025-12-23 02:58:28,064 | INFO | Processed 67200 queries (700 requests) | Latency: 115.37ms | QPS: 768.0
2025-12-23 02:58:28,068 | INFO | Progress: 100/150 requests
2025-12-23 02:58:34,292 | INFO | Processed 72000 queries (750 requests) | Latency: 107.64ms | QPS: 864.0
2025-12-23 02:58:34,292 | INFO | Completed: 18.71s | 14400 pairs | 769.66 pairs/s
2025-12-23 02:58:34,293 | INFO |
============================================================
2025-12-23 02:58:34,293 | INFO | Experiment 6/7: batch_size=96, concurrency=8
2025-12-23 02:58:34,293 | INFO | ============================================================
2025-12-23 02:58:34,293 | INFO | Starting benchmark: 150 requests, concurrency=8, batch_size=96
2025-12-23 02:58:40,424 | INFO | Processed 76800 queries (800 requests) | Latency: 102.77ms | QPS: 864.0
2025-12-23 02:58:46,626 | INFO | Processed 81600 queries (850 requests) | Latency: 108.99ms | QPS: 864.0
2025-12-23 02:58:46,630 | INFO | Progress: 100/150 requests
2025-12-23 02:58:52,787 | INFO | Processed 86400 queries (900 requests) | Latency: 115.75ms | QPS: 864.0
2025-12-23 02:58:52,788 | INFO | Completed: 18.49s | 14400 pairs | 778.59 pairs/s
2025-12-23 02:58:52,789 | INFO |
============================================================
2025-12-23 02:58:52,789 | INFO | Experiment 7/7: batch_size=96, concurrency=12
2025-12-23 02:58:52,789 | INFO | ============================================================
2025-12-23 02:58:52,789 | INFO | Starting benchmark: 150 requests, concurrency=12, batch_size=96
2025-12-23 02:58:58,961 | INFO | Processed 91200 queries (950 requests) | Latency: 104.49ms | QPS: 864.0
2025-12-23 02:59:05,407 | INFO | Processed 96000 queries (1000 requests) | Latency: 116.68ms | QPS: 768.0
2025-12-23 02:59:05,411 | INFO | Progress: 100/150 requests
2025-12-23 02:59:11,620 | INFO | Processed 100800 queries (1050 requests) | Latency: 108.92ms | QPS: 864.0
2025-12-23 02:59:11,621 | INFO | Completed: 18.83s | 14400 pairs | 764.64 pairs/s
2025-12-23 02:59:11,622 | INFO | Completed 7 experiments
2025-12-23 02:59:11,623 | INFO | Results saved to ml_inference_server/docs/experiments/06a_concurrency_mps_results.md

========================================================================================================================
EXPERIMENT SUMMARY (Cross-Encoder)
========================================================================================================================
Batch  Conc  Pairs    Time     Lat Avg    Lat P95    Lat P99    TP Avg       TP P99
------------------------------------------------------------------------------------------------------------------------
96     1     14400    20.2     134.6      176.7      255.1      713.3        939.9
96     2     14400    18.7     248.8      298.9      350.2      769.3        456.0
96     3     14400    18.5     368.7      429.1      447.3      776.5        363.5
96     4     14400    18.7     493.1      554.0      605.5      771.9        357.9
96     6     14400    18.7     737.3      825.8      857.1      769.7        362.0
96     8     14400    18.5     965.0      1065.9     1109.1     778.6        361.7
96     12    14400    18.8     1453.0     1658.7     1699.7     764.6        356.3
========================================================================================================================

Results saved to: ml_inference_server/docs/experiments/06a_concurrency_mps_results.md

Capturing dashboard screenshot...
2025-12-23 02:59:12,908 | INFO | Navigating to http://localhost:8080 (attempt 1/3)...
2025-12-23 02:59:13,359 | INFO | Waiting for page to be fully loaded...
2025-12-23 02:59:13,861 | INFO | Metrics frozen - experiment stopped
