# Changelog

All notable changes to WarPy40K are recorded here.

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
