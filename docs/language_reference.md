# WarPy40K Language Reference — v1.0.1

This document describes the stable language core available in WarPy40K 1.0.

## Lexical basics

### Comments

Single-line comments start with `#`:

```text
# This is a comment
x = 42
```

### Identifiers

Identifiers may contain letters, digits, and underscores, but may not begin with a digit. Names are case-sensitive.

### Literals

Currently supported literals:

```text
42
3.14
"For the Emperor!"
True
False
```

Strings use double quotes. Scientific-notation numeric literals and single-quoted strings are not part of the v1.0 grammar.

## Variables and assignment

Variables are created or updated through assignment:

```text
x = 42
y = x + 10
```

At top level, assignments are stored in the global interpreter environment. Inside a user-defined function, assignments are local to that invocation.

## Operators

### Arithmetic

| Operator | Meaning |
|---|---|
| `+` | addition |
| `-` | subtraction |
| `*` | multiplication |
| `/` | division |
| `^` | exponentiation |

### Comparison

```text
==  !=  >  <  >=  <=
```

### Boolean logic

```text
AND
OR
NOT
```

Parentheses may be used for grouping.

## Blocks

Blocks are delimited by braces:

```text
{
    x = 1
    y = 2
}
```

Whitespace and indentation improve readability but do not define block structure.

## Conditional execution

```text
if condition {
    statement
}
else {
    other_statement
}
```

Example:

```text
x = 10

if x > 5 {
    print("greater")
}
else {
    print("smaller or equal")
}
```

`else` is optional.

## While loops

`while` is fully supported in v1.0 and has no artificial iteration limit:

```text
counter = 0

while counter < 5 {
    print(counter)
    counter = counter + 1
}
```

A program may therefore intentionally or accidentally fail to terminate.

## User-defined functions

Functions use `def`, a parameter list, and a block body:

```text
def add(a, b) {
    return a + b
}

result = add(20, 22)
```

Function arity is checked at runtime.

### Function scope

Each function call receives a fresh local scope for parameters and assignments.
Braced blocks do not create additional scopes in v1.0.1:

```text
x = 100

def identity(x) {
    return x
}

identity(42)
x
```

The final value of `x` is still `100`.

Function names remain visible through their lexical environment, enabling recursion.

### Recursion

```text
def factorial(n) {
    if n <= 1 {
        return 1
    }

    return n * factorial(n - 1)
}

factorial(6)
```

This evaluates to `720`.

## Return

`return` exits the nearest user-defined function immediately:

```text
def find(limit) {
    x = 0

    while True {
        if x >= limit {
            return x
        }
        x = x + 1
    }
}
```

A `return` reached inside nested `if` statements, blocks, or loops unwinds the function call. Using `return` outside a user-defined function is a runtime error.

## Built-in functions

WarPy40K 1.0.1 exposes the following built-ins:

| Function | Description |
|---|---|
| `print(...)` | print values |
| `input(prompt)` | read user input |
| `int(x)` | convert a number, Boolean, or decimal string to an integer |
| `float(x)` | convert a number, Boolean, or decimal string to a float |
| `str(x)` | convert a runtime value to text |
| `random()` | random float in `[0, 1)` |
| `abs(x)` | absolute value |
| `min(...)` | minimum |
| `max(...)` | maximum |
| `pow(x, y)` | exponentiation |
| `len(x)` | length of a supported host-backed value |
| `range(...)` | create a host-backed range |
| `exit(code)` | terminate execution |

Some built-ins still expose Python-hosted runtime values. Reducing this host-language leakage is part of the post-1.0 roadmap.

`input` always returns a string. Use `int(...)` or `float(...)` before numeric
arithmetic; multiplying input by `1` does not perform numeric conversion.

## Built-in constants

```text
FAITH
CORRUPTION
POPULATION
True
False
```

Default values are currently:

```text
FAITH = 100
CORRUPTION = 0
POPULATION = 1000000
```

## WarPy40K expressions

### `Inquisition`

Evaluates the truthiness of a target. Without a target, it evaluates to `True`.

```text
Inquisition 42
```

### `Emperor`

Applies the current faith factor to a numeric target. Without a target, it returns the language's current high-value Emperor marker.

```text
Emperor 100
```

### `Chaos`

Applies corruption/randomness to a target or produces a random value when used without a target.

```text
Chaos 100
```

### `Purge`

Reduces a target according to its runtime type, such as numeric zero or an empty string.

```text
Purge 42
```

### `Exterminatus`

Evaluates an optional target for side effects and represents total annihilation.

```text
Exterminatus 42
```

### `Bless`

Increases numeric targets by 10% and applies a positive transformation to supported values.

```text
Bless 100
```

### `Curse`

Decreases numeric targets by 10% and applies a negative transformation to supported values.

```text
Curse 100
```

The deeper semantics of these language-specific concepts will evolve during the 1.x series. See [roadmap.md](roadmap.md).

## Turing completeness

WarPy40K 1.0 includes a constructive Turing-completeness demonstration in [`examples/minsky_universal.wp40k`](../examples/minsky_universal.wp40k).

That source file implements a universal interpreter for encoded deterministic two-counter Minsky machines using WarPy40K itself.

See [turing_completeness.md](turing_completeness.md) for the construction and proof argument.

## Current grammar sketch

The following is descriptive rather than a formal parser specification:

```text
program        := statement*
statement      := if_stmt
                | while_stmt
                | function_def
                | return_stmt
                | block
                | expression

if_stmt        := "if" expression statement ("else" statement)?
while_stmt     := "while" expression statement
function_def   := "def" IDENTIFIER "(" parameters? ")" block
parameters     := IDENTIFIER ("," IDENTIFIER)*
return_stmt    := "return" expression?
block          := "{" statement* "}"
```

A formal versioned grammar is planned for a later 1.x release.
