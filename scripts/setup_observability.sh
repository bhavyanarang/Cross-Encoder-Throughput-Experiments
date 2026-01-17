#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

mkdir -p "$PROJECT_ROOT/data/prometheus"
mkdir -p "$PROJECT_ROOT/data/grafana"

echo "Pulling observability images..."
docker compose pull
