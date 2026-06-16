# WarPy40K

A toy programming language that uses expressions and terminology from the Warhammer 40K universe.

## Overview

WarPy40K is a simple interpreted language that incorporates concepts and keywords from the Warhammer 40K universe. It's designed to be fun and educational, demonstrating how to build a simple programming language interpreter.

## Features

- **Warhammer 40K Themed Expressions**: Special keywords like `Inquisition`, `Emperor`, `Chaos`, `Purge`, `Exterminatus`, `Bless`, and `Curse`
- **Standard Programming Constructs**: Variables, arithmetic operations, comparisons, logical operators
- **Built-in Functions**: `print()`, `random()`, `abs()`, `min()`, `max()`, `pow()`
- **Built-in Constants**: `FAITH`, `CORRUPTION`, `POPULATION`
- **Interactive REPL**: Command-line interface for interactive coding
- **File Execution**: Run WarPy40K scripts from files

## Installation

```bash
# Clone the repository
git clone https://github.com/dcasseb/WarPy40K.git
cd WarPy40K

# Install in development mode
pip install -e .

# Or install from PyPI (when available)
pip install WarPy40K
```

## Usage

### Command Line

```bash
# Run a WarPy40K file
warpy40k my_script.wp40k

# Execute a single line of code
warpy40k -c "Inquisition Emperor + Chaos"

# Start interactive REPL
warpy40k -i

# Display tokens instead of executing
warpy40k --tokens my_script.wp40k

# Display AST instead of executing
warpy40k --ast my_script.wp40k
```

### Python Module

```python
from warpy40k import evaluate

# Evaluate a WarPy40K expression
result = evaluate("Bless Emperor 100")
print(result)  # Output: 110.0

# Or use the components directly
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser
from warpy40k.interpreter import Interpreter

source = "1 + 2 * 3"
lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
interpreter = Interpreter()
result = interpreter.execute(ast)
```

## Language Reference

### Basic Syntax

```
# Comments
# This is a comment

# Variables
x = 42
y = 100

# Arithmetic
1 + 2     # Addition
5 - 3     # Subtraction
2 * 3     # Multiplication
6 / 2     # Division
2 ^ 3     # Power (2^3 = 8)

# Comparison
1 == 2    # Equal
1 != 2    # Not equal
1 > 2     # Greater than
1 < 2     # Less than
1 >= 2    # Greater than or equal
1 <= 2    # Less than or equal

# Logical operators
True AND False
True OR False
NOT True

# Parentheses for grouping
(1 + 2) * 3
```

### Warhammer 40K Expressions

| Expression | Description | Example | Result |
|------------|-------------|---------|--------|
| `Inquisition` | Truth/judgment - evaluates target's truthiness | `Inquisition 42` | `True` |
| `Inquisition` | Without target, returns True | `Inquisition` | `True` |
| `Emperor` | Divine power - multiplies target by faith factor | `Emperor 100` | `100.0` |
| `Emperor` | Without target, returns high value | `Emperor` | `1000` |
| `Chaos` | Corruption/randomness - adds randomness to target | `Chaos 100` | `100 + random` |
| `Chaos` | Without target, returns random value | `Chaos` | `0-100` |
| `Purge x` | Destruction - sets target to zero/empty | `Purge 42` | `0` |
| `Exterminatus x` | Total annihilation - destroys target | `Exterminatus 42` | `None` |
| `Bless x` | Positive modification - increases target by 10% | `Bless 100` | `110.0` |
| `Curse x` | Negative modification - decreases target by 10% | `Curse 100` | `90.0` |

### Built-in Constants

- `FAITH` - Default faith value (100)
- `CORRUPTION` - Default corruption level (0)
- `POPULATION` - Default population (1,000,000)

### Built-in Functions

- `print(x)` - Print value to console
- `random()` - Return random float between 0 and 1
- `abs(x)` - Absolute value
- `min(x, y, ...)` - Minimum value
- `max(x, y, ...)` - Maximum value
- `pow(x, y)` - x raised to power y

## Examples

### Simple Arithmetic

```
# Basic math
result = 2 + 3 * 4
print(result)  # Output: 14

# With parentheses
result = (2 + 3) * 4
print(result)  # Output: 20
```

### Using WarPy40K Expressions

```
# Inquisition - judgment
faithful = Inquisition FAITH
print(faithful)  # Output: True

# Emperor - divine power
blessedValue = Emperor 100
print(blessedValue)  # Output: 100.0

# Chaos - corruption
corruptedValue = Chaos 100
print(corruptedValue)  # Output: 100 + random factor

# Purge - destruction
purified = Purge 42
print(purified)  # Output: 0

# Bless and Curse
blessed = Bless 100
cursed = Curse 100
print(blessed)  # Output: 110.0
print(cursed)   # Output: 90.0
```

### Complex Example

```
# Calculate the Emperor's blessing on a planet's population
planetPopulation = 1000000
blessedPopulation = Bless Emperor planetPopulation
print("Blessed population:", blessedPopulation)

# Check if a heretic should be purged
faithLevel = 50
shouldPurge = NOT Inquisition faithLevel
print("Should purge:", shouldPurge)  # Output: Should purge: False

# Chaos corruption effect
corruptionLevel = 10
corruptedValue = Chaos 100
print("Corrupted value:", corruptedValue)
```

## Project Structure

```
WarPy40K/
├── src/
│   └── warpy40k/
│       ├── __init__.py      # Package initialization and evaluate function
│       ├── __main__.py      # Command-line entry point
│       ├── tokens.py        # Token definitions
│       ├── lexer.py         # Lexical analyzer
│       ├── parser.py        # Parser (creates AST)
│       ├── ast.py           # Abstract Syntax Tree nodes
│       └── interpreter.py   # Interpreter (executes AST)
├── tests/
│   ├── __init__.py
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_interpreter.py
├── pyproject.toml           # Project configuration
├── README.md
└── .gitignore
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src/warpy40k

# Run specific test file
pytest tests/test_lexer.py
```

### Code Formatting

```bash
# Format code with black
black src/ tests/

# Sort imports
isort src/ tests/
```

### Type Checking

```bash
mypy src/warpy40k
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the Warhammer 40K universe created by Games Workshop
- Built with Python's excellent standard library
- Thanks to all contributors and users

**For the Emperor!**
