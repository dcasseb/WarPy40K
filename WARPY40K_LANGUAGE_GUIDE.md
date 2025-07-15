# WarPy40K Language Guide

## Introduction

**WarPy40K** is a toy programming language inspired by the Warhammer 40,000 universe. It is designed to be fun, readable, and expressive, with a unique set of commands and a simple, approachable syntax. This guide covers every aspect of the language, from variables and types to loops, conditionals, and the full command set.

---

## 1. File Structure and Running Code

- WarPy40K source files use the `.wp40k` extension.
- You can run a script with:
  ```bash
  python3 warpy_interpreter.py tests/your_script.wp40k
  ```
- Lint your code for errors and style:
  ```bash
  python3 warpy_linter.py tests/your_script.wp40k
  ```

---

## 2. Language Syntax Overview

### 2.1. Statements

A WarPy40K program is a sequence of **statements**. Each statement can be:
- A variable declaration
- An assignment
- A command call
- A loop (`for` or `while`)
- A conditional (`if`/`else`)

### 2.2. Comments

- Comments start with `#` and continue to the end of the line.
- Comments are ignored during execution and can be used for documentation.
- Example:
  ```warpy40k
  # This is a comment
  i: dg = 0  # Initialize counter
  ```

---

## 3. Variables and Types

### 3.1. Declaration

Declare a variable with a type and initial value:
```warpy40k
variable_name: type = value
```
- Example:
  ```warpy40k
  i: dg = 0
  name: servitor = "imperial_servant"
  power: psykers = 100
  ```

#### Supported Types

| Type         | Description                        | Example Value      |
|--------------|------------------------------------|--------------------|
| `dg`         | Generic number (integer/float)     | `0`, `42`, `3.14`  |
| `servitor`   | String or identifier               | `"servant"`        |
| `blob`       | Arbitrary data (string/number)     | `"data"`, `123`    |
| `psykers`    | Number, often for psychic power    | `100`              |
| `void_shields` | Boolean or status                | `true`, `false`    |

### 3.2. Assignment

Assign a new value to an existing variable:
```warpy40k
variable_name = expression
```
- Example:
  ```warpy40k
  i = i + 1
  name = "new_name"
  ```

---

## 4. Expressions

### 4.1. Literals

- **Numbers:** `0`, `42`, `3.14`
- **Strings:** `"hello world"`
- **Booleans:** `true`, `false` (as values for `void_shields`)

### 4.2. Variables

- Use variable names directly in expressions:
  ```warpy40k
  result = i + power
  ```

### 4.3. Arithmetic Operations

WarPy40K supports a full set of arithmetic operations with proper operator precedence:

#### Basic Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `+` | Addition | `a + b` | Sum of a and b |
| `-` | Subtraction | `a - b` | Difference of a and b |
| `*` | Multiplication | `a * b` | Product of a and b |
| `/` | Division | `a / b` | Quotient of a divided by b |
| `%` | Modulo | `a % b` | Remainder of a divided by b |

#### Examples

```warpy40k
# Basic arithmetic
a: dg = 10
b: dg = 3
c: dg = 2

sum: dg = a + b        # 13
diff: dg = a - b       # 7
product: dg = a * b    # 30
quotient: dg = a / b   # 3.333...
remainder: dg = a % b  # 1
```

#### Operator Precedence

Arithmetic operators follow standard precedence rules (highest to lowest):

1. **Parentheses** `()` - Highest precedence
2. **Multiplication** `*`, **Division** `/`, **Modulo** `%` - Same precedence
3. **Addition** `+`, **Subtraction** `-` - Same precedence

```warpy40k
# Precedence examples
result1: dg = 2 + 3 * 4    # 14 (not 20)
result2: dg = (2 + 3) * 4  # 20
result3: dg = 10 / 2 + 3   # 8 (not 2)
result4: dg = 10 % 3 + 1   # 2
```

#### Complex Expressions

You can combine multiple operations in a single expression:

```warpy40k
# Complex arithmetic
x: dg = 5
y: dg = 2
z: dg = 3

# Multiple operations
result: dg = x * y + z     # 13 (5 * 2 + 3)
result2: dg = x + y * z    # 11 (5 + 2 * 3)
result3: dg = (x + y) * z  # 21 ((5 + 2) * 3)

# Using modulo
remainder: dg = x % y      # 1
power: dg = x * x % 3      # 1 (25 % 3)
```

#### Division and Modulo Notes

- **Division** (`/`) always returns a float result, even for integer division
- **Modulo** (`%`) works with both integers and floats
- Division by zero will cause a runtime error
- Modulo by zero will cause a runtime error

```warpy40k
# Division examples
a: dg = 10
b: dg = 3

div: dg = a / b        # 3.3333333333333335
mod: dg = a % b        # 1

# Float arithmetic
c: dg = 10.5
d: dg = 2.5

float_div: dg = c / d  # 4.2
float_mod: dg = c % d  # 0.5
```

### 4.4. Comparisons

- Supported operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
  ```warpy40k
  if i >= 0:
      ...
  ```

### 4.5. Logical Operators

- Use `and` and `or` to combine conditions:
  ```warpy40k
  if i > 0 and power < 100:
      ...
  ```

---

## 5. Commands

Commands are the heart of WarPy40K, each inspired by Warhammer 40K lore. They are called like functions, with or without arguments.

### 5.1. Command Syntax

```warpy40k
command_name()
command_name(argument)
```

### 5.2. Full Command List

| Command                        | Usage Example                        | Description/Effect (default implementation)                |
|--------------------------------|--------------------------------------|------------------------------------------------------------|
| `the_emperor_protects()`       | `the_emperor_protects()`             | Logs: The Emperor protects!                                |
| `only_in_death_does_duty_end()`| `only_in_death_does_duty_end()`      | Logs: Only in death does duty end.                         |
| `even_in_death_i_still_serve()`| `even_in_death_i_still_serve()`      | Logs: Even in death, I still serve!                        |
| `no_pity_no_remorse_no_fear()` | `no_pity_no_remorse_no_fear()`       | Logs: No pity, no remorse, no fear!                        |
| `burn_the_heretic(arg)`        | `burn_the_heretic("traitor")`      | Logs: Burn the heretic: arg                                |
| `pain_is_temporary_glory_is_forever()` | ... | Logs: Pain is temporary, glory is forever.           |
| `faith_is_my_shield()`         | `faith_is_my_shield()`               | Logs: Faith is my shield!                                  |
| `we_are_angels_of_death()`     | `we_are_angels_of_death()`           | Logs: We are the Angels of Death!                          |
| `we_are_one()`                 | `we_are_one()`                       | Logs: We are one.                                          |
| `WAAAGH()`                     | `WAAAGH()`                           | Logs: The orks rally!                                      |
| `taste_chaos()`                | `taste_chaos()`                      | Logs: Warp corrupts your soul.                             |
| `for_the_emperor()`            | `for_the_emperor()`                  | Logs: For the Emperor!                                     |
| `purge_the_xenos(arg)`         | `purge_the_xenos("xenos")`         | Logs: Xenos purged: arg!                                   |
| `the_emperors_will_be_done()`  | `the_emperors_will_be_done()`        | Logs: The Emperor's will is fulfilled.                     |
| `fear_is_the_mind_killer()`    | `fear_is_the_mind_killer()`          | Logs: Fear suppressed.                                     |
| `ave_imperator()`              | `ave_imperator()`                    | Logs: Ave Imperator! Glory to the Emperor!                 |
| `the_path_is_set()`            | `the_path_is_set()`                  | Logs: The path is set. We proceed.                         |
| `farseers_vision()`            | `farseers_vision()`                  | Logs: The Farseer foresees...                              |
| `more_dakka()`                 | `more_dakka()`                       | Logs: More dakka! Fire everything!                         |
| `ork_cunning()`                | `ork_cunning()`                      | Logs: Cunning plan!                                        |
| `blood_for_the_blood_god()`    | `blood_for_the_blood_god()`          | Logs: Blood for the Blood God!                             |
| `let_the_galaxy_burn()`        | `let_the_galaxy_burn()`              | Logs: The galaxy burns!                                    |
| `servitor()`                   | `servitor()`                         | Returns: "servitor_instance" (for advanced use)          |
| `vox_cast(msg)`                | `vox_cast("message")`                | Prints a message with [VOX] prefix (Warhammer 40K style print) |

---

## 6. Control Flow

### 6.1. For Loops

Iterate over a range of numbers:
```warpy40k
for i in 1..5:
    the_emperor_protects()
```
- The loop variable (`i`) takes values from the start to the end (inclusive).

### 6.2. While Loops

Repeat as long as a condition is true:
```warpy40k
while i < 10:
    for_the_emperor()
    i = i + 1
```

### 6.3. Conditionals

Branch your code with `if` and `else`:
```warpy40k
if power > 50:
    the_emperors_will_be_done()
    ave_imperator()
else:
    fear_is_the_mind_killer()
    burn_the_heretic("weak_psyker")
```
- You can nest `if` statements and use logical operators.

---

## 7. Example: Fibonacci Sequence

```warpy40k
start: dg = 0
end: dg = 5

a: dg = 0
b: dg = 1
i: dg = 0
c: dg = 0

if start == 0:
    burn_the_heretic(a)

for i in 1..end:
    c = a + b
    a = b
    b = c
    if i >= start and i <= end:
        burn_the_heretic(a)
```

---

## 8. Advanced Features

- **Nested Loops:** You can nest `for` and `while` loops.
- **Chained Conditionals:** Use `and`/`or` for complex conditions.
- **String Concatenation:** Use `+` to concatenate strings (e.g., `"heretic_" + str(i)`).
- **All commands can be called with or without arguments as specified.**

---

## 9. Linting and Best Practices

- Use the linter to catch errors and style issues before running your code.
- Avoid using undeclared variables.
- Keep lines under 120 characters for readability.
- Use comments to document your code and explain complex logic.

---

## 10. Editor Support

- **VS Code:** Install the WarPy40K syntax extension for full highlighting and theme support.
- **Sublime Text:** Use the provided syntax definition for rich highlighting.

---

## 11. Project Structure

A typical WarPy40K project might look like:
```
WarPy40K/
  warpy_interpreter.py
  warpy_linter.py
  tests/
    your_script.wp40k
  warpy40k-syntax/
  warpy40k-sublime/
  ...
```

---

## 12. Further Reading

- See the `README.md` for installation and usage.
- See the `LINTER_README.md` for error codes and integration.
- Explore the `tests/` directory for more example scripts.

---

## 13. Quick Reference

### Variable Declaration
```warpy40k
x: dg = 10
```
### Assignment
```warpy40k
x = x + 1
```
### For Loop
```warpy40k
for i in 1..5:
    command()
```
### While Loop
```warpy40k
while x < 10:
    command()
```
### If/Else
```warpy40k
if x > 0:
    command()
else:
    other_command()
```
### Command Call
```warpy40k
the_emperor_protects()
burn_the_heretic("traitor")
```

---

## 14. Tips

- Use meaningful variable names.
- Use the linter to check your code before running.
- Explore the command set for fun and thematic output.
- Try combining loops, conditionals, and commands to create interesting scripts!

---

*For the Emperor!* 