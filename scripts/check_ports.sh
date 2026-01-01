#!/bin/bash
# Check for port conflicts (orphaned servers)
# Usage: ./check_ports.sh

echo "=== Checking ports 50051 (gRPC) and 8080 (HTTP) ==="
echo ""

echo "Port 50051 (gRPC):"
lsof -nP -iTCP:50051 -sTCP:LISTEN || echo "  ✓ Free"

echo ""
echo "Port 8080 (HTTP):"
lsof -nP -iTCP:8080 -sTCP:LISTEN || echo "  ✓ Free"

echo ""
