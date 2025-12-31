#!/bin/bash
# Count processes before/after server runs
# Usage: ./count_processes.sh [before|after]
# Run "before" before starting server, "after" after stopping

MODE="${1:-before}"

echo "=== Process count check ($MODE) ==="
echo ""

echo "Main server processes (python.*src.main):"
MAIN=$(pgrep -af "python.*src\.main" 2>/dev/null || true)
if [ -z "$MAIN" ]; then
    echo "  ✓ None found"
    MAIN_COUNT=0
else
    echo "$MAIN"
    MAIN_COUNT=$(echo "$MAIN" | wc -l | tr -d ' ')
fi

echo ""
echo "All Python processes:"
PYTHON_COUNT=$(ps aux | grep -E "python" | grep -v grep | wc -l | tr -d ' ')
echo "  Count: $PYTHON_COUNT"

echo ""
echo "Summary:"
echo "  Main processes: $MAIN_COUNT"
echo "  Total Python: $PYTHON_COUNT"
echo ""

# Save to file for comparison
OUTPUT_FILE="/tmp/process_count_${MODE}.txt"
echo "Main: $MAIN_COUNT" > "$OUTPUT_FILE"
echo "Python: $PYTHON_COUNT" >> "$OUTPUT_FILE"
echo "Saved to: $OUTPUT_FILE"

