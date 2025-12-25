"""Benchmark models."""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkState:
    """State container for benchmark execution."""

    interrupted: bool = False

    def handle_interrupt(self, signum, frame):
        self.interrupted = True
        logger.warning("\nInterrupt received - finishing current operation...")
