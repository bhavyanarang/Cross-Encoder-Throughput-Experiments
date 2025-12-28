#!/bin/bash
# Monitor ports + main process every 2 seconds
# Usage: ./monitor_processes.sh
# Stop with Ctrl+C

echo "Monitoring processes and ports every 2 seconds..."
echo "Press Ctrl+C to stop"
echo ""

while true; do
    date
    echo "  Port 50051:"
    lsof -nP -iTCP:50051 -sTCP:LISTEN 2>/dev/null || echo "    Free"
    echo "  Port 8080:"
    lsof -nP -iTCP:8080 -sTCP:LISTEN 2>/dev/null || echo "    Free"
    echo "  Main processes:"
    pgrep -af "python.*src\.main" 2>/dev/null || echo "    None"
    echo ""
    sleep 2
done
