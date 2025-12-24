# ML Inference Server - Documentation Index

## 📚 Documentation Overview

This folder contains comprehensive documentation for the ML Inference Server, including architecture diagrams, code quality analysis, and experiment results.

---

## 🚀 Quick Navigation

### Getting Started
- **[QUICK_START.md](QUICK_START.md)** - Get up and running in 5 minutes
- **[../experiments/15_production_optimal.yaml](../experiments/15_production_optimal.yaml)** - Optimal production configuration

### Architecture & Design
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete HLD/LLD with Mermaid diagrams
- **[VISUAL_SUMMARY.md](VISUAL_SUMMARY.md)** - Visual architecture diagrams
- **[CODE_QUALITY_ANALYSIS.md](CODE_QUALITY_ANALYSIS.md)** - Code quality issues and refactoring plan

### Experiment Results
- **[experiments/all_results.md](experiments/all_results.md)** - All experiment results
- **[experiments/systematic_experiment_summary.md](experiments/systematic_experiment_summary.md)** - Performance analysis

---

## 📖 Documentation Structure

```
docs/
├── README.md                          ← You are here
├── QUICK_START.md                     ← 5-minute setup guide
├── ARCHITECTURE.md                    ← Complete HLD/LLD
├── VISUAL_SUMMARY.md                  ← Architecture diagrams
├── CODE_QUALITY_ANALYSIS.md           ← Code quality report
└── experiments/
    ├── all_results.md                 ← All experiment results
    ├── systematic_experiment_summary.md ← Performance analysis
    └── screenshots/                   ← Dashboard screenshots
```

---

## 🎯 What to Read First

### If you're a **New User**
1. [QUICK_START.md](QUICK_START.md) - Get started in 5 minutes
2. [VISUAL_SUMMARY.md](VISUAL_SUMMARY.md) - Understand the architecture visually

### If you're a **Developer**
1. [ARCHITECTURE.md](ARCHITECTURE.md) - Understand the system design
2. [CODE_QUALITY_ANALYSIS.md](CODE_QUALITY_ANALYSIS.md) - Code quality and best practices
3. [experiments/systematic_experiment_summary.md](experiments/systematic_experiment_summary.md) - Performance characteristics

### If you're an **Architect**
1. [ARCHITECTURE.md](ARCHITECTURE.md) - HLD/LLD with diagrams
2. [VISUAL_SUMMARY.md](VISUAL_SUMMARY.md) - Visual architecture
3. [experiments/all_results.md](experiments/all_results.md) - Detailed performance data

### If you're a **Performance Engineer**
1. [experiments/systematic_experiment_summary.md](experiments/systematic_experiment_summary.md) - Performance analysis
2. [experiments/all_results.md](experiments/all_results.md) - All experiment results
3. [ARCHITECTURE.md](ARCHITECTURE.md) - Performance characteristics section

---

## 📊 Key Performance Results

From systematic experiments (1,190 experiments total):

| Configuration | Throughput | Latency (P50) | Latency (P99) | Use Case |
|---------------|-----------|---------------|---------------|----------|
| **Production Optimal** | **719 p/s** | **178ms** | **211ms** | **Balanced (Recommended)** |
| Latency-Sensitive | 519 p/s | 92ms | 165ms | Low-latency applications |
| High-Throughput | 776 p/s | 369ms | 447ms | Batch processing |

**Configuration:** `experiments/15_production_optimal.yaml`

---

## 🏗️ Architecture Highlights

### System Components
1. **gRPC Server** - Accept client requests (port 50051)
2. **Scheduler** - Route requests, apply length-aware batching
3. **Model Pool** - Manage worker processes (round-robin)
4. **Worker Processes** - Run model inference (isolated MPS contexts)
5. **Metrics Collector** - Track latency, throughput, padding
6. **HTTP Server** - Serve metrics/dashboard (port 8080)

### Key Design Decisions
- **Process-Based Parallelism:** Avoids Metal command buffer conflicts on Apple Silicon
- **Length-Aware Batching:** Reduces padding waste by 25%
- **Dynamic Batching:** Improves throughput by 35%
- **FP16 Precision:** +10-12% throughput on MPS/MLX

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed diagrams.

---

## 🔧 Configuration Guide

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

### High-Throughput
```yaml
batching:
  max_batch_size: 96
  timeout_ms: 50
experiment:
  concurrency_levels: [3]
```
**Performance:** 776 p/s @ 369ms latency

---

## 📈 Experiment Summary

### Systematic Experiments Conducted
- **Phase 1:** Backend comparison (PyTorch, MPS, MLX, ONNX, Compiled)
- **Phase 2:** Batch size optimization (8-256)
- **Phase 3:** Concurrency analysis (1-12 workers)
- **Phase 4:** Multi-model stress test
- **Phase 5:** Dynamic batching evaluation
- **Phase 6:** Length-aware batching optimization

### Key Findings
1. MPS and MLX backends perform identically (~520-530 p/s)
2. Optimal batch size: 64 (balances throughput and latency)
3. Optimal concurrency: 2 (avoids MPS overload)
4. Dynamic batching: +35% throughput
5. Length-aware batching: -25% latency

See [experiments/systematic_experiment_summary.md](experiments/systematic_experiment_summary.md) for details.

---

## 🐛 Troubleshooting

### Common Issues

**"Socket closed" / Connection refused**
- **Cause:** MPS instability with high concurrency
- **Fix:** Reduce `concurrency_levels` to 1-2
- **Reference:** [ARCHITECTURE.md - Troubleshooting](ARCHITECTURE.md#troubleshooting)

**High padding waste (>50%)**
- **Cause:** Mixed sequence lengths in batch
- **Fix:** Enable `enable_length_aware_batching: true`
- **Reference:** [ARCHITECTURE.md - Design Decisions](ARCHITECTURE.md#key-design-decisions)

**Low throughput (<500 p/s)**
- **Cause:** Batch size too small
- **Fix:** Increase `max_batch_size` to 64
- **Reference:** [experiments/systematic_experiment_summary.md](experiments/systematic_experiment_summary.md)

---

## 🎓 Learning Path

### Beginner
1. Read [QUICK_START.md](QUICK_START.md)
2. Start server with production config
3. Test with client
4. Monitor metrics dashboard

### Intermediate
1. Read [ARCHITECTURE.md](ARCHITECTURE.md) - HLD section
2. Understand request flow
3. Explore different configurations
4. Run experiments

### Advanced
1. Read [ARCHITECTURE.md](ARCHITECTURE.md) - LLD section
2. Understand process-based parallelism
3. Read [CODE_QUALITY_ANALYSIS.md](CODE_QUALITY_ANALYSIS.md)
4. Contribute improvements

---

## 📝 Document Summaries

### QUICK_START.md
- **Purpose:** Get started in 5 minutes
- **Audience:** New users
- **Content:** Installation, server startup, client testing, monitoring

### ARCHITECTURE.md
- **Purpose:** Complete system documentation
- **Audience:** Developers, architects
- **Content:** HLD, LLD, Mermaid diagrams, data structures, API reference

### VISUAL_SUMMARY.md
- **Purpose:** Visual architecture overview
- **Audience:** Visual learners, architects
- **Content:** 9 Mermaid diagrams showing system architecture, data flow, deployment

### CODE_QUALITY_ANALYSIS.md
- **Purpose:** Code quality report and refactoring plan
- **Audience:** Maintainers, developers
- **Content:** Issues identified, refactoring plan, best practices, metrics

### experiments/all_results.md
- **Purpose:** Complete experiment results
- **Audience:** Performance engineers
- **Content:** 1,190 experiment results with detailed metrics

### experiments/systematic_experiment_summary.md
- **Purpose:** Performance analysis and recommendations
- **Audience:** All users
- **Content:** Experiment phases, key findings, optimal configurations

---

## 🔗 External Resources

### Related Files
- **Production Config:** `../experiments/15_production_optimal.yaml`
- **Main Entry Point:** `../main.py`
- **Client:** `../client.py`
- **Server:** `../server/grpc_server.py`

### Monitoring
- **Dashboard:** http://localhost:8080
- **Metrics API:** http://localhost:8080/metrics

---

## 📞 Support

### Documentation Issues
If you find errors or have suggestions for the documentation, please:
1. Check [CODE_QUALITY_ANALYSIS.md](CODE_QUALITY_ANALYSIS.md) for known issues
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) for design decisions
3. Consult [experiments/systematic_experiment_summary.md](experiments/systematic_experiment_summary.md) for performance data

### Performance Issues
1. Check [experiments/all_results.md](experiments/all_results.md) for expected performance
2. Review [ARCHITECTURE.md - Troubleshooting](ARCHITECTURE.md#troubleshooting)
3. Verify configuration matches recommended settings

---

## 🎯 Quick Reference

### Start Server
```bash
python main.py --experiment experiments/15_production_optimal.yaml
```

### Monitor Metrics
```bash
open http://localhost:8080
```

### Run Client
```bash
python client.py
```

### Run Experiments
```bash
./run_experiment.sh experiments/15_production_optimal.yaml
```

---

## 📊 Documentation Metrics

| Document | Lines | Diagrams | Purpose |
|----------|-------|----------|---------|
| ARCHITECTURE.md | 800+ | 5 Mermaid | Complete HLD/LLD |
| VISUAL_SUMMARY.md | 400+ | 9 Mermaid | Visual architecture |
| CODE_QUALITY_ANALYSIS.md | 600+ | 0 | Code quality report |
| QUICK_START.md | 300+ | 0 | Getting started guide |
| all_results.md | 1,190 | 0 | All experiment results |

**Total:** 3,000+ lines of documentation with 14 Mermaid diagrams

---

## 🏆 Documentation Achievements

- ✅ Complete HLD with system architecture diagrams
- ✅ Detailed LLD with sequence diagrams
- ✅ Visual architecture summary with 9 diagrams
- ✅ Code quality analysis with refactoring plan
- ✅ Quick start guide for new users
- ✅ Comprehensive experiment results (1,190 experiments)
- ✅ Performance analysis and recommendations
- ✅ Troubleshooting guide
- ✅ API reference
- ✅ Deployment guide

---

**Last Updated:** December 24, 2025
**Version:** 1.0
**Status:** Complete
