#!/bin/bash
# Lint the codebase using ruff

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
    echo "Error: venv directory not found."
    exit 1
fi

source venv/bin/activate

if ! command -v ruff &> /dev/null; then
    echo "Installing ruff..."
    pip install -q ruff>=0.1.0
fi

echo "Running ruff linter..."
ruff check --fix --unsafe-fixes src/ tests/

echo ""
echo "Running ruff formatter..."
ruff format src/ tests/

echo ""
echo "All checks passed!"
