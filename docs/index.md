# WarPy40K 1.1 Documentation

Welcome to the documentation for **WarPy40K 1.1**, a small Warhammer 40K-inspired interpreted language with its own lexer, parser, AST, runtime semantics, native structured data, unrestricted loops, functions, recursion, and a constructive Turing-completeness demonstration.

## Documentation

- **[Getting Started](getting_started.md)** — installation and basic usage
- **[Language Reference](language_reference.md)** — current v1.1 syntax and semantics, including Squad/Dataslate
- **[Official Showcase](showcase_v10.md)** — design notes for *The Vault of Vharax*; the executable example is now refactored for v1.1 native data
- **[Turing Completeness](turing_completeness.md)** — constructive two-counter Minsky-machine demonstration
- **[Language Roadmap](roadmap.md)** — identity-focused roadmap through the exploratory Forge Era
- **[WarPy40K Expressions](warpy_expressions.md)** — themed expressions and their current behavior
- **[Tutorials](tutorials.md)** — guided examples
- **[Examples](examples.md)** — program examples
- **[API Reference](api_reference.md)** — using WarPy40K from Python

## Quick start

```bash
git clone https://github.com/dcasseb/WarPy40K.git
cd WarPy40K
pip install -e .
```

Run the official interactive showcase:

```bash
warpy40k examples/vault_of_vharax.wp40k
```

Run the constructive universal-machine demonstration:

```bash
warpy40k examples/minsky_universal.wp40k
```

The two examples deliberately serve different purposes: *The Vault of Vharax* demonstrates practical interactive programming and native structured data; the Minsky-machine example demonstrates computational universality.

## What v1.1 adds

WarPy40K 1.1 introduces a language-owned data model:

```text
party = Squad[
    Dataslate{name: "Acolyte", health: 100},
    Dataslate{name: "Interrogator", health: 120}
]

print(party[0].health)
Deploy(party, Dataslate{name: "Servo Skull", health: 20})

wounded = Inscribe(party[0], "health", 75)
print(wounded.health)
```

- `Squad` is ordered and explicitly mutable through `Deploy`, `Extract`, and `Reassign`.
- `Dataslate` is immutable by default; `Inscribe` and `Erase` return new records.
- Index and field access are native AST/runtime operations, not Python attribute/container access.

## Current language core

WarPy40K 1.1 supports:

- scalar values, variables, arithmetic, comparisons, and Boolean logic;
- braces-delimited blocks;
- `if` / `else` and unrestricted `while`;
- functions, lexical call scopes, `return`, and recursion;
- native `Squad` collections and `Dataslate` records;
- built-ins and explicit `int`, `float`, and `str` conversions;
- WarPy40K-specific expressions;
- whole-file CLI execution, REPL, token inspection, and AST inspection.

Under the usual theoretical unbounded-memory abstraction, WarPy40K is Turing complete and includes an explicit constructive universal-machine artifact.

## Next milestone

The next planned language release is **v1.2 — Orders and Pattern Dispatch**, intended to replace many nested decision trees with a WarPy40K-native dispatch model capable of matching ordinary values and structured `Squad`/`Dataslate` data.

See the [Language Roadmap](roadmap.md) for the full plan.
