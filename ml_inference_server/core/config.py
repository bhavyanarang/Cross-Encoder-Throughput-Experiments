"""
Pydantic configuration models for type-safe configuration.

Replaces raw dict configuration with validated, typed models.
"""

from typing import Literal, Optional, Any
from pydantic import BaseModel, Field, model_validator


class ModelInstanceConfig(BaseModel):
    """Configuration for a single model instance."""
    
    name: str = Field(description="HuggingFace model name or path")
    device: str = Field(default="mps", description="Device to run on (mps, cpu, cuda)")
    backend: Literal["pytorch", "mps", "mlx", "onnx", "compiled"] = Field(
        default="mps",
        description="Backend implementation to use"
    )
    use_fp16: bool = Field(default=True, description="Use FP16 precision")
    compile_model: bool = Field(default=False, description="Use torch.compile")
    
    # Backend-specific options
    quantization_bits: int = Field(default=16, description="Quantization bits for MLX")
    onnx_optimize: bool = Field(default=True, description="Enable ONNX optimization")
    onnx_use_coreml: bool = Field(default=True, description="Use CoreML for ONNX")
    compile_mode: str = Field(default="reduce-overhead", description="torch.compile mode")


class ModelPoolConfig(BaseModel):
    """Configuration for the model pool (multi-model support)."""
    
    instances: list[ModelInstanceConfig] = Field(
        default_factory=list,
        description="List of model instances to load"
    )
    routing_strategy: Literal["round_robin", "least_busy"] = Field(
        default="round_robin",
        description="Strategy for routing requests to model instances"
    )


class BatchingConfig(BaseModel):
    """Configuration for request batching."""
    
    enabled: bool = Field(default=False, description="Enable dynamic batching")
    max_batch_size: int = Field(default=8, ge=1, description="Maximum batch size")
    timeout_ms: float = Field(default=100, ge=0, description="Batch timeout in milliseconds")
    length_aware_batching: bool = Field(
        default=False,
        description="Sort pairs by length to reduce padding"
    )


class ServerNetworkConfig(BaseModel):
    """Network configuration for servers."""
    
    host: str = Field(default="0.0.0.0", description="Server bind address")
    port: int = Field(default=50051, ge=1, le=65535, description="gRPC server port")
    http_port: int = Field(default=8080, ge=1, le=65535, description="HTTP metrics port")
    grpc_workers: int = Field(default=10, ge=1, description="gRPC thread pool workers")


class ExperimentConfig(BaseModel):
    """Configuration for running experiments."""
    
    batch_sizes: list[int] = Field(default=[1, 8, 16, 32], description="Batch sizes to test")
    concurrency_levels: list[int] = Field(default=[1], description="Concurrency levels to test")
    benchmark_requests: int = Field(default=100, ge=1, description="Requests per experiment")
    warmup_iterations: int = Field(default=10, ge=0, description="Warmup iterations")


class ScreenshotConfig(BaseModel):
    """Configuration for dashboard screenshots."""
    
    enabled: bool = Field(default=False, description="Enable automatic screenshots")
    output_dir: str = Field(
        default="docs/experiments/screenshots",
        description="Directory for screenshots"
    )


class LegacyModelConfig(BaseModel):
    """Legacy single-model configuration for backward compatibility."""
    
    name: str
    device: str = "mps"
    backend: str = "pytorch"
    quantized: bool = False
    quantization_mode: str = "fp16"
    
    # Backend-specific nested configs (legacy format)
    mps: dict = Field(default_factory=dict)
    mlx: dict = Field(default_factory=dict)
    onnx: dict = Field(default_factory=dict)
    compiled: dict = Field(default_factory=dict)


class ServerConfig(BaseModel):
    """Complete server configuration."""
    
    # New multi-model config
    model_pool: Optional[ModelPoolConfig] = Field(
        default=None,
        description="Multi-model pool configuration"
    )
    
    # Legacy single-model config (for backward compatibility)
    model: Optional[LegacyModelConfig] = Field(
        default=None,
        description="Legacy single-model configuration"
    )
    
    batching: BatchingConfig = Field(default_factory=BatchingConfig)
    server: ServerNetworkConfig = Field(default_factory=ServerNetworkConfig)
    experiment: ExperimentConfig = Field(default_factory=ExperimentConfig)
    screenshot: ScreenshotConfig = Field(default_factory=ScreenshotConfig)
    
    # Experiment metadata
    _experiment_name: str = ""
    _experiment_description: str = ""
    _experiment_path: str = ""
    
    @model_validator(mode="after")
    def ensure_model_config(self) -> "ServerConfig":
        """Ensure either model_pool or model is configured."""
        if self.model_pool is None and self.model is None:
            # Create default model config
            self.model = LegacyModelConfig(
                name="cross-encoder/ms-marco-MiniLM-L-6-v2"
            )
        return self
    
    def get_model_pool_config(self) -> ModelPoolConfig:
        """
        Get model pool config, converting from legacy format if needed.
        
        This provides backward compatibility with old single-model configs.
        """
        if self.model_pool is not None:
            return self.model_pool
        
        # Convert legacy config to model pool with single instance
        if self.model is not None:
            instance = self._convert_legacy_to_instance(self.model)
            return ModelPoolConfig(
                instances=[instance],
                routing_strategy="round_robin"
            )
        
        raise ValueError("No model configuration found")
    
    def _convert_legacy_to_instance(self, legacy: LegacyModelConfig) -> ModelInstanceConfig:
        """Convert legacy model config to ModelInstanceConfig."""
        # Extract backend-specific options
        use_fp16 = True
        compile_model = False
        quantization_bits = 16
        onnx_optimize = True
        onnx_use_coreml = True
        compile_mode = "reduce-overhead"
        
        if legacy.backend == "mps":
            use_fp16 = legacy.mps.get("fp16", True)
            compile_model = legacy.mps.get("compile", False)
        elif legacy.backend == "mlx":
            quantization_bits = legacy.mlx.get("bits", 16)
        elif legacy.backend == "onnx":
            onnx_optimize = legacy.onnx.get("optimize", True)
            onnx_use_coreml = legacy.onnx.get("use_gpu", True)
        elif legacy.backend == "compiled":
            compile_mode = legacy.compiled.get("mode", "reduce-overhead")
            use_fp16 = legacy.compiled.get("fp16", True)
        elif legacy.backend == "pytorch":
            if legacy.quantized and legacy.quantization_mode == "fp16":
                use_fp16 = True
        
        return ModelInstanceConfig(
            name=legacy.name,
            device=legacy.device,
            backend=legacy.backend,
            use_fp16=use_fp16,
            compile_model=compile_model,
            quantization_bits=quantization_bits,
            onnx_optimize=onnx_optimize,
            onnx_use_coreml=onnx_use_coreml,
            compile_mode=compile_mode,
        )


def load_config_from_dict(data: dict) -> ServerConfig:
    """
    Load ServerConfig from a dictionary, handling both new and legacy formats.
    
    Args:
        data: Configuration dictionary (e.g., from YAML)
        
    Returns:
        Validated ServerConfig instance
    """
    # Handle legacy 'model' key format
    if "model" in data and "model_pool" not in data:
        model_data = data.get("model", {})
        data["model"] = LegacyModelConfig(**model_data).model_dump()
    
    return ServerConfig(**data)

