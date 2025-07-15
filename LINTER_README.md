# WarPy40K Language Linter

A comprehensive linter for the WarPy40K programming language. Checks syntax, validates commands and variables, and provides helpful error messages for robust code quality.

> See the main [README.md](./README.md) for project overview, interpreter usage, and syntax highlighting.

## Features

- **Syntax Validation**: Ensures WarPy40K syntax rules, command structure, variable declarations, assignments, loops, and conditionals are correct.
- **Command Validation**: Verifies all commands exist in the WarPy40K command set, checks argument syntax, and validates string literals and variable references.
- **Variable Analysis**: Tracks variable declarations and usage, detects undeclared/unused variables, and validates names against reserved keywords.
- **Control Flow Analysis**: Validates for/while loop structures, loop variable declarations, and conditional expressions.
- **Arithmetic Expression Validation**: Validates arithmetic operations (+, -, *, /, %) with proper operator precedence and parentheses.
- **Code Style Checks**: Detects trailing whitespace, long lines, and unsupported comments.

## Installation

The linter is a standalone Python script. Requires Python 3.6+ and no extra dependencies.

```bash
chmod +x warpy_linter.py
python3 warpy_linter.py tests/test_fibonacci.wp40k
```

## Usage

```bash
python3 warpy_linter.py tests/test_fibonacci.wp40k
```

For help:
```bash
python3 warpy_linter.py --help
```

### Exit Codes
- `0` - No errors found (warnings may still be present)
- `1` - Errors found

## Error Codes and Messages

### ❌ ERRORS (Must be fixed)

| Code | Description | Example | Fix |
|------|-------------|---------|-----|
| `UNKNOWN_SYNTAX` | Invalid syntax | `invalid_syntax_here` | Check WarPy40K syntax documentation |
| `UNKNOWN_COMMAND` | Command doesn't exist | `unknown_command()` | Use valid WarPy40K commands |
| `MISSING_COLON` | Loop missing colon | `for i in 1..5` | Add `:` at end |
| `INVALID_CONDITION` | Invalid condition | `while invalid_condition:` | Use comparison operators |
| `UNDECLARED_VARIABLE` | Variable used before declaration | `x = undeclared_var` | Declare variable first |
| `RESERVED_KEYWORD` | Using reserved keyword | `for: dg = 0` | Use different variable name |
| `INVALID_VAR_DECL` | Invalid variable declaration | `bad_var: invalid_type = 123` | Use `variable: type = value` |
| `MISSING_PARENTHESIS` | Missing closing parenthesis | `the_emperor_protects(` | Add `)` |
| `INVALID_STRING` | Invalid string literal | `"unclosed_string` | Close string with `"` |
| `EMPTY_EXPRESSION` | Empty expression | `x = ` | Provide valid expression |
| `INVALID_ARITHMETIC` | Invalid arithmetic expression | `x = a / 0` | Check for division by zero or invalid operations |

### ⚠️ WARNINGS (Should be reviewed)

| Code | Description | Example | Fix |
|------|-------------|---------|-----|
| `TRAILING_WHITESPACE` | Trailing spaces | `command() ` | Remove trailing spaces |
| `LINE_TOO_LONG` | Line > 120 characters | Very long line... | Break into multiple lines |
| `UNUSED_VARIABLE` | Variable declared but not used | `x: dg = 0` | Use variable or remove |
| `UNDECLARED_VARIABLE` | Variable used but not declared | `x = some_var` | Declare variable first |
| `INCOMPLETE_COMMAND` | Command appears incomplete | `command(` | Check for missing parentheses or syntax errors |

### ℹ️ INFO (Informational)

| Code | Description | Example |
|------|-------------|---------|
| `INCOMPLETE_COMMAND` | Command appears incomplete | `command(` |

## Examples

### ✅ Valid WarPy40K Code
```warpy40k
start: dg = 0
end: dg = 5

a: dg = 0
b: dg = 1
i: dg = 0
c: dg = 0

if start == 0:
    burn_the_heretic(a)

for i in 1..end:
    c = a + b
    a = b
    b = c
    if i >= start and i <= end:
        burn_the_heretic(a)

# Arithmetic operations
x: dg = 10
y: dg = 3
z: dg = x * y + 2  # 32
remainder: dg = x % y  # 1
```

### ❌ Code with Errors
```warpy40k
invalid_syntax_here
unknown_command()
for i in 1..5  # Missing colon
while invalid_condition:  # Invalid condition
    for_the_emperor()
x = undeclared_var  # Undeclared variable
```

## Integration

### VS Code Integration
Add to your VS Code settings for automatic linting:

```json
{
    "files.associations": {
        "*.wp40k": "plaintext"
    },
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": false,
    "python.linting.mypyEnabled": false,
    "python.linting.customLinterEnabled": true,
    "python.linting.customLinterPath": "./warpy_linter.py",
    "python.linting.customLinterArgs": ["${file}"]
}
```

### Git Hooks
Add to your pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit

for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.wp40k$'); do
    python3 warpy_linter.py "$file"
    if [ $? -ne 0 ]; then
        echo "Linting failed for $file"
        exit 1
    fi
done
```

## Configuration

The linter is designed to be lightweight and doesn't require configuration files. All rules are built-in and follow WarPy40K language specifications.

## Troubleshooting & FAQ

**Q: What arithmetic operations are supported?**
A: WarPy40K supports addition (+), subtraction (-), multiplication (*), division (/), and modulo (%) with proper operator precedence and parentheses.

**Q: Can I use the linter in my editor or CI?**
A: Yes! See the integration section above for VS Code and Git hooks.

## Contributing

To extend the linter:
1. Add new validation methods to the `WarPy40KLinter` class
2. Update the `valid_commands` set with new commands
3. Add new error codes to the `LintIssue` class
4. Update this documentation

## License

This linter is part of the WarPy40K project and follows the same license terms. See `LICENSE` for details.

---

*For the Emperor!* 🛡️ 