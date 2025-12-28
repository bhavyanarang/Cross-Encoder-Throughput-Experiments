import threading
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.server.models import InferenceResult


@dataclass
class PendingRequest:
    pairs: list[tuple[str, str]]
    result_future: threading.Event
    result: "InferenceResult | None" = None
    submit_time: float = 0.0
