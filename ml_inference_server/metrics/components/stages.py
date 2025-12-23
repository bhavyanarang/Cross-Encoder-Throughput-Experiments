"""
Stage Metrics - Tracks per-stage timing statistics.
"""

import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Dict

import numpy as np


@dataclass
class StageStats:
    """Statistics for a single stage."""
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    avg_ms: float = 0.0
    count: int = 0


@dataclass
class StageMetrics:
    """
    Container for per-stage timing statistics.
    
    Tracks latencies for a single stage (e.g., tokenization, inference).
    """
    
    latencies: list = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    def record(self, duration_ms: float) -> None:
        """Record a timing measurement."""
        with self._lock:
            self.latencies.append(duration_ms)
    
    def get_stats(self) -> StageStats:
        """Get P50/P95/P99 statistics."""
        with self._lock:
            if not self.latencies:
                return StageStats()
            
            arr = np.array(self.latencies)
            return StageStats(
                p50_ms=float(np.percentile(arr, 50)),
                p95_ms=float(np.percentile(arr, 95)),
                p99_ms=float(np.percentile(arr, 99)),
                avg_ms=float(np.mean(arr)),
                count=len(arr),
            )
    
    def reset(self) -> None:
        """Reset all measurements."""
        with self._lock:
            self.latencies = []


@dataclass
class StageMetricsGroup:
    """
    Group of stage metrics for the inference pipeline.
    
    Tracks timing for each stage:
    - grpc_receive: Time to deserialize gRPC request
    - tokenize: Time to tokenize pairs
    - queue_wait: Time request waited in queue
    - model_inference: GPU forward pass time
    - grpc_send: Time to serialize + send response
    """
    
    grpc_receive: StageMetrics = field(default_factory=StageMetrics)
    tokenize: StageMetrics = field(default_factory=StageMetrics)
    queue_wait: StageMetrics = field(default_factory=StageMetrics)
    model_inference: StageMetrics = field(default_factory=StageMetrics)
    grpc_send: StageMetrics = field(default_factory=StageMetrics)
    
    # Recent timings for history charts
    recent_tokenize: deque = field(default_factory=lambda: deque(maxlen=200))
    recent_inference: deque = field(default_factory=lambda: deque(maxlen=200))
    recent_queue_wait: deque = field(default_factory=lambda: deque(maxlen=200))
    
    # Last values for live display
    last_tokenize_ms: float = 0.0
    last_inference_ms: float = 0.0
    last_queue_wait_ms: float = 0.0
    
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    def record(
        self,
        t_grpc_receive: float = 0.0,
        t_tokenize: float = 0.0,
        t_queue_wait: float = 0.0,
        t_model_inference: float = 0.0,
        t_grpc_send: float = 0.0,
    ) -> None:
        """
        Record per-stage timing measurements.
        
        Args:
            t_grpc_receive: Time to deserialize gRPC request (ms)
            t_tokenize: Time to tokenize pairs (ms)
            t_queue_wait: Time request waited in queue (ms)
            t_model_inference: GPU forward pass time (ms)
            t_grpc_send: Time to serialize + send response (ms)
        """
        now = time.time()
        
        with self._lock:
            if t_grpc_receive > 0:
                self.grpc_receive.record(t_grpc_receive)
            
            if t_tokenize > 0:
                self.tokenize.record(t_tokenize)
                self.last_tokenize_ms = t_tokenize
                self.recent_tokenize.append((now, t_tokenize))
            
            if t_queue_wait > 0:
                self.queue_wait.record(t_queue_wait)
                self.last_queue_wait_ms = t_queue_wait
                self.recent_queue_wait.append((now, t_queue_wait))
            
            if t_model_inference > 0:
                self.model_inference.record(t_model_inference)
                self.last_inference_ms = t_model_inference
                self.recent_inference.append((now, t_model_inference))
            
            if t_grpc_send > 0:
                self.grpc_send.record(t_grpc_send)
    
    def get_all_stats(self) -> Dict[str, StageStats]:
        """Get statistics for all stages."""
        return {
            "grpc_receive": self.grpc_receive.get_stats(),
            "tokenize": self.tokenize.get_stats(),
            "queue_wait": self.queue_wait.get_stats(),
            "model_inference": self.model_inference.get_stats(),
            "grpc_send": self.grpc_send.get_stats(),
        }
    
    def get_percentages(self, total_avg_ms: float) -> Dict[str, float]:
        """
        Get stage percentages of total latency.
        
        Args:
            total_avg_ms: Average total latency in ms
            
        Returns:
            Dict with tokenize_pct, inference_pct, other_pct
        """
        if total_avg_ms <= 0:
            return {"tokenize_pct": 0.0, "inference_pct": 0.0, "other_pct": 100.0}
        
        tokenize_stats = self.tokenize.get_stats()
        inference_stats = self.model_inference.get_stats()
        
        tokenize_pct = tokenize_stats.avg_ms / total_avg_ms * 100
        inference_pct = inference_stats.avg_ms / total_avg_ms * 100
        other_pct = 100 - tokenize_pct - inference_pct
        
        return {
            "tokenize_pct": round(tokenize_pct, 1),
            "inference_pct": round(inference_pct, 1),
            "other_pct": round(other_pct, 1),
        }
    
    def get_queue_wait_analysis(self, total_avg_ms: float) -> Dict:
        """
        Get queue wait time analysis.
        
        Args:
            total_avg_ms: Average total latency in ms
            
        Returns:
            Dict with queue wait stats and percentage of total
        """
        stats = self.queue_wait.get_stats()
        queue_pct = (stats.avg_ms / total_avg_ms * 100) if total_avg_ms > 0 else 0
        
        return {
            "avg_ms": round(stats.avg_ms, 2),
            "p50_ms": round(stats.p50_ms, 2),
            "p95_ms": round(stats.p95_ms, 2),
            "p99_ms": round(stats.p99_ms, 2),
            "count": stats.count,
            "queue_pct_of_latency": round(queue_pct, 1),
            "last_ms": round(self.last_queue_wait_ms, 2),
        }
    
    def reset(self) -> None:
        """Reset all stage metrics."""
        with self._lock:
            self.grpc_receive.reset()
            self.tokenize.reset()
            self.queue_wait.reset()
            self.model_inference.reset()
            self.grpc_send.reset()
            self.recent_tokenize.clear()
            self.recent_inference.clear()
            self.recent_queue_wait.clear()
            self.last_tokenize_ms = 0.0
            self.last_inference_ms = 0.0
            self.last_queue_wait_ms = 0.0


__all__ = ["StageMetrics", "StageMetricsGroup", "StageStats"]

