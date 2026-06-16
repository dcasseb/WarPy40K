# Getting Started with WarPy40K

This guide will help you install and start using WarPy40K.

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/dcasseb/WarPy40K.git
cd WarPy40K

# Install in development mode
pip install -e .
```

### Install Dependencies (Optional)

For development and testing:

```bash
pip install -r requirements-dev.txt
```

## 🚀 Running WarPy40K

### Command Line Usage

```bash
# Run a WarPy40K file
warpy40k my_program.wp40k

# Execute a single line of code
warpy40k -c "print('Hello from WarPy40K!')"

# Start interactive REPL
warpy40k -i

# Display tokens (for debugging)
warpy40k --tokens my_program.wp40k

# Display AST (for debugging)
warpy40k --ast my_program.wp40k
```

### Python Module Usage

```python
from warpy40k import evaluate

# Evaluate a single expression
result = evaluate("1 + 2")
print(result)  # Output: 3

# Evaluate WarPy40K expressions
result = evaluate("Bless Emperor 100")
print(result)  # Output: 110.0
```

## 📝 Creating Your First Program

Create a file named `hello.wp40k` with the following content:

```python
# This is a comment
print("For the Emperor!")
print("Welcome to WarPy40K")
```

Run it:

```bash
warpy40k hello.wp40k
```

Expected output:
```
For the Emperor!
Welcome to WarPy40K
```

## 🎯 Using the REPL

Start the interactive REPL:

```bash
warpy40k -i
```

You'll see:
```
WarPy40K Interactive REPL
Type 'exit' or 'quit' to exit
Type 'help' for information
Type 'reset' to clear all variables

>>> 
```

Try some commands:
```
>>> 1 + 2
3
>>> x = 10
10
>>> x * 2
20
>>> Inquisition 42
True
>>> Emperor
1000
>>> exit
May the Emperor protect you!
```

## 📁 Project Structure

```
WarPy40K/
├── src/warpy40k/           # Source code
│   ├── __init__.py       # Main package init
│   ├── __main__.py       # CLI entry point
│   ├── tokens.py         # Token definitions
│   ├── lexer.py          # Lexical analyzer
│   ├── parser.py         # Parser
│   ├── ast.py            # Abstract Syntax Tree
│   └── interpreter.py    # Interpreter
├── examples/              # Example programs
│   ├── hello.wp40k
│   ├── calculator.wp40k
│   ├── variables.wp40k
│   ├── warpy_demo.wp40k
│   └── control_flow.wp40k
├── tests/                 # Test suite
├── docs/                 # Documentation
├── pyproject.toml        # Project configuration
└── README.md             # Project overview
```

## ✅ Verifying Installation

Run the test suite to make sure everything is working:

```bash
python test_project.py
```

You should see:
```
Running WarPy40K Tests
========================================
Testing Lexer...
✓ Lexer tests passed
Testing Parser...
✓ Parser tests passed
Testing Interpreter...
✓ Interpreter tests passed
Testing Complex Expressions...
✓ Complex expression tests passed
Testing Control Flow...
✓ Control flow tests passed
========================================
🎉 All tests passed!
```

## 🔧 Troubleshooting

### "Command not found: warpy40k"

Make sure you've installed the package:
```bash
pip install -e .
```

### "ModuleNotFoundError: No module named 'warpy40k'"

Set the Python path:
```bash
PYTHONPATH=src python -m warpy40k your_program.wp40k
```

Or install the package:
```bash
pip install -e .
```

### Syntax Errors

Check your code for:
- Missing parentheses
- Incorrect operator usage
- Unknown keywords

Use `--tokens` to see how your code is tokenized:
```bash
warpy40k --tokens your_program.wp40k
```

Use `--ast` to see the parsed structure:
```bash
warpy40k --ast your_program.wp40k
```

## 📖 Next Steps

Now that you're set up, continue with:

- **[Language Reference](language_reference.md)** - Complete syntax guide
- **[Tutorials](tutorials.md)** - Step-by-step programming guides
- **[WarPy40K Expressions](warpy_expressions.md)** - Learn about special keywords
