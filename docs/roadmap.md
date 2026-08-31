# WarPy40K Language Roadmap

WarPy40K should evolve as its own small language, not as Python with Warhammer terminology. New features should change how programs are modeled, validated, executed, or inspected while preserving a compact and understandable implementation.

## Design principles

1. **Theme must affect semantics.** A themed keyword should do more than rename a Python construct.
2. **Keep the deterministic core explicit.** Randomness and external effects should become visible execution concepts.
3. **Preserve inspectability.** Tokens, AST, scopes, runtime values, and eventually bytecode should remain understandable.
4. **Prefer a few strong abstractions.** Avoid accumulating every Python convenience feature.
5. **Treat 1.x as a compatibility line.** Stable 1.0 programs should continue to run throughout 1.x unless behavior is explicitly experimental.
6. **Own the runtime data model.** Public WarPy40K values should have specified WarPy40K semantics rather than accidental Python container behavior.
7. **Use the official showcase as a language benchmark.** New features should improve real WarPy40K source, not exist only as isolated syntax demonstrations.

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

Delivered:

- `Squad[...]` ordered mutable collections;
- zero-based indexing and chained access;
- explicit `Deploy`, `Extract`, and `Reassign` mutation;
- `Dataslate{field: value}` immutable-by-default structured records;
- `.field` lookup and structural equality;
- persistent `Inscribe` and `Erase` transformations;
- `Purge` semantics for native data;
- official showcase refactored around a Squad/Dataslate sector and relic model.

Identity contribution: WarPy40K owns a meaningful structured-data model instead of exposing Python `list` and `dict` as surface semantics.

---

## v1.2 — Orders and Pattern Dispatch

**Theme:** Decisions are expressed as orders over structured data.  
**Status:** implemented.

Basic form:

```text
Order action {
    When "1" {
        print("Boltgun")
    }

    When "2" {
        print("Chainsword")
    }

    Otherwise {
        print("Invalid order")
    }
}
```

Delivered semantics:

- ordered first-match-wins dispatch;
- no implicit fall-through;
- optional `Otherwise` fallback;
- exact literal patterns;
- negative numeric patterns;
- `_` wildcard patterns;
- identifier bindings scoped to the selected clause;
- optional Boolean guards using `When pattern if condition`;
- partial structural `Dataslate` patterns;
- exact-shape `Squad` patterns;
- nested pattern bindings;
- duplicate-binding and invalid-clause diagnostics;
- unmatched Orders without `Otherwise` perform no action;
- explicit Order/pattern AST nodes and interpreter matching logic.

Example with structured data:

```text
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

The v1.2 *Vault of Vharax* showcase uses `Order` for exploration and combat command dispatch, replacing the largest nested action-selection `if` trees.

Not yet included:

- rest/spread patterns for Squads;
- static exhaustiveness analysis;
- `Order` as a value-producing expression;
- user-defined pattern protocols.

Identity contribution: command-style dispatch now composes directly with WarPy40K's native structured data rather than copying a conventional `switch` statement.

See [orders.md](orders.md) for the full v1.2 semantics.

---

## v1.3 — The Warp Effect Model

**Theme:** Nondeterminism becomes explicit in source code.  
**Status:** next milestone.

Today, `Chaos` delegates directly to runtime randomness. v1.3 should make nondeterminism a visible, controllable language effect.

Proposed form:

```text
Warp seed 42 {
    roll = Chaos 100
    print(roll)
}
```

Target semantics:

- explicit Warp regions for nondeterministic computation;
- deterministic seeded replay;
- a per-Warp random stream rather than ambient process-global randomness;
- nested Warp behavior with specified seed/stream rules;
- recording and replaying Chaos outcomes for tests;
- deterministic headless showcase runs without monkeypatching Python randomness;
- explicit policy for legacy `Chaos` outside Warp regions during the 1.x compatibility line.

### Proposed runtime model

```text
Deterministic WarPy execution
          ↓ enters
Warp region(seed / replay source)
          ↓
Chaos draws from region-local stream
          ↓ exits
Deterministic WarPy execution
```

### v1.3 showcase benchmark

*The Vault of Vharax* should gain a seeded mode such that the same Warp seed and the same player choices reproduce the same exploration events, attacks, damage, and outcome.

A concrete acceptance criterion:

> Running a complete scripted game twice with the same Warp seed must produce byte-for-byte identical gameplay output, while a different seed must be able to produce a different trace.

This will make the Warp a real execution concept rather than only a thematic spelling of random-number generation.

---

## v1.4 — Inquisition Contracts

**Theme:** Judgment becomes executable specification.

Goals:

- assertions with source locations;
- function preconditions and postconditions;
- optional runtime contract checking;
- diagnostics showing failed conditions and relevant values;
- compatibility with the existing truth/judgment expression.

Potential direction:

```text
Inquisition health > 0
```

and later contract forms attached to functions.

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
- native-data and Order-pattern inspection;
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

> A small, inspectable, Turing-complete language with its own structured data, pattern-oriented command dispatch, Warhammer-inspired semantics around judgment and corruption/nondeterminism, explicit effect authorization, and machine introspection.

Python remains the implementation host in the near term. WarPy40K should progressively expose fewer accidental Python semantics and more explicitly specified behavior.
