# WarPy40K Language Roadmap

WarPy40K should evolve as its own small language, not as Python with Warhammer terminology. New features should change how programs are modeled, validated, executed, or inspected while preserving a compact and understandable implementation.

## Design principles

1. **Theme must affect semantics.** A themed keyword should do more than rename a Python construct.
2. **Keep the deterministic core explicit.** Randomness and external effects should become visible execution concepts.
3. **Preserve inspectability.** Tokens, AST, scopes, runtime values, and eventually bytecode should remain understandable.
4. **Prefer a few strong abstractions.** Avoid accumulating every Python convenience feature.
5. **Treat 1.x as a compatibility line.** Stable 1.0 programs should continue to run throughout 1.x unless behavior is explicitly experimental.
6. **Own the runtime data model.** Public WarPy40K values should have specified WarPy40K semantics rather than accidental Python container behavior.

---

## v1.0 — Universal Core

**Theme:** The Machine Spirit awakens.  
**Status:** implemented.

Delivered:

- unrestricted `while`;
- user-defined functions, lexical call scopes, recursion, and real `return`;
- constructive two-counter Minsky-machine universality demonstration;
- official terminal showcase *The Vault of Vharax*;
- regression/quality CI hardened in v1.0.1.

Identity contribution: WarPy40K has a complete computational core and can interpret another universal machine model from encoded data.

---

## v1.1 — Squads and Dataslates

**Theme:** Native data should feel organized rather than borrowed from Python.  
**Status:** implemented.

### `Squad`

`Squad` is a first-class ordered mutable WarPy40K collection:

```text
squad = Squad["Acolyte", "Interrogator"]
Deploy(squad, "Servo Skull")
Reassign(squad, 0, "Veteran Acolyte")
removed = Extract(squad, 1)
print(squad[0])
```

Implemented semantics:

- `Squad[...]` literal syntax;
- zero-based indexing;
- chained access such as `party[0].health`;
- `len()`;
- stable `Squad[...]` representation;
- explicit mutation with `Deploy`, `Extract`, and `Reassign`;
- `Purge squad` returns an empty Squad.

### `Dataslate`

`Dataslate` is a first-class immutable-by-default structured record:

```text
marine = Dataslate{name: "Titus", health: 100}
wounded = Inscribe(marine, "health", 75)
print(marine.health)
print(wounded.health)
```

Implemented semantics:

- `Dataslate{field: value}` literal syntax;
- identifier or string field names;
- duplicate-field rejection;
- `.field` lookup;
- structural equality;
- stable representation;
- `len()`;
- persistent `Inscribe` update/add operation;
- persistent `Erase` operation;
- `Purge dataslate` returns an empty Dataslate.

### Showcase validation

*The Vault of Vharax* now stores its sector manifest as a `Squad` of `Dataslate` records and its recovered relics as structured native values.

Identity contribution: WarPy40K now owns a meaningful structured-data model instead of exposing Python `list` and `dict` as surface semantics.

---

## v1.2 — Orders and Pattern Dispatch

**Theme:** Decisions are expressed as orders over structured data.

Proposed form:

```text
Order target {
    When 0 { ... }
    When Dataslate{status: "Heretic"} { ... }
    Otherwise { ... }
}
```

Goals:

- exact-value patterns;
- Boolean guards;
- pattern matching against `Squad` and `Dataslate` values;
- simple destructuring/binding;
- no implicit fall-through;
- exhaustiveness diagnostics where practical;
- lowering into a small AST/runtime core rather than a large hidden subsystem.

The final grammar should be prototyped against *The Vault of Vharax*: enemy and event dispatch should become clearer than the current nested `if` trees.

---

## v1.3 — The Warp Effect Model

**Theme:** Nondeterminism becomes explicit in source code.

Concept:

```text
Warp seed 42 {
    x = Chaos 100
}
```

Goals:

- deterministic seeded replay;
- explicit scope for randomness;
- record/replay of Warp outcomes in tests;
- controlled behavior for `Chaos` outside sanctioned Warp contexts;
- make RNG a language concept rather than a thin call into Python randomness.

---

## v1.4 — Inquisition Contracts

**Theme:** Judgment becomes executable specification.

Goals:

- assertions with source locations;
- function preconditions and postconditions;
- optional runtime contract checking;
- diagnostics showing failed conditions and relevant values;
- compatibility with the existing truth/judgment expression.

---

## v1.5 — Codex Modules

**Theme:** Programs become collections of explicit codices.

Goals:

- module-local scope;
- explicit imports and exports;
- deterministic module resolution;
- standard-library modules behind the same abstraction;
- no arbitrary Python imports.

Possible conceptual syntax:

```text
Invoke Math from Codex Core
```

---

## v1.6 — Sanctioned Effects

**Theme:** Side effects become capabilities rather than ambient privileges.

Target capabilities:

- console and file I/O;
- environment access;
- process exit;
- time;
- networking if eventually supported.

Pure computation should be distinguishable from functions requiring sanctioned effects.

---

## v1.7 — Crusades: Structured Iteration

**Theme:** Campaign over data instead of manual index bookkeeping.

Goals:

- native iterable protocol;
- high-level iteration over `Squad`, ranges, and module-defined iterables;
- clear loop-variable scope;
- specified behavior when mutation is attempted during traversal;
- lower into the existing small control-flow core.

Conceptually:

```text
Crusade unit in squad {
    print(unit.name)
}
```

---

## v1.8 — Machine-Spirit Introspection

**Theme:** The runtime explains itself.

Goals:

- stable textual AST format;
- execution trace mode;
- environment/scope inspection;
- function-call tracing;
- native-data inspection;
- deterministic snapshots for tests/tutorials;
- Minsky-machine trace visualization data.

---

## v1.9 — Forge Bytecode

**Theme:** Separate language semantics from the Python tree-walking implementation.

Goals:

- lower AST to a small documented bytecode;
- add a compact VM and disassembler;
- preserve the tree-walking interpreter as a reference implementation;
- differential tests: AST result == bytecode VM result;
- keep bytecode deterministic and inspectable.

---

## v2.0 — The Independent Runtime

**Theme:** WarPy40K becomes a language platform rather than only a Python-hosted interpreter project.

Candidate milestones:

- bytecode VM becomes the primary engine;
- stable module/data/effect semantics;
- versioned language specification;
- standard library built on WarPy40K abstractions;
- conformance suite independent of Python implementation details;
- self-host at least one meaningful compiler/interpreter component.

Full self-hosting is not required. The key transition is that visible language semantics no longer depend on accidental Python behavior.

---

## Post-v2.0 — The Forge Era (exploratory)

These are research directions rather than release promises. They sequence the foundations necessary for simulation and eventual 3D applications.

### v2.1 — Vectors and Matrices

- fixed-size vector/matrix values;
- explicit numeric precision and conversion rules;
- deterministic geometry/simulation algebra.

### v2.2 — Buffers and Data Layout

- packed numeric buffers and typed views;
- documented memory/layout rules;
- efficient structured-data transfer.

### v2.3 — Sanctioned Native Interface

- capability-gated foreign-function boundary;
- versioned ownership/calling conventions;
- audited adapters for native libraries rather than arbitrary imports.

### v2.4 — Real-Time Host Loop

- window, clock, and input abstractions;
- update/render timing semantics;
- deterministic headless mode for tests.

### v2.5 — Jobs and Concurrency

- bounded job/task model;
- explicit synchronization;
- deterministic scheduling modes;
- no unspecified shared-state concurrency.

### v2.6 — Graphics and Simulation Runtime

- mesh, material, camera, scene, and simulation abstractions;
- minimal rendering backend through the sanctioned native interface;
- small conformance scenes and 3D experiments.

A concrete long-term benchmark is **1,000 WarPy40K-controlled entities updating in a 3D environment in real time, with simulation logic written in WarPy40K and rendering delegated through a specified native backend**.

---

## Deliberately not prioritized

Do not add these merely because Python has them:

- classes/inheritance;
- decorators;
- comprehensions;
- multiple equivalent loop syntaxes;
- unrestricted reflection into Python objects;
- arbitrary Python imports;
- implicit operator overloading;
- async syntax before a clear concurrency model exists.

## Long-term identity

> A small, inspectable, Turing-complete language with its own structured data, Warhammer-inspired semantics around judgment and corruption/nondeterminism, explicit effect authorization, and machine introspection.

Python remains the implementation host in the near term. WarPy40K should progressively expose fewer accidental Python semantics and more explicitly specified behavior.
