# WarPy40K API Reference

This document describes how to use WarPy40K as a Python library.

## 📦 Package Overview

The `warpy40k` package provides a complete interpreter for the WarPy40K language that can be used programmatically.

## 📥 Installation

```bash
pip install -e .
```

## 🎯 Main Functions

### evaluate()

Evaluate a WarPy40K expression or program.

**Signature:**
```python
def evaluate(source: str, use_global: bool = True) -> Any
```

**Parameters:**
- `source` (str): The WarPy40K code to evaluate
- `use_global` (bool): If `True`, use the global interpreter (variables persist across calls). If `False`, create a new interpreter for this evaluation.

**Returns:**
- The result of the evaluation, or `None` if no result

**Raises:**
- `WarPy40KError`: If there's a syntax or runtime error

**Example:**
```python
from warpy40k import evaluate

# Simple expression
result = evaluate("1 + 2")
print(result)  # Output: 3

# WarPy40K expression
result = evaluate("Bless Emperor 100")
print(result)  # Output: 110.0

# With variable persistence
from warpy40k import reset_interpreter

reset_interpreter()
evaluate("x = 10")
evaluate("y = 20")
result = evaluate("x + y")
print(result)  # Output: 30
```

### reset_interpreter()

Reset the global interpreter, clearing all variables and state.

**Signature:**
```python
def reset_interpreter() -> None
```

**Example:**
```python
from warpy40k import evaluate, reset_interpreter

# Set some variables
evaluate("x = 10")
evaluate("y = 20")

# Reset
reset_interpreter()

# Variables are now cleared
result = evaluate("x")  # Raises WarPy40KError: x is not defined
```

### get_interpreter()

Get the global interpreter instance.

**Signature:**
```python
def get_interpreter() -> Interpreter
```

**Returns:**
- The global `Interpreter` instance

**Example:**
```python
from warpy40k import get_interpreter

interpreter = get_interpreter()
# Use interpreter directly if needed
```

## 🏗️ Classes

### WarPy40KError

Custom exception for WarPy40K errors.

**Attributes:**
- `message` (str): The error message
- `line` (int): Line number where error occurred
- `column` (int): Column number where error occurred

**Example:**
```python
from warpy40k import evaluate, WarPy40KError

try:
    result = evaluate("1 / 0")
except WarPy40KError as e:
    print(f"Error at line {e.line}, column {e.column}: {e.message}")
```

### Interpreter

The main interpreter class for executing WarPy40K AST nodes.

**Methods:**
- `execute(node: ASTNode) -> Any`: Execute an AST node
- `_init_builtins()`: Initialize built-in functions and constants

**Example:**
```python
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
print(result)  # Output: 7
```

### Lexer

Lexical analyzer for converting source code to tokens.

**Methods:**
- `tokenize() -> List[Token]`: Tokenize the entire source
- `next_token() -> Optional[Token]`: Get the next token

**Example:**
```python
from warpy40k.lexer import Lexer

source = "1 + 2"
lexer = Lexer(source)
tokens = lexer.tokenize()
for token in tokens:
    print(token)
```

### Parser

Recursive descent parser for converting tokens to AST.

**Methods:**
- `parse() -> Program`: Parse all tokens into a Program AST node

**Example:**
```python
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser

source = "1 + 2"
lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
print(ast)  # Output: Program(statements=1)
```

## 📊 Token Types

The `TokenType` enum defines all token types:

### Basic Types
- `INTEGER` - Integer literals
- `FLOAT` - Float literals
- `STRING` - String literals
- `BOOLEAN` - Boolean literals (True, False)
- `IDENTIFIER` - Identifiers (variable names, etc.)

### WarPy40K Keywords
- `INQUISITION` - Inquisition keyword
- `EMPEROR` - Emperor keyword
- `CHAOS` - Chaos keyword
- `XENOS` - Xenos keyword
- `HERETIC` - Heretic keyword
- `PURGE` - Purge keyword
- `EXTERMINATUS` - Exterminatus keyword
- `BLESS` - Bless keyword
- `CURSE` - Curse keyword
- `FAITH` - Faith keyword
- `WARP` - Warp keyword

### Operators
- `PLUS` - `+`
- `MINUS` - `-`
- `MULTIPLY` - `*`
- `DIVIDE` - `/`
- `POWER` - `^`
- `EQ` - `==`
- `NEQ` - `!=`
- `GT` - `>`
- `LT` - `<`
- `GTE` - `>=`
- `LTE` - `<=`
- `AND` - `AND` or `&&`
- `OR` - `OR` or `||`
- `NOT` - `NOT` or `!`

### Punctuation
- `LPAREN` - `(`
- `RPAREN` - `)`
- `LBRACE` - `{`
- `RBRACE` - `}`
- `COMMA` - `,`
- `SEMICOLON` - `;`
- `COLON` - `:`
- `ASSIGN` - `=`

### Special
- `EOF` - End of file
- `WHITESPACE` - Whitespace (ignored)
- `COMMENT` - Comments (ignored)

## 🌲 AST Node Types

The `NodeType` enum defines all AST node types:

### Program Structure
- `PROGRAM` - Root program node
- `BLOCK` - Block of statements

### Expressions
- `EXPRESSION` - Generic expression
- `LITERAL` - Literal value
- `IDENTIFIER` - Identifier reference
- `BINARY_OP` - Binary operation
- `UNARY_OP` - Unary operation

### Statements
- `VARIABLE_DECLARATION` - Variable declaration
- `VARIABLE_ASSIGNMENT` - Variable assignment
- `FUNCTION_CALL` - Function call
- `IF_STATEMENT` - If statement
- `WHILE_LOOP` - While loop
- `RETURN_STATEMENT` - Return statement

### WarPy40K Specific
- `INQUISITION_EXPR` - Inquisition expression
- `EMPEROR_EXPR` - Emperor expression
- `CHAOS_EXPR` - Chaos expression
- `PURGE_EXPR` - Purge expression
- `EXTERMINATUS_EXPR` - Exterminatus expression
- `BLESS_EXPR` - Bless expression
- `CURSE_EXPR` - Curse expression

## 🔧 Utility Functions

### Token

Represents a token in the source code.

**Attributes:**
- `type` (TokenType): The token type
- `value` (str): The token value
- `line` (int): Line number
- `column` (int): Column number

**Methods:**
- `__repr__()`: String representation
- `__eq__()`: Equality comparison

### ASTNode

Base class for all AST nodes.

**Attributes:**
- `node_type` (NodeType): The node type
- `line` (int): Line number
- `column` (int): Column number

## 📚 Complete Example: Building a Custom Interpreter

Here's a complete example of using the WarPy40K components directly:

```python
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser
from warpy40k.interpreter import Interpreter
from warpy40k import WarPy40KError

def custom_evaluate(source: str) -> Any:
    """Custom evaluation function with error handling."""
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        return interpreter.execute(ast)
    except WarPy40KError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Use the custom evaluator
result = custom_evaluate("1 + 2")
print(result)  # Output: 3

result = custom_evaluate("Bless Emperor 100")
print(result)  # Output: 110.0
```

## 🎯 Use Cases

### 1. Embedding WarPy40K in Your Application

```python
from warpy40k import evaluate

# Allow users to enter WarPy40K expressions
user_input = "Inquisition 42"
result = evaluate(user_input)
print(f"Result: {result}")
```

### 2. Creating a Custom REPL

```python
from warpy40k import evaluate, reset_interpreter

def custom_repl():
    print("Custom WarPy40K REPL")
    reset_interpreter()
    
    while True:
        try:
            code = input(">>> ")
            if code.lower() in ('exit', 'quit'):
                break
            result = evaluate(code, use_global=True)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}")

custom_repl()
```

### 3. Batch Processing

```python
from warpy40k import evaluate, reset_interpreter

# Process multiple expressions
expressions = [
    "x = 10",
    "y = 20",
    "x + y",
    "Bless Emperor x",
]

reset_interpreter()
for expr in expressions:
    result = evaluate(expr, use_global=True)
    if result is not None:
        print(f"{expr} = {result}")
```

### 4. Syntax Validation

```python
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser
from warpy40k import WarPy40KError

def validate_syntax(source: str) -> bool:
    """Check if source code has valid syntax."""
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser.parse()
        return True
    except WarPy40KError:
        return False
    except Exception:
        return False

# Test syntax
print(validate_syntax("1 + 2"))  # Output: True
print(validate_syntax("1 +"))   # Output: False
```

## 📖 Next Steps

- **[Getting Started](getting_started.md)** - Installation and basic usage
- **[Language Reference](language_reference.md)** - Complete syntax guide
- **[Tutorials](tutorials.md)** - Step-by-step programming guides
- **[Examples](examples.md)** - Complete example programs
