# WarPy40K Language Reference

This document provides a complete reference for the WarPy40K programming language.

## 📝 Basic Syntax

### Comments

Single-line comments start with `#`:

```python
# This is a comment
x = 42  # Inline comment
```

### Variables

Variables are created by assignment:

```python
x = 42          # Integer
name = "John"   # String
faith = True    # Boolean
```

Variable names:
- Can contain letters, numbers, and underscores
- Cannot start with a number
- Are case-sensitive

### Literals

#### Numbers

```python
42      # Integer
3.14    # Float
-10     # Negative integer
2.5e3   # Scientific notation (not yet supported)
```

#### Strings

```python
"Hello"         # Double quotes
'World'         # Single quotes
"Line 1\nLine 2"  # Newline escape
```

#### Booleans

```python
True
False
```

## 🔢 Operators

### Arithmetic Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `1 + 2` | `3` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `2 * 3` | `6` |
| `/` | Division | `6 / 2` | `3.0` |
| `^` | Power | `2 ^ 3` | `8` |

### Comparison Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `==` | Equal | `1 == 1` | `True` |
| `!=` | Not equal | `1 != 2` | `True` |
| `>` | Greater than | `2 > 1` | `True` |
| `<` | Less than | `1 < 2` | `True` |
| `>=` | Greater or equal | `2 >= 2` | `True` |
| `<=` | Less or equal | `1 <= 2` | `True` |

### Logical Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `AND` | Logical AND | `True AND False` | `False` |
| `OR` | Logical OR | `True OR False` | `True` |
| `NOT` | Logical NOT | `NOT True` | `False` |

### Operator Precedence

From highest to lowest:

1. Parentheses `()`
2. Power `^`
3. Multiplication `*`, Division `/`
4. Addition `+`, Subtraction `-`
5. Comparison operators (`==`, `!=`, `>`, `<`, `>=`, `<=`)
6. Logical NOT `NOT`
7. Logical AND `AND`
8. Logical OR `OR`

Example:
```python
1 + 2 * 3      # 1 + (2 * 3) = 7
(1 + 2) * 3   # (1 + 2) * 3 = 9
NOT True AND False  # (NOT True) AND False = False
```

## 📋 Statements

### Assignment

```python
x = 42
y = x + 10
```

### If Statement

```python
if condition
    statement1
    statement2
else
    statement3
    statement4
```

Example:
```python
x = 10
if x > 5
    print("x is greater than 5")
else
    print("x is 5 or less")
```

Nested if:
```python
if x > 5
    if y > 10
        print("Both conditions true")
    else
        print("Only first condition true")
else
    print("First condition false")
```

### Expression Statements

Any expression can be a statement:

```python
1 + 2          # Evaluates and discards result
x = 42         # Assignment
print("hello")   # Function call
```

## 🔄 Control Flow

### If/Else

See [If Statement](#if-statement) above.

### While Loops

**Note**: While loops are partially implemented but may have issues with infinite loops.

```python
while condition
    statement1
    statement2
```

Example:
```python
counter = 1
while counter <= 5
    print(counter)
    counter = counter + 1
```

## 📞 Function Calls

### Built-in Functions

| Function | Description | Example |
|----------|-------------|---------|
| `print(x)` | Print value to console | `print("Hello")` |
| `input(prompt)` | Get user input | `name = input("Name: ")` |
| `random()` | Random float [0, 1) | `r = random()` |
| `abs(x)` | Absolute value | `abs(-5)` |
| `min(x, y, ...)` | Minimum value | `min(1, 2, 3)` |
| `max(x, y, ...)` | Maximum value | `max(1, 2, 3)` |
| `pow(x, y)` | Power | `pow(2, 3)` |
| `len(x)` | Length | `len("hello")` |
| `range(start, end)` | Range | `range(1, 5)` |
| `exit(code)` | Exit program | `exit(0)` |

### Function Call Syntax

```python
function_name(arg1, arg2, arg3)
```

Example:
```python
print("Hello", "World")
result = min(1, 2, 3)
```

## 🌟 WarPy40K Specific Expressions

WarPy40K includes special keywords inspired by the Warhammer 40K universe:

| Expression | Syntax | Description | Example |
|------------|--------|-------------|---------|
| Inquisition | `Inquisition [target]` | Truth/judgment | `Inquisition 42` |
| Emperor | `Emperor [target]` | Divine power | `Emperor 100` |
| Chaos | `Chaos [target]` | Corruption/randomness | `Chaos` |
| Purge | `Purge target` | Destruction | `Purge 42` |
| Exterminatus | `Exterminatus [target]` | Total annihilation | `Exterminatus` |
| Bless | `Bless target` | Positive modification | `Bless 100` |
| Curse | `Curse target` | Negative modification | `Curse 100` |

See [WarPy40K Expressions](warpy_expressions.md) for detailed explanations.

## 🏷️ Built-in Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `FAITH` | 100 | Default faith value |
| `CORRUPTION` | 0 | Default corruption level |
| `POPULATION` | 1000000 | Default population |
| `True` | `True` | Boolean true |
| `False` | `False` | Boolean false |

## 📊 Types

### Numbers

- **Integer**: Whole numbers (`42`, `-10`)
- **Float**: Decimal numbers (`3.14`, `-0.5`)

### Strings

- Sequences of characters enclosed in quotes
- Support escape sequences

### Booleans

- `True` or `False`
- Result of comparisons and logical operations

### None

- Special value representing nothing
- Returned by `Exterminatus` and some other operations

## 🔧 Type Conversion

WarPy40K performs automatic type conversion in some cases:

```python
"Hello " + "World"   # String concatenation
1 + 2               # Integer addition
1 + 2.5             # Float addition (2 becomes 2.0)
```

**Note**: Explicit type conversion is not yet supported.

## 📝 Best Practices

### Code Style

- Use descriptive variable names
- Add comments to explain complex logic
- Keep lines short for readability
- Use consistent indentation

### Example of Good Style

```python
# Calculate the Emperor's blessing on a planet
planet_population = 1000000
faith_level = 80

# Check if the planet is worthy
if Inquisition faith_level
    # Bless the planet
    blessed_population = Bless Emperor planet_population
    print("Blessed population:")
    print(blessed_population)
else
    # Purge the heretics
    print("The planet must be purged!")
```

### Example of Poor Style

```python
p=1000000
f=80
if Inquisition f
Bless Emperor p
else
Purge p
```

## 🐛 Common Mistakes

### Forgetting Variable Assignment

```python
# Wrong: Trying to use a variable before assignment
print(x)  # Error: x is not defined

# Right: Assign first
x = 42
print(x)  # Output: 42
```

### Incorrect Operator Usage

```python
# Wrong: Using = for comparison
if x = 5  # Error: Assignment in condition
    print("x is 5")

# Right: Use == for comparison
if x == 5
    print("x is 5")
```

### Missing Parentheses

```python
# Wrong: Missing closing parenthesis
print("Hello"

# Right: Include all parentheses
print("Hello")
```

## 📖 Next Steps

- **[WarPy40K Expressions](warpy_expressions.md)** - Learn about special keywords
- **[Tutorials](tutorials.md)** - Step-by-step programming guides
- **[Examples](examples.md)** - See complete example programs
