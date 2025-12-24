"""Metrics DTOs."""

from dataclasses import dataclass


@dataclass
class LatencyStats:
    count: int = 0
    avg_ms: float = 0.0
    min_ms: float = 0.0
    max_ms: float = 0.0
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0


@dataclass
class ThroughputStats:
    instant_qps: float = 0.0
    avg_qps: float = 0.0
    total_queries: int = 0
    total_requests: int = 0


@dataclass
class PaddingStats:
    avg_padding_pct: float = 0.0
    p50_padding_pct: float = 0.0
    p95_padding_pct: float = 0.0
    total_wasted_pct: float = 0.0


@dataclass
class StageStats:
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    avg_ms: float = 0.0
    count: int = 0
