#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

mkdir -p "$PROJECT_ROOT/data/prometheus"
mkdir -p "$PROJECT_ROOT/data/grafana"

echo "Starting observability services with Docker..."
docker compose up -d --remove-orphans

echo "Services are running."
echo "Prometheus: http://localhost:9091"
echo "Grafana: http://localhost:3001"
