#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SCRIPT_DIR"

if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: No virtual environment found (.venv or venv)."
    exit 1
fi

if ! command -v ruff &> /dev/null; then
    echo "Installing ruff..."
    pip install -q ruff>=0.1.0
fi

echo "Fixing trailing whitespace..."
find . -type f \( -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "*.md" -o -name "*.json" -o -name "*.toml" -o -name "*.idx" \) \
    -not -path "./.venv/*" -not -path "./venv/*" -not -path "./.git/*" \
    -exec sed -i '' 's/[[:space:]]*$//' {} \; 2>/dev/null || true

echo "Fixing end of files (ensuring newline)..."
find . -type f \( -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "*.md" -o -name "*.json" -o -name "*.toml" -o -name "*.idx" \) \
    -not -path "./.venv/*" -not -path "./venv/*" -not -path "./.git/*" \
    -exec sh -c 'test -s "$1" && test "$(tail -c 1 "$1" | wc -l)" -eq 0 && echo >> "$1"' _ {} \; 2>/dev/null || true

echo ""
echo "Running ruff linter..."
ruff check --fix --unsafe-fixes .

echo ""
echo "Running ruff formatter..."
ruff format .

echo ""
echo "All checks passed!"
