# High-Level Design: Async Inference Service

## Executive Summary

The Async Inference Service is a non-blocking, queue-based inference pipeline designed to handle high-throughput, latency-sensitive inference workloads without impacting the main synchronous request path. It enables clients to submit inference requests asynchronously, retrieve results via polling, and benefit from automatic batching for improved throughput.

**Key Benefits:**
- **Non-blocking**: gRPC handlers return immediately; clients poll for results
- **Automatic batching**: Multiple requests are combined into a single batch for efficient inference
- **Full observability**: Detailed metrics for every stage (tokenization, inference, queue wait)
- **Feature-gated**: Can be enabled/disabled without code changes via configuration
- **Backward compatible**: Existing synchronous inference path remains unchanged

## Problem Statement

### Current State
The existing inference system uses a synchronous, blocking architecture:
- Client submits request → Server blocks until inference completes → Returns result
- Works well for single requests but doesn't scale for high throughput scenarios
- No automatic batching across concurrent requests
- Difficult to handle bursty traffic patterns

### Desired State
Enable high-throughput, scalable inference without blocking the main request handler:
- Clients submit requests and receive an ID immediately
- Requests are queued and processed in batches automatically
- Clients poll for results when ready
- Full metrics visibility into request lifecycle
- Multiple worker threads process requests independently

## Architecture Overview

The async inference pipeline operates as a parallel path to the existing synchronous inference:

**Core Concept:**
1. **Request Submission Phase**: Client calls `InferAsync(pairs)` → receives `request_id` immediately (non-blocking)
2. **Request Processing Phase**: Worker threads continuously pull requests from queue, batch them, tokenize, infer
3. **Result Retrieval Phase**: Client polls `GetAsyncResult(request_id)` → receives results when ready

**Key Components:**
- **AsyncInferenceController**: Orchestrates entire pipeline, manages queues and workers
- **AsyncInferenceWorker**: Independent worker threads that process batches
- **ModelService**: Encapsulates model loading, quantization, compilation, and inference
- **Request/Response Envelopes**: Data structures for tracking requests through the system

See `d3_diagrams.html` for interactive D3.js visualizations of the system architecture, request flow timeline, and batching strategy.

## System Components

### 1. Request/Response Envelopes

**RequestEnvelope** - Represents a single inference request in the system
- Contains query-document pairs to infer
- Tracks submission time for latency measurement
- Includes threading.Event for result signaling
- Holds the result once processing completes

**ResponseEnvelope** - Represents inference results and metrics
- Contains inference scores
- Includes comprehensive timing metrics:
  - `t_tokenize_ms`: Time spent tokenizing
  - `t_model_inference_ms`: Time spent in model inference
  - `t_queue_wait_ms`: Time waiting in input queue
  - `t_worker_processing_ms`: Total time worker spent on request
  - `t_total_ms`: End-to-end latency
- Includes token statistics and padding efficiency metrics
- Includes worker and device information for debugging

### 2. AsyncInferenceController

**Purpose**: Orchestrates the entire async inference pipeline

**Responsibilities**:
- Manages input and output queues
- Creates and manages worker threads
- Tracks pending requests and their results
- Implements the result collection loop
- Handles request submission and result retrieval

**Key Methods**:
- `submit_request(pairs)`: Non-blocking request submission
- `get_result(request_id, timeout)`: Poll for result with timeout
- `start()`: Initialize workers and start processing
- `stop()`: Graceful shutdown

**Thread Safety**:
- Uses `threading.Queue` for inter-thread communication (thread-safe)
- Uses `threading.Lock` to protect the pending requests dictionary
- Uses `threading.Event` for result signaling

### 3. AsyncInferenceWorker

**Purpose**: Process batches of requests independently

**Responsibilities**:
- Load model and tokenizer on worker startup
- Retrieve requests from input queue
- Batch requests together for efficiency
- Tokenize batches
- Run inference
- Create response envelopes with metrics
- Place results in output queue

**Batching Strategy**:
- Blocking pull: Wait for first request (timeout 100ms)
- Non-blocking pull: Collect additional requests until deadline or max batch size
- Process entire batch together to maximize throughput

**Single Model Per Worker**:
- Each worker thread has its own model instance
- No concurrent access to model (thread-local)
- Enables true parallelism without GIL contention

### 4. ModelService

**Purpose**: Encapsulate model loading and inference logic

**Responsibilities**:
- Load model backend with specified device
- Apply quantization if configured
- Apply compilation if configured
- Execute inference on tokenized batches
- Clean up resources on shutdown

**Benefits**:
- Abstracts backend complexity from worker
- Enables code reuse between sync and async paths
- Single responsibility: model operations only
- Testable in isolation

### 5. gRPC Integration

**New RPC Methods**:

- `InferAsync(AsyncInferRequest)`: Submit async inference request
  - Input: List of query-document pairs
  - Output: Unique request_id
  - Behavior: Non-blocking, returns immediately

- `GetAsyncResult(GetAsyncResultRequest)`: Poll for result
  - Input: request_id from InferAsync response
  - Output: Status (PENDING/DONE/ERROR) + results if ready
  - Behavior: Polls internal state, returns immediately

**Existing Methods**:
- `Infer()`: Unchanged synchronous path
- All existing functionality preserved

## Configuration

### Feature Flags and Settings

```yaml
async_inference:
  enabled: false                 # Master feature flag
  worker_threads: 2              # Number of worker threads
  input_queue_size: 1000         # Max queued requests
  output_queue_size: 1000        # Max queued results
  request_timeout_ms: 30000      # Client-side poll timeout
  worker_init_timeout_ms: 60000  # Model loading timeout

tokenizer_pool:
  enabled: false                 # Tokenizer pooling feature
  pool_size: 2                   # Number of tokenizer instances
```

### Enabling Async Inference

To enable in experiments:

```yaml
# experiments/async_enabled.yaml
# Inherits from base_config.yaml

async_inference:
  enabled: true
  worker_threads: 4
  input_queue_size: 2000
  request_timeout_ms: 45000

tokenizer_pool:
  enabled: true
  pool_size: 4
```

## Metrics and Observability

### Metrics Collected Per Request

Each response includes comprehensive timing and statistical data:

**Timing Metrics** (milliseconds):
- `t_tokenize_ms`: Tokenization time
- `t_model_inference_ms`: Model inference execution time
- `t_queue_wait_ms`: Time in input queue waiting for processing
- `t_worker_processing_ms`: Total worker processing time
- `t_total_ms`: End-to-end latency from submission to result

**Token Statistics**:
- `total_tokens`: Total tokens processed (including padding)
- `real_tokens`: Non-padded tokens
- `padded_tokens`: Padding tokens added
- `padding_ratio`: Efficiency metric (real_tokens / total_tokens)

**Batch Information**:
- `max_seq_length`: Longest sequence in batch
- `avg_seq_length`: Average sequence length
- `batch_size`: Number of requests in batch

**System Information**:
- `worker_id`: Which worker processed this request
- `device`: Device used (cuda, mps, cpu, etc.)
- `model_name`: Model identifier

### Status Polling

Result polling status values:
- `PENDING`: Request still processing
- `DONE`: Result ready with scores and metrics
- `ERROR`: Processing failed, error_message included
- `TIMEOUT`: Result not ready within client timeout

## Scalability and Performance

### Throughput Optimization

1. **Automatic Batching**: Multiple requests processed together
   - Reduces per-request overhead
   - Improves GPU/accelerator utilization
   - Trade-off: Slight latency increase for better overall throughput

2. **Worker Thread Tuning**:
   - More workers = higher concurrency
   - Each worker needs its own model instance (memory tradeoff)
   - Recommended: 2-4 workers per model instance

3. **Tokenizer Pooling** (optional):
   - Reuse tokenizer instances across workers
   - Reduces memory if tokenizer is large
   - Improves cache locality

### Handling Load Spikes

- Input queue provides buffer for bursty traffic
- Workers automatically batch overflow requests
- Clients can implement backpressure (stop submitting) if queue fills
- Error returned if input queue becomes full

### Resource Utilization

- **Memory**: Each worker loads one model instance
  - Formula: `base_memory + (worker_threads × model_memory)`
  - Example: 2GB base + 4 workers × 5GB model = 22GB total

- **CPU**: Limited contention via GIL (one model per worker)
  - Workers operate independently (minimal cross-thread state)
  - Suitable for CPU-bound inference or GPU-accelerated inference

## Thread Safety Guarantees

| Component | Concurrency | Mechanism |
|-----------|------------|-----------|
| Input Queue | Multiple workers reading | `queue.Queue` (thread-safe) |
| Output Queue | Multiple workers writing | `queue.Queue` (thread-safe) |
| Pending Requests Dict | Controller + workers | `threading.Lock` |
| Model Instance | Single worker only | One instance per worker |
| Result Signaling | Controller signals client | `threading.Event` |

## Feature Gates and Backward Compatibility

### Enabling/Disabling

- Feature completely disabled by default (`async_inference.enabled: false`)
- No performance impact when disabled (no code path executed)
- Can be toggled per deployment without code changes

### Backward Compatibility

- **Synchronous path unchanged**: Existing `Infer()` RPC untouched
- **Opt-in for clients**: Only clients calling `InferAsync()` use new path
- **Independent processing**: Async and sync paths don't interfere
- **Graceful degradation**: If async fails, sync path still works

## Error Handling and Resilience

### Request-Level Error Handling

- Individual request failures don't crash worker
- Errors captured in ResponseEnvelope with status `ERROR`
- Other requests in batch continue processing
- Worker thread remains alive and processes next batch

### Queue Full Conditions

- Submitting when input queue full raises `RuntimeError`
- Client can implement retry logic or backpressure
- Prevents unbounded memory growth

### Model Loading Failures

- Initialization failures logged and caught
- Worker thread exits if model fails to load
- Other workers continue (fault isolation)
- System degrades gracefully to fewer workers

### Timeout Handling

- Individual requests can timeout
- Client sees `TIMEOUT` status when polling
- Request is cleaned up after expiration
- Worker continues processing other requests

## Deployment Scenarios

### Scenario 1: Latency-Sensitive Service

Enable with conservative settings:
```yaml
async_inference:
  enabled: true
  worker_threads: 1              # Minimize overhead
  input_queue_size: 100
  request_timeout_ms: 15000      # Quick timeout
```

Use case: Real-time scoring with sub-100ms requirements

### Scenario 2: High-Throughput Batch Processing

Enable with aggressive batching:
```yaml
async_inference:
  enabled: true
  worker_threads: 4              # More parallelism
  input_queue_size: 5000
  request_timeout_ms: 60000      # Longer timeout OK
```

Use case: Daily batch scoring of millions of pairs

### Scenario 3: Production Tuning

Enable with balanced settings:
```yaml
async_inference:
  enabled: true
  worker_threads: 2              # 1 per model replica
  input_queue_size: 2000
  request_timeout_ms: 45000      # 45 second max latency

tokenizer_pool:
  enabled: true
  pool_size: 2                   # Shared tokenizers
```

Use case: Production API handling varied load patterns

## Future Extensions

### Multi-Model Support Per Worker

Currently: One model per worker thread

Future: Single worker can route requests to multiple models
- Requires request routing logic
- Needs model selection in request
- Benefits: Better resource utilization, dynamic model serving

### Adaptive Batching

Currently: Fixed timeout/max-batch-size parameters

Future: Adaptive batching based on queue depth and latency targets
- Monitor queue length and response times
- Dynamically adjust batch timeout
- Benefits: Better SLA compliance, improved latency

### Request Prioritization

Currently: FIFO request processing

Future: Priority levels in request envelope
- High-priority requests processed first
- Low-priority requests batched aggressively
- Benefits: SLA differentiation, VIP customer handling

### Circuit Breaker Pattern

Currently: No explicit circuit breaking

Future: Stop accepting requests if system overloaded
- Monitor queue depth and latency
- Reject new requests if thresholds exceeded
- Benefits: Prevent cascading failures

## Monitoring and Debugging

### Key Metrics to Track

**Latency Percentiles** (p50, p95, p99):
- End-to-end latency (`t_total_ms`)
- Queue wait time (`t_queue_wait_ms`)
- Inference time (`t_model_inference_ms`)

**Throughput**:
- Requests per second
- Pairs per second (accounting for variable request sizes)
- Tokens per second

**Resource Utilization**:
- Queue depths (input and output)
- Worker thread utilization
- Model memory usage

**Error Rates**:
- Request errors (processing failures)
- Queue full errors
- Timeout errors

### Debug Information

Each response includes:
- `worker_id`: Which worker processed
- `batch_size`: Size of batch processed with
- `device`: GPU/CPU/other
- `model_name`: Which model version
- Detailed timing breakdown

### Recommended Alerting

- Alert if p95 latency > 50 second SLA
- Alert if queue full errors exceed 1%
- Alert if worker thread crashes
- Alert if output queue not draining

## Summary

The Async Inference Service provides a scalable, non-blocking inference pipeline suitable for high-throughput workloads. By leveraging automatic batching, independent worker threads, and comprehensive metrics, it enables efficient inference processing without impacting the main request path.

Key design principles:
- **Non-blocking**: Clients never wait for inference to complete
- **Automatic batching**: Multiple requests combined for efficiency
- **Observable**: Full metrics on every request
- **Fault-tolerant**: Failures contained to individual requests
- **Scalable**: Add workers or tune batching for higher throughput
- **Feature-gated**: Can be enabled/disabled without code changes

**For interactive D3.js flow diagrams, see `d3_diagrams.html`**

## Interactive Diagram Features

The `d3_diagrams.html` file provides three interactive D3.js visualizations:

1. **System Architecture Diagram**
   - Shows complete pipeline from gRPC layer through workers to backend services
   - Hover over workers to see highlighting
   - "Animate Data Flow" button shows packets flowing through the system
   - Interactive visual of how requests move through queues to workers

2. **Request Flow Timeline**
   - Depicts parallel client, server, and worker operations on a timeline
   - Shows non-blocking nature: client gets ID immediately while workers process in parallel
   - "Play Animation" button animates a request token moving through the pipeline
   - Visualizes timing and concurrency

3. **Request Batching Strategy**
   - Illustrates input queue → worker batching → output queue flow
   - Shows the 4-step batch processing pipeline
   - Displays efficiency gains with different batch sizes (1x to 8x throughput)
   - Demonstrates why batching improves throughput at slight latency cost

Open `d3_diagrams.html` in a web browser to explore all interactive features.
