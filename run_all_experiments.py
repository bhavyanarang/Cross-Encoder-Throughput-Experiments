#!/usr/bin/env python3
"""
Run all experiments sequentially.

This script:
1. Lists all experiment configs
2. For each experiment:
   - Starts the server with that config
   - Runs the client benchmark
   - Stops the server
   - Saves results to separate markdown files
"""

import os
import sys
import subprocess
import time
import signal
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

# Add ml_inference_server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "ml_inference_server"))
from utils.config_loader import list_available_experiments


def run_experiment(experiment_path: str, output_dir: str = "ml_inference_server/docs/experiments"):
    """Run a single experiment."""
    experiment_name = Path(experiment_path).stem
    logger.info(f"\n{'='*80}")
    logger.info(f"Starting experiment: {experiment_name}")
    logger.info(f"Config: {experiment_path}")
    logger.info(f"{'='*80}\n")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{experiment_name}_results.md")
    
    # Start server
    logger.info("Starting inference server...")
    server_cmd = [
        sys.executable,
        "ml_inference_server/main.py",
        "--experiment", experiment_path
    ]
    
    server_process = subprocess.Popen(
        server_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Wait for server to be ready
    logger.info("Waiting for server to initialize...")
    time.sleep(10)  # Give server time to load model
    
    # Check if server is still running
    if server_process.poll() is not None:
        logger.error("Server failed to start!")
        stdout, _ = server_process.communicate()
        logger.error(f"Server output:\n{stdout}")
        return False
    
    try:
        # Run client benchmark
        logger.info("Running benchmark...")
        client_cmd = [
            sys.executable,
            "ml_inference_server/client.py",
            "--experiment",
            "--config", experiment_path,
            "--output", output_file
        ]
        
        result = subprocess.run(
            client_cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode != 0:
            logger.error(f"Client benchmark failed!")
            logger.error(f"STDOUT:\n{result.stdout}")
            logger.error(f"STDERR:\n{result.stderr}")
            return False
        
        logger.info(f"Benchmark completed successfully!")
        logger.info(f"Results saved to: {output_file}")
        
        return True
        
    except subprocess.TimeoutExpired:
        logger.error("Benchmark timed out!")
        return False
        
    except Exception as e:
        logger.error(f"Error running benchmark: {e}")
        return False
        
    finally:
        # Stop server
        logger.info("Stopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            logger.warning("Server didn't stop gracefully, killing...")
            server_process.kill()
            server_process.wait()
        
        # Give system time to clean up
        time.sleep(2)


def main():
    """Run all experiments."""
    # List all experiments
    experiments = list_available_experiments()
    
    if not experiments:
        logger.error("No experiments found in ml_inference_server/experiments/")
        return 1
    
    logger.info(f"Found {len(experiments)} experiments:")
    for exp in experiments:
        logger.info(f"  - {Path(exp).stem}")
    
    # Run each experiment
    results = {}
    for experiment_path in experiments:
        experiment_name = Path(experiment_path).stem
        success = run_experiment(experiment_path)
        results[experiment_name] = success
        
        if not success:
            logger.warning(f"Experiment {experiment_name} failed, continuing with next...")
    
    # Print summary
    logger.info(f"\n{'='*80}")
    logger.info("EXPERIMENT SUMMARY")
    logger.info(f"{'='*80}")
    
    for exp_name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        logger.info(f"{exp_name:<30} {status}")
    
    logger.info(f"{'='*80}\n")
    
    # Return exit code
    failed_count = sum(1 for success in results.values() if not success)
    if failed_count > 0:
        logger.warning(f"{failed_count} experiment(s) failed")
        return 1
    
    logger.info("All experiments completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

