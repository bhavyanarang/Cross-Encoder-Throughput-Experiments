#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

mkdir -p "$PROJECT_ROOT/data/prometheus"
mkdir -p "$PROJECT_ROOT/data/grafana"

echo "Starting observability services (prometheus + grafana)..."
docker compose up -d prometheus grafana --remove-orphans

echo "Services are running."
echo "Prometheus: http://localhost:9091"
echo "Grafana: http://localhost:3001"
