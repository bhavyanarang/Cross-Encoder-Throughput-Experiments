"""Configuration models."""

from typing import Literal

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    name: str = Field(description="HuggingFace model name")
    device: str = "mps"
    backend: Literal["pytorch", "mps", "mlx", "onnx", "compiled", "tensorrt"] = "mps"
    quantization: Literal["fp32", "fp16", "int8", "int4"] = "fp16"
    compile_model: bool = False
    max_length: int = 512
    onnx_optimize: bool = True


class PoolConfig(BaseModel):
    instances: list[ModelConfig] = Field(default_factory=list)


class TokenizerPoolConfig(BaseModel):
    enabled: bool = True
    num_workers: int = 3
    model_name: str = ""  # If empty, uses same model as inference


class BatchConfig(BaseModel):
    enabled: bool = False
    max_batch_size: int = 8
    timeout_ms: float = 100
    length_aware: bool = False


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    grpc_port: int = 50051
    http_port: int = 8080
    grpc_workers: int = 10


class Config(BaseModel):
    model_pool: PoolConfig = Field(default_factory=PoolConfig)
    tokenizer_pool: TokenizerPoolConfig = Field(default_factory=TokenizerPoolConfig)
    batching: BatchConfig = Field(default_factory=BatchConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    name: str = ""
    description: str = ""
