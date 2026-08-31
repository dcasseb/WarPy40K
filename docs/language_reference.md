# WarPy40K Language Reference — v1.2.0

This document describes the stable language core available in WarPy40K 1.2.

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

Arithmetic: `+ - * / ^`  
Comparison: `== != > < >= <=`  
Boolean logic: `AND OR NOT`

Parentheses may be used for grouping.

## Blocks and control flow

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

Function arity is checked at runtime. Each invocation receives fresh parameter/local state while retaining lexical visibility of enclosing definitions. Braced blocks do not create additional scopes.

`return` exits the nearest user-defined function immediately, including from nested blocks or loops. `return` outside a function is a runtime error.

## Native structured data

### Squad

`Squad` is an ordered mutable WarPy40K collection:

```text
party = Squad[
    Dataslate{name: "Acolyte", health: 100},
    Dataslate{name: "Interrogator", health: 120}
]

print(party[0].health)
Deploy(party, Dataslate{name: "Servo Skull", health: 20})
```

Supported operations:

| Operation | Semantics |
|---|---|
| `len(squad)` | number of members |
| `Deploy(squad, value)` | append in place and return the Squad |
| `Extract(squad)` | remove and return the last member |
| `Extract(squad, index)` | remove and return member at index |
| `Reassign(squad, index, value)` | replace member in place |
| `Purge squad` | return a new empty Squad |

Indexing is zero-based and requires an integer.

### Dataslate

`Dataslate` is an immutable-by-default structured record:

```text
marine = Dataslate{name: "Titus", health: 100}
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

Field names may be identifiers or strings. Duplicate fields are rejected. Missing-field access is a runtime error.

### Chained access

```text
party[0].stats.health
```

Postfix access is represented by explicit WarPy40K AST nodes rather than Python attribute/container access.

## Order pattern dispatch

`Order` is a statement that matches a target against ordered `When` patterns:

```text
Order action {
    When "1" {
        print("Boltgun")
    }

    When "2" {
        print("Chainsword")
    }

    Otherwise {
        print("Invalid order")
    }
}
```

Semantics:

- clauses are tested top-to-bottom;
- the first matching clause executes;
- there is no fall-through;
- `Otherwise` is optional and must be last;
- an unmatched Order without `Otherwise` performs no action.

### Pattern kinds

Literal patterns:

```text
When 42 { ... }
When -1 { ... }
When "Heretic" { ... }
When True { ... }
```

Wildcard:

```text
When _ { ... }
```

Binding:

```text
Order 42 {
    When value {
        print(value)
    }
}
```

A plain identifier in a pattern creates a temporary binding. It does not look up a variable with that name.

Partial Dataslate pattern:

```text
Order target {
    When Dataslate{status: "Heretic", threat: level} {
        print(level)
    }
}
```

Extra fields on the target Dataslate are allowed.

Exact-shape Squad pattern:

```text
Order Squad["Titus", 100] {
    When Squad[name, health] {
        print(name, health)
    }
}
```

The number of members must currently match exactly.

### Guards

Bindings are visible in an optional `if` guard:

```text
Order target {
    When Dataslate{status: "Heretic", threat: level} if level > 5 {
        print("Exterminatus review")
    }

    When Dataslate{status: "Heretic"} {
        print("Purge")
    }
}
```

If a structural pattern matches but its guard is false, matching proceeds to the next `When`.

Pattern bindings are restored/removed after the clause. Ordinary assignments to other variables retain normal surrounding-scope behavior.

See [orders.md](orders.md) for the dedicated v1.2 guide.

## Built-in functions

| Function | Description |
|---|---|
| `print(...)` | print values |
| `input(prompt)` | read a string |
| `int(x)` / `float(x)` / `str(x)` | explicit conversion |
| `random()` | random float in `[0, 1)` |
| `abs(x)` | absolute value |
| `min(...)` / `max(...)` | extrema |
| `pow(x, y)` | exponentiation |
| `len(x)` | length for supported values |
| `range(...)` | host-backed range value |
| `Deploy`, `Extract`, `Reassign` | Squad operations |
| `Inscribe`, `Erase` | persistent Dataslate transformations |
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
| `Inquisition target` | truth/judgment |
| `Emperor target` | faith-factor transformation |
| `Chaos target` | corruption/randomness |
| `Purge target` | reset according to runtime type |
| `Exterminatus target` | total-annihilation marker |
| `Bless target` | positive transformation |
| `Curse target` | negative transformation |

The next milestone, v1.3, develops `Chaos` into an explicit Warp nondeterminism model.

## Turing completeness

WarPy40K includes a constructive demonstration in [`examples/minsky_universal.wp40k`](../examples/minsky_universal.wp40k), which implements an interpreter for deterministic two-counter Minsky machines in WarPy40K itself.

See [turing_completeness.md](turing_completeness.md) for the construction and scope of the claim.

## Grammar sketch

```text
program          := statement*
statement        := if_stmt
                  | while_stmt
                  | function_def
                  | return_stmt
                  | order_stmt
                  | block
                  | expression

order_stmt       := "Order" expression "{" order_clause+ "}" ";"?
order_clause     := "When" pattern ("if" expression)? statement
                  | "Otherwise" statement

pattern          := scalar_literal
                  | "-" NUMBER
                  | IDENTIFIER
                  | "_"
                  | dataslate_pattern
                  | squad_pattern

dataslate_pattern:= "Dataslate" "{" (pattern_field ("," pattern_field)*)? "}"
pattern_field    := (IDENTIFIER | STRING) ":" pattern
squad_pattern    := "Squad" "[" (pattern ("," pattern)*)? "]"

squad_literal    := "Squad" "[" (expression ("," expression)*)? "]"
dataslate_literal:= "Dataslate" "{" (field ("," field)*)? "}"
field            := (IDENTIFIER | STRING) ":" expression
```

A formal versioned grammar remains planned for a later 1.x release.
