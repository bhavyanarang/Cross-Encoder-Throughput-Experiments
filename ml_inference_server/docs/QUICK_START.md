# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
cd ml_inference_server
pip install -r requirements.txt
```

### 2. Start the Server (Production Config)

```bash
# Use the optimal production configuration (719 p/s @ 178ms latency)
python main.py --experiment experiments/15_production_optimal.yaml
```

### 3. Test with Client

```bash
# In another terminal
python client.py
```

### 4. Monitor Metrics

Open in browser: http://localhost:8080

---

## 📊 Performance Expectations

| Configuration | Throughput | Latency (P50) | Latency (P99) | Use Case |
|---------------|-----------|---------------|---------------|----------|
| **Production Optimal** | **719 p/s** | **178ms** | **211ms** | **Balanced (Recommended)** |
| Latency-Sensitive | 519 p/s | 92ms | 165ms | Low-latency apps |
| High-Throughput | 776 p/s | 369ms | 447ms | Batch processing |

---

## 🎯 Key Features

### 1. Dynamic Batching
Automatically aggregates small requests into larger batches for better GPU utilization.

```yaml
batching:
  enabled: true
  max_batch_size: 64  # Optimal for MPS
  timeout_ms: 20      # Low latency
```

### 2. Length-Aware Batching
Sorts pairs by length to reduce padding waste by ~25%.

```yaml
scheduler:
  enable_length_aware_batching: true
```

### 3. Process-Based Parallelism
Each worker runs in a separate process with its own MPS context (avoids Metal conflicts).

```yaml
# Automatically configured based on concurrency_levels
experiment:
  concurrency_levels: [2]  # 2 worker processes
```

### 4. Real-Time Metrics
Monitor latency, throughput, padding waste, and per-stage timings.

- Dashboard: http://localhost:8080
- JSON API: http://localhost:8080/metrics

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Complete HLD/LLD with Mermaid diagrams |
| [CODE_QUALITY_ANALYSIS.md](CODE_QUALITY_ANALYSIS.md) | Code quality analysis and refactoring plan |
| [experiments/all_results.md](experiments/all_results.md) | All experiment results |
| [experiments/systematic_experiment_summary.md](experiments/systematic_experiment_summary.md) | Performance analysis |

---

## 🔧 Configuration Options

### Latency-Sensitive (Low Latency)

```yaml
batching:
  max_batch_size: 32
  timeout_ms: 10
experiment:
  concurrency_levels: [1]
```

**Performance:** 519 p/s @ 92ms latency

### Balanced (Recommended)

```yaml
batching:
  max_batch_size: 64
  timeout_ms: 20
experiment:
  concurrency_levels: [2]
```

**Performance:** 719 p/s @ 178ms latency

### High-Throughput (Batch Processing)

```yaml
batching:
  max_batch_size: 96
  timeout_ms: 50
experiment:
  concurrency_levels: [3]
```

**Performance:** 776 p/s @ 369ms latency

---

## 📈 Running Experiments

### Single Experiment

```bash
./run_experiment.sh experiments/15_production_optimal.yaml
```

### Systematic Experiments

```bash
python run_systematic_experiments.py
```

Results saved to: `docs/experiments/`

---

## 🏗️ Architecture Overview

```
Client → gRPC Server → Scheduler → Model Pool → Worker Processes
                           ↓
                    Metrics Collector → Dashboard
```

**Key Components:**
1. **gRPC Server:** Accept client requests
2. **Scheduler:** Route requests, apply length-aware batching
3. **Model Pool:** Manage worker processes (round-robin)
4. **Worker Processes:** Run model inference (isolated MPS contexts)
5. **Metrics Collector:** Track latency, throughput, padding
6. **Dashboard:** Real-time monitoring UI

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed diagrams.

---

## 🎓 Learn More

### Understanding the Results

**Throughput (pairs/sec):** How many query-document pairs processed per second
**Latency P50:** Median latency (50% of requests faster than this)
**Latency P99:** 99th percentile latency (only 1% of requests slower)
**Padding Ratio:** % of tokens that are padding (lower is better)

### Why Process-Based?

Apple Silicon's Metal framework has **command buffer conflicts** with multi-threading. Process-based parallelism gives each worker its own MPS context, enabling true parallel inference.

### Why Length-Aware Batching?

**Without:** All sequences padded to max length → 70% waste
**With:** Similar-length sequences batched together → 30% waste

**Result:** 25% latency reduction
