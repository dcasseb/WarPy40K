# WarPy40K

**Current version: 1.0.0**

A small Warhammer 40K-inspired interpreted programming language implemented in Python, with its own lexer, recursive-descent parser, AST, runtime semantics, functions, recursion, unrestricted control flow, and a constructive Turing-completeness demonstration.

## WarPy40K 1.0

Version **1.0.0** marks the transition from an experimental themed interpreter to a small but complete computational language core.

WarPy40K now supports:

- variables and mutable assignment;
- integers, floats, strings, and Booleans;
- arithmetic and comparisons;
- Boolean logic;
- `if` / `else`;
- unrestricted `while`;
- braces-delimited blocks;
- user-defined functions;
- function parameters and arity validation;
- lexical function scopes;
- `return` with real control-flow unwind;
- direct recursion;
- built-in functions;
- WarPy40K-specific expressions;
- REPL and file execution;
- token and AST inspection.

Under the standard theoretical abstraction in which memory and integer size are treated as unbounded, **WarPy40K 1.0 is Turing complete**.

Unlike the earlier claim based only on the presence of unrestricted loops, v1.0 includes a **constructive demonstration**: [`examples/minsky_universal.wp40k`](examples/minsky_universal.wp40k) implements a universal interpreter for encoded deterministic two-counter Minsky machines entirely in WarPy40K source code.

See [`docs/turing_completeness.md`](docs/turing_completeness.md) for the construction and proof argument.

## Constructive universality demonstration

The v1.0 example defines the fixed function:

```text
run_minsky(program, program_base, field_base, start_pc, c1, c2, max_steps, trace)
```

The simulated Minsky program is supplied as a natural number. WarPy40K decodes instructions from that integer and executes the corresponding counter-machine transitions.

Instruction set:

| Opcode | Meaning |
|---:|---|
| `0` | `HALT` |
| `1` | increment counter 1 and jump |
| `2` | increment counter 2 and jump |
| `3` | decrement-or-zero-jump on counter 1 |
| `4` | decrement-or-zero-jump on counter 2 |

An instruction is encoded with a field base `F`:

```text
word = opcode + F * A + F^2 * B
```

and a complete finite program is encoded with program base `P`:

```text
program = sum(word_i * P^i)
```

The included demonstration machine transfers `C2` into `C1`.

Starting from:

```text
C1 = 3
C2 = 4
```

it halts with:

```text
C1 = 7
C2 = 0
```

Run it with:

```bash
warpy40k examples/minsky_universal.wp40k
```

The automated v1.0 tests also execute different encoded machines, exercise the zero branch of `DECJZ`, and validate a deliberately non-halting program through the optional debugging step guard.

## Why this is stronger than a hard-coded example

`run_minsky` is fixed while `program` is data.

That means the same WarPy40K source interpreter can execute different finite two-counter machine programs simply by receiving different encoded integers.

Conceptually:

```text
Turing machine
      ↓ simulation
Two-counter Minsky machine
      ↓ natural-number encoding
WarPy40K run_minsky(program, ...)
      ↓
WarPy40K runtime
```

Because deterministic two-counter Minsky machines are computationally universal, this supplies a constructive route from a universal machine model into WarPy40K.

As with every real implementation of a Turing-complete language, actual execution is still limited by physical memory, time, the host Python runtime, and the operating system.

## Example syntax

### Variables

```text
x = 42
y = x + 10
```

### Conditionals

```text
if x > 5 {
    print("greater")
}
else {
    print("smaller or equal")
}
```

### While

```text
counter = 0

while counter < 5 {
    counter = counter + 1
}
```

### Functions and recursion

```text
def factorial(n) {
    if n <= 1 {
        return 1
    }

    return n * factorial(n - 1)
}

print(factorial(6))
```

## WarPy40K expressions

WarPy40K includes language-specific expressions inspired by the Warhammer 40K setting:

| Expression | Current role |
|---|---|
| `Inquisition` | truth/judgment |
| `Emperor` | faith-based transformation |
| `Chaos` | corruption/randomness |
| `Purge` | destructive/reset transformation |
| `Exterminatus` | total-annihilation semantic marker |
| `Bless` | positive transformation |
| `Curse` | negative transformation |

The post-1.0 roadmap deliberately develops these concepts into deeper semantics instead of merely adding Python features under themed names.

## Installation

```bash
git clone https://github.com/dcasseb/WarPy40K.git
cd WarPy40K
pip install -e .
```

## Command line

```bash
# Run a program
warpy40k examples/recursion.wp40k

# Run the v1.0 universal-machine demonstration
warpy40k examples/minsky_universal.wp40k

# Execute source directly
warpy40k -c "Bless Emperor 100"

# Start the REPL
warpy40k -i

# Inspect tokens
warpy40k --tokens examples/minsky_universal.wp40k

# Inspect AST
warpy40k --ast examples/minsky_universal.wp40k
```

## Python API

```python
from warpy40k import evaluate

result = evaluate("2 + 3 * 4")
print(result)  # 14
```

Python is currently the **implementation host**, not the WarPy40K surface language. WarPy40K source is tokenized, parsed into its own AST, and executed by its own interpreter rather than being passed to Python `eval()` or `exec()`.

Some runtime values and built-ins are still Python-backed. Reducing accidental host-language behavior is an explicit goal of the 1.x roadmap.

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
Lexical runtime environments
      ↓
Result / effects
```

## Version milestones

### v0.8

- basic lexer/parser/interpreter pipeline;
- variables and expressions;
- conditional execution;
- internal but inaccessible loop infrastructure;
- not yet defensibly Turing complete as a surface language.

### v0.9

- unrestricted `while` exposed in the surface language;
- user-defined functions;
- parameters and lexical call scopes;
- real `return` unwind;
- recursion;
- computational core becomes Turing complete under the usual theoretical model.

### v1.0 — Current

- universal two-counter Minsky-machine interpreter written in WarPy40K;
- machine programs encoded as natural-number data;
- constructive Turing-completeness documentation;
- automated v1.0 machine-interpreter tests;
- package metadata promoted to `1.0.0`;
- language roadmap shifts from “mini-Python functionality” toward explicitly WarPy40K semantics.

## Identity-focused roadmap

The full roadmap is maintained in [`docs/roadmap.md`](docs/roadmap.md).

Planned milestones:

| Version | Direction |
|---|---|
| **1.1** | **Squads & Dataslates** — WarPy40K-owned collection and structured-data types |
| **1.2** | **Orders** — pattern-oriented command dispatch |
| **1.3** | **Warp effect model** — explicit, seedable, replayable nondeterminism |
| **1.4** | **Inquisition contracts** — assertions, preconditions, and postconditions |
| **1.5** | **Codex modules** — native module/export/import semantics |
| **1.6** | **Sanctioned effects** — explicit capabilities for I/O and external effects |
| **1.7** | **Crusades** — structured iteration over WarPy40K iterables |
| **1.8** | **Machine-Spirit introspection** — stable AST/runtime tracing and scope inspection |
| **1.9** | **Forge bytecode** — small documented bytecode plus VM |
| **2.0** | **Independent runtime** — language semantics increasingly independent of accidental Python behavior |

The guiding rule is simple:

> New features should have WarPy40K semantics, not merely Python semantics with Warhammer terminology.

## Documentation

- [`docs/language_reference.md`](docs/language_reference.md) — v1.0 language reference
- [`docs/turing_completeness.md`](docs/turing_completeness.md) — constructive universality proof
- [`docs/roadmap.md`](docs/roadmap.md) — post-1.0 language roadmap
- [`docs/warpy_expressions.md`](docs/warpy_expressions.md) — themed expressions
- [`docs/api_reference.md`](docs/api_reference.md) — Python-host API

## Development

```bash
pip install -r requirements-dev.txt
pytest
pytest --cov=src/warpy40k
```

Formatting and type checks:

```bash
black src/ tests/
isort src/ tests/
mypy src/warpy40k
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Acknowledgments

- Inspired by the Warhammer 40K universe created by Games Workshop
- Implemented in Python as an educational programming-language/interpreter project

**For the Emperor!**
