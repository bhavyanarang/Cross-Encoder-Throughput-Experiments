import logging
import os

logger = logging.getLogger(__name__)


class ProcessMonitor:
    def __init__(self):
        self._process = None
        self._initialized = False

    def _init_process(self) -> None:
        if self._initialized:
            return
        try:
            import psutil

            self._process = psutil.Process(os.getpid())
            self._process.cpu_percent()
        except ImportError:
            self._process = None
        self._initialized = True

    def get_cpu_percent(self) -> float:
        self._init_process()
        if self._process:
            try:
                return self._process.cpu_percent(interval=None)
            except Exception:
                pass
        return 0.0
