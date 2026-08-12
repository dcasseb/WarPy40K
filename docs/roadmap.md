# WarPy40K Language Roadmap

This roadmap defines the evolution of WarPy40K after 1.0. The goal is not to reproduce Python feature-for-feature with Warhammer 40K names. Future features should give the language a recognizable semantic identity while preserving a small, understandable interpreter core.

## Design principles

### 1. Theme must affect semantics

A feature should not exist only because a Python keyword was renamed. New concepts should change how programs are modeled, validated, or executed.

### 2. Keep the deterministic core explicit

Ordinary WarPy40K code should remain predictable. Randomness, I/O, mutation across module boundaries, and other effects should become increasingly explicit rather than silently spreading through the runtime.

### 3. Preserve inspectability

WarPy40K is an educational language. Users should be able to inspect tokens, AST nodes, runtime state, and eventually bytecode without requiring a large compiler toolchain.

### 4. Prefer a small number of strong abstractions

The language should avoid accumulating every Python convenience feature. A smaller orthogonal set of constructs is preferable to many overlapping forms.

### 5. Treat 1.x as a compatibility line

Programs written for 1.0 should continue to work throughout the 1.x series unless a behavior is clearly documented as experimental.

---

## v1.0 — Universal Core

**Theme:** The Machine Spirit awakens.

Status: implemented.

Goals:

- stabilize unrestricted `while`;
- stabilize user-defined functions, lexical call scopes, recursion, and `return`;
- provide a constructive Turing-completeness demonstration;
- implement a universal two-counter Minsky-machine interpreter in WarPy40K itself;
- add regression tests proving that the interpreter can execute different encoded machines;
- publish the formal construction in `docs/turing_completeness.md`.

Identity contribution:

WarPy40K 1.0 establishes that the language is not merely a themed expression evaluator. It has a complete computational core that can interpret another universal machine model from encoded data.

---

## v1.1 — Squads and Dataslates

**Theme:** Native data should feel organized rather than borrowed from Python.

Introduce two first-class data abstractions.

### `Squad`

An ordered mutable collection with language-level operations for composition and extraction. It should be a WarPy40K runtime type rather than exposing Python `list` directly.

Proposed capabilities:

- literal syntax for creating a squad;
- indexing;
- append/remove operations;
- iteration support once a native iteration protocol exists;
- equality and length;
- explicit copying semantics.

### `Dataslate`

A key/value record abstraction designed for named structured state.

Proposed capabilities:

- literal syntax;
- field lookup;
- immutable-by-default values with explicit update operations;
- structural equality;
- predictable serialization for debugging and REPL display.

Why this matters:

Instead of simply exposing Python lists and dictionaries, WarPy40K begins to own its runtime data model.

---

## v1.2 — Orders and Pattern Dispatch

**Theme:** Programs express decisions as orders rather than long chains of nested conditionals.

Add a pattern-dispatch construct tentatively named `Order`.

Conceptually:

```text
Order target {
    When 0 { ... }
    When 1 { ... }
    Otherwise { ... }
}
```

The final grammar may differ, but the semantic goals are:

- exact-value patterns;
- Boolean guards;
- destructuring of `Squad` and `Dataslate` values;
- exhaustiveness diagnostics where possible;
- no implicit fall-through.

This should not merely clone Python `match`. The language should favor explicit command-style dispatch and simple inspectable AST semantics.

---

## v1.3 — The Warp Effect Model

**Theme:** Nondeterminism should be visible in source code.

`Chaos` is currently a normal expression backed by randomness. v1.3 should evolve randomness into an explicit effect system centered on `Warp` regions.

Proposed semantics:

```text
Warp seed 42 {
    x = Chaos 100
}
```

Goals:

- deterministic seeded replay;
- explicit scope for randomness;
- ability to record/replay Warp outcomes in tests;
- runtime error or warning for uncontrolled nondeterminism outside an allowed Warp context, depending on compatibility decisions;
- preserve `Chaos` as a domain-specific source of nondeterministic values rather than a thin alias of `random()`.

Identity contribution:

The Warp becomes a real execution concept: a controlled boundary between deterministic computation and nondeterministic effects.

---

## v1.4 — Inquisition Contracts

**Theme:** `Inquisition` becomes more than truthiness.

Extend the existing concept into language-level contracts and assertions.

Potential forms:

```text
Inquisition condition
Inquisition value satisfies predicate
```

Goals:

- assertions with source locations;
- function preconditions and postconditions;
- optional runtime contract checking;
- useful diagnostic output showing the failed condition and current values;
- preserve the short expression form for Boolean judgment where compatibility requires it.

This gives a core WarPy40K keyword a deeper semantic role instead of adding unrelated new syntax.

---

## v1.5 — Codex Modules

**Theme:** Programs become collections of named codices rather than Python-backed files with incidental visibility.

Introduce a native module system tentatively centered on `Codex`.

Goals:

- explicit exports;
- explicit imports;
- module-local scope;
- deterministic resolution rules;
- no automatic access to arbitrary Python modules;
- standard-library modules implemented behind the same public abstraction.

Possible conceptual syntax:

```text
Invoke Math from Codex Core
```

The exact syntax should be prototyped before stabilization.

---

## v1.6 — Sanctioned Effects

**Theme:** Side effects become capabilities rather than ambient privileges.

Introduce explicit capability boundaries for operations such as:

- console/file I/O;
- environment access;
- process exit;
- time;
- networking if it is ever added.

Pure functions should be distinguishable from functions that require sanctioned capabilities.

Potential concepts:

- `Sanctioned` effect blocks;
- effect metadata on functions;
- REPL display of required capabilities;
- test mode that denies undeclared effects.

Identity contribution:

The language gains a thematic but technically meaningful distinction between pure computation and externally authorized effects.

---

## v1.7 — Crusades: Structured Iteration

**Theme:** Iteration should express campaigns over data rather than only manual counter loops.

Add a native iterable protocol and one high-level loop construct, tentatively named `Crusade`.

Goals:

- iterate over `Squad` values, ranges, and module-defined iterables;
- clear ownership of the loop variable;
- no hidden mutation of the collection being traversed;
- compatibility with `while` rather than replacement of it.

The construct should compile or lower into a small existing core so the interpreter remains understandable.

---

## v1.8 — Machine-Spirit Introspection

**Theme:** The runtime explains itself.

Expand WarPy40K's educational tooling into first-class introspection.

Goals:

- stable textual AST format;
- execution trace mode;
- environment/scope inspection;
- function call tracing;
- Minsky-machine trace visualization data;
- deterministic snapshots suitable for tests and tutorials.

This version should make WarPy40K especially useful for teaching interpreters, control flow, scopes, and computation models.

---

## v1.9 — Forge Bytecode

**Theme:** Separate language semantics from the Python tree-walking implementation.

Introduce a compact WarPy40K bytecode and a small virtual machine.

Goals:

- lower AST to bytecode;
- preserve tree-walking interpreter as a reference implementation during transition;
- deterministic bytecode format;
- disassembler;
- differential tests: AST interpreter result == bytecode VM result;
- no dependency on Python `eval` or `exec`.

The bytecode should be intentionally small and documented.

---

## v2.0 — The Independent Runtime

**Theme:** WarPy40K becomes a language platform rather than only a Python-hosted interpreter project.

Candidate milestones:

- bytecode VM becomes the primary execution engine;
- stable module/data/effect semantics;
- versioned language specification;
- standard library built around WarPy40K abstractions rather than direct Python objects;
- self-host one meaningful compiler/interpreter component, such as the Minsky encoder, parser utilities, or a subset compiler;
- conformance test suite independent of implementation details.

Full self-hosting is not required for 2.0. The important transition is that the externally visible language semantics no longer depend on accidental Python behavior.

---

## Features deliberately not prioritized

The following should not be added merely because Python has them:

- classes and inheritance;
- decorators;
- list/dict comprehensions;
- multiple equivalent loop syntaxes;
- implicit operator overloading;
- unrestricted reflection into Python objects;
- arbitrary Python imports;
- async syntax before the language has a clear concurrency model.

Any of these may eventually be justified, but only if they fit WarPy40K's own semantic model.

## Long-term identity

The intended identity is:

> A small, inspectable, Turing-complete language with Warhammer-inspired semantics around judgment, corruption/nondeterminism, structured data, authorization of effects, and machine introspection.

Python remains the implementation host in the near term. The language itself should progressively expose fewer accidental Python semantics and more explicitly specified WarPy40K behavior.
