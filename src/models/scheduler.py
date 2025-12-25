"""Scheduler models."""

import threading
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import InferenceResult


@dataclass
class PendingRequest:
    """Pending request for scheduler queue."""

    pairs: list[tuple[str, str]]
    result_future: threading.Event
    result: "InferenceResult | None" = None
    submit_time: float = 0.0
