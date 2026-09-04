# WarPy40K Performance Benchmarks

This directory contains the official performance baseline for WarPy40K.

The primary goal is not to claim competitive performance for the current
Python-hosted tree-walking interpreter. The goal is to make runtime evolution
measurable and reproducible, especially the planned transition to Forge
bytecode and a dedicated VM.

## Running the suite

From the repository root:

```bash
python benchmarks/run_benchmarks.py
```

Run selected workloads:

```bash
python benchmarks/run_benchmarks.py \
  --benchmark arithmetic_loop \
  --benchmark order_dispatch
```

Override sample count:

```bash
python benchmarks/run_benchmarks.py --samples 5
```

Write machine-readable results:

```bash
python benchmarks/run_benchmarks.py \
  --json benchmarks/results/v1.2-local.json
```

### v1.4 contract overhead

Inquisition Contracts have a dedicated paired benchmark so validation overhead
is explicit instead of being mixed into the historical v1.2 baseline:

```bash
python benchmarks/run_contract_benchmark.py
```

The same parsed AST is executed with `contracts_enabled=True` and
`contracts_enabled=False`. The script reports both median execution times and
the enabled/disabled ratio. Conditions are intentionally nontrivial enough to
exercise function preconditions and postconditions repeatedly, while both modes
must return the same program result.

For a CI smoke check:

```bash
python benchmarks/run_contract_benchmark.py --samples 1 --warmups 0
```

## Metrics

Each canonical workload reports:

- `exec med`: median execution-only latency;
- `exec p95`: 95th-percentile execution-only latency;
- `e2e med`: median tokenize + parse + execute latency;
- `python`: median latency of the equivalent Python workload;
- `exec/Py`: execution-only slowdown relative to Python.

Execution-only mode parses source once and reuses the AST, but creates a fresh
WarPy40K interpreter for every timed sample. This preserves identical initial
program state without charging lexer/parser cost to the runtime measurement.

End-to-end mode constructs a fresh lexer, parser, AST, and interpreter for
every sample.

The v1.4 contract benchmark separately reports contract-enabled and
contract-disabled execution medians plus their ratio.

## Canonical workloads

| Benchmark | Purpose |
|---|---|
| `arithmetic_loop` | baseline tree-walker overhead for scalar loops/arithmetic |
| `function_calls` | user-function call and scope overhead |
| `recursion_fib18` | recursive call overhead and return unwinding |
| `order_dispatch` | v1.2 `Order` matching and branch dispatch |
| `squad` | native mutable collection operations and indexed access |
| `dataslate` | persistent record update and field access |
| `minsky_interpreter` | the constructive two-counter interpreter model used by the v1.0 universality demonstration |

The Minsky workload executes the same encoded transfer-machine design as the
official constructive example, with a smaller input chosen so that repeated
benchmark samples remain practical.

The contract benchmark is intentionally kept as a paired auxiliary benchmark
rather than folded into the v1.2 canonical corpus. This preserves the historical
baseline while still making v1.4 validation overhead reproducible.

## Python comparisons

Python baselines are deliberately straightforward equivalents, not hand-tuned
NumPy/C extensions. The comparison answers:

> How much interpreter/runtime overhead does WarPy40K add over expressing the
> same small algorithm directly in CPython?

For the Minsky benchmark, both implementations use the same repeated-subtraction
`nat_div`/`nat_mod` strategy so the ratio primarily measures language/runtime
overhead rather than a different decoding algorithm.

Ratios should still be interpreted cautiously. WarPy40K built-ins may delegate
to efficient Python host operations, while user-level loops repeatedly dispatch
AST nodes through the tree-walking interpreter.

## Reproducibility rules

For meaningful comparisons between versions:

1. use the same physical machine when possible;
2. use the same Python implementation/version;
3. close heavy background applications;
4. keep power/performance mode stable;
5. run the suite more than once;
6. compare medians before individual minima/maxima;
7. save JSON results with a name identifying the WarPy40K version and machine.

Do not compare GitHub-hosted-runner timings directly with local-machine timings.

## CI policy

CI performs a one-sample smoke run to ensure every canonical workload remains
valid and returns the expected result. It also performs a one-sample smoke of
the v1.4 paired contract benchmark in both enabled and disabled modes. CI does
**not** enforce latency or slowdown thresholds because shared runners are too
noisy for trustworthy microbenchmark regression gates.

## Future baseline use

The suite should remain source-compatible through the 1.x line where practical.
The most important planned comparison is:

```text
WarPy40K 1.2 tree walker
          ↓ compare
WarPy40K 1.9 Forge VM
          ↓ compare
WarPy40K 2.x optimized/native paths
```

When Forge bytecode is introduced, execution-only results should be split into
at least:

- tree-walker execution;
- bytecode compilation cost;
- Forge VM execution;
- full source-to-result end-to-end latency.

This benchmark corpus is therefore part of the language's compatibility and
engineering history, not merely a one-off performance test.
