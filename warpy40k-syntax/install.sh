#!/bin/bash

# WarPy40K Syntax Highlighting Extension Installer

echo "Installing WarPy40K Syntax Highlighting Extension..."

# Check if VS Code is installed
if ! command -v code &> /dev/null; then
    echo "Error: VS Code is not installed or not in PATH"
    echo "Please install VS Code first: https://code.visualstudio.com/"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if we're in the right directory
if [ ! -f "$SCRIPT_DIR/package.json" ]; then
    echo "Error: package.json not found. Please run this script from the warpy40k-syntax directory."
    exit 1
fi

# Install the extension
echo "Installing extension from: $SCRIPT_DIR"
code --install-extension "$SCRIPT_DIR"

if [ $? -eq 0 ]; then
    echo "✅ WarPy40K Syntax Highlighting Extension installed successfully!"
    echo ""
    echo "To test the extension:"
    echo "1. Open VS Code"
    echo "2. Create a new file with .wp40k extension"
    echo "3. Start typing WarPy40K code to see syntax highlighting"
    echo ""
    echo "Example:"
    echo "  the_emperor_protects()"
    echo "  i: dg = 0"
    echo "  for i in 1..5:"
    echo "      for_the_emperor()"
else
    echo "❌ Failed to install extension"
    exit 1
fi 