import numpy as np


def compute_latency_stats(latencies: list) -> dict:
    if not latencies:
        return {"avg_ms": 0, "p50_ms": 0, "p95_ms": 0, "p99_ms": 0}
    arr = np.array(latencies)
    return {
        "avg_ms": float(np.mean(arr)),
        "p50_ms": float(np.percentile(arr, 50)),
        "p95_ms": float(np.percentile(arr, 95)),
        "p99_ms": float(np.percentile(arr, 99)),
    }
