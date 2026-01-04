#!/bin/bash
# Start Prometheus and Grafana locally

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BIN_DIR="$PROJECT_ROOT/bin"
LOG_DIR="$PROJECT_ROOT/logs"

mkdir -p "$LOG_DIR"

# Versions (must match setup script)
PROM_DIR=$(ls -d "$BIN_DIR"/prometheus-*.linux-amd64 2>/dev/null | head -n 1)
GRAFANA_DIR=$(ls -d "$BIN_DIR"/grafana-* 2>/dev/null | head -n 1)

if [ -z "$PROM_DIR" ] || [ -z "$GRAFANA_DIR" ]; then
    echo "Binaries not found. Please run scripts/setup_observability.sh first."
    exit 1
fi

# Start Prometheus (always restart to pick up config changes)
echo "Stopping any existing Prometheus..."
pkill -9 -f "prometheus --config.file" 2>/dev/null || true
sleep 2

echo "Starting Prometheus..."
nohup "$PROM_DIR/prometheus" \
    --config.file="$PROJECT_ROOT/conf/prometheus/prometheus.yml" \
    --storage.tsdb.path="$PROJECT_ROOT/data/prometheus" \
    --web.listen-address="0.0.0.0:9091" \
    > "$LOG_DIR/prometheus.log" 2>&1 &
echo "Prometheus started (PID: $!) on port 9091."

# Start Grafana (always restart to pick up config changes)
echo "Stopping any existing Grafana..."
pkill -9 -f "grafana-server" 2>/dev/null || true
sleep 2

echo "Starting Grafana..."
cd "$GRAFANA_DIR"
# Create custom config to point provisioning to our project
cat > conf/custom.ini <<EOF
[paths]
provisioning = $PROJECT_ROOT/conf/grafana/provisioning
[server]
http_port = 3001
[auth.anonymous]
enabled = true
org_role = Admin
[security]
admin_password = admin
admin_user = admin
EOF

nohup ./bin/grafana-server \
    --config=conf/custom.ini \
    --homepath="$GRAFANA_DIR" \
    > "$LOG_DIR/grafana.log" 2>&1 &
echo "Grafana started (PID: $!)."
cd "$PROJECT_ROOT"

echo "Services are running."
echo "Prometheus: http://localhost:9091"
echo "Grafana: http://localhost:3001"
