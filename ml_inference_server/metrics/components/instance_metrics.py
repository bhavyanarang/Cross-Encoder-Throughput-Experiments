"""
Per-Instance Metrics - Track utilization and idle time for each model instance.

Provides metrics for:
- Idle time percentage per model instance
- Request counts per instance
- Utilization tracking
"""

import time
import threading
from dataclasses import dataclass, field


@dataclass
class InstanceStats:
    """Statistics for a single model instance."""
    instance_id: int
    instance_name: str
    request_count: int = 0
    total_busy_time_s: float = 0.0
    total_idle_time_s: float = 0.0
    utilization_pct: float = 0.0
    idle_pct: float = 100.0
    is_busy: bool = False
    last_request_time: float = 0.0
    avg_request_latency_ms: float = 0.0


class InstanceMetricsTracker:
    """
    Tracks per-instance metrics for model pool.
    
    Thread-safe: uses internal locking for all operations.
    
    Usage:
        tracker = InstanceMetricsTracker()
        tracker.register_instance(0, "model-0")
        tracker.register_instance(1, "model-1")
        
        # When inference starts
        tracker.mark_busy(0)
        
        # When inference ends
        tracker.mark_idle(0, latency_ms=15.5)
        
        # Get stats
        stats = tracker.get_all_stats()
    """
    
    def __init__(self):
        self._instances: dict[int, dict] = {}
        self._lock = threading.Lock()
        self._start_time = time.time()
    
    def register_instance(self, instance_id: int, name: str = "") -> None:
        """
        Register a new model instance for tracking.
        
        Args:
            instance_id: Unique identifier for the instance
            name: Human-readable name (e.g., "minilm-0")
        """
        with self._lock:
            self._instances[instance_id] = {
                "name": name or f"instance-{instance_id}",
                "request_count": 0,
                "total_busy_time_s": 0.0,
                "busy_start_time": None,
                "is_busy": False,
                "latencies_ms": [],
                "last_request_time": 0.0,
            }
    
    def mark_busy(self, instance_id: int) -> None:
        """
        Mark an instance as busy (starting inference).
        
        Args:
            instance_id: Instance to mark as busy
        """
        with self._lock:
            if instance_id not in self._instances:
                return
            
            instance = self._instances[instance_id]
            instance["is_busy"] = True
            instance["busy_start_time"] = time.time()
    
    def mark_idle(self, instance_id: int, latency_ms: float = 0.0) -> None:
        """
        Mark an instance as idle (finished inference).
        
        Args:
            instance_id: Instance to mark as idle
            latency_ms: Latency of the completed request
        """
        with self._lock:
            if instance_id not in self._instances:
                return
            
            instance = self._instances[instance_id]
            now = time.time()
            
            # Calculate busy time for this request
            if instance["busy_start_time"] is not None:
                busy_duration = now - instance["busy_start_time"]
                instance["total_busy_time_s"] += busy_duration
            
            instance["is_busy"] = False
            instance["busy_start_time"] = None
            instance["request_count"] += 1
            instance["last_request_time"] = now
            
            if latency_ms > 0:
                instance["latencies_ms"].append(latency_ms)
                # Keep only last 100 latencies for memory efficiency
                if len(instance["latencies_ms"]) > 100:
                    instance["latencies_ms"] = instance["latencies_ms"][-100:]
    
    def get_instance_stats(self, instance_id: int) -> InstanceStats:
        """
        Get statistics for a specific instance.
        
        Args:
            instance_id: Instance to get stats for
            
        Returns:
            InstanceStats with utilization metrics
        """
        with self._lock:
            if instance_id not in self._instances:
                return InstanceStats(instance_id=instance_id, instance_name="unknown")
            
            return self._compute_stats(instance_id)
    
    def get_all_stats(self) -> list[InstanceStats]:
        """
        Get statistics for all registered instances.
        
        Returns:
            List of InstanceStats, one per instance
        """
        with self._lock:
            return [self._compute_stats(i) for i in sorted(self._instances.keys())]
    
    def _compute_stats(self, instance_id: int) -> InstanceStats:
        """Compute stats for an instance (must hold lock)."""
        instance = self._instances[instance_id]
        elapsed = time.time() - self._start_time
        
        # Calculate current busy time if currently busy
        total_busy = instance["total_busy_time_s"]
        if instance["is_busy"] and instance["busy_start_time"]:
            total_busy += time.time() - instance["busy_start_time"]
        
        # Calculate utilization percentage
        utilization_pct = (total_busy / elapsed * 100) if elapsed > 0 else 0.0
        idle_pct = 100.0 - utilization_pct
        
        # Calculate average latency
        latencies = instance["latencies_ms"]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        
        return InstanceStats(
            instance_id=instance_id,
            instance_name=instance["name"],
            request_count=instance["request_count"],
            total_busy_time_s=total_busy,
            total_idle_time_s=elapsed - total_busy,
            utilization_pct=round(utilization_pct, 2),
            idle_pct=round(idle_pct, 2),
            is_busy=instance["is_busy"],
            last_request_time=instance["last_request_time"],
            avg_request_latency_ms=round(avg_latency, 2),
        )
    
    def get_summary(self) -> dict:
        """
        Get summary of all instance metrics.
        
        Returns:
            Dictionary with instance metrics summary
        """
        all_stats = self.get_all_stats()
        
        if not all_stats:
            return {
                "num_instances": 0,
                "instances": [],
                "avg_utilization_pct": 0.0,
                "avg_idle_pct": 100.0,
                "total_requests": 0,
            }
        
        total_requests = sum(s.request_count for s in all_stats)
        avg_utilization = sum(s.utilization_pct for s in all_stats) / len(all_stats)
        
        return {
            "num_instances": len(all_stats),
            "instances": [
                {
                    "id": s.instance_id,
                    "name": s.instance_name,
                    "request_count": s.request_count,
                    "utilization_pct": s.utilization_pct,
                    "idle_pct": s.idle_pct,
                    "is_busy": s.is_busy,
                    "avg_latency_ms": s.avg_request_latency_ms,
                }
                for s in all_stats
            ],
            "avg_utilization_pct": round(avg_utilization, 2),
            "avg_idle_pct": round(100.0 - avg_utilization, 2),
            "total_requests": total_requests,
        }
    
    def get_history_snapshot(self) -> dict:
        """
        Get current utilization percentages for chart history.
        
        Returns:
            Dictionary with per-instance utilization for charts
        """
        all_stats = self.get_all_stats()
        
        return {
            "utilization_pct": [s.utilization_pct for s in all_stats],
            "idle_pct": [s.idle_pct for s in all_stats],
            "request_counts": [s.request_count for s in all_stats],
            "is_busy": [s.is_busy for s in all_stats],
        }
    
    def reset(self) -> None:
        """Reset all instance metrics."""
        with self._lock:
            for instance in self._instances.values():
                instance["request_count"] = 0
                instance["total_busy_time_s"] = 0.0
                instance["busy_start_time"] = None
                instance["is_busy"] = False
                instance["latencies_ms"] = []
                instance["last_request_time"] = 0.0
            self._start_time = time.time()


__all__ = ["InstanceMetricsTracker", "InstanceStats"]

