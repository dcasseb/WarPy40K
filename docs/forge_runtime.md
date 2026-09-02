# Forge Runtime Architecture

This document describes the long-term execution architecture planned for WarPy40K: moving the production runtime away from CPython while preserving the Python implementation as a semantic reference.

The goal is **not merely to rewrite the interpreter in a faster implementation language**. The goal is to remove avoidable layers of interpretation, own the runtime value model, enable real multicore execution, and leave a clean path toward native compilation.

The roadmap remains authoritative for release sequencing. This document explains the architectural direction behind the v1.9 Forge Bytecode, v2.0 Independent Runtime, and later Forge Era milestones.

---

## 1. Current architecture

WarPy40K 1.2 is implemented as a Python-hosted tree-walking interpreter:

```text
WarPy40K source
      ↓
Lexer
      ↓
Parser
      ↓
AST
      ↓
Python tree walker
      ↓
CPython bytecode/runtime
      ↓
Native host code
      ↓
CPU
```

This architecture is intentionally simple and inspectable. It has been valuable for defining language semantics, building the AST, developing `Squad`, `Dataslate`, `Order`, functions, recursion, and the constructive Minsky-machine demonstration.

It also imposes a significant execution cost. A single WarPy40K operation may require several recursive AST visits, Python function calls, dynamic type checks, scope lookups, and Python object operations before reaching the underlying native operation.

The official v1.2 benchmark suite exists specifically to preserve this implementation as a measurable historical baseline.

---

## 2. The target: Python as reference, not production runtime

The long-term objective is:

> **Python remains the historical/reference interpreter; normal production execution moves to a Forge runtime with its own VM, values, scheduler, and native execution path.**

The Python tree walker remains useful because it is small and semantically direct. It can act as an executable specification against which new runtimes are checked.

During the transition, the same program should be executable by both engines:

```text
program.wp40k
     │
     ├── Python reference interpreter → result A
     │
     └── Forge runtime               → result B

             expected: A == B
```

Differential testing is therefore a core migration strategy rather than a temporary convenience.

---

## 3. Why removing Python from the hot path matters

A simple statement such as:

```text
x = x + 1
```

currently executes conceptually through layers similar to:

```text
Assignment AST node
      ↓
Binary-operation AST node
      ↓
identifier lookup
      ↓
literal evaluation
      ↓
Python integer operation
      ↓
Python object result
```

A Forge VM should instead be able to lower the same operation to compact instructions such as:

```text
LOAD_LOCAL 0
PUSH_INT 1
IADD
STORE_LOCAL 0
```

A native VM can execute these instructions directly without repeated Python AST dispatch.

Removing Python from the hot path therefore eliminates an entire execution layer, but the largest gains come when this is combined with a runtime designed specifically for WarPy40K.

---

## 4. Migration stages

### Stage A — Python reference tree walker

**Current state.**

Responsibilities:

- define and validate semantics;
- remain highly inspectable;
- serve as differential-testing oracle;
- provide the v1.2 historical performance baseline.

Performance work at this stage should focus on measurement and correctness rather than aggressive micro-optimization.

### Stage B — Forge bytecode

The AST is lowered into a compact, documented instruction set:

```text
WarPy source
     ↓
Lexer / Parser
     ↓
AST
     ↓
Forge compiler
     ↓
Forge bytecode
```

Bytecode provides a stable boundary between frontend semantics and execution engine design.

Important properties:

- deterministic compilation;
- disassembly and inspection;
- differential tests against the tree walker;
- specialized opcodes where measurements justify them;
- explicit function-call and control-flow representation.

The v1.9 roadmap target is at least a **10× geometric-mean execution-only speedup** over the v1.2 tree walker on the canonical CPU-bound benchmark suite.

### Stage C — Native Forge VM

The production bytecode engine moves to a native implementation, with **Rust as the preferred current candidate**.

Conceptually:

```text
WarPy source
      ↓
Forge bytecode
      ↓
Native Forge VM
      ↓
CPU
```

The choice of Rust is architectural, not ideological. It provides:

- performance in the C/C++ class;
- memory safety;
- strong concurrency primitives;
- good C interoperability;
- a suitable ecosystem for VM, runtime, networking, graphics, and JIT integration.

Rust is a current design preference, not yet a stable language specification requirement.

### Stage D — Native value model

Removing Python from the VM is not sufficient if every WarPy40K value is still represented as a Python object.

The Forge runtime should eventually own its value representation.

A scalar might use a tagged value:

```text
Value
├── tag: Integer
└── payload: int64
```

or specialized VM registers/slots where possible.

This permits instructions such as:

```text
IADD
ISUB
IMUL
FADD
FMUL
```

instead of routing every arithmetic operation through generic Python objects.

### Stage E — Specialized structured data

WarPy40K-native types should gain representations chosen for their semantics and workload.

A homogeneous numeric Squad could eventually be represented as contiguous data:

```text
Squad<Int>

[int64][int64][int64][int64]...
```

rather than an array of pointers to boxed objects.

A Dataslate implementation may use stable field layouts where shape specialization is safe:

```text
Dataslate layout #17

+0   health : int64
+8   armor  : int64
+16  faith  : int64
```

A field access can then become a fixed-offset operation rather than a general string lookup.

The public language does not need to expose the optimization strategy. Runtime specialization must preserve structural WarPy40K semantics.

---

## 5. Compiling `Order`

`Order` is a high-value candidate for specialization because many common cases are statically recognizable.

For example:

```text
Order action {
    When 1 { ... }
    When 2 { ... }
    When 3 { ... }
    Otherwise { ... }
}
```

can potentially lower to a compact integer dispatch or jump table rather than invoking the general recursive pattern matcher for every execution.

Conceptually:

```text
SWITCH_INT action
    1 → L1
    2 → L2
    3 → L3
    _ → L4
```

More complex nested Dataslate/Squad patterns can continue to use structured matching instructions.

The optimization rule is simple: **specialize when semantics are provably preserved; otherwise use the general matcher.**

---

## 6. Real multicore execution

A Python-hosted runtime inherits the execution constraints of its host. A native Forge runtime can instead define concurrency as a WarPy40K runtime capability.

The planned direction is a job/task model with isolated or explicitly shared state and message-oriented communication.

Conceptually:

```text
                 Forge Scheduler
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Worker 0       Worker 1       Worker 2
          │             │             │
        Core 0         Core 1         Core 2
```

Future abstractions such as `Detachment` and `VoxChannel` may map onto this scheduler without exposing native-thread implementation details directly in source code.

Performance targets currently defined in the roadmap are:

- at least **3× throughput with four workers** on embarrassingly parallel CPU workloads;
- at least **5× throughput with eight workers** where workload and hardware permit;
- parallel speedup must not hide regressions in single-worker execution.

A deterministic scheduler mode should remain available for tests and replay even if maximum-throughput scheduling is nondeterministic.

---

## 7. Native numeric kernels and simulation

Some workloads should not execute element-by-element through a bytecode interpreter at all.

Future `Vector`, `Matrix`, and packed `Buffer` operations should be able to delegate bulk work to optimized native kernels:

```text
WarPy control logic
       ↓
Forge native interface
       ↓
SIMD / optimized CPU kernel / GPU backend
```

This allows WarPy40K to remain expressive at the language level while using efficient implementations for arithmetic-heavy operations.

The long-term simulation target remains:

> **1,000 WarPy40K-controlled entities at 60 Hz, with a complete update budget of no more than 16.67 ms per frame on documented reference hardware.**

Rendering and bulk numeric kernels may be delegated to specified native backends; simulation rules and entity logic should remain authored in WarPy40K.

---

## 8. Optional JIT and AOT paths

A bytecode VM still interprets instructions. Once the VM and value model are stable, hot code could optionally be compiled to machine code.

### JIT

A future JIT pipeline could be:

```text
Forge bytecode
      ↓
profile hot functions/loops
      ↓
JIT compiler
      ↓
native machine code
```

Candidate backend technologies include **Cranelift** and **LLVM**, but neither is currently a committed dependency.

Cranelift may be attractive for fast runtime compilation; LLVM may be attractive for more aggressive optimization and AOT compilation.

### AOT

A future ahead-of-time compiler could offer a release path conceptually similar to:

```text
warpyc --release game.wp40k
```

with a pipeline such as:

```text
WarPy source
     ↓
AST
     ↓
Forge IR
     ↓
LLVM / Cranelift / native backend
     ↓
platform machine code
```

This would permit multiple execution modes:

```text
Development      → reference interpreter / Forge VM
Portable release → Forge bytecode
Native release   → AOT-compiled executable
```

JIT and AOT are post-v2.x optimization directions, not requirements for the v2.0 Independent Runtime.

---

## 9. Possible long-term compiler architecture

A mature architecture may look like:

```text
                   WarPy40K source
                         │
                         ▼
                    Forge Frontend
                         │
                         ▼
                      Forge IR
                   ┌─────┴─────┐
                   │           │
                   ▼           ▼
             Forge Bytecode   Native IR
                   │           │
                   ▼           ▼
                Forge VM   JIT / AOT backend
                   │           │
                   └─────┬─────┘
                         ▼
                    Forge Runtime
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          Scheduler   Native API   Memory/Data
              │          │          │
              ▼          ▼          ▼
            cores     SIMD/GPU    buffers
```

The exact internal boundaries may change, but the architectural invariant should remain:

> Language semantics must not depend on accidental CPython behavior.

---

## 10. Self-hosting

Full self-hosting is not required for WarPy40K to become independent from Python.

A realistic progression is:

```text
Phase 1
Python: lexer + parser + AST + reference interpreter
Native: Forge VM

Phase 2
Native: lexer + parser + compiler + VM + runtime
Python: reference implementation only

Phase 3
WarPy40K: selected standard-library/tooling/compiler components
Native: runtime + low-level backend
```

The v2.0 roadmap requires self-hosting at least one meaningful component, not the entire implementation.

---

## 11. Expected performance effect

Performance cannot be predicted exactly before the runtime exists, and all release claims must be benchmarked on controlled hardware.

The expected progression is nevertheless clear:

| Architecture | Expected relative effect |
|---|---|
| Python tree walker | historical baseline |
| optimized Python tree walker | small/moderate gains |
| bytecode VM still hosted in Python | moderate gains |
| native Forge VM | large gains |
| native values + specialized bytecode | large additional gains |
| multicore scheduler | large throughput gains on parallel workloads |
| native SIMD/GPU kernels | potentially very large gains for bulk numeric work |
| JIT/AOT | potential to approach native-language performance on hot code |

The important point is that these improvements **compound**. Removing Python is valuable, but the full performance opportunity comes from removing Python *and* adopting a purpose-built VM, value representation, scheduler, and native compilation path.

---

## 12. Performance comparison philosophy

WarPy40K should use three reference levels:

```text
C / Rust     → practical native-performance ceiling
CPython      → dynamic-language comparison baseline
WarPy v1.2   → historical tree-walker baseline
```

Future releases should report their position relative to all three where practical.

The objective is not to claim universal parity with C or Rust. Success means progressively reducing avoidable runtime overhead while preserving WarPy40K's semantics and delivering enough throughput for its intended applications.

---

## 13. Architectural non-goals

The Forge transition should **not**:

- change stable semantics merely to make benchmarks look better;
- expose arbitrary native pointers or host objects as language semantics;
- make the Python reference implementation unusable as a correctness oracle;
- require JIT/AOT for ordinary programs to run;
- introduce unrestricted shared-memory concurrency before its semantics are specified;
- optimize only synthetic benchmarks while the official showcase or simulation workloads regress;
- obscure the runtime so completely that bytecode, scheduling, and value behavior can no longer be inspected.

---

## Summary

WarPy40K is currently **implemented in Python**, but Python is not intended to define the permanent performance ceiling of the language.

The long-term execution model is:

```text
Python tree walker
    ↓ reference implementation
Forge bytecode
    ↓
Native Forge VM
    ↓
Native value model
    ↓
Multicore scheduler + native kernels
    ↓
Optional JIT/AOT
```

The intended destination is a WarPy40K runtime in which Python is useful for history, testing, and semantic reference, while normal high-performance execution is handled by the independent Forge platform.
