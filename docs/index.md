# WarPy40K Documentation

Welcome to the documentation for **WarPy40K 1.0**, a small Warhammer 40K-inspired interpreted programming language with its own lexer, parser, AST, runtime semantics, unrestricted loops, user-defined functions, recursion, and a constructive Turing-completeness demonstration.

## Documentation

- **[Getting Started](getting_started.md)** — installation and basic usage
- **[Language Reference](language_reference.md)** — current v1.0 syntax and semantics
- **[Turing Completeness](turing_completeness.md)** — constructive proof using a universal two-counter Minsky-machine interpreter
- **[Language Roadmap](roadmap.md)** — identity-focused roadmap from v1.0 toward v2.0
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

Run a program:

```bash
warpy40k examples/recursion.wp40k
```

Run the universal Minsky-machine demonstration:

```bash
warpy40k examples/minsky_universal.wp40k
```

The expected final result of the included transfer-machine example is `7`.

## Current language core

WarPy40K 1.0 supports:

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
- WarPy40K-specific expressions;
- REPL, token inspection, and AST inspection.

Under the usual theoretical unbounded-memory abstraction, WarPy40K 1.0 is Turing complete. The repository contains an explicit universal-machine construction rather than relying only on that observation.

## Direction after 1.0

The 1.x series is intended to strengthen WarPy40K's identity instead of reproducing Python feature-for-feature. Planned concepts include native `Squad` and `Dataslate` data types, an explicit Warp nondeterminism model, Inquisition contracts, Codex modules, sanctioned effect capabilities, structured iteration, runtime introspection, and eventually a small WarPy40K bytecode VM.

See the [Language Roadmap](roadmap.md) for the full plan.
