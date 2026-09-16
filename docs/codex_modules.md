# Codex Modules

WarPy40K v1.5 introduces explicit file modules called Codices.

## Import and export

```text
Invoke clamp from Codex Core
value = clamp(15, 0, 10)
```

A module exposes names explicitly:

```text
def add(a, b) { return a + b; }
private_value = 99
Codex Export add
```

Only exported names cross the module boundary. Module-private variables and helpers remain available to exported functions through their lexical closure.

## Resolution

A Codex name maps deterministically to a `.wp40k` file. Resolution order is:

1. the directory of the currently executing Codex;
2. configured `module_paths`, in order;
3. the bundled WarPy40K standard-library directory.

Absolute paths, parent traversal (`..`), and non-`.wp40k` module extensions are rejected. WarPy40K never delegates Codex loading to Python imports.

String module specs allow nested paths:

```text
Invoke report from Codex "campaign/Mission"
```

## Cache

Each resolved module path is evaluated at most once per interpreter. Repeated imports reuse the same exported values. Circular imports fail with `ModuleLoadError`.

## Standard library

The first bundled Codex is `Core.wp40k`, containing `identity` and `clamp`. It is loaded through exactly the same parser/runtime abstraction as user Codices.

## Python API

```python
Interpreter(module_paths=[Path("modules")])
```

The order of `module_paths` is significant and deterministic.
