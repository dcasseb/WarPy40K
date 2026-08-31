# Changelog

All notable changes to WarPy40K are recorded here.

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
  sectors are now represented as a `Squad` of `Dataslate` records and recovered
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
