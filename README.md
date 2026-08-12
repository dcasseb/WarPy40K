# WarPy40K

**Current version: 0.8**

A toy interpreted programming language that uses expressions and terminology inspired by the Warhammer 40K universe.

## Overview

WarPy40K is an educational interpreted language built in Python. It combines conventional programming constructs with Warhammer 40K-themed expressions such as `Inquisition`, `Emperor`, `Chaos`, `Purge`, `Exterminatus`, `Bless`, and `Curse`.

The project is currently at **version 0.8**. The lexer, recursive-descent parser, Abstract Syntax Tree (AST), tree-walking interpreter, command-line interface, REPL, variables, expressions, assignments, conditionals, blocks, and built-in functions are already implemented.

The codebase also contains internal infrastructure for `while` loops: `WhileLoopNode` exists in the AST, `_parse_while_statement()` exists in the parser, and the interpreter can execute a `WhileLoopNode`. However, source-level `while` dispatch is currently disabled in the normal parser flow.

For that reason, **WarPy40K v0.8 is not yet claimed to be Turing complete**. Once unrestricted looping is exposed through the surface language and validated end-to-end, the existing combination of mutable variables, integer arithmetic, comparisons, conditional branching, and loop execution should provide the machinery needed for a constructive demonstration of Turing completeness.

## Development Status — v0.8

| Capability | Status | Notes |
|---|---|---|
| Lexer / tokenization | ✅ Implemented | Handles literals, operators, identifiers, punctuation, and WarPy40K keywords |
| Recursive-descent parser | ✅ Implemented | Parses the currently supported surface language |
| Abstract Syntax Tree | ✅ Implemented | Includes expressions, assignments, conditionals, blocks, calls, returns, and loop nodes |
| Tree-walking interpreter | ✅ Implemented | Executes the AST directly |
| Variables and mutable assignment | ✅ Implemented | Variables are stored in the interpreter environment |
| Arithmetic | ✅ Implemented | `+`, `-`, `*`, `/`, `^` |
| Comparisons | ✅ Implemented | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| Boolean logic | ✅ Implemented | `AND`, `OR`, `NOT` |
| `if` / `else` | ✅ Implemented | Conditional branching is supported |
| Blocks | ✅ Implemented | Grouped statements are represented and executed |
| Built-in function calls | ✅ Implemented | I/O, randomness, math helpers, and utilities |
| User-defined functions | ❌ Not implemented | Calls currently resolve names from the interpreter environment |
| `while` AST node | ✅ Implemented | `WhileLoopNode` exists |
| `while` runtime execution | ✅ Implemented | Interpreter executes a `WhileLoopNode` without an artificial iteration limit |
| `while` surface syntax | ⚠️ Partial | Parser routine exists, but normal `while` dispatch is disabled |
| Turing completeness | ❌ Not yet claimed | Surface language currently lacks an accessible unbounded loop or equivalent recursion mechanism |

### Why v0.8 is not yet Turing complete

WarPy40K already contains most of the ingredients commonly used to construct a universal computational model:

- mutable variables;
- integer arithmetic;
- comparisons;
- conditional branching;
- blocks;
- an internal unbounded `while` execution mechanism.

However, in version 0.8, a normal WarPy40K source program cannot create a `WhileLoopNode` through the public parser path because the `while` dispatch is disabled. Without an accessible unbounded loop, recursion, or another equivalent mechanism, the current surface language does not yet provide a defensible demonstration of Turing completeness.

The AST and runtime are already prepared for this next step. A future version can enable and validate `while`, then demonstrate computational universality constructively—for example by implementing a two-counter Minsky machine in WarPy40K.

## Features

- **Warhammer 40K-themed expressions**: `Inquisition`, `Emperor`, `Chaos`, `Purge`, `Exterminatus`, `Bless`, and `Curse`
- **Variables and assignment**
- **Arithmetic operations**
- **Comparison operators**
- **Logical operators**
- **Conditional execution with `if` / `else`**
- **Block statements**
- **Built-in functions**: `print()`, `input()`, `random()`, `abs()`, `min()`, `max()`, `pow()`, `len()`, `range()`, and `exit()`
- **Built-in constants**: `FAITH`, `CORRUPTION`, `POPULATION`, `True`, and `False`
- **Interactive REPL**
- **File execution** for WarPy40K scripts
- **Token and AST inspection** through the CLI
- **Internal loop infrastructure** under development

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

result = evaluate("Bless Emperor 100")
print(result)  # Output: 110.0

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

```text
# Comments
# This is a comment

# Variables
x = 42
y = 100

# Assignment
x = x + 1

# Arithmetic
1 + 2
5 - 3
2 * 3
6 / 2
2 ^ 3

# Comparison
1 == 2
1 != 2
1 > 2
1 < 2
1 >= 2
1 <= 2

# Logical operators
True AND False
True OR False
NOT True

# Parentheses
(1 + 2) * 3
```

### Conditionals

WarPy40K supports conditional execution through `if` and `else`.

```text
x = 10

if x > 5 {
    print("x is greater than 5")
}
else {
    print("x is 5 or less")
}
```

### While Loops — Experimental / Partial

The AST and interpreter already contain support for `while` loops, and the parser contains `_parse_while_statement()`. However, the normal parser dispatch for the `while` keyword is disabled in v0.8.

As a result, `while` should currently be considered an **internal/experimental feature rather than supported surface syntax**.

The intended form is conceptually:

```text
counter = 0
while counter < 10 {
    counter = counter + 1
}
```

Enabling and validating this behavior end-to-end is one of the main milestones after v0.8.

### Warhammer 40K Expressions

| Expression | Description | Example | Result |
|---|---|---|---|
| `Inquisition` | Truth/judgment — evaluates target truthiness | `Inquisition 42` | `True` |
| `Inquisition` | Without target, returns true | `Inquisition` | `True` |
| `Emperor` | Divine power — multiplies numeric target by faith factor | `Emperor 100` | `100.0` |
| `Emperor` | Without target, returns a high value | `Emperor` | `1000` |
| `Chaos` | Corruption/randomness | `Chaos 100` | Target plus chaos factor |
| `Chaos` | Without target, returns a random value | `Chaos` | `0-100` |
| `Purge x` | Destruction — maps evaluated target to zero/empty | `Purge 42` | `0` |
| `Exterminatus x` | Total annihilation | `Exterminatus 42` | `None` |
| `Bless x` | Positive modification — increases numeric targets by 10% | `Bless 100` | `110.0` |
| `Curse x` | Negative modification — decreases numeric targets by 10% | `Curse 100` | `90.0` |

### Built-in Constants

- `FAITH` — default faith value (`100`)
- `CORRUPTION` — default corruption level (`0`)
- `POPULATION` — default population (`1,000,000`)
- `True` — boolean true
- `False` — boolean false

### Built-in Functions

- `print(...)` — print values to the console
- `input(prompt)` — read input from the user
- `random()` — return a random float between 0 and 1
- `abs(x)` — absolute value
- `min(...)` — minimum value
- `max(...)` — maximum value
- `pow(x, y)` — `x` raised to the power `y`
- `len(x)` — length of a supported value
- `range(...)` — create a range object
- `exit(code)` — terminate execution

## Examples

### Simple Arithmetic

```text
result = 2 + 3 * 4
print(result)  # Output: 14

result = (2 + 3) * 4
print(result)  # Output: 20
```

### Using WarPy40K Expressions

```text
faithful = Inquisition FAITH
print(faithful)  # Output: True

blessedValue = Emperor 100
print(blessedValue)  # Output: 100.0

corruptedValue = Chaos 100
print(corruptedValue)

purified = Purge 42
print(purified)  # Output: 0

blessed = Bless 100
cursed = Curse 100
print(blessed)  # Output: 110.0
print(cursed)   # Output: 90.0
```

## Architecture

WarPy40K follows a conventional interpreter pipeline:

```text
Source code
    ↓
Lexer
    ↓
Tokens
    ↓
Recursive-descent Parser
    ↓
Abstract Syntax Tree (AST)
    ↓
Interpreter
    ↓
Program result / side effects
```

## Project Structure

```text
WarPy40K/
├── src/
│   └── warpy40k/
│       ├── __init__.py      # Package initialization and evaluate function
│       ├── __main__.py      # Command-line entry point / REPL
│       ├── tokens.py        # Token definitions
│       ├── lexer.py         # Lexical analyzer
│       ├── parser.py        # Recursive-descent parser
│       ├── ast.py           # Abstract Syntax Tree nodes
│       └── interpreter.py   # AST interpreter/runtime
├── docs/                    # Additional documentation
├── examples/                # Example WarPy40K programs
├── tests/                   # Automated tests
├── pyproject.toml           # Project configuration
├── README.md
└── .gitignore
```

## Roadmap

### v0.8 — Current

- [x] Lexer and token model
- [x] Recursive-descent parser
- [x] AST representation
- [x] Tree-walking interpreter
- [x] Variables and assignment
- [x] Arithmetic, comparisons, and boolean logic
- [x] `if` / `else`
- [x] Blocks
- [x] Built-in function calls
- [x] WarPy40K-specific expressions
- [x] CLI and REPL
- [x] Internal `WhileLoopNode`
- [x] Runtime execution for `WhileLoopNode`
- [ ] Enable `while` in the surface-language parser
- [ ] Validate loop syntax and semantics end-to-end
- [ ] Add dedicated loop regression tests

### Toward v1.0

- [ ] Stabilize the surface syntax
- [ ] Complete and document loop semantics
- [ ] Add a constructive Turing-completeness demonstration
- [ ] Implement a small universal model such as a two-counter Minsky machine in WarPy40K
- [ ] Improve runtime error reporting
- [ ] Expand test coverage
- [ ] Reconcile all language documentation with the implemented grammar and semantics

## Development

### Running Tests

```bash
pip install -r requirements-dev.txt
pytest
pytest --cov=src/warpy40k
```

### Code Formatting

```bash
black src/ tests/
isort src/ tests/
```

### Type Checking

```bash
mypy src/warpy40k
```

## Contributing

Contributions are welcome. Please feel free to submit issues or pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the Warhammer 40K universe created by Games Workshop
- Built with Python
- Created as an educational programming-language and interpreter project

**For the Emperor!**
