# WarPy40K

**Current version: 1.1.0**

A small Warhammer 40K-inspired interpreted programming language implemented in Python, with its own lexer, recursive-descent parser, AST, runtime semantics, native structured data, functions, recursion, unrestricted control flow, and a constructive Turing-completeness demonstration.

## WarPy40K 1.1 — Squads & Dataslates

Version **1.1.0** is the first release in which WarPy40K owns meaningful structured-data semantics instead of relying only on host-language scalar values.

The release introduces:

- `Squad[...]`: an ordered mutable WarPy40K collection;
- `Dataslate{field: value}`: an immutable-by-default structured record;
- native indexing such as `squad[0]`;
- native field access such as `marine.health`;
- chained access such as `party[0].health`;
- explicit Squad operations: `Deploy`, `Extract`, and `Reassign`;
- persistent Dataslate transformations: `Inscribe` and `Erase`;
- structural Dataslate equality and stable language-level representations;
- `Purge` semantics for native structured values;
- the v1.1 refactor of *The Vault of Vharax* using Squads and Dataslates.

The design deliberately does **not** expose Python `list` or `dict` as the language's public data model.

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
- built-in functions and explicit `int`, `float`, `str` conversions;
- WarPy40K-specific expressions;
- REPL and whole-file execution;
- token and AST inspection.

## Native data

### Squad

A `Squad` is ordered and mutable:

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

`len(squad)` returns the member count.

### Dataslate

A `Dataslate` is a structured record and is immutable by default:

```text
marine = Dataslate{name: "Titus", health: 100}
wounded = Inscribe(marine, "health", 75)

print(marine.health)   # 100
print(wounded.health)  # 75
```

`Inscribe` returns a new Dataslate, updating or adding a field. `Erase` returns a new Dataslate without a field:

```text
public_record = Erase(
    Dataslate{name: "Agent", clearance: "Omega"},
    "clearance"
)
```

This persistent-record model is intentionally different from Squad mutation.

## Official showcase — The Vault of Vharax

The official interactive showcase is a terminal roguelike/RPG written in WarPy40K:

```bash
warpy40k examples/vault_of_vharax.wp40k
```

The v1.1 version models its four dungeon sectors as a `Squad` of `Dataslate` records:

```text
sectors = Squad[
    Dataslate{name: "Ash Gate", enemy: "Scrap Cultist", enemy_health: 44},
    Dataslate{name: "Reliquary of Static", enemy: "Warp-Touched Skitarii", enemy_health: 58}
]

sector = sectors[depth - 1]
print(sector.name)
```

Recovered relics are also stored as structured values and added with `Deploy`.

The game demonstrates interactive I/O, state, loops, functions, RNG, combat, native data, and the thematic expressions `Chaos`, `Inquisition`, `Bless`, `Curse`, `Emperor`, `Purge`, and `Exterminatus`.

## Constructive Turing completeness

Under the standard theoretical abstraction in which memory and integer size are unbounded, WarPy40K is Turing complete.

The repository includes a constructive demonstration:

```bash
warpy40k examples/minsky_universal.wp40k
```

`examples/minsky_universal.wp40k` implements, in WarPy40K itself, an interpreter for deterministic two-counter Minsky machines. The finite instruction payload is encoded as a natural number and decoded/executed by a fixed WarPy40K program.

See [`docs/turing_completeness.md`](docs/turing_completeness.md) for the formal construction and scope of the claim.

## WarPy40K expressions

| Expression | Current role |
|---|---|
| `Inquisition` | truth/judgment |
| `Emperor` | faith-based transformation |
| `Chaos` | corruption/randomness |
| `Purge` | reset/destructive transformation, including empty native data values |
| `Exterminatus` | total-annihilation semantic marker |
| `Bless` | positive transformation |
| `Curse` | negative transformation |

Future versions deepen these concepts rather than merely renaming Python features.

## Installation

```bash
git clone https://github.com/dcasseb/WarPy40K.git
cd WarPy40K
pip install -e .
```

## Command line

```bash
# Official v1.1 showcase
warpy40k examples/vault_of_vharax.wp40k

# Universal-machine demonstration
warpy40k examples/minsky_universal.wp40k

# Execute source directly
warpy40k -c "party = Squad[Dataslate{name: \"Acolyte\", health: 100}]; party[0].health"

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

### v0.9

Unrestricted loops, user-defined functions, lexical call scopes, `return`, and recursion completed the general-purpose computational core.

### v1.0

Added the constructive two-counter Minsky-machine universality demonstration and *The Vault of Vharax* terminal showcase.

### v1.0.1

Stabilized CLI execution, conversions, examples, CI, typing, linting, coverage, and the precision of the universality documentation.

### v1.1 — Current

Added WarPy40K-owned structured data with mutable `Squad`, persistent `Dataslate`, native access syntax, explicit data operations, regression tests, and a structured-data refactor of the official showcase.

## Identity-focused roadmap

See [`docs/roadmap.md`](docs/roadmap.md).

| Version | Direction |
|---|---|
| **1.2** | **Orders** — pattern-oriented command dispatch over values and native data |
| **1.3** | **Warp effect model** — explicit, seedable, replayable nondeterminism |
| **1.4** | **Inquisition contracts** — assertions, preconditions, and postconditions |
| **1.5** | **Codex modules** — native module/export/import semantics |
| **1.6** | **Sanctioned effects** — capability boundaries for external effects |
| **1.7** | **Crusades** — structured iteration over Squads and other iterables |
| **1.8** | **Machine-Spirit introspection** — stable AST/runtime tracing |
| **1.9** | **Forge bytecode** — documented bytecode plus VM |
| **2.0** | **Independent runtime** — increasingly implementation-independent semantics |
| **2.1–2.6** | **Forge Era (exploratory)** — vectors, buffers, native interface, real-time execution, concurrency, and eventual 3D simulation |

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
