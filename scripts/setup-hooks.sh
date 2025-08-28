#!/bin/bash
# Setup pre-commit hooks for Claude Code Commands

set -e

echo "🔧 Setting up pre-commit hooks..."

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit || {
        echo "❌ Failed to install pre-commit. Please install manually:"
        echo "   pip install pre-commit"
        echo "   or"
        echo "   brew install pre-commit"
        exit 1
    }
fi

# Install the pre-commit hooks
echo "🔗 Installing hooks..."
pre-commit install

# Run hooks on all files to check current state
echo "🧪 Running initial validation..."
pre-commit run --all-files || {
    echo ""
    echo "⚠️  Some files need fixes. This is normal for initial setup."
    echo "The hooks will run automatically on future commits."
}

echo ""
echo "✅ Pre-commit hooks installed successfully!"
echo ""
echo "Hooks will run automatically before each commit to:"
echo "  - Validate command structure"
echo "  - Check naming conventions"
echo "  - Verify version metadata"
echo "  - Fix markdown formatting"
echo "  - Ensure consistent line endings"
echo ""
echo "To run manually: pre-commit run --all-files"
echo "To skip hooks: git commit --no-verify"