#!/bin/bash
# Monitor metrics every 2 seconds (no >10s sleep constraint)
# Usage: ./monitor_metrics.sh
# Stop with Ctrl+C

echo "Monitoring metrics every 2 seconds..."
echo "Press Ctrl+C to stop"
echo ""

while true; do
    date
    METRICS=$(curl -s http://localhost:8080/metrics 2>/dev/null)
    if [ -n "$METRICS" ] && ! echo "$METRICS" | grep -q "Connection refused\|Failed to connect"; then
        echo "$METRICS" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    print(f"  throughput: {d.get(\"throughput_qps\", 0):.2f} QPS")
    print(f"  avg_ms: {d.get(\"avg_ms\", 0):.2f} ms")
    print(f"  gpu_mem: {d.get(\"gpu_memory_mb\", 0):.2f} MB")
    print(f"  cpu: {d.get(\"cpu_percent\", 0):.2f}%")
except:
    print("  (error parsing)")
'
    else
        echo "  Server not accessible"
    fi
    echo ""
    sleep 2
done

