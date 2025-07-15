# WarPy40K Syntax Highlighting for VS Code

A Visual Studio Code extension that provides rich syntax highlighting for the WarPy40K programming language.

> See the main [WarPy40K README](../README.md) for language features, interpreter, and linter usage.

## Features

- Syntax highlighting for `.wp40k` files
- Support for all WarPy40K language constructs:
  - Commands (e.g., `the_emperor_protects`, `for_the_emperor`)
  - Variable declarations and assignments
  - Loop constructs (`for`, `while`)
  - Conditional statements (`if`, `else`)
  - Data types (`dg`, `servitor`, `blob`, `psykers`, `void_shields`)
  - Operators (`+`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `..`, `:`)
  - Strings and numbers

## Installation

### Method 1: Install from VSIX (Recommended)

1. Download the latest `warpy40k-syntax-*.vsix` file from the releases or build it locally.
2. In VS Code, press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) and select `Extensions: Install from VSIX...`.
3. Select the `.vsix` file.
4. Open a `.wp40k` file to see syntax highlighting.

### Method 2: Development Install

1. Clone the repository and open the `warpy40k-syntax` folder in VS Code.
2. Press `F5` to launch an Extension Development Host window.
3. Open a `.wp40k` file to test the highlighting.

## Language Features

### Commands
```warpy40k
the_emperor_protects()
for_the_emperor()
burn_the_heretic("heretic")
```

### Variable Declarations
```warpy40k
i: dg = 0
name: servitor = "servant"
```

### Assignments
```warpy40k
i = i + 1
counter = 42
```

### Loops
```warpy40k
for i in 1..10:
    the_emperor_protects()

while x < 5:
    x = x + 1
```

### Conditionals
```warpy40k
if i > 0:
    for_the_emperor()
else:
    burn_the_heretic("traitor")
```

## Color Scheme

The extension uses your current VS Code color theme. Language elements are highlighted with distinct scopes:
- **Commands**: Function color
- **Keywords**: Control flow color
- **Types**: Storage type color
- **Variables**: Variable color
- **Strings**: String color
- **Numbers**: Number color
- **Operators**: Operator color

## Troubleshooting & FAQ

**Q: Syntax highlighting doesn't appear?**
- Make sure the extension is installed and enabled.
- Open a `.wp40k` file (or set the language mode to WarPy40K manually).
- Reload VS Code if needed.

**Q: How do I set the language mode manually?**
- Click the language indicator in the bottom right and select `WarPy40K`.

**Q: Can I customize the colors?**
- Yes! Add custom rules to your VS Code color theme using the provided scopes (see `syntaxes/warpy40k.tmLanguage.json`).

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Edit `syntaxes/warpy40k.tmLanguage.json` or related files
3. Test with a `.wp40k` file
4. Submit a pull request

## Support

If you encounter issues:
- Check the VS Code output/console for errors
- Create an issue on the GitHub repository
- Include the WarPy40K code that causes the problem

## License

This extension is part of the WarPy40K project. See `LICENSE` for details.

---

*For the Emperor!* 🛡️ 