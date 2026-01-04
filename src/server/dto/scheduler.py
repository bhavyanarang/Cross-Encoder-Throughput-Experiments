import threading
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.server.dto import InferenceResult


@dataclass
class PendingRequest:
    pairs: list[tuple[str, str]]
    result_future: threading.Event
    result: Optional["InferenceResult"] = None
    submit_time: float = 0.0
    error: Optional[Exception] = None
