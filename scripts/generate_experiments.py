#!/usr/bin/env python3
"""Generate structured experiment configs following the experiment plan."""

from pathlib import Path

import yaml

EXPERIMENTS_DIR = Path(__file__).parent.parent / "experiments"


def generate_backend_baseline():
    """Phase 1: Backend baseline experiments."""
    experiments = [
        {
            "name": "01_backend_pytorch",
            "description": "PyTorch backend baseline",
            "model": {"backend": "pytorch", "device": "mps", "quantization": "fp16"},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [1]},
        },
        {
            "name": "02_backend_mps",
            "description": "MPS backend baseline",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [1]},
        },
        {
            "name": "03_backend_mlx",
            "description": "MLX backend baseline",
            "model": {"backend": "mlx", "mlx": {"bits": 16, "group_size": 64}},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [1]},
        },
        {
            "name": "04_backend_compiled",
            "description": "torch.compile backend baseline",
            "model": {"backend": "compiled", "compiled": {"mode": "reduce-overhead", "fp16": True}},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [1]},
        },
    ]
    return experiments


def generate_batch_size_experiments():
    """Phase 2: Batch size optimization."""
    return [
        {
            "name": "05a_batch_size_mps",
            "description": "Batch size sweep on MPS backend",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "experiment": {
                "batch_sizes": [8, 16, 32, 48, 64, 96, 128, 192, 256],
                "concurrency_levels": [1],
            },
        },
        {
            "name": "05b_batch_size_mlx",
            "description": "Batch size sweep on MLX backend",
            "model": {"backend": "mlx", "mlx": {"bits": 16, "group_size": 64}},
            "experiment": {
                "batch_sizes": [8, 16, 32, 48, 64, 96, 128, 192, 256],
                "concurrency_levels": [1],
            },
        },
    ]


def generate_concurrency_experiments():
    """Phase 3: Concurrency optimization."""
    return [
        {
            "name": "06a_concurrency_mps",
            "description": "Concurrency sweep on MPS backend",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "experiment": {"batch_sizes": [96], "concurrency_levels": [1, 2, 4, 6, 8, 12]},
        },
        {
            "name": "06b_concurrency_mlx",
            "description": "Concurrency sweep on MLX backend",
            "model": {"backend": "mlx", "mlx": {"bits": 16, "group_size": 64}},
            "experiment": {"batch_sizes": [96], "concurrency_levels": [1, 2, 4, 6, 8, 12]},
        },
    ]


def generate_dynamic_batching_basic():
    """Phase 4: Dynamic batching basic comparison."""
    return [
        {
            "name": "07a_dynamic_batch_baseline",
            "description": "Baseline without dynamic batching",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "batching": {"enabled": False},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [4]},
        },
        {
            "name": "07b_dynamic_batch_enabled",
            "description": "Dynamic batching enabled",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "batching": {"enabled": True, "max_batch_size": 96, "timeout_ms": 50},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [4]},
        },
    ]


def generate_dynamic_batching_timeout():
    """Phase 5: Dynamic batching timeout sweep."""
    return [
        {
            "name": "08a_dynamic_batch_timeout_mps",
            "description": "Dynamic batching timeout sweep on MPS",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "batching": {"enabled": True, "max_batch_size": 96, "timeout_ms": 50},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [4]},
            # Note: timeout_ms will be varied manually or via script
        },
        {
            "name": "08b_dynamic_batch_timeout_mlx",
            "description": "Dynamic batching timeout sweep on MLX",
            "model": {"backend": "mlx", "mlx": {"bits": 16, "group_size": 64}},
            "batching": {"enabled": True, "max_batch_size": 96, "timeout_ms": 50},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [4]},
        },
    ]


def generate_dynamic_batching_max_batch():
    """Phase 6: Dynamic batching max batch size."""
    return [
        {
            "name": "09a_dynamic_batch_max_batch_mps",
            "description": "Dynamic batching max_batch_size sweep on MPS",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "batching": {"enabled": True, "max_batch_size": 96, "timeout_ms": 50},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [4]},
        },
        {
            "name": "09b_dynamic_batch_max_batch_mlx",
            "description": "Dynamic batching max_batch_size sweep on MLX",
            "model": {"backend": "mlx", "mlx": {"bits": 16, "group_size": 64}},
            "batching": {"enabled": True, "max_batch_size": 96, "timeout_ms": 50},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [4]},
        },
    ]


def generate_length_aware_experiments():
    """Phase 7: Length-aware batching."""
    return [
        {
            "name": "10a_padding_baseline",
            "description": "Baseline padding analysis - random ordering",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "batching": {"enabled": False, "length_aware_batching": False},
            "experiment": {"batch_sizes": [64], "concurrency_levels": [1]},
        },
        {
            "name": "10b_padding_length_aware",
            "description": "Length-aware batching - sorted by token length",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "batching": {
                "enabled": True,
                "max_batch_size": 64,
                "timeout_ms": 50,
                "length_aware_batching": True,
            },
            "experiment": {"batch_sizes": [64], "concurrency_levels": [1]},
        },
    ]


def generate_quantization_experiments():
    """Phase 8: Quantization comparison."""
    return [
        {
            "name": "11a_quantization_fp32",
            "description": "FP32 quantization baseline",
            "model": {"backend": "mps", "quantization": "fp32"},
            "experiment": {"batch_sizes": [96], "concurrency_levels": [1]},
        },
        {
            "name": "11b_quantization_fp16",
            "description": "FP16 quantization (baseline)",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "experiment": {"batch_sizes": [96], "concurrency_levels": [1]},
        },
    ]


def generate_max_length_experiments():
    """Phase 9: Max sequence length."""
    return [
        {
            "name": "12a_max_length_mps",
            "description": "Max sequence length sweep on MPS",
            "model": {"backend": "mps", "mps": {"fp16": True}, "max_length": 512},
            "experiment": {"batch_sizes": [64], "concurrency_levels": [1]},
            # Note: max_length will be varied manually
        },
        {
            "name": "12b_max_length_mlx",
            "description": "Max sequence length sweep on MLX",
            "model": {"backend": "mlx", "mlx": {"bits": 16, "group_size": 64}, "max_length": 512},
            "experiment": {"batch_sizes": [64], "concurrency_levels": [1]},
        },
    ]


def generate_multi_model_experiments():
    """Phase 10: Multi-model pool."""
    base_model = {
        "name": "cross-encoder/ms-marco-MiniLM-L-6-v2",
        "backend": "mps",
        "device": "mps",
        "use_fp16": True,
    }

    return [
        {
            "name": "13a_multi_model_2x",
            "description": "Two model instances with round-robin routing",
            "model_pool": {
                "instances": [base_model.copy(), base_model.copy()],
                "routing_strategy": "round_robin",
            },
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "batching": {"enabled": False},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [4]},
        },
        {
            "name": "13b_multi_model_3x",
            "description": "Three model instances with round-robin routing",
            "model_pool": {
                "instances": [base_model.copy() for _ in range(3)],
                "routing_strategy": "round_robin",
            },
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "batching": {"enabled": False},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [4]},
        },
        {
            "name": "13c_multi_model_4x",
            "description": "Four model instances with round-robin routing",
            "model_pool": {
                "instances": [base_model.copy() for _ in range(4)],
                "routing_strategy": "round_robin",
            },
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "batching": {"enabled": False},
            "experiment": {"batch_sizes": [32], "concurrency_levels": [4]},
        },
    ]


def generate_compile_mode_experiments():
    """Phase 11: Compilation modes."""
    return [
        {
            "name": "14a_compile_default",
            "description": "torch.compile with default mode",
            "model": {"backend": "compiled", "compiled": {"mode": "default", "fp16": True}},
            "experiment": {"batch_sizes": [64], "concurrency_levels": [1]},
        },
        {
            "name": "14b_compile_reduce_overhead",
            "description": "torch.compile with reduce-overhead mode",
            "model": {"backend": "compiled", "compiled": {"mode": "reduce-overhead", "fp16": True}},
            "experiment": {"batch_sizes": [64], "concurrency_levels": [1]},
        },
        {
            "name": "14c_compile_max_autotune",
            "description": "torch.compile with max-autotune mode",
            "model": {"backend": "compiled", "compiled": {"mode": "max-autotune", "fp16": True}},
            "experiment": {"batch_sizes": [64], "concurrency_levels": [1]},
        },
    ]


def generate_optimal_combined():
    """Phase 12: Combined optimizations."""
    return [
        {
            "name": "15a_optimal_mps",
            "description": "MPS with optimal settings from all phases",
            "model": {"backend": "mps", "mps": {"fp16": True}},
            "batching": {
                "enabled": True,
                "max_batch_size": 96,
                "timeout_ms": 50,
                "length_aware_batching": True,
            },
            "experiment": {"batch_sizes": [96], "concurrency_levels": [4]},
        },
        {
            "name": "15b_optimal_mlx",
            "description": "MLX with optimal settings from all phases",
            "model": {"backend": "mlx", "mlx": {"bits": 16, "group_size": 64}},
            "batching": {
                "enabled": True,
                "max_batch_size": 96,
                "timeout_ms": 50,
                "length_aware_batching": True,
            },
            "experiment": {"batch_sizes": [96], "concurrency_levels": [4]},
        },
    ]


def save_experiment(exp_config: dict):
    """Save experiment config to YAML file."""
    output_file = EXPERIMENTS_DIR / f"{exp_config['name']}.yaml"

    # Remove name from config (it's in filename)
    config = {k: v for k, v in exp_config.items() if k != "name"}

    with open(output_file, "w") as f:
        f.write(f"# Experiment {exp_config['name']}\n")
        f.write(f'name: "{exp_config["name"]}"\n')
        f.write(f'description: "{exp_config["description"]}"\n\n')
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Generated: {output_file}")


def main():
    """Generate all structured experiments."""
    print("Generating structured experiment configs...")
    print("=" * 60)

    all_experiments = []
    all_experiments.extend(generate_backend_baseline())
    all_experiments.extend(generate_batch_size_experiments())
    all_experiments.extend(generate_concurrency_experiments())
    all_experiments.extend(generate_dynamic_batching_basic())
    all_experiments.extend(generate_dynamic_batching_timeout())
    all_experiments.extend(generate_dynamic_batching_max_batch())
    all_experiments.extend(generate_length_aware_experiments())
    all_experiments.extend(generate_quantization_experiments())
    all_experiments.extend(generate_max_length_experiments())
    all_experiments.extend(generate_multi_model_experiments())
    all_experiments.extend(generate_compile_mode_experiments())
    all_experiments.extend(generate_optimal_combined())

    print(f"\nTotal experiments to generate: {len(all_experiments)}\n")

    for exp in all_experiments:
        save_experiment(exp)

    print("\n" + "=" * 60)
    print(f"Generated {len(all_experiments)} experiment configs")
    print("Experiments follow the structured plan in EXPERIMENT_PLAN.md")


if __name__ == "__main__":
    main()
