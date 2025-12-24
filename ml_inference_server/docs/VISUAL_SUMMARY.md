# Visual Architecture Summary

## System Overview

```mermaid
graph TB
    subgraph "External"
        C1[Client 1]
        C2[Client 2]
        CN[Client N]
        BROWSER[Web Browser]
    end

    subgraph "Server Layer - Port 50051"
        GRPC[gRPC Server<br/>ThreadPool: 10 workers]
    end

    subgraph "Processing Layer"
        SCH[Scheduler<br/>Request Router]
        LAB{Length-Aware<br/>Batching?}
    end

    subgraph "Model Pool - Process Based"
        MP[Model Pool Manager<br/>Round-Robin Routing]

        subgraph "Worker 1"
            W1[Worker Process<br/>PID: 12345]
            M1[Model + Tokenizer]
            MPS1[MPS Context 1]
        end

        subgraph "Worker 2"
            W2[Worker Process<br/>PID: 12346]
            M2[Model + Tokenizer]
            MPS2[MPS Context 2]
        end
    end

    subgraph "Monitoring - Port 8080"
        MC[Metrics Collector]
        HTTP[HTTP Server]
        DASH[Dashboard UI]
    end

    C1 --> GRPC
    C2 --> GRPC
    CN --> GRPC

    GRPC --> SCH
    SCH --> LAB
    LAB -->|Yes: Sort by length| MP
    LAB -->|No: Direct| MP

    MP --> W1
    MP --> W2

    W1 --> M1
    M1 --> MPS1

    W2 --> M2
    M2 --> MPS2

    SCH --> MC
    MC --> HTTP
    HTTP --> DASH
    BROWSER --> HTTP

    style GRPC fill:#e1f5ff
    style SCH fill:#fff4e1
    style MP fill:#ffe1e1
    style W1 fill:#e1ffe1
    style W2 fill:#e1ffe1
    style MC fill:#ffe1ff
    style DASH fill:#f0f0f0
```

---

## Request Flow (Detailed)

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant gRPC as gRPC Server
    participant Scheduler
    participant Batcher as Length-Aware<br/>Batcher
    participant Pool as Model Pool
    participant Worker
    participant Metrics

    Client->>gRPC: Infer(pairs)<br/>[query, doc]
    Note over gRPC: Deserialize<br/>protobuf

    gRPC->>Scheduler: schedule(pairs)
    Note over Scheduler: Record arrival time

    alt Length-Aware Batching Enabled
        Scheduler->>Batcher: sort_by_length(pairs)
        Note over Batcher: Estimate token lengths<br/>Sort shortest → longest
        Batcher-->>Scheduler: sorted_pairs + unsort_fn
    end

    Scheduler->>Pool: infer(pairs)
    Note over Pool: Select worker<br/>(round-robin)

    Pool->>Worker: WorkItem(req_id, pairs)

    Note over Worker: Stage 1: Tokenize<br/>(12ms)
    Note over Worker: Stage 2: Model Forward<br/>(165ms)
    Note over Worker: Stage 3: Compute Scores

    Worker-->>Pool: WorkResult(scores, timings)
    Pool-->>Scheduler: InferenceResult

    alt Length-Aware Batching Enabled
        Scheduler->>Scheduler: unsort_fn(scores)
        Note over Scheduler: Restore original order
    end

    Scheduler->>Metrics: record(latency, padding, stages)

    Scheduler-->>gRPC: scores, latency_ms
    Note over gRPC: Serialize<br/>protobuf

    gRPC-->>Client: InferResponse
```

---

## Model Pool Architecture

```mermaid
graph LR
    subgraph "Parent Process"
        direction TB
        MP[Model Pool Manager]
        IQ[Input Queue<br/>multiprocessing.Queue]
        OQ[Output Queue<br/>multiprocessing.Queue]
        RT[Result Router<br/>Background Thread]
        FUTURES[Pending Requests<br/>Dict[req_id → Future]]
    end

    subgraph "Worker Process 1 - PID 12345"
        direction TB
        W1[Worker Main Loop]
        M1[CrossEncoder Model]
        T1[Tokenizer]
        MPS1[MPS Context 1<br/>Isolated Metal]
    end

    subgraph "Worker Process 2 - PID 12346"
        direction TB
        W2[Worker Main Loop]
        M2[CrossEncoder Model]
        T2[Tokenizer]
        MPS2[MPS Context 2<br/>Isolated Metal]
    end

    MP --> IQ
    IQ --> W1
    IQ --> W2

    W1 --> M1
    W1 --> T1
    M1 --> MPS1

    W2 --> M2
    W2 --> T2
    M2 --> MPS2

    W1 --> OQ
    W2 --> OQ
    OQ --> RT
    RT --> FUTURES
    FUTURES --> MP

    style MP fill:#ffe1e1
    style IQ fill:#fff4e1
    style OQ fill:#fff4e1
    style W1 fill:#e1f5ff
    style W2 fill:#e1f5ff
    style MPS1 fill:#e1ffe1
    style MPS2 fill:#e1ffe1
```

---

## Backend Class Hierarchy

```mermaid
classDiagram
    class BaseBackend {
        <<abstract>>
        +model_name: str
        +device: str
        +model: Any
        +_is_loaded: bool
        +load_model()* void
        +infer(pairs)* ndarray
        +infer_with_timing(pairs)* InferenceResult
        +warmup()* void
        +get_model_info()* dict
        +sync_device() void
        +clear_memory() void
    }

    class MPSBackend {
        +device: "mps"
        +use_fp16: bool
        +load_model() void
        +infer_with_timing() InferenceResult
        +warmup() void
    }

    class MLXBackend {
        +quantization_bits: int
        +group_size: int
        +load_model() void
        +infer_with_timing() InferenceResult
        +warmup() void
    }

    class PyTorchBackend {
        +device: "cpu"/"cuda"
        +load_model() void
        +infer_with_timing() InferenceResult
        +warmup() void
    }

    class ONNXBackend {
        +use_coreml: bool
        +optimize: bool
        +load_model() void
        +infer_with_timing() InferenceResult
        +warmup() void
    }

    BaseBackend <|-- MPSBackend
    BaseBackend <|-- MLXBackend
    BaseBackend <|-- PyTorchBackend
    BaseBackend <|-- ONNXBackend

    note for BaseBackend "Abstract base class\nDefines interface for all backends"
    note for MPSBackend "Apple Silicon GPU\nFP16 support\n~720 p/s"
    note for MLXBackend "Apple MLX framework\nQuantization support\n~720 p/s"
```

---

## Metrics System Composition

```mermaid
graph TB
    subgraph "MetricsCollector"
        MC[MetricsCollector<br/>Facade Pattern]

        subgraph "Components"
            LAT[LatencyTracker<br/>P50, P95, P99]
            TP[ThroughputTracker<br/>QPS, Pairs/sec]
            PAD[PaddingAnalyzer<br/>Waste %, Tokens]
            STAGE[StageMetrics<br/>Tokenize, Inference]
        end

        EXP[ExperimentInfo<br/>Name, Backend, Device]
    end

    subgraph "Data Sources"
        SCH[Scheduler]
        WORKER[Worker Process]
    end

    subgraph "Consumers"
        HTTP[HTTP /metrics]
        DASH[Dashboard UI]
        JSON[JSON Export]
    end

    SCH --> MC
    WORKER --> MC

    MC --> LAT
    MC --> TP
    MC --> PAD
    MC --> STAGE
    MC --> EXP

    MC --> HTTP
    MC --> DASH
    MC --> JSON

    style MC fill:#e1ffe1
    style LAT fill:#fff4e1
    style TP fill:#fff4e1
    style PAD fill:#fff4e1
    style STAGE fill:#fff4e1
```

---

## Data Flow Diagram

```mermaid
flowchart TD
    START([Client Request])
    GRPC[gRPC Deserialize]
    SCHED[Scheduler]

    SORT{Length-Aware<br/>Batching?}
    SORT_YES[Sort by Length]
    SORT_NO[Direct Pass]

    POOL[Model Pool]
    ROUTE{Select Worker}
    W1[Worker 1]
    W2[Worker 2]

    TOKEN[Tokenize Pairs]
    INFER[Model Inference]
    SCORES[Compute Scores]

    UNSORT{Need Unsort?}
    UNSORT_YES[Restore Order]
    UNSORT_NO[Direct Pass]

    METRICS[Record Metrics]
    RESPONSE[gRPC Serialize]
    END([Return to Client])

    START --> GRPC
    GRPC --> SCHED
    SCHED --> SORT

    SORT -->|Yes| SORT_YES
    SORT -->|No| SORT_NO
    SORT_YES --> POOL
    SORT_NO --> POOL

    POOL --> ROUTE
    ROUTE -->|Round Robin| W1
    ROUTE -->|Round Robin| W2

    W1 --> TOKEN
    W2 --> TOKEN
    TOKEN --> INFER
    INFER --> SCORES

    SCORES --> UNSORT
    UNSORT -->|Yes| UNSORT_YES
    UNSORT -->|No| UNSORT_NO

    UNSORT_YES --> METRICS
    UNSORT_NO --> METRICS

    METRICS --> RESPONSE
    RESPONSE --> END

    style START fill:#e1f5ff
    style END fill:#e1ffe1
    style SORT fill:#fff4e1
    style ROUTE fill:#fff4e1
    style UNSORT fill:#fff4e1
    style INFER fill:#ffe1e1
```

---

## Performance Optimization Flow

```mermaid
graph TB
    subgraph "Optimization Techniques"
        DB[Dynamic Batching<br/>+35% throughput]
        LAB[Length-Aware Batching<br/>-25% latency]
        FP16[FP16 Precision<br/>+10-12% throughput]
        PROC[Process-Based Pool<br/>True Parallelism]
    end

    subgraph "Configuration"
        BATCH[Batch Size: 64]
        CONC[Concurrency: 2]
        TIMEOUT[Timeout: 20ms]
    end

    subgraph "Results"
        TP[Throughput: 719 p/s]
        LAT[Latency P50: 178ms]
        P99[Latency P99: 211ms]
        PAD[Padding: 32%]
    end

    DB --> BATCH
    LAB --> BATCH
    FP16 --> BATCH
    PROC --> CONC

    BATCH --> TP
    CONC --> TP
    TIMEOUT --> LAT
    LAB --> PAD

    TP --> RESULT[Production Ready]
    LAT --> RESULT
    P99 --> RESULT
    PAD --> RESULT

    style DB fill:#e1f5ff
    style LAB fill:#e1f5ff
    style FP16 fill:#e1f5ff
    style PROC fill:#e1f5ff
    style RESULT fill:#e1ffe1
```

---

## Deployment Architecture

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[Nginx / HAProxy]
    end

    subgraph "Server Instance 1"
        GRPC1[gRPC :50051]
        HTTP1[HTTP :8080]
        POOL1[Model Pool<br/>2 Workers]
    end

    subgraph "Server Instance 2"
        GRPC2[gRPC :50051]
        HTTP2[HTTP :8080]
        POOL2[Model Pool<br/>2 Workers]
    end

    subgraph "Monitoring"
        PROM[Prometheus]
        GRAF[Grafana]
    end

    CLIENTS[Clients] --> LB
    LB --> GRPC1
    LB --> GRPC2

    HTTP1 --> PROM
    HTTP2 --> PROM
    PROM --> GRAF

    style LB fill:#e1f5ff
    style GRPC1 fill:#fff4e1
    style GRPC2 fill:#fff4e1
    style PROM fill:#ffe1e1
    style GRAF fill:#e1ffe1
```

---

## Configuration Decision Tree

```mermaid
graph TD
    START{What's your<br/>priority?}

    START -->|Low Latency| LAT_SENS
    START -->|High Throughput| HIGH_TP
    START -->|Balanced| BALANCED

    LAT_SENS[Latency-Sensitive Config]
    LAT_SENS --> LAT_BATCH[Batch: 32]
    LAT_SENS --> LAT_CONC[Concurrency: 1]
    LAT_SENS --> LAT_TIMEOUT[Timeout: 10ms]
    LAT_BATCH --> LAT_RESULT[519 p/s @ 92ms]
    LAT_CONC --> LAT_RESULT
    LAT_TIMEOUT --> LAT_RESULT

    BALANCED[Balanced Config]
    BALANCED --> BAL_BATCH[Batch: 64]
    BALANCED --> BAL_CONC[Concurrency: 2]
    BALANCED --> BAL_TIMEOUT[Timeout: 20ms]
    BAL_BATCH --> BAL_RESULT[719 p/s @ 178ms]
    BAL_CONC --> BAL_RESULT
    BAL_TIMEOUT --> BAL_RESULT

    HIGH_TP[High-Throughput Config]
    HIGH_TP --> TP_BATCH[Batch: 96]
    HIGH_TP --> TP_CONC[Concurrency: 3]
    HIGH_TP --> TP_TIMEOUT[Timeout: 50ms]
    TP_BATCH --> TP_RESULT[776 p/s @ 369ms]
    TP_CONC --> TP_RESULT
    TP_TIMEOUT --> TP_RESULT

    style START fill:#e1f5ff
    style LAT_RESULT fill:#e1ffe1
    style BAL_RESULT fill:#e1ffe1
    style TP_RESULT fill:#e1ffe1
```

---

## Summary

This visual guide provides:

1. **System Overview** - High-level architecture
2. **Request Flow** - Detailed sequence diagram
3. **Model Pool** - Process-based parallelism
4. **Backend Hierarchy** - Class structure
5. **Metrics System** - Component composition
6. **Data Flow** - Request processing pipeline
7. **Performance Optimization** - Techniques and results
8. **Deployment** - Production architecture
9. **Configuration** - Decision tree for config selection

**Key Takeaway:** The system uses process-based parallelism for true concurrent inference on Apple Silicon, with dynamic and length-aware batching for optimal performance (719 p/s @ 178ms latency).
