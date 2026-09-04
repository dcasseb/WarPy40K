# Changelog

All notable changes to WarPy40K are recorded here.

## 1.4.0 — 2026-09-04

### Added

- `Inquisition Assert <condition>` executable assertions.
- Function `Inquisition Requires <condition>` preconditions.
- Function `Inquisition Ensures <condition>` postconditions with temporary `result`.
- `ContractViolation` diagnostics with relevant values.
- Optional checking through `Interpreter(contracts_enabled=False)`.

## 1.3.0 — 2026-09-03

### Added

- Explicit `Warp seed <integer> { ... }` nondeterministic regions.
- Region-local deterministic random streams shared by `Chaos` and `random()`.
- Nested Warp regions with independent streams and correct parent restoration.
- Runtime Warp trace recording through `Interpreter.warp_trace`.
- Deterministic replay through `Interpreter(warp_replay=...)`.

### Semantics

- A Warp seed expression is evaluated exactly once on region entry.
- Seeds must be integers; Booleans, floats, and strings are rejected.
- Functions called from inside a Warp region consume the active region stream.
- Nested Warp draws do not perturb the parent region stream.
- Runtime errors and returns restore the previous Warp stream through cleanup.
- `Chaos` and `random()` outside Warp preserve legacy global randomness.
- `seed` remains an ordinary identifier outside contextual `Warp seed` syntax.

### Replay

- Warp traces store normalized random draws in execution order.
- Replaying a trace reproduces decisions independently of the new region seed.
- Replay exhaustion and invalid values fail instead of generating fresh entropy.

## 1.2.0 — 2026-09-02

### Added

- `Order target { ... }` pattern-oriented dispatch.
- `When pattern { ... }` clauses with first-match-wins semantics and no fall-through.
- Optional `Otherwise` fallback clauses.
- Optional Boolean guards using `When pattern if condition { ... }`.
- Literal patterns for numbers, strings, and Booleans, including negative numeric literals.
- `_` wildcard patterns.
- Local binding patterns such as `When value { ... }`.
- Partial structural `Dataslate{field: pattern}` matching with nested bindings.
- Exact-shape `Squad[pattern, ...]` matching.
- Dedicated Order-pattern AST nodes and regression coverage.
- Official performance benchmark suite covering arithmetic, function calls,
  recursion, `Order`, `Squad`, `Dataslate`, and the encoded Minsky interpreter.
- Execution-only and end-to-end benchmark modes with median, p95, min, and max
  timing plus equivalent Python baselines where practical.
- Machine-readable benchmark output for preserving reproducible historical
  performance baselines.
- Forge Runtime architecture documentation describing the path from the Python
  reference interpreter to Forge bytecode, a native VM, native value storage,
  multicore scheduling, native kernels, and optional JIT/AOT compilation.

### Semantics

- Pattern identifiers bind matched values; they are not variable lookups.
- Pattern bindings are visible to the clause guard and body, then restored/removed after the clause.
- Ordinary assignments performed by a matched clause retain normal surrounding-scope behavior.
- Duplicate bindings in one pattern are rejected.
- `Otherwise` may appear at most once and must follow all `When` clauses.
- An unmatched `Order` without `Otherwise` performs no action and returns `None` at runtime.

### Showcase

- Refactored *The Vault of Vharax* exploration and combat command dispatch to use `Order` instead of nested action-selection `if` trees.
- Added showcase regression checks requiring native Order nodes to remain present.

### Performance and roadmap

- Established v1.2 as the historical tree-walker performance baseline.
- Made performance a first-class roadmap objective with measurable targets for
  Forge VM speedup, CPython-relative performance, structured data, multicore
  scaling, native numeric kernels, and real-time simulation.
- Defined the v1.9 Forge VM target as at least a 10x geometric-mean
  execution-only speedup over the v1.2 tree walker on canonical CPU-bound
  benchmarks.
- Defined long-term multicore targets of at least 3x throughput with four
  workers and at least 5x with eight workers where hardware and workload permit.
- Defined a long-term simulation target of 1,000 WarPy40K-controlled entities
  at 60 Hz within a 16.67 ms update budget on documented reference hardware.
- Documented Python as the long-term semantic/reference implementation rather
  than the intended permanent production-runtime dependency.

### Quality

- Full tests and benchmark smoke checks run on Python 3.8, 3.10, and 3.12.
- Black, isort, flake8, mypy, and the coverage gate remain release quality gates.
- Benchmark timings remain informational rather than hard CI thresholds because
  shared CI hardware is noisy.

## 1.1.0 — 2026-08-31

### Added

- Native `Squad[...]` ordered mutable collections.
- Native `Dataslate{field: value}` immutable-by-default structured records.
- Postfix Squad indexing with `value[index]` and Dataslate field access with
  `value.field`, including chained access such as `party[0].health`.
- Explicit Squad operations: `Deploy`, `Extract`, and `Reassign`.
- Persistent Dataslate operations: `Inscribe` and `Erase`.
- Structural Dataslate equality, native representations, and `len()` support.
- `Purge` behavior for Squad and Dataslate values.
- Dedicated v1.1 regression tests for parsing, access, mutation, persistence,
  equality, and native runtime values.

### Changed

- Refactored *The Vault of Vharax* into the official v1.1 showcase. Vault
  sectors are represented as a `Squad` of `Dataslate` records and recovered
  relics are stored as structured values.
- Extended lexer punctuation with `[`, `]`, and `.` for native data syntax.
- Extended the AST and parser with explicit structured-data nodes rather than
  translating native data syntax into host-language containers.
- Improved CI formatting diagnostics by showing Black diffs on failure.
- Promoted runtime and package metadata to `1.1.0`.

### Design

- `Squad` mutation is explicit and in-place through language operations.
- `Dataslate` values are persistent: `Inscribe` and `Erase` return new values
  and leave the original record unchanged.
- Python `list` and `dict` remain implementation details rather than public
  WarPy40K surface-language types.

## 1.0.1 — 2026-08-13

### Added

- Explicit `int`, `float`, and `str` conversion built-ins.
- Integration tests for CLI file execution and bundled examples.
- Full deterministic victory, defeat, corruption, and invalid-action coverage
  for *The Vault of Vharax*.
- Minsky-machine coverage for every opcode, branch, and invalid input path.
- CI gates for formatting, imports, linting, typing, and test coverage.

### Fixed

- Execute complete source files exactly once instead of retrying after partial
  line-by-line side effects.
- Keep file execution script-like by suppressing implicit final-expression
  output while preserving expression output for `-c` and the REPL.
- Use real numeric conversion in the calculator and documentation examples.
- Use the language's supported double-quoted string syntax in CLI examples.
- Synchronize runtime and package version metadata.
- Keep development-only dependencies out of the core requirements file.
- State the constructive machine encoding precisely as a finite tuple whose
  instruction payload is a natural number.

### Documentation

- Added primary academic references for the counter-machine universality claim.
- Extended the roadmap with an explicitly exploratory post-v2.0 Forge Era.

## 1.0.0

- Introduced user-defined functions, recursion, unrestricted `while`, and real
  `return` control flow.
- Added the constructive two-counter Minsky-machine interpreter.
- Added *The Vault of Vharax* as the official terminal showcase.
