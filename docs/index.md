# WarPy40K 1.0.1 Documentation

Welcome to the documentation for **WarPy40K 1.0.1**, a small Warhammer 40K-inspired interpreted programming language with its own lexer, parser, AST, runtime semantics, unrestricted loops, user-defined functions, recursion, and a constructive Turing-completeness demonstration.

## Documentation

- **[Getting Started](getting_started.md)** — installation and basic usage
- **[Language Reference](language_reference.md)** — current v1.0.1 syntax and semantics
- **[Official v1.0 Showcase](showcase_v10.md)** — *The Vault of Vharax*, a terminal roguelike/RPG written entirely in WarPy40K
- **[Turing Completeness](turing_completeness.md)** — constructive proof using a universal two-counter Minsky-machine interpreter
- **[Language Roadmap](roadmap.md)** — identity-focused roadmap through the exploratory post-v2.0 Forge Era
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

Run the universal Minsky-machine demonstration:

```bash
warpy40k examples/minsky_universal.wp40k
```

These examples deliberately serve different purposes: *The Vault of Vharax* demonstrates practical interactive programming, while the Minsky-machine example demonstrates computational universality.

## Current language core

WarPy40K 1.0.1 supports:

- variables and mutable assignment;
- arithmetic and comparisons;
- Boolean logic;
- braces-delimited blocks;
- `if` / `else`;
- unrestricted `while`;
- user-defined functions;
- lexical function scopes;
- `return`;
- direct recursion;
- built-in functions;
- explicit `int`, `float`, and `str` conversions;
- WarPy40K-specific expressions;
- REPL, token inspection, and AST inspection.

Under the usual theoretical unbounded-memory abstraction, WarPy40K 1.0 is Turing complete. The repository contains an explicit universal-machine construction rather than relying only on that observation.

## Direction after 1.0

The 1.x series is intended to strengthen WarPy40K's identity instead of reproducing Python feature-for-feature. Planned concepts include native `Squad` and `Dataslate` data types, an explicit Warp nondeterminism model, Inquisition contracts, Codex modules, sanctioned effect capabilities, structured iteration, runtime introspection, and eventually a small WarPy40K bytecode VM.

The official roguelike showcase is also intended to evolve with those milestones. For example, v1.1 can replace scalar inventory/state patterns with native `Squad` and `Dataslate` values, providing a concrete application-level benchmark for each new feature.

See the [Language Roadmap](roadmap.md) for the full plan.
