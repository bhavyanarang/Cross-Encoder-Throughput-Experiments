#!/usr/bin/env python3
"""
Run systematic experiments sequentially.

This script:
1. Runs experiments in numbered order (01_*, 02_*, etc.)
2. Takes a screenshot of the dashboard after each experiment
3. Includes full experiment config in results
4. Determines findings from each step before proceeding
"""

import os
import sys
import subprocess
import time
import signal
import logging
import json
import yaml
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

# Add ml_inference_server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "ml_inference_server"))
from utils.config_loader import load_experiment_config

EXPERIMENTS_DIR = Path(__file__).parent / "ml_inference_server" / "experiments"
OUTPUT_DIR = Path(__file__).parent / "ml_inference_server" / "docs" / "experiments"
SCREENSHOTS_DIR = OUTPUT_DIR / "screenshots"


def take_screenshot(experiment_name: str) -> str:
    """Take a screenshot of the dashboard using macOS screencapture."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = SCREENSHOTS_DIR / f"{experiment_name}_{timestamp}.png"
    
    try:
        # Use macOS screencapture - captures the entire screen
        # -x: no sound, -C: capture cursor
        subprocess.run(
            ["screencapture", "-x", str(screenshot_path)],
            timeout=5
        )
        logger.info(f"Screenshot saved: {screenshot_path}")
        return str(screenshot_path)
    except Exception as e:
        logger.warning(f"Failed to take screenshot: {e}")
        return ""


def save_results_with_config(results: list, config: dict, output_file: Path, screenshot_path: str = ""):
    """Save experiment results with full config to markdown file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    experiment_name = config.get('_experiment_name', 'unnamed')
    description = config.get('_experiment_description', 'N/A')
    backend = config['model'].get('backend', 'pytorch')
    device = config['model']['device']
    batching_enabled = config.get('batching', {}).get('enabled', False)
    
    with open(output_file, "w") as f:
        f.write(f"# {experiment_name}\n\n")
        f.write(f"**Description:** {description}\n\n")
        f.write(f"**Timestamp:** {timestamp}\n\n")
        
        # Full Configuration
        f.write("## Experiment Configuration\n\n")
        f.write("```yaml\n")
        # Remove internal metadata keys
        config_to_print = {k: v for k, v in config.items() if not k.startswith('_')}
        f.write(yaml.dump(config_to_print, default_flow_style=False, sort_keys=False))
        f.write("```\n\n")
        
        # Screenshot reference
        if screenshot_path:
            rel_path = os.path.relpath(screenshot_path, output_file.parent)
            f.write(f"## Dashboard Screenshot\n\n")
            f.write(f"![Dashboard]({rel_path})\n\n")
        
        # Results Summary
        f.write("## Results Summary\n\n")
        f.write(f"**Backend:** `{backend}` | **Device:** `{device}` | **Dynamic Batching:** `{batching_enabled}`\n\n")
        
        f.write("| Batch | Conc | Pairs | Time(s) | Lat Avg | Lat P95 | Lat P99 | TP Avg | TP P95 |\n")
        f.write("|-------|------|-------|---------|---------|---------|---------|--------|--------|\n")
        
        for r in results:
            if 'error' in r:
                f.write(f"| {r['batch_size']} | {r['concurrency']} | ERROR | - | - | - | - | - | - |\n")
            else:
                f.write(f"| {r['batch_size']} | {r['concurrency']} | {r['total_pairs']} | "
                        f"{r['total_time_s']:.2f} | {r['latency_avg_ms']:.1f}ms | {r['latency_p95_ms']:.1f}ms | "
                        f"{r['latency_p99_ms']:.1f}ms | {r['throughput_avg']:.1f} | {r['throughput_p95']:.1f} |\n")
        
        # Analysis
        successful = [r for r in results if 'error' not in r]
        if successful:
            best_throughput = max(successful, key=lambda x: x['throughput_avg'])
            best_latency = min(successful, key=lambda x: x['latency_avg_ms'])
            avg_throughput = sum(r['throughput_avg'] for r in successful) / len(successful)
            avg_latency = sum(r['latency_avg_ms'] for r in successful) / len(successful)
            
            f.write(f"\n## Key Findings\n\n")
            f.write(f"| Metric | Value | Configuration |\n")
            f.write(f"|--------|-------|---------------|\n")
            f.write(f"| **Best Throughput** | {best_throughput['throughput_avg']:.1f} pairs/s | batch={best_throughput['batch_size']}, conc={best_throughput['concurrency']} |\n")
            f.write(f"| **Best Latency** | {best_latency['latency_avg_ms']:.1f}ms | batch={best_latency['batch_size']}, conc={best_latency['concurrency']} |\n")
            f.write(f"| Avg Throughput | {avg_throughput:.1f} pairs/s | across all configs |\n")
            f.write(f"| Avg Latency | {avg_latency:.1f}ms | across all configs |\n")
    
    logger.info(f"Results saved to {output_file}")
    return successful


def run_experiment(experiment_path: Path) -> dict:
    """Run a single experiment and return results."""
    experiment_name = experiment_path.stem
    logger.info(f"\n{'='*80}")
    logger.info(f"Starting experiment: {experiment_name}")
    logger.info(f"Config: {experiment_path}")
    logger.info(f"{'='*80}\n")
    
    # Load config for metadata
    config = load_experiment_config(str(experiment_path))
    
    # Determine Python executable
    venv_python = Path(__file__).parent / "venv" / "bin" / "python"
    python_exec = str(venv_python) if venv_python.exists() else sys.executable
    
    # Start server
    logger.info("Starting inference server...")
    server_cmd = [
        python_exec,
        "ml_inference_server/main.py",
        "--experiment", str(experiment_path)
    ]
    
    server_process = subprocess.Popen(
        server_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Wait for server to be ready
    logger.info("Waiting for server to initialize (15s)...")
    time.sleep(15)
    
    if server_process.poll() is not None:
        logger.error("Server failed to start!")
        stdout, _ = server_process.communicate()
        logger.error(f"Server output:\n{stdout}")
        return {"success": False, "error": "Server failed to start", "config": config}
    
    output_file = OUTPUT_DIR / f"{experiment_name}_results.md"
    
    try:
        # Run client benchmark
        logger.info("Running benchmark...")
        client_cmd = [
            python_exec,
            "ml_inference_server/client.py",
            "--experiment",
            "--config", str(experiment_path),
            "--output", str(output_file)
        ]
        
        result = subprocess.run(
            client_cmd,
            capture_output=True,
            text=True,
            timeout=900  # 15 minute timeout
        )
        
        if result.returncode != 0:
            logger.error(f"Benchmark failed!")
            logger.error(f"STDERR:\n{result.stderr}")
            return {"success": False, "error": result.stderr, "config": config}
        
        logger.info("Benchmark completed!")
        
        # Wait a moment for metrics to stabilize
        time.sleep(2)
        
        # Take screenshot of dashboard
        logger.info("Taking dashboard screenshot...")
        screenshot_path = take_screenshot(experiment_name)
        
        return {
            "success": True,
            "config": config,
            "output_file": str(output_file),
            "screenshot": screenshot_path
        }
        
    except subprocess.TimeoutExpired:
        logger.error("Benchmark timed out!")
        return {"success": False, "error": "Timeout", "config": config}
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"success": False, "error": str(e), "config": config}
        
    finally:
        logger.info("Stopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()
        time.sleep(3)


def get_numbered_experiments() -> list:
    """Get experiments that start with a number (e.g., 01_, 02_)."""
    experiments = []
    for f in EXPERIMENTS_DIR.glob("*.yaml"):
        if f.name != "base_config.yaml" and f.stem[0].isdigit():
            experiments.append(f)
    return sorted(experiments, key=lambda x: x.stem)


def main():
    """Run all numbered experiments sequentially."""
    experiments = get_numbered_experiments()
    
    if not experiments:
        logger.error("No numbered experiments found (e.g., 01_*, 02_*)")
        logger.info("Available configs:")
        for f in EXPERIMENTS_DIR.glob("*.yaml"):
            logger.info(f"  - {f.name}")
        return 1
    
    logger.info(f"\n{'='*80}")
    logger.info("SYSTEMATIC EXPERIMENT SUITE")
    logger.info(f"{'='*80}")
    logger.info(f"Found {len(experiments)} experiments:")
    for exp in experiments:
        logger.info(f"  - {exp.stem}")
    logger.info(f"{'='*80}\n")
    
    # Ask for confirmation
    input("Press Enter to start experiments (Ctrl+C to cancel)...")
    
    results = {}
    for experiment_path in experiments:
        result = run_experiment(experiment_path)
        results[experiment_path.stem] = result
        
        if not result["success"]:
            logger.warning(f"Experiment {experiment_path.stem} failed: {result.get('error', 'Unknown')}")
            cont = input("Continue with next experiment? (y/n): ")
            if cont.lower() != 'y':
                break
        else:
            logger.info(f"✓ {experiment_path.stem} completed successfully")
    
    # Print summary
    logger.info(f"\n{'='*80}")
    logger.info("EXPERIMENT SUMMARY")
    logger.info(f"{'='*80}")
    
    for exp_name, result in results.items():
        status = "✓ SUCCESS" if result["success"] else f"✗ FAILED: {result.get('error', 'Unknown')[:50]}"
        logger.info(f"{exp_name:<30} {status}")
    
    logger.info(f"{'='*80}")
    logger.info(f"Results saved to: {OUTPUT_DIR}")
    logger.info(f"Screenshots saved to: {SCREENSHOTS_DIR}")
    
    return 0 if all(r["success"] for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())

