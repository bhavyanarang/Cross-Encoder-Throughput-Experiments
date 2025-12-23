"""
Proto module - gRPC protocol buffer definitions.

Re-exports generated pb2 modules for cleaner imports.
"""

import os
import sys

# Add proto directory to path for imports
_proto_dir = os.path.dirname(os.path.abspath(__file__))
if _proto_dir not in sys.path:
    sys.path.insert(0, _proto_dir)

# Import generated modules
try:
    from . import inference_pb2
    from . import inference_pb2_grpc
except ImportError:
    # Fallback for when running from different working directory
    import inference_pb2
    import inference_pb2_grpc

__all__ = ["inference_pb2", "inference_pb2_grpc"]

