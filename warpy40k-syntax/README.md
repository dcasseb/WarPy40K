# WarPy40K Syntax Highlighting

A VS Code extension that provides syntax highlighting for the WarPy40K programming language.

## Features

- Syntax highlighting for `.wp40k` files
- Support for all WarPy40K language constructs:
  - Commands (the_emperor_protects, for_the_emperor, etc.)
  - Variable declarations and assignments
  - Loop constructs (for, while)
  - Conditional statements (if, else)
  - Data types (dg, servitor, blob, psykers, void_shields)
  - Operators (+, =, ==, !=, <, >, <=, >=, .., :)
  - Strings and numbers
  - Comments (#)

## Installation

1. Clone this repository
2. Open the `warpy40k-syntax` folder in VS Code
3. Press `F5` to run the extension in a new Extension Development Host window
4. Open a `.wp40k` file to see the syntax highlighting

## Language Features

### Commands
All WarPy40K commands are highlighted as functions:
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

### Comments
```warpy40k
# This is a comment
i: dg = 0  # Initialize counter
```

## Color Scheme

The extension uses standard VS Code color themes and will adapt to your current theme. Different language elements are highlighted with distinct colors:

- **Commands**: Function color
- **Keywords**: Control flow color
- **Types**: Storage type color
- **Variables**: Variable color
- **Strings**: String color
- **Numbers**: Number color
- **Operators**: Operator color
- **Comments**: Comment color

## Contributing

Feel free to submit issues and enhancement requests!

## License

This extension is part of the WarPy40K project. 