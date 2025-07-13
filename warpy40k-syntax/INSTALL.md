# WarPy40K Syntax Highlighting Extension - Installation Guide

## Quick Installation

### Method 1: Using the Install Script (Recommended)
```bash
cd warpy40k-syntax
./install.sh
```

### Method 2: Manual Installation
1. Open VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Extensions: Install from VSIX..."
4. Navigate to the `warpy40k-syntax` folder and select it

### Method 3: Development Installation
1. Clone the repository
2. Open the `warpy40k-syntax` folder in VS Code
3. Press `F5` to run the extension in a new Extension Development Host window

## Testing the Extension

1. Create a new file with `.wp40k` extension
2. Add some WarPy40K code:

```warpy40k
# Test the syntax highlighting
i: dg = 0
for i in 1..5:
    the_emperor_protects()
    if i > 3:
        for_the_emperor()
    else:
        burn_the_heretic("test")
```

3. You should see:
   - Comments in green
   - Commands in red/bold
   - Keywords (for, if, else) in purple/bold
   - Variables in light blue
   - Types (dg) in teal/italic
   - Numbers in light green
   - Operators in white

## Using the WarPy40K Dark Theme

1. Press `Ctrl+K Ctrl+T` (or `Cmd+K Cmd+T` on Mac)
2. Select "WarPy40K Dark" from the theme list
3. Enjoy the Warhammer 40K inspired color scheme!

## Features Included

### Syntax Highlighting
- ✅ All WarPy40K commands
- ✅ Variable declarations and assignments
- ✅ Loop constructs (for, while)
- ✅ Conditional statements (if, else)
- ✅ Data types (dg, servitor, blob, psykers, void_shields)
- ✅ Operators (+, =, ==, !=, <, >, <=, >=, .., :)
- ✅ Strings and numbers
- ✅ Comments (#)

### Editor Features
- ✅ Auto-closing brackets and quotes
- ✅ Comment support
- ✅ Indentation rules
- ✅ Code folding

### Custom Theme
- ✅ Dark theme with Warhammer 40K inspired colors
- ✅ Commands highlighted in bold red
- ✅ Types in italic teal
- ✅ Keywords in bold purple

## Troubleshooting

### Extension Not Working
1. Check if VS Code is up to date
2. Try reloading VS Code (`Ctrl+Shift+P` → "Developer: Reload Window")
3. Check the Extensions panel for any error messages

### Syntax Highlighting Not Appearing
1. Make sure the file has `.wp40k` extension
2. Check if the language mode is set to "WarPy40K" (bottom-right corner)
3. Try manually setting the language mode: `Ctrl+Shift+P` → "Change Language Mode" → "WarPy40K"

### Theme Not Available
1. Make sure the extension is properly installed
2. Try reloading VS Code
3. Check if the theme appears in the theme selector

## Uninstalling

To uninstall the extension:
1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for "WarPy40K"
4. Click the gear icon and select "Uninstall"

## Contributing

To contribute to the syntax highlighting:
1. Fork the repository
2. Make your changes to the grammar file (`syntaxes/warpy40k.tmLanguage.json`)
3. Test with the development installation method
4. Submit a pull request

## Support

If you encounter any issues:
1. Check the VS Code Developer Console for errors
2. Create an issue on the GitHub repository
3. Include the WarPy40K code that's causing problems

---

**For the Emperor!** 🛡️ 