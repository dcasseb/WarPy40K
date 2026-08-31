# WarPy40K 1.2 Documentation

Welcome to the documentation for **WarPy40K 1.2**, a small Warhammer 40K-inspired interpreted language with its own lexer, parser, AST, runtime semantics, native structured data, pattern-oriented command dispatch, unrestricted loops, functions, recursion, and a constructive Turing-completeness demonstration.

## Documentation

- **[Getting Started](getting_started.md)** — installation and basic usage
- **[Language Reference](language_reference.md)** — current v1.2 syntax and semantics
- **[Orders and Pattern Dispatch](orders.md)** — `Order`, `When`, `Otherwise`, bindings, guards, Squad patterns, and Dataslate patterns
- **[Official Showcase](showcase_v10.md)** — design notes for *The Vault of Vharax*; the executable example evolves with each release
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

## What v1.2 adds

WarPy40K 1.2 introduces native pattern-oriented command dispatch:

```text
target = Dataslate{status: "Heretic", threat: 8, name: "Vharax"}

Order target {
    When Dataslate{status: "Heretic", threat: level} if level > 5 {
        print("Exterminatus review")
    }

    When Dataslate{status: "Heretic"} {
        print("Purge")
    }

    Otherwise {
        print("Observe")
    }
}
```

`Order` uses ordered first-match-wins semantics without fall-through. Patterns can match literals, wildcard `_`, bindings, exact-shape Squads, and partial Dataslates. Bindings can be referenced by guards and clause bodies.

## Current language core

WarPy40K 1.2 supports:

- scalar values, variables, arithmetic, comparisons, and Boolean logic;
- braces-delimited blocks;
- `if` / `else` and unrestricted `while`;
- functions, lexical call scopes, `return`, and recursion;
- native `Squad` collections and `Dataslate` records;
- `Order` / `When` / `Otherwise` structured dispatch with guards and bindings;
- built-ins and explicit `int`, `float`, and `str` conversions;
- WarPy40K-specific expressions;
- whole-file CLI execution, REPL, token inspection, and AST inspection.

Under the usual theoretical unbounded-memory abstraction, WarPy40K is Turing complete and includes an explicit constructive universal-machine artifact.

## Next milestone

The next planned release is **v1.3 — The Warp Effect Model**. It will turn `Chaos` randomness into an explicit, seedable and replayable language effect so complete game/simulation traces can be reproduced deterministically.

See the [Language Roadmap](roadmap.md) for the acceptance criteria and full release plan.
