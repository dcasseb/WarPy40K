#!/bin/bash

# WarPy40K Sublime Text Syntax Highlighting Installer

echo "Installing WarPy40K Syntax Highlighting for Sublime Text..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine Sublime Text packages directory based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    SUBLIME_PACKAGES="$HOME/Library/Application Support/Sublime Text/Packages/User"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows
    SUBLIME_PACKAGES="$APPDATA/Sublime Text/Packages/User"
else
    # Linux - try Sublime Text 4 first, then fallback to ST3
    if [ -d "$HOME/.config/sublime-text/Packages/User" ]; then
        SUBLIME_PACKAGES="$HOME/.config/sublime-text/Packages/User"
    else
        SUBLIME_PACKAGES="$HOME/.config/sublime-text-3/Packages/User"
    fi
fi

# Create the User packages directory if it doesn't exist
mkdir -p "$SUBLIME_PACKAGES"

# Copy the syntax file
echo "Copying syntax file to: $SUBLIME_PACKAGES"
cp "$SCRIPT_DIR/WarPy40K.sublime-syntax" "$SUBLIME_PACKAGES/"

# Copy the settings file
echo "Copying settings file to: $SUBLIME_PACKAGES"
cp "$SCRIPT_DIR/WarPy40K.sublime-settings" "$SUBLIME_PACKAGES/"

if [ $? -eq 0 ]; then
    echo "✅ WarPy40K Syntax Highlighting installed successfully!"
    echo ""
    echo "To test the syntax highlighting:"
    echo "1. Open Sublime Text"
    echo "2. Create a new file with .wp40k extension"
    echo "3. Start typing WarPy40K code to see syntax highlighting"
    echo ""
    echo "Example:"
    echo "  the_emperor_protects()"
    echo "  i: dg = 0"
    echo "  for i in 1..5:"
    echo "      for_the_emperor()"
    echo ""
    echo "If syntax highlighting doesn't appear automatically:"
    echo "1. Open a .wp40k file"
    echo "2. Go to View → Syntax → User → WarPy40K"
    echo "3. Or press Ctrl+Shift+P and type 'Set Syntax: WarPy40K'"
else
    echo "❌ Failed to install syntax highlighting"
    exit 1
fi 