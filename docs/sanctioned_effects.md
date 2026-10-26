# Sanctioned Effects — WarPy40K v1.6

WarPy40K v1.6 introduces runtime-checked effect capabilities without changing the existing computational core.

## Syntax

```text
Sanction console, time {
    print(Clock())
}
```

Capabilities are contextual identifiers, not reserved keywords. Supported effect labels:
`console`, `file_read`, `file_write`, `environment`, `process`, `time`.

For example:

```text
Sanction file_write, file_read {
    WriteFile("report.txt", "The Emperor protects.")
    print(ReadFile("report.txt"))
}
```

The second example also needs `console` in its Sanction list in strict mode.

## Host authorization

The embedding host explicitly supplies grants:

```python
from pathlib import Path
from warpy40k import Interpreter

runtime = Interpreter(
    granted_effects=["console", "file_read", "file_write", "time"],
    strict_effects=True,
    file_root=Path("./workspace"),
)
```

Declaring `Sanction` never grants a new capability by itself. A region is entered only if every declared capability was approved by the host. Regions nest restrictively: nested Sanctions cannot expand the active capability set. Context is restored in `finally` even for return/exception and shared across loaded Codices.

A capability is checked at the call site of each effectful builtin. Pure computation has no authorization check in the ordinary arithmetic/function path.

## Builtins

| Builtin | Capability | Semantics |
| --- | --- | --- |
| `print(...)`, `input(prompt)` | `console` | Standard terminal interaction |
| `ReadFile(relative_path)` | `file_read` | UTF-8 file text |
| `WriteFile(relative_path, string)` | `file_write` | Write UTF-8 file text |
| `GetEnv(name)` | `environment` | Environment value, or empty string |
| `Clock()` | `time` | Host wall-clock timestamp |
| `exit(code)` | `process` | Request host process termination |

The file capabilities additionally require the host to configure `file_root`. Absolute paths, `..` components, and resolved symlink paths escaping that root are rejected.

**Security boundary:** Path resolution alone is not a race-free OS sandbox: hostile concurrent filesystem mutation can defeat a check-then-open sequence. For untrusted source, run the interpreter under an OS sandbox and do not treat `file_root` as a security boundary against concurrent local attackers. Similarly, `GetEnv` exposes all environment keys once permitted; use a sanitized process environment.

## Compatibility and strict mode

By default, old WarPy40K 1.x programs retain ambient `print`, `input`, and `exit` when no region is active. New file/environment/time APIs always require an active region and grants.

In `strict_effects=True`, even console and process actions require explicitly granted, active `Sanction` regions.

Networking is not implemented in v1.6. Any network effect requires an explicit later milestone.

## Current limitations

The v1.6 system is a runtime authorization model, not a static compiler effect type system. Pure/effectful function classification is currently dynamic. The module loader still reads source files independently from `file_read` grants; module origins remain controlled through Codex resolution rules. Execution of untrusted Codices is not a substitute for process isolation.
