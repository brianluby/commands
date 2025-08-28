#!/bin/bash
# Run validation tests for Claude Code commands

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🧪 Running Claude Code Command Validation Tests..."
echo "================================================"

# Run Python validation framework
python3 "$SCRIPT_DIR/test_framework.py" --path "$PROJECT_ROOT" --output "$SCRIPT_DIR/validation_report.md"

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ All validation tests passed!"
else
    echo "❌ Validation tests failed. Check the report for details."
    cat "$SCRIPT_DIR/validation_report.md"
    exit 1
fi

# Optional: Run specific command tests
if [ -f "$SCRIPT_DIR/test_commands.py" ]; then
    echo ""
    echo "🔧 Running command-specific tests..."
    python3 "$SCRIPT_DIR/test_commands.py"
fi

echo ""
echo "📊 Validation report saved to: tests/validation_report.md"