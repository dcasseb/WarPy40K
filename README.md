# WarPy40K

**Current version: 1.4.0**

A small Warhammer 40K-inspired interpreted programming language implemented in Python, with its own lexer, recursive-descent parser, AST, runtime semantics, native structured data, pattern-oriented command dispatch, explicit replayable nondeterminism, functions, recursion, unrestricted control flow, and a constructive Turing-completeness demonstration.

## WarPy40K 1.3 — The Warp Effect Model

Version **1.3.0** turns nondeterminism into an explicit language/runtime effect while preserving the legacy behavior of `Chaos` and `random()` outside Warp regions.

The release introduces:

- `Warp seed <integer> { ... }` regions;
- deterministic region-local random streams;
- shared deterministic draws for `Chaos` and the built-in `random()`;
- nested Warp regions with independent streams;
- correct parent-stream restoration after nested execution, errors, and returns;
- seed expressions evaluated exactly once;
- normalized Warp trace recording through `Interpreter.warp_trace`;
- deterministic replay through `Interpreter(warp_replay=...)`;
- explicit failures for exhausted or invalid replay traces.

Example:

```text
Warp seed 42 {
    first = Chaos
    second = random()
    print(first, second)
}
```

Running the same program with the same inputs and seed reproduces the same random decisions inside the Warp region.

Nested regions do not perturb their parent stream:

```text
Warp seed 10 {
    first = random()

    Warp seed 99 {
        nested = Chaos
    }

    second = random()
}
```

The contextual word `seed` is not globally reserved; it remains a normal identifier outside `Warp seed` syntax.

See [`docs/warp_effect_model.md`](docs/warp_effect_model.md) for the complete v1.3 semantics.

## WarPy40K 1.2 — Orders & Pattern Dispatch

Version **1.2.0** added a WarPy40K-native decision model that composes directly with the structured data introduced in v1.1.

It introduced:

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

## WarPy40K 1.4 — Inquisition Contracts

Version **1.4.0** adds executable assertions plus function preconditions and postconditions. Contract checking can be disabled through `Interpreter(contracts_enabled=False)`. See [`docs/inquisition_contracts.md`](docs/inquisition_contracts.md).

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
- explicit `Warp` nondeterministic regions;
- trace recording and deterministic replay of Warp decisions;
- built-in functions and explicit `int`, `float`, `str` conversions;
- WarPy40K-specific expressions;
- REPL and whole-file execution;
- token and AST inspection.

## Warp effect model

A Warp region owns a deterministic random stream:

```text
Warp seed 1337 {
    roll = Chaos
    sample = random()
}
```

`Chaos` and `random()` consume the same active stream. A function called from inside the region also consumes that stream:

```text
def draw() {
    return random()
}

Warp seed 1337 {
    a = random()
    b = draw()
}
```

At the Python API level, the reference interpreter can capture and replay normalized decisions:

```python
interpreter = Interpreter()
interpreter.execute(ast)
trace = interpreter.warp_trace

replay = Interpreter(warp_replay=trace)
replay.execute(ast)
assert replay.warp_replay_complete
```

The trace represents random decisions rather than Python RNG internal state, giving the future Forge runtime a portable replay contract.

Outside a Warp region, `Chaos` and `random()` retain their legacy process-global randomness behavior for 1.x compatibility.

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

The current showcase demonstrates:

- `Squad` and `Dataslate` world/inventory data;
- interactive I/O and mutable game state;
- `Order` dispatch for strategic and combat commands;
- loops and functions;
- RNG-driven events and combat;
- `Chaos`, `Inquisition`, `Bless`, `Curse`, `Emperor`, `Purge`, and `Exterminatus`.

The showcase remains a regression workload while the v1.3 Warp model establishes a deterministic foundation for future reproducible simulations and headless tests.

## Performance benchmarks

WarPy40K includes an official benchmark suite under [`benchmarks/`](benchmarks/). It establishes a reproducible performance baseline for the tree-walking interpreter and makes future runtime changes measurable, especially the planned Forge bytecode VM.

Run the default suite:

```bash
python benchmarks/run_benchmarks.py
```

Save machine-readable results:

```bash
python benchmarks/run_benchmarks.py --json benchmarks/results/v1.2-local.json
```

The v1.2 tree walker remains the historical performance baseline even as language semantics continue evolving.

The suite reports median and p95 latency for two modes:

- **execution-only** — parse once, then execute the same AST with a fresh interpreter per sample;
- **end-to-end** — tokenize, parse, and execute from source for every sample.

Canonical workloads cover arithmetic loops, user-function calls, recursion, `Order`, `Squad`, `Dataslate`, and a small two-counter Minsky-machine program. Equivalent Python baselines are reported where practical, along with the WarPy/Python slowdown ratio. Timing results are intentionally **not** used as a CI pass/fail threshold because shared CI hardware is noisy.

See [`benchmarks/README.md`](benchmarks/README.md) for methodology and interpretation.

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
| `Chaos` | corruption/randomness; deterministic inside Warp |
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
# Official showcase
warpy40k examples/vault_of_vharax.wp40k

# Universal-machine demonstration
warpy40k examples/minsky_universal.wp40k

# Execute source directly
warpy40k -c "Warp seed 42 { print(Chaos) }"

# REPL
warpy40k -i
```

## Development

```bash
pip install -r requirements-dev.txt
pytest
pytest --cov=warpy40k
black src/ tests/ benchmarks/
isort src/ tests/ benchmarks/
flake8 src/ tests/ benchmarks/
mypy src/warpy40k
python benchmarks/run_benchmarks.py
```

GitHub Actions enforces formatting, import order, linting, typing, test coverage, and the supported Python test matrix. Performance measurements are informational rather than gating.

## Documentation

- [`docs/language_reference.md`](docs/language_reference.md) — language syntax and semantics
- [`docs/warp_effect_model.md`](docs/warp_effect_model.md) — deterministic nondeterminism, traces, and replay
- [`docs/orders.md`](docs/orders.md) — v1.2 Order pattern semantics
- [`docs/turing_completeness.md`](docs/turing_completeness.md) — constructive universality demonstration
- [`docs/forge_runtime.md`](docs/forge_runtime.md) — path toward an independent native runtime
- [`docs/roadmap.md`](docs/roadmap.md) — identity-focused release plan and performance targets
- [`docs/showcase_v10.md`](docs/showcase_v10.md) — showcase design notes
- [`docs/warpy_expressions.md`](docs/warpy_expressions.md) — themed expressions
- [`benchmarks/README.md`](benchmarks/README.md) — performance benchmark methodology
- [`CHANGELOG.md`](CHANGELOG.md) — release notes

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgments

- Inspired by the Warhammer 40K universe created by Games Workshop
- Implemented in Python as an educational programming-language/interpreter project

**For the Emperor!**
