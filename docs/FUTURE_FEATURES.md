# WarPy40K: Future Functionalities & Improvements

This document tracks planned features, bug fixes, and enhancements for the WarPy40K language and interpreter. Contributions and suggestions are welcome!

---

## Core Interpreter Improvements

- **Correct vox_cast Functionality**
  - Ensure `vox_cast` prints string arguments as expected, including proper parsing and output of string literals.
  - Add support for string concatenation and variable interpolation in `vox_cast`.

- **Robust String Literal Handling**
  - Improve parsing of string literals (support for escape sequences, multi-line strings, etc.).
  - Fix any remaining issues with empty or malformed strings.

- **Input Functionality**
  - Ensure `hear_the_emperors_voice` reliably receives and returns user input.
  - Add input validation and error handling for numeric and string types.

- **Error Reporting & Debugging**
  - Provide clearer error messages for syntax and runtime errors.
  - Add line/column reporting for parse and execution errors.
  - Implement a debug mode for step-by-step execution tracing.

- **Type System Enhancements**
  - Enforce type checking for variable assignments and command arguments.
  - Add support for type inference and type conversion where appropriate.

---

## Language Features

- **Functions & Procedures**
  - Add user-defined functions with parameters and return values.
  - Support for function calls and recursion.

- **Data Structures**
  - Implement arrays/lists and dictionaries/maps.
  - Add support for iterating over collections.

- **Advanced Control Flow**
  - Add support for `break`, `continue`, and `return` statements.
  - Implement switch/case or pattern matching constructs.

- **Modules & Imports**
  - Allow splitting code into multiple files and importing modules.

---

## Tooling & Ecosystem

- **Testing Framework**
  - Create a test runner for `.wp40k` scripts with assertions and output checks.

- **Linter Enhancements**
  - Expand static analysis to catch more error types and style issues.
  - Add auto-fix suggestions for common problems.

- **Editor Integration**
  - Improve syntax highlighting and autocompletion for VS Code and Sublime Text extensions.
  - Add code snippets and documentation popups.

---

## Documentation

- **Language Reference**
  - Keep the command reference and language guide up to date with new features.

- **Tutorials & Examples**
  - Add more example scripts demonstrating advanced features and best practices.

---

## Known Issues

- String literals may be parsed as empty strings in some cases (Earley parser limitation).
- Error messages may lack context or line numbers.
- Some commands may not handle arguments or types robustly.

---

*Last updated: [15-07-2025]*