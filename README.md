# WarPy40K

**Current version: 0.9.0**

A Warhammer 40K-inspired interpreted programming language implemented in Python.

## Overview

WarPy40K combines a conventional tree-walking interpreter with expressions and terminology inspired by the Warhammer 40K universe. The language includes variables, arithmetic, comparisons, Boolean logic, conditionals, unrestricted `while` loops, user-defined functions, lexical function scopes, `return`, and recursion.

Version **0.9.0** is the first WarPy40K release with a complete general-purpose control-flow core.

Under the standard theoretical model in which program memory is treated as unbounded, **WarPy40K v0.9 is Turing complete**. In particular, mutable integer variables, conditional branching, and unrestricted `while` loops are sufficient to encode a two-counter Minsky machine. As with Python, C, or any language running on real hardware, actual executions are naturally limited by available memory and other machine resources.

A constructive Minsky-machine example/proof remains planned as an explicit documentation milestone before v1.0.

## What changed in v0.9

| Capability | v0.8 | v0.9 |
|---|---:|---:|
| Variables and assignment | ✅ | ✅ |
| Arithmetic / comparisons / Boolean logic | ✅ | ✅ |
| `if` / `else` | ✅ | ✅ |
| Blocks | ✅ | ✅ |
| Built-in functions | ✅ | ✅ |
| `while` runtime node | Internal only | ✅ Surface syntax |
| Unrestricted `while` | ❌ | ✅ |
| User-defined functions | ❌ | ✅ |
| Function parameters | ❌ | ✅ |
| Lexical function scopes | ❌ | ✅ |
| `return` with real control-flow unwind | ❌ | ✅ |
| Recursion | ❌ | ✅ |
| Turing-complete computational core | ❌ | ✅ |

## Core language features

- Variables and mutable assignment
- Integers, floats, strings, and Booleans
- Arithmetic: `+`, `-`, `*`, `/`, `^`
- Comparisons: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Boolean operators: `AND`, `OR`, `NOT`
- `if` / `else`
- Unrestricted `while` loops
- User-defined functions with `def`
- Function parameters and arity validation
- Lexical function scopes
- `return`
- Direct recursion
- Built-in functions
- WarPy40K-specific expressions
- REPL and file execution
- Token and AST inspection through the CLI

## Installation

```bash
git clone https://github.com/dcasseb/WarPy40K.git
cd WarPy40K
pip install -e .
```

## Usage

### Command line

```bash
# Run a source file
warpy40k examples/recursion.wp40k

# Execute a single expression
warpy40k -c "Bless Emperor 100"

# Start the REPL
warpy40k -i

# Inspect tokens
warpy40k --tokens examples/recursion.wp40k

# Inspect the AST
warpy40k --ast examples/recursion.wp40k
```

### Python API

```python
from warpy40k import evaluate

result = evaluate("2 + 3 * 4")
print(result)  # 14
```

## Language reference

### Variables

```text
x = 42
y = x + 10
```

### Conditionals

Blocks use braces when more than one statement should belong to a branch.

```text
x = 10

if x > 5 {
    print("greater")
}
else {
    print("smaller or equal")
}
```

### While loops

`while` is fully available in v0.9 and has no artificial iteration limit.

```text
counter = 0

while counter < 5 {
    print(counter)
    counter = counter + 1
}
```

This ability to repeat computation for an input-dependent and potentially unbounded number of iterations is one of the key differences between v0.8 and v0.9.

### User-defined functions

Functions are declared with `def`, followed by their parameter list and a block body.

```text
def add(a, b) {
    return a + b
}

result = add(20, 22)
print(result)
```

Each function invocation gets a fresh local scope. Parameters and assignments created inside the function do not implicitly overwrite global variables with the same names.

```text
x = 100

def identity(x) {
    return x
}

print(identity(42))
print(x)  # 100
```

### Recursion

User-defined functions can call themselves because function names remain visible through their lexical environment.

```text
def factorial(n) {
    if n <= 1 {
        return 1
    }

    return n * factorial(n - 1)
}

print(factorial(6))  # 720
```

A recursive Fibonacci implementation is also supported:

```text
def fibonacci(n) {
    if n <= 1 {
        return n
    }

    return fibonacci(n - 1) + fibonacci(n - 2)
}

print(fibonacci(10))  # 55
```

### Return semantics

`return` exits the nearest user-defined function immediately, even when it is reached inside nested blocks or loops.

```text
def first_at_least(limit) {
    x = 0

    while True {
        if x >= limit {
            return x
        }
        x = x + 1
    }
}
```

Using `return` outside a user-defined function is a runtime error.

## WarPy40K expressions

| Expression | Description | Example |
|---|---|---|
| `Inquisition` | Evaluate truthiness | `Inquisition 42` |
| `Emperor` | Apply the faith factor | `Emperor 100` |
| `Chaos` | Apply corruption/randomness | `Chaos 100` |
| `Purge` | Reduce a value to zero/empty | `Purge 42` |
| `Exterminatus` | Total annihilation | `Exterminatus 42` |
| `Bless` | Increase numeric value by 10% | `Bless 100` |
| `Curse` | Decrease numeric value by 10% | `Curse 100` |

## Built-ins

- `print(...)`
- `input(prompt)`
- `random()`
- `abs(x)`
- `min(...)`
- `max(...)`
- `pow(x, y)`
- `len(x)`
- `range(...)`
- `exit(code)`

Built-in constants:

- `FAITH = 100`
- `CORRUPTION = 0`
- `POPULATION = 1000000`
- `True`
- `False`

## Architecture

```text
Source code
    ↓
Lexer
    ↓
Tokens
    ↓
Recursive-descent parser
    ↓
Abstract Syntax Tree
    ↓
Tree-walking interpreter
    ↓
Runtime environments / results
```

Function calls in v0.9 add a lexical environment layer on top of the global interpreter environment. Recursive calls therefore receive independent parameter/local-variable dictionaries while retaining access to enclosing definitions.

## Project structure

```text
WarPy40K/
├── src/
│   └── warpy40k/
│       ├── __init__.py
│       ├── __main__.py
│       ├── tokens.py
│       ├── lexer.py
│       ├── parser.py
│       ├── ast.py
│       └── interpreter.py
├── docs/
├── examples/
│   ├── recursion.wp40k
│   └── ...
├── tests/
│   ├── test_v09.py
│   └── ...
├── pyproject.toml
└── README.md
```

## Roadmap

### v0.9 — Current

- [x] Enable unrestricted `while` in surface syntax
- [x] Add dedicated control-flow tokens
- [x] Add user-defined functions
- [x] Add function parameters
- [x] Add lexical call scopes
- [x] Implement `return` control-flow unwind
- [x] Enable direct recursion
- [x] Validate recursive factorial and Fibonacci
- [x] Add v0.9 regression tests
- [x] Synchronize package version metadata

### Toward v1.0

- [ ] Add an explicit two-counter Minsky-machine implementation
- [ ] Publish a constructive Turing-completeness demonstration
- [ ] Stabilize the grammar and language specification
- [ ] Improve source-location-aware runtime errors
- [ ] Expand function and scope semantics
- [ ] Expand automated regression coverage
- [ ] Reconcile all secondary documentation with the v0.9 grammar

## Development

```bash
pip install -r requirements-dev.txt
pytest
pytest --cov=src/warpy40k
```

Formatting and type checks:

```bash
black src/ tests/
isort src/ tests/
mypy src/warpy40k
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Acknowledgments

- Inspired by the Warhammer 40K universe created by Games Workshop
- Built in Python as an educational programming-language/interpreter project

**For the Emperor!**
