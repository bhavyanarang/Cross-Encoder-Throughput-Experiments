#!/bin/bash
# Check server metrics (if server is running)
# Usage: ./check_metrics.sh

echo "=== Fetching metrics from http://localhost:8080/metrics ==="
echo ""

METRICS=$(curl -s http://localhost:8080/metrics 2>/dev/null)

if [ -z "$METRICS" ] || echo "$METRICS" | grep -q "Connection refused\|Failed to connect"; then
    echo "  ✗ Server is not running or not accessible"
    echo ""
    exit 1
fi

# Pretty print key metrics
echo "$METRICS" | python3 << 'PYTHON'
import sys
import json

try:
    data = json.load(sys.stdin)

    print("Key Metrics:")
    print("  throughput_qps:", data.get("throughput_qps", "N/A"))
    print("  avg_ms:", data.get("avg_ms", "N/A"))
    print("  p95_ms:", data.get("p95_ms", "N/A"))
    print("  p99_ms:", data.get("p99_ms", "N/A"))
    print("")

    print("Stage Timings:")
    stages = data.get("stage_timings", {})
    print("  tokenize_ms:", stages.get("avg_tokenize_ms", "N/A"))
    print("  inference_ms:", stages.get("avg_inference_ms", "N/A"))
    print("  queue_wait_ms:", stages.get("avg_queue_wait_ms", "N/A"))
    print("  overhead_ms:", stages.get("avg_overhead_ms", "N/A"))
    print("  mp_queue_send_ms:", stages.get("avg_mp_queue_send_ms", "N/A"))
    print("  mp_queue_receive_ms:", stages.get("avg_mp_queue_receive_ms", "N/A"))
    print("")

    print("Resource Usage:")
    print("  gpu_memory_mb:", data.get("gpu_memory_mb", "N/A"))
    print("  cpu_percent:", data.get("cpu_percent", "N/A"))
    print("  estimated_gpu_utilization_pct:", data.get("estimated_gpu_utilization_pct", "N/A"))
    print("")

    print("Full JSON (first 2000 chars):")
    json_str = json.dumps(data, indent=2)
    print(json_str[:2000])
    if len(json_str) > 2000:
        print("... (truncated)")

except Exception as e:
    print(f"Error parsing metrics: {e}")
    print("Raw output:")
    sys.stdin.seek(0)
    print(sys.stdin.read()[:2000])
PYTHON

echo ""

