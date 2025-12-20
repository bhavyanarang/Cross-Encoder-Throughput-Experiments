#!/bin/bash
# Lint the codebase using ruff

cd "$(dirname "$0")"
source venv/bin/activate

echo "Running ruff linter..."
ruff check ml_inference_server/

echo ""
echo "Running ruff formatter check..."
ruff format --check ml_inference_server/

