#!/bin/bash
# Download and setup Prometheus and Grafana locally

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BIN_DIR="$PROJECT_ROOT/bin"

# Versions
PROM_VERSION="2.53.0"
GRAFANA_VERSION="11.0.0"

mkdir -p "$BIN_DIR"
cd "$BIN_DIR"

# Prometheus
if [ ! -d "prometheus-$PROM_VERSION.linux-amd64" ]; then
    echo "Downloading Prometheus $PROM_VERSION..."
    wget -q "https://github.com/prometheus/prometheus/releases/download/v$PROM_VERSION/prometheus-$PROM_VERSION.linux-amd64.tar.gz"
    tar xzf "prometheus-$PROM_VERSION.linux-amd64.tar.gz"
    rm "prometheus-$PROM_VERSION.linux-amd64.tar.gz"
    echo "Prometheus installed."
else
    echo "Prometheus already installed."
fi

# Grafana
if [ ! -d "grafana-v$GRAFANA_VERSION" ]; then
    echo "Downloading Grafana $GRAFANA_VERSION..."
    wget -q "https://dl.grafana.com/oss/release/grafana-$GRAFANA_VERSION.linux-amd64.tar.gz"
    tar xzf "grafana-$GRAFANA_VERSION.linux-amd64.tar.gz"
    rm "grafana-$GRAFANA_VERSION.linux-amd64.tar.gz"
    echo "Grafana installed."
else
    echo "Grafana already installed."
fi

echo "Setup complete. Binaries are in $BIN_DIR"
