# WarPy40K

**Current version: 1.2.0**

A small Warhammer 40K-inspired interpreted programming language implemented in Python, with its own lexer, recursive-descent parser, AST, runtime semantics, native structured data, pattern-oriented command dispatch, functions, recursion, unrestricted control flow, and a constructive Turing-completeness demonstration.

## WarPy40K 1.2 — Orders & Pattern Dispatch

Version **1.2.0** adds a WarPy40K-native decision model that composes directly with the structured data introduced in v1.1.

The release introduces:

- `Order target { ... }` dispatch;
- ordered `When pattern { ... }` clauses with first-match-wins semantics;
- optional `Otherwise` fallback;
- no implicit fall-through;
- literal and wildcard patterns;
- local pattern bindings;
- optional guards using `When pattern if condition`;
- partial `Dataslate` structural patterns;
- exact-shape `Squad` patterns;
- dedicated pattern/Order AST nodes and runtime matching;
- the v1.2 refactor of *The Vault of Vharax* using `Order` for exploration and combat commands.

Example:

```text
target = Dataslate{
    name: "Vharax",
    status: "Heretic",
    threat: 8
}

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

A plain identifier inside a pattern is a temporary binding. Dataslate patterns are partial, so extra target fields are allowed. Squad patterns currently require an exact member count.

See [`docs/orders.md`](docs/orders.md) for the complete v1.2 semantics.

## Core language

WarPy40K supports:

- integers, floats, strings, and Booleans;
- variables and mutable assignment;
- arithmetic, comparisons, and Boolean logic;
- `if` / `else`;
- unrestricted `while`;
- braces-delimited blocks;
- user-defined functions and parameters;
- lexical function scopes;
- `return` with real control-flow unwind;
- direct recursion;
- native `Squad` and `Dataslate` values;
- native `Order` pattern dispatch;
- built-in functions and explicit `int`, `float`, `str` conversions;
- WarPy40K-specific expressions;
- REPL and whole-file execution;
- token and AST inspection.

## Native data

### Squad

A `Squad` is ordered and explicitly mutable:

```text
party = Squad[
    Dataslate{name: "Acolyte", health: 100},
    Dataslate{name: "Interrogator", health: 120}
]

print(party[0].name)
Deploy(party, Dataslate{name: "Servo Skull", health: 20})
Reassign(party, 0, Dataslate{name: "Veteran Acolyte", health: 110})
removed = Extract(party, 1)
```

### Dataslate

A `Dataslate` is an immutable-by-default structured record:

```text
marine = Dataslate{name: "Titus", health: 100}
wounded = Inscribe(marine, "health", 75)

print(marine.health)   # 100
print(wounded.health)  # 75
```

`Inscribe` and `Erase` return new Dataslates instead of mutating the original.

## Order patterns

Literal dispatch:

```text
Order action {
    When "1" { print("Boltgun") }
    When "2" { print("Chainsword") }
    Otherwise { print("Invalid order") }
}
```

Wildcard and binding:

```text
Order reading {
    When 0 { print("Clear") }
    When value if value > 90 { print("Critical:", value) }
    When _ { print("Nominal") }
}
```

Structured Dataslate matching:

```text
Order marine {
    When Dataslate{health: hp} if hp <= 0 {
        print("Battle brother fallen")
    }

    When Dataslate{name: name} {
        print(name, "still stands")
    }
}
```

Structured Squad matching:

```text
Order Squad["Titus", 100] {
    When Squad[name, health] {
        print(name, health)
    }
}
```

Bindings exist only while evaluating the selected clause's guard/body; ordinary assignments made by the body keep their normal surrounding-scope behavior.

## Official showcase — The Vault of Vharax

The official interactive showcase is a terminal roguelike/RPG written in WarPy40K:

```bash
warpy40k examples/vault_of_vharax.wp40k
```

The current version demonstrates:

- `Squad` and `Dataslate` world/inventory data;
- interactive I/O and mutable game state;
- `Order` dispatch for strategic and combat commands;
- loops and functions;
- RNG-driven events and combat;
- `Chaos`, `Inquisition`, `Bless`, `Curse`, `Emperor`, `Purge`, and `Exterminatus`.

The showcase is also a regression benchmark: CI verifies its structured-data model, presence of native `Order` AST nodes, withdrawal, victory, defeat, corruption, invalid commands, and medicae behavior.

## Constructive Turing completeness

Under the standard theoretical abstraction in which memory and integer size are unbounded, WarPy40K is Turing complete.

The repository includes a constructive demonstration:

```bash
warpy40k examples/minsky_universal.wp40k
```

`examples/minsky_universal.wp40k` implements, in WarPy40K itself, an interpreter for deterministic two-counter Minsky machines. See [`docs/turing_completeness.md`](docs/turing_completeness.md) for the formal construction and scope of the claim.

## WarPy40K expressions

| Expression | Current role |
|---|---|
| `Inquisition` | truth/judgment |
| `Emperor` | faith-based transformation |
| `Chaos` | corruption/randomness |
| `Purge` | reset/destructive transformation |
| `Exterminatus` | total-annihilation semantic marker |
| `Bless` | positive transformation |
| `Curse` | negative transformation |

The roadmap deepens these semantics instead of merely adding Python features with themed names.

## Installation

```bash
git clone https://github.com/dcasseb/WarPy40K.git
cd WarPy40K
pip install -e .
```

## Command line

```bash
# Official v1.2 showcase
warpy40k examples/vault_of_vharax.wp40k

# Universal-machine demonstration
warpy40k examples/minsky_universal.wp40k

# Execute source directly
warpy40k -c "Order 2 { When 1 { print(\"one\") } When 2 { print(\"two\") } }"

# REPL
warpy40k -i

# Inspect source
warpy40k --tokens examples/vault_of_vharax.wp40k
warpy40k --ast examples/vault_of_vharax.wp40k
```

## Python host API

```python
from warpy40k import evaluate

result = evaluate('Dataslate{name: "Titus", health: 100}.health')
print(result)  # 100
```

Python is the current **implementation host**, not the WarPy40K surface language. Source is tokenized, parsed into WarPy40K's own AST, and executed by its interpreter; it is not passed to Python `eval()` or `exec()`.

## Architecture

```text
WarPy40K source
      ↓
Lexer
      ↓
Tokens
      ↓
Recursive-descent parser
      ↓
WarPy40K AST
      ↓
Tree-walking interpreter
      ↓
WarPy40K runtime values / lexical environments
      ↓
Results and effects
```

## Version milestones

### v1.0

Universal computational core, constructive two-counter Minsky-machine demonstration, and the first *Vault of Vharax* showcase.

### v1.1

WarPy40K-owned structured data with mutable `Squad`, persistent `Dataslate`, native access syntax, and explicit data operations.

### v1.2 — Current

Pattern-oriented command dispatch with `Order`, `When`, `Otherwise`, guards, bindings, Squad patterns, Dataslate patterns, and showcase integration.

## Identity-focused roadmap

See [`docs/roadmap.md`](docs/roadmap.md).

| Version | Direction |
|---|---|
| **1.3** | **Warp effect model** — explicit, seedable, replayable nondeterminism |
| **1.4** | **Inquisition contracts** — assertions, preconditions, and postconditions |
| **1.5** | **Codex modules** — native module/export/import semantics |
| **1.6** | **Sanctioned effects** — capability boundaries for external effects |
| **1.7** | **Crusades** — structured iteration over Squads and other iterables |
| **1.8** | **Machine-Spirit introspection** — stable AST/runtime tracing |
| **1.9** | **Forge bytecode** — documented bytecode plus VM |
| **2.0** | **Independent runtime** — increasingly implementation-independent semantics |
| **2.1–2.6** | **Forge Era (exploratory)** — vectors, buffers, native interface, real-time execution, concurrency, and eventual 3D simulation |

The next milestone, **v1.3**, will make the Warp a real execution boundary: seeded Chaos streams, deterministic replay, and reproducible game/simulation traces.

> New features should have WarPy40K semantics, not merely Python semantics with Warhammer terminology.

## Development

```bash
pip install -r requirements-dev.txt
pytest
pytest --cov=warpy40k
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/warpy40k
```

GitHub Actions enforces formatting, import order, linting, typing, test coverage, and the supported Python test matrix.

## Documentation

- [`docs/language_reference.md`](docs/language_reference.md) — language syntax and semantics
- [`docs/orders.md`](docs/orders.md) — v1.2 pattern dispatch guide
- [`docs/turing_completeness.md`](docs/turing_completeness.md) — constructive universality demonstration
- [`docs/roadmap.md`](docs/roadmap.md) — identity-focused release plan
- [`docs/showcase_v10.md`](docs/showcase_v10.md) — original showcase design notes
- [`docs/warpy_expressions.md`](docs/warpy_expressions.md) — themed expressions
- [`CHANGELOG.md`](CHANGELOG.md) — release notes

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgments

- Inspired by the Warhammer 40K universe created by Games Workshop
- Implemented in Python as an educational programming-language/interpreter project

**For the Emperor!**
