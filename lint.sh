#!/bin/bash
# Lint the codebase using ruff

set -e  # Exit on error

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: venv directory not found. Please create a virtual environment first."
    exit 1
fi

# Activate venv
source venv/bin/activate

# Check if ruff is installed, install if not
if ! command -v ruff &> /dev/null; then
    echo "ruff not found. Installing ruff..."
    pip install -q ruff>=0.1.0
fi

echo "Running ruff linter (with auto-fix)..."
if ! ruff check --fix --unsafe-fixes ml_inference_server/; then
    echo "Some linting errors could not be auto-fixed. Please review manually."
    exit 1
fi

echo ""
echo "Running ruff formatter (auto-formatting)..."
ruff format ml_inference_server/

echo ""
echo "All checks passed and fixes applied!"
