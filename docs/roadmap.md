# WarPy40K Language Roadmap

WarPy40K should evolve as its own small language, not as Python with Warhammer terminology. New features should change how programs are modeled, validated, executed, inspected, or accelerated while preserving a compact and understandable implementation.

## Design principles

1. **Theme must affect semantics.** A themed keyword should do more than rename a Python construct.
2. **Keep the deterministic core explicit.** Randomness and external effects should become visible execution concepts.
3. **Preserve inspectability.** Tokens, AST, scopes, runtime values, bytecode, scheduling, and performance behavior should remain understandable.
4. **Prefer a few strong abstractions.** Avoid accumulating every Python convenience feature.
5. **Treat 1.x as a compatibility line.** Stable 1.0 programs should continue to run throughout 1.x unless behavior is explicitly experimental.
6. **Own the runtime data model.** Public WarPy40K values should have specified WarPy40K semantics rather than accidental Python container behavior.
7. **Use the official showcase as a language benchmark.** New features should improve real WarPy40K source, not exist only as isolated syntax demonstrations.
8. **Treat performance as a language-platform goal.** Runtime changes should produce measurable improvements on the official benchmark suite without sacrificing semantic clarity, determinism, or correctness.

---

## Performance strategy

Performance is a first-class roadmap objective from v1.2 onward. The goal is not to prematurely optimize the Python-hosted tree walker, but to establish objective baselines now and progressively replace avoidable interpretation overhead with explicitly designed runtime machinery.

The official benchmark suite under [`../benchmarks/`](../benchmarks/) is the reference for performance work. Comparisons should normally be made on the same hardware, Python/runtime version, operating system, benchmark revision, and configuration.

The suite currently measures:

- arithmetic loops;
- user-function calls;
- recursion;
- `Order` dispatch;
- `Squad` operations;
- persistent `Dataslate` operations;
- the encoded two-counter Minsky interpreter;
- execution-only latency;
- end-to-end lexer + parser + execution latency;
- equivalent Python baselines where practical.

### Performance principles

1. **Correctness before speed.** A faster runtime that changes stable language semantics is a regression.
2. **Measure before optimizing.** New optimization work should be justified against the benchmark suite or a reproducible workload.
3. **Keep historical baselines.** The v1.2 tree-walking interpreter is the reference implementation against which future Forge runtimes are compared.
4. **Separate frontend and runtime cost.** Lexer/parser improvements and execution-engine improvements should be measured independently.
5. **Do not use noisy shared CI timings as hard pass/fail gates.** CI should ensure benchmarks remain executable; performance regression thresholds belong on controlled hardware or statistically stable environments.
6. **Prefer scalable runtime architecture over micro-optimizing Python dispatch.** The primary long-term wins should come from bytecode, specialized values, native operations, parallel execution, and eventually JIT/AOT opportunities.
7. **Parallel speedup must be measured separately from single-thread speed.** Multicore execution is not a substitute for an efficient single-worker runtime.

### Reference performance targets

The targets below are engineering goals rather than compatibility guarantees. They may be refined as the runtime gains more representative benchmarks.

| Milestone | Target |
|---|---|
| **v1.2 baseline** | preserve reproducible tree-walker measurements and Python comparison data |
| **v1.9 Forge VM** | at least **10× geometric-mean speedup** over the v1.2 tree walker on CPU-bound execution-only benchmarks |
| **v1.9 Forge VM** | no canonical CPU-bound benchmark should regress materially versus the tree walker without documented justification |
| **v2.0 runtime** | target common scalar/control-flow workloads within roughly **10× CPython** on the same machine |
| **v2.x optimized VM** | target common scalar/control-flow workloads within roughly **3–5× CPython** where semantics permit |
| **Structured data** | target `Squad`/`Dataslate` canonical workloads within roughly **5× CPython** by the optimized v2.x runtime |
| **4 CPU workers** | target at least **3× throughput** versus one worker on embarrassingly parallel benchmark workloads |
| **8 CPU workers** | target at least **5× throughput** versus one worker where workload size and hardware permit |
| **Native numeric kernels** | vector/matrix/buffer operations should approach optimized native-library throughput rather than execute element-by-element through the interpreter |
| **Long-term simulation benchmark** | **1,000 WarPy40K-controlled entities at 60 Hz**, with a full update budget of **≤16.67 ms/frame** on documented reference hardware |

For native-code comparisons, C/Rust should be treated as a practical performance ceiling rather than a required equality target. A bytecode VM may remain several times slower than optimized native code while still being successful if it offers predictable semantics, fast enough application behavior, and scalable parallelism.

A future JIT or AOT compiler is optional rather than required for v2.0. If introduced later, an aspirational target for hot scalar code is approximately **1.5–8× optimized C/Rust**, depending on workload and dynamic-language semantics.

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

Performance contribution:

- official performance benchmark suite established;
- execution-only and end-to-end timing separated;
- Python comparison baselines established;
- v1.2 tree-walker becomes the historical performance reference for Forge VM work.

Not yet included:

- rest/spread patterns for Squads;
- static exhaustiveness analysis;
- `Order` as a value-producing expression;
- user-defined pattern protocols.

Identity contribution: command-style dispatch now composes directly with WarPy40K's native structured data rather than copying a conventional `switch` statement.

See [orders.md](orders.md) for the full v1.2 semantics.

---

## v1.3 — The Warp Effect Model ✅

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

Performance acceptance:

- Warp bookkeeping should remain a small fraction of total runtime for RNG-heavy benchmark workloads;
- deterministic replay must not require re-parsing source or rebuilding the AST for every random draw.

This will make the Warp a real execution concept rather than only a thematic spelling of random-number generation.

---

## v1.4 — Inquisition Contracts

**Theme:** Judgment becomes executable specification.

Goals:

- assertions with source locations;
- function preconditions and postconditions;
- optional runtime contract checking;
- diagnostics showing failed conditions and relevant values;
- compatibility with the existing truth/judgment expression;
- benchmark contract-enabled and contract-disabled execution separately so validation overhead is explicit.

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
- no arbitrary Python imports;
- module loading should be cached and benchmarked independently from steady-state execution.

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

Performance goal: capability checks should have predictable bounded overhead and should not force unrelated pure computations through an expensive dynamic authorization path.

---

## v1.7 — Crusades: Structured Iteration

**Theme:** Campaign over data instead of manual index bookkeeping.

Goals:

- native iterable protocol;
- high-level iteration over `Squad`, ranges, and module-defined iterables;
- clear loop-variable scope;
- specified behavior when mutation is attempted during traversal;
- lower into the existing small control-flow core;
- benchmark `Crusade` against equivalent indexed `while` loops to ensure the high-level syntax does not introduce disproportionate overhead.

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
- Minsky-machine trace visualization data;
- profiling hooks capable of attributing time to functions, node classes, built-ins, and eventually bytecode instructions;
- introspection disabled by default should add negligible steady-state overhead.

Performance contribution: v1.8 should provide the profiling information needed to guide Forge VM implementation with measured hotspots rather than intuition.

---

## v1.9 — Forge Bytecode

**Theme:** Separate language semantics from the Python tree-walking implementation and deliver the first major runtime-performance transition.

Goals:

- lower AST to a small documented bytecode;
- add a compact VM and disassembler;
- preserve the tree-walking interpreter as a reference implementation;
- differential tests: AST result == bytecode VM result;
- keep bytecode deterministic and inspectable;
- introduce specialized scalar opcodes where justified by benchmarks;
- avoid repeated AST type-dispatch in hot loops;
- record bytecode instruction counts and runtime profiles in benchmark output where useful.

### v1.9 performance acceptance criteria

- achieve at least **10× geometric-mean execution-only speedup** over the v1.2 tree-walker baseline on the canonical CPU-bound benchmark suite, measured on the same reference hardware;
- improve arithmetic loops, function calls, recursion, and `Order` dispatch materially rather than obtaining the speedup only from one specialized benchmark;
- preserve all stable 1.x semantics under differential testing;
- keep parser/frontend time reported separately so VM gains cannot be obscured by end-to-end measurement;
- document any canonical workload that does not improve and the reason why.

The Forge VM does **not** need to match C/Rust or a mature JIT at this stage. The milestone succeeds if it removes the dominant tree-walking overhead and establishes a runtime architecture that can be optimized further.

---

## v2.0 — The Independent Runtime

**Theme:** WarPy40K becomes a language platform rather than only a Python-hosted interpreter project.

Candidate milestones:

- bytecode VM becomes the primary engine;
- stable module/data/effect semantics;
- versioned language specification;
- standard library built on WarPy40K abstractions;
- conformance suite independent of Python implementation details;
- self-host at least one meaningful compiler/interpreter component;
- define a stable runtime-value representation suitable for further specialization and parallel execution;
- establish a documented reference machine for official performance comparisons.

### v2.0 performance goals

- target common scalar/control-flow workloads within roughly **10× CPython** on the same reference machine;
- maintain at least the v1.9 **10×+ speedup over the historical v1.2 tree walker**;
- ensure structured-data workloads do not regress as runtime values become more independent from Python;
- separate startup, compilation/loading, and steady-state execution costs in published benchmark reports;
- make performance data part of release validation, even when thresholds remain informational rather than hard CI gates.

Full self-hosting is not required. The key transition is that visible language semantics and primary execution behavior no longer depend on accidental Python behavior.

---

## Post-v2.0 — The Forge Era (exploratory)

These are research directions rather than release promises. They sequence the foundations necessary for high-performance simulation and eventual 3D applications.

### v2.1 — Vectors and Matrices

- fixed-size vector/matrix values;
- explicit numeric precision and conversion rules;
- deterministic geometry/simulation algebra;
- specialized storage and opcodes for common vector/matrix operations where useful;
- benchmark scalar WarPy implementations against optimized native kernels.

Performance goal: vector/matrix bulk operations should approach optimized native-library throughput by executing as native kernels rather than element-by-element WarPy dispatch.

### v2.2 — Buffers and Data Layout

- packed numeric buffers and typed views;
- documented memory/layout rules;
- efficient structured-data transfer;
- data-oriented layouts suitable for cache-friendly simulation workloads;
- zero-copy or bounded-copy interfaces where safe and semantically clear.

Performance goal: large numeric workloads should become limited primarily by memory bandwidth/native kernels rather than interpreter object overhead.

### v2.3 — Sanctioned Native Interface

- capability-gated foreign-function boundary;
- versioned ownership/calling conventions;
- audited adapters for native libraries rather than arbitrary imports;
- explicit cost model for marshaling between WarPy and native representations.

Performance goal: repeated native calls should support batching and low-overhead buffer exchange so high-throughput workloads do not spend most of their time crossing the runtime boundary.

### v2.4 — Real-Time Host Loop

- window, clock, and input abstractions;
- update/render timing semantics;
- deterministic headless mode for tests;
- frame-time instrumentation and percentile reporting.

Performance goal: expose p50/p95/p99 update times so real-time programs can detect missed frame budgets rather than relying only on average FPS.

### v2.5 — Jobs and Concurrency

- bounded job/task model;
- explicit synchronization;
- message-oriented communication such as future `Detachment`/`VoxChannel`-style abstractions if adopted;
- deterministic scheduling modes;
- no unspecified shared-state concurrency by default;
- worker-pool implementation independent from the surface syntax;
- parallel benchmark suite with CPU-bound and I/O-bound workloads.

### v2.5 performance acceptance criteria

- **4 workers:** target at least **3× throughput** versus one worker for embarrassingly parallel CPU workloads on a machine with at least four physical/logical execution resources;
- **8 workers:** target at least **5× throughput** versus one worker where hardware and workload size permit;
- report synchronization/channel overhead separately from useful computation;
- preserve a deterministic scheduler mode for replay/testing even if maximum-throughput scheduling is nondeterministic;
- multithreading must improve parallel throughput without masking a regression in single-worker performance.

### v2.6 — Graphics and Simulation Runtime

- mesh, material, camera, scene, and simulation abstractions;
- minimal rendering backend through the sanctioned native interface;
- small conformance scenes and 3D experiments;
- data-oriented agent update path compatible with worker scheduling and native numeric kernels;
- headless simulation benchmark independent of rendering performance.

### v2.6 performance acceptance criterion

A concrete long-term benchmark is:

> **1,000 WarPy40K-controlled entities updating at 60 Hz, with a complete simulation update budget of at most 16.67 ms per frame on documented reference hardware, while simulation logic remains authored in WarPy40K and rendering/numeric kernels may be delegated through specified native backends.**

The benchmark should report at least p50, p95, and p99 frame/update times, CPU utilization, worker count, and whether rendering is enabled.

---

## Possible post-v2.x optimization research

These directions are explicitly optional and should be pursued only if benchmarks justify the complexity.

### Specialized VM execution

- tagged/unboxed scalar representations;
- integer- and float-specialized bytecodes;
- inline caches for frequently resolved operations;
- faster function-call frames;
- optimized `Order` dispatch;
- specialization for common `Squad`/`Dataslate` access patterns.

### JIT or AOT compilation

A future JIT/AOT layer could compile hot Forge bytecode into native machine code. This is not required for v2.0.

If pursued, an aspirational target for hot scalar CPU workloads is approximately **1.5–8× optimized C/Rust**, depending on dynamic semantics and workload shape. Matching native languages universally is not a requirement.

The main purpose of JIT/AOT would be to close the remaining gap for hot compute-heavy WarPy code after the VM, data model, and native-kernel architecture have already matured.

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
- async syntax before a clear concurrency model exists;
- low-level shared-memory primitives before the concurrency semantics are defined;
- performance tricks that make the language/runtime substantially less inspectable without measured benefit.

## Long-term identity

> A small, inspectable, Turing-complete language with its own structured data, Warhammer-inspired semantics around judgment and corruption/nondeterminism, explicit effect authorization, machine introspection, and a progressively optimized runtime capable of scalable parallel simulation.

Python remains the implementation host in the near term. WarPy40K should progressively expose fewer accidental Python semantics, more explicitly specified behavior, and measurably better execution performance as the Forge runtime matures.
