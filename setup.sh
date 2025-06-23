#!/bin/bash
#
# Setup script for awesome-secure-mcp-servers development environment
#

set -e

echo "🛡️ Setting up awesome-secure-mcp-servers development environment..."

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -f "data/servers.json" ]; then
    echo "❌ Error: Please run this script from the awesome-secure-mcp-servers root directory"
    exit 1
fi

# Check Node.js version
echo "📦 Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed. Please install Node.js 16 or later."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Error: Node.js version 16 or later is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Check Python version
echo "🐍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
echo "✅ Python version: $PYTHON_VERSION"

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install --user bandit safety semgrep requests packaging PyGithub

# Install optional security tools
echo "🔧 Installing optional security tools..."

# Try to install additional tools (non-fatal if they fail)
if command -v npm &> /dev/null; then
    echo "  Installing retire.js..."
    npm install -g retire || echo "  ⚠️  Failed to install retire.js (optional)"
fi

if command -v go &> /dev/null; then
    echo "  Installing gosec..."
    go install github.com/securecodewarrior/gosec/v2/cmd/gosec@latest || echo "  ⚠️  Failed to install gosec (optional)"
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.py
chmod +x setup.sh

# Validate data schema
echo "✅ Validating data schema..."
npm run validate

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Available commands:"
echo "  npm run validate          - Validate server data"
echo "  npm run security-scan     - Run security scanning"
echo "  npm run generate-report   - Generate security report"
echo "  npm test                  - Run all validation tests"
echo ""
echo "To get started:"
echo "  1. Review the data/servers.json file"
echo "  2. Run 'npm run validate' to check data integrity"
echo "  3. Run 'npm run security-scan' to perform security validation"
echo ""
echo "For more information, see README.md and CONTRIBUTING.md"