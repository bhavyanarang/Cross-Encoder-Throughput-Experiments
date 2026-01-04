#!/bin/bash
# Download and setup Prometheus and Grafana locally

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BIN_DIR="$PROJECT_ROOT/bin"

# Versions
PROM_VERSION="2.53.0"
GRAFANA_VERSION="11.0.0"

# Detect OS and architecture
OS=$(uname -s)
ARCH=$(uname -m)

if [ "$OS" = "Darwin" ]; then
    PROM_OS="darwin"
    if [ "$ARCH" = "arm64" ]; then
        PROM_ARCH="arm64"
    else
        PROM_ARCH="amd64"
    fi
    GRAFANA_OS="darwin"
    GRAFANA_ARCH="$ARCH"
else
    PROM_OS="linux"
    PROM_ARCH="amd64"
    GRAFANA_OS="linux"
    GRAFANA_ARCH="amd64"
fi

mkdir -p "$BIN_DIR"
cd "$BIN_DIR"

# Prometheus
PROM_DIRNAME="prometheus-$PROM_VERSION.$PROM_OS-$PROM_ARCH"
if [ ! -d "$PROM_DIRNAME" ]; then
    echo "Downloading Prometheus $PROM_VERSION for $PROM_OS-$PROM_ARCH..."
    curl -sL "https://github.com/prometheus/prometheus/releases/download/v$PROM_VERSION/$PROM_DIRNAME.tar.gz" -o "prometheus-temp.tar.gz"
    tar xzf "prometheus-temp.tar.gz"
    rm "prometheus-temp.tar.gz"
    echo "Prometheus installed."
else
    echo "Prometheus already installed."
fi

# Grafana
GRAFANA_DIRNAME="grafana-v$GRAFANA_VERSION"
if [ ! -d "$GRAFANA_DIRNAME" ]; then
    echo "Downloading Grafana $GRAFANA_VERSION for $GRAFANA_OS-$GRAFANA_ARCH..."
    curl -sL "https://dl.grafana.com/oss/release/grafana-$GRAFANA_VERSION.$GRAFANA_OS-$GRAFANA_ARCH.tar.gz" -o "grafana-temp.tar.gz"
    tar xzf "grafana-temp.tar.gz"
    rm "grafana-temp.tar.gz"
    echo "Grafana installed."
else
    echo "Grafana already installed."
fi

echo "Setup complete. Binaries are in $BIN_DIR"
