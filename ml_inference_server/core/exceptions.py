"""
Custom exception hierarchy for the ML inference server.

Provides specific exception types for different error scenarios,
enabling better error handling and debugging.
"""


class InferenceServerError(Exception):
    """Base exception for all inference server errors."""

    pass


class BackendError(InferenceServerError):
    """Error in backend operations."""

    pass


class ModelLoadError(BackendError):
    """Failed to load model into memory."""

    def __init__(self, model_name: str, reason: str):
        self.model_name = model_name
        self.reason = reason
        super().__init__(f"Failed to load model '{model_name}': {reason}")


class InferenceError(BackendError):
    """Error during model inference."""

    def __init__(self, message: str, batch_size: int = 0):
        self.batch_size = batch_size
        super().__init__(message)


class ConfigurationError(InferenceServerError):
    """Invalid or missing configuration."""

    def __init__(self, message: str, field: str = ""):
        self.field = field
        super().__init__(message)


class RoutingError(InferenceServerError):
    """Error in model pool routing."""

    def __init__(self, message: str, strategy: str = ""):
        self.strategy = strategy
        super().__init__(message)
