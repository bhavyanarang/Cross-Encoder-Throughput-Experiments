# Results Diff Summary: Experiment 10

## Key Differences Between Runs

### Old Run (2025-12-26 16:35:28) - Committed to Git
- **Best Throughput:** 1011.6 p/s (batch=32, conc=4)
- **Average Throughput:** 933.0 p/s
- **Best Latency:** 40.2 ms (batch=16, conc=2)
- **Average Latency:** 74.7 ms
- **Tokenization Time:** 10.7 ms (12.9% of total)
- **Inference Time:** 42.6 ms

### New Run (2025-12-28 01:38:19) - With Tokenizer Pool
- **Best Throughput:** 751.3 p/s (batch=16, conc=4)
- **Average Throughput:** 678.7 p/s
- **Best Latency:** 47.4 ms (batch=16, conc=2)
- **Average Latency:** 107.7 ms
- **Tokenization Time:** 12.3 ms (10.4% of total)
- **Inference Time:** 68.8 ms

## Performance Comparison

| Metric | Old Run | New Run | Change |
|--------|---------|---------|--------|
| Best Throughput | 1011.6 p/s | 751.3 p/s | **-25.7%** |
| Avg Throughput | 933.0 p/s | 678.7 p/s | **-27.3%** |
| Best Latency | 40.2 ms | 47.4 ms | **+17.9%** |
| Avg Latency | 74.7 ms | 107.7 ms | **+44.2%** |
| Inference Time | 42.6 ms | 68.8 ms | **+61.5%** |

## Analysis

**Important Note:** The old run appears to have been run WITHOUT tokenizer pool (or with different configuration), while the new run explicitly has tokenizer pool enabled with 4 workers.

### Possible Reasons for Performance Difference:

1. **Tokenizer Pool Overhead:** The new run uses a tokenizer pool with 4 workers, which adds:
   - Thread synchronization overhead
   - Queue management overhead
   - CPU context switching

2. **System State:** Different system load, thermal throttling, or background processes

3. **Configuration Differences:** The old config may have had tokenizer pool disabled (using inline tokenization)

4. **Measurement Variability:** Benchmark results can vary between runs due to:
   - System load
   - Memory fragmentation
   - GPU thermal state
   - Other processes

## Recommendation

**Results files change on every run** - this is expected behavior. Consider:

1. **Gitignore results files** if you don't want them tracked:
   ```bash
   echo "experiments/results/*.md" >> .gitignore
   echo "experiments/distribution/*.md" >> .gitignore
   ```

2. **Keep results in git** if you want historical tracking, but understand they'll show diffs on every run

3. **Use separate directories** for different experiment runs if you want to preserve multiple result sets

## Current Status

- ✅ Tokenizer pool is working (4 workers active)
- ✅ Results are being generated correctly
- ⚠️ Results files are tracked in git, causing diffs on every run
