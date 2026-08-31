# WarPy40K Language Reference — v1.1.0

This document describes the stable language core available in WarPy40K 1.1.

## Lexical basics

Single-line comments start with `#`. Identifiers may contain letters, digits, and underscores, may not begin with a digit, and are case-sensitive.

Scalar literals:

```text
42
3.14
"For the Emperor!"
True
False
```

Strings use double quotes. Scientific-notation numeric literals and single-quoted strings are not currently part of the grammar.

## Variables and assignment

```text
x = 42
y = x + 10
```

Top-level assignments live in the global environment. Function parameters and assignments live in a fresh local scope for each invocation.

## Operators

Arithmetic:

```text
+  -  *  /  ^
```

Comparison:

```text
==  !=  >  <  >=  <=
```

Boolean logic:

```text
AND  OR  NOT
```

Parentheses may be used for grouping.

## Blocks and control flow

Blocks use braces:

```text
if condition {
    statement
}
else {
    other_statement
}
```

`while` is unrestricted:

```text
counter = 0
while counter < 5 {
    counter = counter + 1
}
```

Whitespace and indentation improve readability but do not define block structure.

## Functions, scope, and recursion

```text
def factorial(n) {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}
```

Function arity is checked at runtime. Each invocation receives fresh parameter/local state while retaining lexical visibility of enclosing definitions. Braced blocks do not create additional scopes in v1.1.

`return` exits the nearest user-defined function immediately, including from nested blocks or loops. `return` outside a function is a runtime error.

## Native structured data

### Squad

`Squad` is an ordered mutable WarPy40K collection.

Literal syntax:

```text
numbers = Squad[10, 20, 30]
party = Squad[
    Dataslate{name: "Acolyte", health: 100},
    Dataslate{name: "Interrogator", health: 120}
]
```

Access is zero-based:

```text
numbers[1]          # 20
party[0].health     # 100
```

Supported operations:

| Operation | Semantics |
|---|---|
| `len(squad)` | number of members |
| `Deploy(squad, value)` | append a member in place and return the Squad |
| `Extract(squad)` | remove and return the final member |
| `Extract(squad, index)` | remove and return a member by index |
| `Reassign(squad, index, value)` | replace a member in place and return the Squad |
| `Purge squad` | return a new empty Squad |

Squad indexing requires an integer. Mutation is intentionally explicit.

### Dataslate

`Dataslate` is an immutable-by-default structured record.

```text
marine = Dataslate{
    name: "Titus",
    health: 100,
    rank: "Captain"
}
```

Fields can be accessed with `.`:

```text
marine.name
marine.health
```

Field names in a literal may be identifiers or strings. Duplicate fields are rejected by the parser.

Dataslate updates are persistent:

```text
wounded = Inscribe(marine, "health", 75)

print(marine.health)   # 100
print(wounded.health)  # 75
```

Supported operations:

| Operation | Semantics |
|---|---|
| `len(dataslate)` | number of fields |
| `Inscribe(dataslate, key, value)` | return a new record with key added/updated |
| `Erase(dataslate, key)` | return a new record without key |
| `Purge dataslate` | return a new empty Dataslate |
| `==` / `!=` | structural equality |

Access to a missing field is a runtime error. `Inscribe` and `Erase` never mutate the original Dataslate.

### Chained access

Postfix access composes:

```text
party = Squad[
    Dataslate{name: "Acolyte", stats: Dataslate{health: 88}}
]

party[0].stats.health
```

This is parsed into explicit WarPy40K index/field AST nodes rather than delegated to Python attribute access.

## Built-in functions

| Function | Description |
|---|---|
| `print(...)` | print values |
| `input(prompt)` | read a string from standard input |
| `int(x)` | convert a number, Boolean, or decimal string to integer |
| `float(x)` | convert a number, Boolean, or decimal string to float |
| `str(x)` | convert a runtime value to text |
| `random()` | random float in `[0, 1)` |
| `abs(x)` | absolute value |
| `min(...)` / `max(...)` | extrema |
| `pow(x, y)` | exponentiation |
| `len(x)` | length for supported values, including Squad/Dataslate |
| `range(...)` | host-backed range value |
| `Deploy(...)` | Squad append |
| `Extract(...)` | Squad removal |
| `Reassign(...)` | Squad indexed replacement |
| `Inscribe(...)` | persistent Dataslate update/add |
| `Erase(...)` | persistent Dataslate field removal |
| `exit(code)` | terminate execution |

Some built-ins remain Python-hosted. Reducing host-language leakage remains a roadmap goal.

## Built-in constants

```text
FAITH = 100
CORRUPTION = 0
POPULATION = 1000000
True
False
```

## WarPy40K expressions

| Expression | Current semantics |
|---|---|
| `Inquisition target` | evaluate target truthiness; without target => `True` |
| `Emperor target` | apply the current faith factor to numeric targets |
| `Chaos target` | apply corruption/randomness to a target; without target => random value |
| `Purge target` | reset according to runtime type, including empty Squad/Dataslate |
| `Exterminatus target` | evaluate optional target and represent total annihilation |
| `Bless target` | positive transformation; numeric values increase by 10% |
| `Curse target` | negative transformation; numeric values decrease by 10% |

The thematic semantics will deepen during the 1.x line. See [roadmap.md](roadmap.md).

## Turing completeness

WarPy40K includes a constructive demonstration in [`examples/minsky_universal.wp40k`](../examples/minsky_universal.wp40k), which implements an interpreter for deterministic two-counter Minsky machines in WarPy40K itself.

See [turing_completeness.md](turing_completeness.md) for the construction and scope of the claim.

## Grammar sketch

This is descriptive rather than a formal specification:

```text
program          := statement*
statement        := if_stmt
                  | while_stmt
                  | function_def
                  | return_stmt
                  | block
                  | expression

if_stmt          := "if" expression statement ("else" statement)?
while_stmt       := "while" expression statement
function_def     := "def" IDENTIFIER "(" parameters? ")" block
parameters       := IDENTIFIER ("," IDENTIFIER)*
return_stmt      := "return" expression?
block            := "{" statement* "}"

primary          := scalar_literal
                  | IDENTIFIER
                  | function_call
                  | squad_literal
                  | dataslate_literal
                  | "(" expression ")"
                  | warpy_expression

squad_literal    := "Squad" "[" (expression ("," expression)*)? "]"
dataslate_literal:= "Dataslate" "{" (field ("," field)*)? "}"
field            := (IDENTIFIER | STRING) ":" expression
postfix_access   := primary ("[" expression "]" | "." IDENTIFIER)*
```

A formal versioned grammar remains planned for a later 1.x release.
