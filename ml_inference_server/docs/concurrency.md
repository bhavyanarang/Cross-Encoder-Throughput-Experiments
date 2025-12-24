# Concurrency in ML Inference Server

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT SIDE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ThreadPoolExecutor(max_workers=concurrency)                               │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                          │
│   │Thread 1 │ │Thread 2 │ │Thread 3 │ │Thread 4 │  (concurrency=4)         │
│   │ Req 1   │ │ Req 2   │ │ Req 3   │ │ Req 4   │                          │
│   │ Req 5   │ │ Req 6   │ │ Req 7   │ │ Req 8   │  ← Each thread picks     │
│   │ Req 9   │ │ ...     │ │ ...     │ │ ...     │    next request when     │
│   └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘    previous completes    │
│        │           │           │           │                                │
│        └───────────┴───────────┴───────────┘                                │
│                          │                                                   │
│                     gRPC Channel                                            │
│                    (multiplexed)                                            │
└──────────────────────────┼──────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SERVER SIDE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   grpc.server(ThreadPoolExecutor(max_workers=10))                           │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐        ┌─────────┐                   │
│   │Worker 1 │ │Worker 2 │ │Worker 3 │  ...   │Worker 10│                   │
│   │ Handle  │ │ Handle  │ │ Handle  │        │ Handle  │                   │
│   │ Req A   │ │ Req B   │ │ Req C   │        │ Req J   │                   │
│   └────┬────┘ └────┬────┘ └────┬────┘        └────┬────┘                   │
│        │           │           │                  │                         │
│        └───────────┴───────────┴──────────────────┘                         │
│                          │                                                   │
│                    Scheduler.schedule()                                      │
│                          │                                                   │
│                          ▼                                                   │
│              ┌───────────────────────┐                                      │
│              │   PyTorch Backend     │                                      │
│              │   (MPS GPU)           │  ← Requests serialize here!          │
│              │                       │     GPU processes one at a time      │
│              │   model.encode()      │     (unless batched together)        │
│              └───────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Concurrency Levels Explained

| Concurrency | Client Behavior | Server Behavior | GPU Behavior |
|-------------|-----------------|-----------------|--------------|
| **1** | Send req, wait for response, send next | 1 request at a time | Idle between requests |
| **4** | 4 threads sending simultaneously | Up to 4 workers handling | Requests queue up, less idle time |
| **8** | 8 threads sending simultaneously | Up to 8 workers handling | More queueing, GPU stays busy |

## Why Latency Increases with Concurrency

```
Concurrency=1:                    Concurrency=4:

Client:  [Req1]----[Req2]----     Client:  [Req1][Req2][Req3][Req4]----
                                           ↓    ↓    ↓    ↓
GPU:     [===]    [===]           GPU:     [===][===][===][===]
                                               ↑
         No waiting                       Req 2,3,4 wait in queue!
         Latency = inference time         Latency = queue_time + inference_time
```

## Batching vs Concurrency

| Approach | What it does | GPU Efficiency | Latency Impact |
|----------|--------------|----------------|----------------|
| **Batching** (batch_size=32) | Process 32 texts in ONE forward pass | Very high (GPU parallelism) | Slight increase |
| **Concurrency** (conc=8) | Send 8 requests simultaneously | Medium (overlap network I/O) | Queue waiting |

**Best practice:** Combine moderate batching with moderate concurrency for optimal throughput without excessive latency.
