# Constructive Turing-Completeness Demonstration

WarPy40K 1.0 includes a constructive demonstration of Turing completeness in [`examples/minsky_universal.wp40k`](../examples/minsky_universal.wp40k).

The demonstration is stronger than merely observing that the language has an unrestricted `while`. It implements, in WarPy40K itself, a universal interpreter for deterministic two-counter Minsky machines.

## Claim

Under the standard theoretical abstraction in which integers and available memory are unbounded, WarPy40K can simulate every deterministic two-counter Minsky machine. Two-counter Minsky machines are computationally universal, so WarPy40K is Turing complete under the same abstraction.

Real executions remain bounded by physical memory, time, Python's runtime limits, and the host operating system, just as real implementations of other Turing-complete languages are.

## Machine model

The v1.0 demonstration uses two natural-number counters, `C1` and `C2`, and a program counter `PC`.

A machine program contains instructions with one of five opcodes:

| Opcode | Instruction | Semantics |
|---:|---|---|
| `0` | `HALT` | Stop execution |
| `1` | `INC C1, A` | Increment `C1`, then jump to label `A` |
| `2` | `INC C2, A` | Increment `C2`, then jump to label `A` |
| `3` | `DECJZ C1, A, B` | If `C1 == 0`, jump to `B`; otherwise decrement `C1` and jump to `A` |
| `4` | `DECJZ C2, A, B` | If `C2 == 0`, jump to `B`; otherwise decrement `C2` and jump to `A` |

This instruction set is sufficient for the standard two-counter register-machine model.

## Encoding an instruction as a natural number

Choose a field base `F` larger than every opcode and label used by the encoded machine.

An instruction is encoded as:

```text
word = opcode + F * A + F^2 * B
```

`A` and `B` are jump targets. Instructions that do not use `B` simply store zero there.

WarPy40K extracts fields using arithmetic implemented in the language itself:

```text
field_at(word, 0, F) -> opcode
field_at(word, 1, F) -> A
field_at(word, 2, F) -> B
```

The helper functions `nat_pow`, `nat_div`, and `nat_mod` are all implemented in WarPy40K. They do not rely on a Python-side Minsky-machine helper.

## Encoding an entire program as one natural number

Choose a program base `P` larger than every encoded instruction word.

For instruction word `word_i` at label `i`, encode the complete finite machine program as:

```text
program = sum(word_i * P^i)
```

The universal interpreter retrieves the instruction at the current program counter with:

```text
instruction_at(program, pc, P)
```

Therefore the simulated machine program is data. The WarPy40K interpreter in `run_minsky` is fixed; changing the encoded integer changes the machine being simulated.

That distinction is important: the example is not one hard-coded Minsky machine. It is an interpreter for arbitrary machines in this encoded two-counter model.

## Universal interpreter

The core function is:

```text
run_minsky(program, program_base, field_base, start_pc, c1, c2, max_steps, trace)
```

Its execution cycle is:

1. Decode the instruction at `pc`.
2. Decode `opcode`, `A`, and `B`.
3. Apply the appropriate counter operation.
4. Update `pc`.
5. Repeat until `HALT`.

When `max_steps == 0`, the simulation has no artificial language-level step limit. A non-halting encoded machine can therefore make the WarPy40K program diverge, as expected from a universal computational model.

A positive `max_steps` exists only as a practical debugging guard and does not define the semantics of the unrestricted demonstration.

## Concrete demonstration

The example file encodes a small machine that transfers the value of `C2` into `C1`.

Its program is:

```text
1: DECJZ C2, nonzero -> 2, zero -> 0
2: INC C1, jump -> 1
0: HALT
```

With:

```text
F = 5
P = 15
```

instruction 1 is:

```text
4 + 5 * 2 + 25 * 0 = 14
```

instruction 2 is:

```text
1 + 5 * 1 = 6
```

and the encoded program is:

```text
14 * 15^1 + 6 * 15^2 = 1560
```

Starting with:

```text
C1 = 3
C2 = 4
PC = 1
```

the universal interpreter halts with:

```text
C1 = 7
C2 = 0
```

The function returns `C1`, so the example result is `7`.

## Why this establishes Turing completeness

The constructive argument has two parts.

### 1. WarPy40K implements the universal Minsky interpreter

The implementation uses only WarPy40K language facilities:

- natural-number variables;
- mutable assignment;
- addition, subtraction, and multiplication;
- comparisons;
- `if` / `else`;
- unrestricted `while`;
- user-defined functions;
- function calls and `return`.

The encoded program is not interpreted by Python code specific to Minsky machines. Python hosts the WarPy40K interpreter, but the Minsky-machine decoding and transition algorithm are WarPy40K source code.

### 2. Two-counter Minsky machines are Turing universal

A deterministic two-counter Minsky machine can simulate a Turing machine. Therefore, for any computation expressible by a Turing machine, there exists a finite two-counter Minsky program representing that computation.

Since `run_minsky` accepts an encoded finite Minsky program as data and simulates its transitions, the same fixed WarPy40K program can simulate any machine in that universal model.

Thus, under the standard unbounded-memory abstraction:

```text
Turing machine
      ↓ encoded/simulated by
Two-counter Minsky machine
      ↓ encoded as a natural number
WarPy40K run_minsky
      ↓ executed by
WarPy40K language runtime
```

WarPy40K is Turing complete.

## Automated validation

`tests/test_v10.py` validates the constructive example with several machines:

- the transfer machine from the example (`3 + 4 -> 7` in `C1`);
- a different encoded program that increments `C1` twice (`40 -> 42`);
- the zero branch of `DECJZ`;
- a deliberately non-halting machine controlled by the optional test step guard.

These tests are intended to show that `run_minsky` is interpreting machine data rather than merely reproducing one hard-coded computation.

## Scope of the claim

Turing completeness says something about **computability**, not convenience, performance, safety, or ecosystem maturity.

WarPy40K 1.0 is still a small educational language. Python remains vastly richer in data structures, modules, tooling, libraries, object orientation, exceptions, generators, concurrency, typing, packaging, and runtime optimization.

The importance of the v1.0 milestone is narrower and more fundamental: WarPy40K now has both a universal computational core and a constructive artifact demonstrating it.
