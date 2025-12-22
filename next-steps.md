# Next Steps: Performance Optimization Roadmap

**Last Updated**: December 23, 2025  
**Current Performance**: ~530 pairs/sec @ batch=32, ~60ms latency (MLX/MPS backend)

---

## Phase 1: Bottleneck Identification (Do First!)

Before optimizing, measure where time actually goes. Throughput/latency improvements are usually **bottleneck-shifts** — fix one thing, another becomes the limiter.

### Add Per-Stage Timers

Instrument the request path to capture P50/P95 for each stage:

```
┌─────────────┐    ┌──────────────┐    ┌───────────┐    ┌──────────┐    ┌─────────────┐
│  gRPC recv  │ → │ Tokenization │ → │ Scheduler │ → │  Model   │ → │ gRPC send   │
│   (~1ms?)   │    │   (~?ms)     │    │  (~?ms)   │    │ (~?ms)   │    │   (~1ms?)   │
└─────────────┘    └──────────────┘    └───────────┘    └──────────┘    └─────────────┘
```

**What to measure:**
| Stage | Metric | Why It Matters |
|-------|--------|----------------|
| `t_grpc_receive` | Time to deserialize request | Usually negligible unless payload is huge |
| `t_tokenize` | Time to tokenize (query, doc) pairs | **Often the hidden bottleneck** |
| `t_queue_wait` | Time request waits in batch queue | Shows if batching policy is too aggressive |
| `t_model_inference` | GPU forward pass time | The "real work" |
| `t_grpc_send` | Time to serialize + send response | Usually negligible |

**Expected findings:**
- If `t_tokenize` is >30% of total time → tokenization optimization is high priority
- If `t_queue_wait` is high → batching timeout is too long, or batch size too large
- If `t_model_inference` dominates → look at model-side optimizations (FP16, batch size, etc.)

### Implementation Checklist

- [x] Add timing decorators/context managers to each stage (`utils/stage_timer.py`)
- [x] Log timings per request (or sample 1-in-N for high traffic) (`metrics/collector.py`)
- [x] Add P50/P95/P99 aggregations to metrics endpoint (`stage_breakdown` in `/metrics`)
- [x] Create dashboard view for stage breakdown (`dashboard/` directory with grid layout)

---

## Phase 2: Tokenization Optimization (Usually Huge Wins)

Tokenization is CPU-bound and often the hidden bottleneck in ML serving. The GPU can be starved waiting for tokenized inputs.

### 2.1 Cache Tokenization Results

**Why:** If queries or documents repeat, don't re-tokenize them.

| Cache Level | Use Case | Cache Key | Expected Hit Rate |
|-------------|----------|-----------|-------------------|
| Query cache | Same query reranks different docs | `hash(query_text)` | High if queries repeat |
| Document cache | Same doc scored against many queries | `hash(doc_text)` | High in reranking scenarios |
| Pair cache | Exact (query, doc) repeats | `hash(query + doc)` | Low unless exact duplicates |

**Implementation ideas:**
- LRU cache with configurable size (e.g., 10K entries)
- TTL-based expiry for freshness
- Consider Redis/memcached for multi-process sharing

### 2.2 Parallelize Tokenization

**Why:** Tokenization is CPU-bound; a single thread can't keep up with GPU throughput.

**Options:**
| Approach | Pros | Cons |
|----------|------|------|
| **ThreadPool** | Simple, shares memory | GIL limits true parallelism |
| **ProcessPool** | True parallelism | Serialization overhead |
| **Async tokenizer** | Non-blocking | Still single-threaded |

**Producer-Consumer Pattern:**
```
[Request Queue] → [Tokenizer Pool (N workers)] → [Token Queue] → [GPU Inference] → [Response]
```

- Tokenizer workers run in parallel
- GPU worker consumes pre-tokenized batches
- Overlap tokenization with inference

### 2.3 Explore sequential packing in depth



### 2.4 Batch Tokenization

**Why:** Tokenizing one-by-one has Python loop overhead.

**Current (likely):**
```python
for query, doc in pairs:
    tokens = tokenizer(query, doc)  # One at a time
```

**Better:**
```python
queries, docs = zip(*pairs)
tokens = tokenizer(queries, docs, padding=True, truncation=True)  # Batch
```

- HuggingFace tokenizers use Rust underneath — batching lets it parallelize
- Expect 2-5x speedup over loop

---

## Phase 3: Batching Policy Tuning

Pick a batching strategy that hits your latency SLO while keeping GPU saturated.

### Current Sweet Spot (from experiments)

| Setting | Value | Rationale |
|---------|-------|-----------|
| `max_batch_size` | 64-96 | GPU saturation vs latency trade-off |
| `timeout_ms` | 50 | Low enough for responsiveness |
| `max_concurrency` | 2-4 | Prevent overload |

### Tuning Levers

| Lever | ↑ Increase | ↓ Decrease |
|-------|------------|------------|
| `max_batch_size` | Better throughput, higher latency | Lower latency, less efficient |
| `timeout_ms` | Fuller batches, higher latency | Partial batches, lower latency |
| `max_concurrency` | More parallelism, risk overload | Less queueing, simpler |

### Advanced: Adaptive Batching

Adjust batch size dynamically based on queue depth:

```
if queue_depth > HIGH_THRESHOLD:
    use larger batch, longer timeout (throughput mode)
else:
    use smaller batch, shorter timeout (latency mode)
```

### Advanced: Length-Aware Batching

Group requests by similar token lengths to reduce padding waste:

```
Bucket 1: sequences 0-64 tokens
Bucket 2: sequences 65-128 tokens
Bucket 3: sequences 129-256 tokens
```

- Tighter GPU work (less wasted padding computation)
- Requires knowing token counts before batching (cache or estimate)

---

## Priority Order

Based on typical impact, work on these in order:

| Priority | Task | Expected Impact | Effort |
|----------|------|-----------------|--------|
| 🔴 1 | Add per-stage timers | Unlocks data for all other optimizations | Low |
| 🔴 2 | Batch tokenization | 2-5x tokenization speedup | Low |
| 🟠 3 | Reduce max_length (experiment) | 1.5-2x throughput if acceptable | Low |
| 🟠 4 | Tokenization caching | High if queries/docs repeat | Medium |
| 🟡 5 | Parallel tokenization | Overlap CPU+GPU work | Medium |
| 🟡 6 | Pre-truncation heuristics | Reduce tokenization input size | Low |
| 🟢 7 | Adaptive batching | Fine-tune throughput/latency | Medium |
| 🟢 8 | Length-aware batching | Reduce padding waste | High |

---

## Success Metrics

| Metric | Current | Target | Notes |
|--------|---------|--------|-------|
| Throughput (batch=32) | ~530 p/s | ~700+ p/s | After tokenization optimizations |
| Throughput (batch=64) | ~720 p/s | ~850+ p/s | With parallelization |
| P50 Latency | ~60ms | <50ms | With reduced max_length |
| P95 Latency | ~90ms | <100ms | With better batching |
| Tokenization % of time | Unknown | <20% | After all optimizations |

---

## Notes

- All optimizations assume **MPS/MLX backend** (best performers on Apple Silicon)
- **Compiled backend not recommended** — inductor overhead on MPS is too high
- Measure before and after each change to validate impact

