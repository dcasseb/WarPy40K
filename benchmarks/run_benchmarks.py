#!/usr/bin/env python3
"""Official WarPy40K performance benchmark suite.

The suite intentionally avoids external benchmark dependencies so that results
can be collected with a normal development install. Timing data is descriptive,
not a CI performance gate.
"""

from __future__ import annotations

import argparse
import gc
import json
import math
import platform
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from warpy40k import __version__  # noqa: E402
from warpy40k.interpreter import Interpreter  # noqa: E402
from warpy40k.lexer import Lexer  # noqa: E402
from warpy40k.parser import Parser  # noqa: E402


@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    description: str
    warpy_source: str
    python_callable: Optional[Callable[[], Any]]
    expected: Any
    samples: int = 15
    warmups: int = 3


@dataclass
class TimingSummary:
    median_ms: float
    p95_ms: float
    min_ms: float
    max_ms: float
    samples: int


@dataclass
class BenchmarkResult:
    name: str
    description: str
    result: Any
    execution_only: TimingSummary
    end_to_end: TimingSummary
    python: Optional[TimingSummary]
    execution_slowdown_vs_python: Optional[float]
    end_to_end_slowdown_vs_python: Optional[float]


def percentile(values: Sequence[float], fraction: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile requires at least one value")
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def summarize(seconds: Sequence[float]) -> TimingSummary:
    milliseconds = [value * 1000.0 for value in seconds]
    return TimingSummary(
        median_ms=statistics.median(milliseconds),
        p95_ms=percentile(milliseconds, 0.95),
        min_ms=min(milliseconds),
        max_ms=max(milliseconds),
        samples=len(milliseconds),
    )


def parse_warpy(source: str):
    return Parser(Lexer(source).tokenize()).parse()


def execute_warpy(source: str) -> Any:
    return Interpreter().execute(parse_warpy(source))


def measure(
    callable_: Callable[[], Any], warmups: int, samples: int
) -> Tuple[Any, TimingSummary]:
    result = None
    for _ in range(warmups):
        result = callable_()

    timings: List[float] = []
    gc_was_enabled = gc.isenabled()
    try:
        gc.disable()
        for _ in range(samples):
            start = time.perf_counter()
            result = callable_()
            timings.append(time.perf_counter() - start)
    finally:
        if gc_was_enabled:
            gc.enable()

    return result, summarize(timings)


def python_arithmetic_loop() -> int:
    total = 0
    i = 0
    while i < 20000:
        total = total + i
        i = i + 1
    return total


def python_function_calls() -> int:
    def add3(value: int) -> int:
        return value + 3

    i = 0
    total = 0
    while i < 10000:
        total = add3(total)
        i = i + 1
    return total


def python_recursion() -> int:
    def fib(n: int) -> int:
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    return fib(18)


def python_order_dispatch() -> int:
    i = 0
    choice = 0
    score = 0
    while i < 12000:
        if choice == 0:
            score += 1
        elif choice == 1:
            score += 2
        elif choice == 2:
            score += 3
        else:
            score += 4
        choice += 1
        if choice == 4:
            choice = 0
        i += 1
    return score


def python_squad_workload() -> int:
    squad: List[int] = []
    i = 0
    while i < 6000:
        squad.append(i)
        i += 1
    i = 0
    total = 0
    while i < len(squad):
        total += squad[i]
        i += 1
    return total


def python_dataslate_workload() -> int:
    record: Dict[str, int] = {"health": 100, "faith": 50, "corruption": 0}
    i = 0
    while i < 4000:
        record = {**record, "health": record["health"] + 1}
        i += 1
    return record["health"]


def python_minsky_interpreter() -> int:
    field_base = 5
    program_base = 15
    program = 1560

    def nat_pow(base: int, exponent: int) -> int:
        result = 1
        i = 0
        while i < exponent:
            result *= base
            i += 1
        return result

    def nat_div(numerator: int, denominator: int) -> int:
        quotient = 0
        remainder = numerator
        while remainder >= denominator:
            remainder -= denominator
            quotient += 1
        return quotient

    def nat_mod(value: int, modulus: int) -> int:
        remainder = value
        while remainder >= modulus:
            remainder -= modulus
        return remainder

    def instruction_at(pc: int) -> int:
        scale = nat_pow(program_base, pc)
        shifted = nat_div(program, scale)
        return nat_mod(shifted, program_base)

    def field_at(word: int, index: int) -> int:
        scale = nat_pow(field_base, index)
        shifted = nat_div(word, scale)
        return nat_mod(shifted, field_base)

    pc = 1
    c1 = 3
    c2 = 25
    running = True
    while running:
        word = instruction_at(pc)
        opcode = field_at(word, 0)
        target_a = field_at(word, 1)
        target_b = field_at(word, 2)
        if opcode == 0:
            running = False
        elif opcode == 1:
            c1 += 1
            pc = target_a
        elif opcode == 2:
            c2 += 1
            pc = target_a
        elif opcode == 3:
            if c1 == 0:
                pc = target_b
            else:
                c1 -= 1
                pc = target_a
        elif opcode == 4:
            if c2 == 0:
                pc = target_b
            else:
                c2 -= 1
                pc = target_a
        else:
            raise RuntimeError("invalid opcode")
    return c1


CASES = [
    BenchmarkCase(
        name="arithmetic_loop",
        description="20,000 while-loop iterations with integer addition",
        warpy_source="""
total = 0;
i = 0;
while i < 20000 {
    total = total + i;
    i = i + 1;
}
total;
""",
        python_callable=python_arithmetic_loop,
        expected=199990000,
    ),
    BenchmarkCase(
        name="function_calls",
        description="10,000 user-defined function calls inside a loop",
        warpy_source="""
def add3(value) {
    return value + 3;
}
i = 0;
total = 0;
while i < 10000 {
    total = add3(total);
    i = i + 1;
}
total;
""",
        python_callable=python_function_calls,
        expected=30000,
    ),
    BenchmarkCase(
        name="recursion_fib18",
        description="naive recursive Fibonacci(18)",
        warpy_source="""
def fib(n) {
    if n <= 1 {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}
fib(18);
""",
        python_callable=python_recursion,
        expected=2584,
        samples=9,
        warmups=2,
    ),
    BenchmarkCase(
        name="order_dispatch",
        description="12,000 Order dispatches over four literal branches",
        warpy_source="""
i = 0;
choice = 0;
score = 0;
while i < 12000 {
    Order choice {
        When 0 { score = score + 1; }
        When 1 { score = score + 2; }
        When 2 { score = score + 3; }
        Otherwise { score = score + 4; }
    };
    choice = choice + 1;
    if choice == 4 {
        choice = 0;
    }
    i = i + 1;
}
score;
""",
        python_callable=python_order_dispatch,
        expected=30000,
    ),
    BenchmarkCase(
        name="squad",
        description="Deploy 6,000 integers, then index and sum every member",
        warpy_source="""
squad = Squad[];
i = 0;
while i < 6000 {
    Deploy(squad, i);
    i = i + 1;
}
i = 0;
total = 0;
while i < len(squad) {
    total = total + squad[i];
    i = i + 1;
}
total;
""",
        python_callable=python_squad_workload,
        expected=17997000,
    ),
    BenchmarkCase(
        name="dataslate",
        description="4,000 persistent Dataslate updates followed by field access",
        warpy_source="""
record = Dataslate{health: 100, faith: 50, corruption: 0};
i = 0;
while i < 4000 {
    record = Inscribe(record, "health", record.health + 1);
    i = i + 1;
}
record.health;
""",
        python_callable=python_dataslate_workload,
        expected=4100,
    ),
    BenchmarkCase(
        name="minsky_interpreter",
        description="official encoded two-counter interpreter transferring C2=25",
        warpy_source="""
def nat_pow(base, exponent) {
    result = 1;
    i = 0;
    while i < exponent {
        result = result * base;
        i = i + 1;
    }
    return result;
}

def nat_div(numerator, denominator) {
    quotient = 0;
    remainder = numerator;
    while remainder >= denominator {
        remainder = remainder - denominator;
        quotient = quotient + 1;
    }
    return quotient;
}

def nat_mod(value, modulus) {
    remainder = value;
    while remainder >= modulus {
        remainder = remainder - modulus;
    }
    return remainder;
}

def instruction_at(program, pc, program_base) {
    scale = nat_pow(program_base, pc);
    shifted = nat_div(program, scale);
    return nat_mod(shifted, program_base);
}

def field_at(word, index, field_base) {
    scale = nat_pow(field_base, index);
    shifted = nat_div(word, scale);
    return nat_mod(shifted, field_base);
}

def run_minsky(program, program_base, field_base, start_pc, c1, c2) {
    pc = start_pc;
    running = True;
    while running {
        word = instruction_at(program, pc, program_base);
        opcode = field_at(word, 0, field_base);
        target_a = field_at(word, 1, field_base);
        target_b = field_at(word, 2, field_base);
        if opcode == 0 {
            running = False;
        }
        else {
            if opcode == 1 {
                c1 = c1 + 1;
                pc = target_a;
            }
            else {
                if opcode == 2 {
                    c2 = c2 + 1;
                    pc = target_a;
                }
                else {
                    if opcode == 3 {
                        if c1 == 0 {
                            pc = target_b;
                        }
                        else {
                            c1 = c1 - 1;
                            pc = target_a;
                        }
                    }
                    else {
                        if opcode == 4 {
                            if c2 == 0 {
                                pc = target_b;
                            }
                            else {
                                c2 = c2 - 1;
                                pc = target_a;
                            }
                        }
                        else {
                            return -2;
                        }
                    }
                }
            }
        }
    }
    return c1;
}

run_minsky(1560, 15, 5, 1, 3, 25);
""",
        python_callable=python_minsky_interpreter,
        expected=28,
        samples=7,
        warmups=1,
    ),
]


def run_case(case: BenchmarkCase, samples_override: Optional[int]) -> BenchmarkResult:
    samples = samples_override or case.samples
    ast = parse_warpy(case.warpy_source)

    def execution_only() -> Any:
        return Interpreter().execute(ast)

    def end_to_end() -> Any:
        return execute_warpy(case.warpy_source)

    result, execution_timing = measure(execution_only, case.warmups, samples)
    if result != case.expected:
        raise RuntimeError(
            f"{case.name}: WarPy40K returned {result!r}, expected {case.expected!r}"
        )

    end_result, end_timing = measure(end_to_end, case.warmups, samples)
    if end_result != case.expected:
        raise RuntimeError(
            f"{case.name}: end-to-end returned {end_result!r}, "
            f"expected {case.expected!r}"
        )

    python_timing = None
    execution_slowdown = None
    end_slowdown = None
    if case.python_callable is not None:
        python_result, python_timing = measure(
            case.python_callable, case.warmups, samples
        )
        if python_result != case.expected:
            raise RuntimeError(
                f"{case.name}: Python returned {python_result!r}, "
                f"expected {case.expected!r}"
            )
        if python_timing.median_ms > 0:
            execution_slowdown = execution_timing.median_ms / python_timing.median_ms
            end_slowdown = end_timing.median_ms / python_timing.median_ms

    return BenchmarkResult(
        name=case.name,
        description=case.description,
        result=result,
        execution_only=execution_timing,
        end_to_end=end_timing,
        python=python_timing,
        execution_slowdown_vs_python=execution_slowdown,
        end_to_end_slowdown_vs_python=end_slowdown,
    )


def print_results(results: Sequence[BenchmarkResult]) -> None:
    header = (
        f"{'benchmark':<20} {'exec med':>10} {'exec p95':>10} "
        f"{'e2e med':>10} {'python':>10} {'exec/Py':>10}"
    )
    print(header)
    print("-" * len(header))
    for result in results:
        python_ms = result.python.median_ms if result.python else None
        slowdown = result.execution_slowdown_vs_python
        print(
            f"{result.name:<20} "
            f"{result.execution_only.median_ms:>9.3f}ms "
            f"{result.execution_only.p95_ms:>9.3f}ms "
            f"{result.end_to_end.median_ms:>9.3f}ms "
            f"{python_ms if python_ms is not None else float('nan'):>9.3f}ms "
            f"{slowdown if slowdown is not None else float('nan'):>9.1f}x"
        )


def environment_metadata() -> Dict[str, Any]:
    return {
        "warpy40k_version": __version__,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "machine": platform.machine(),
        "timer": "time.perf_counter",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--benchmark",
        action="append",
        dest="benchmarks",
        help="Run only a named benchmark (repeatable).",
    )
    parser.add_argument(
        "--samples",
        type=int,
        help="Override the sample count for every selected benchmark.",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Write environment metadata and results to this JSON file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected = CASES
    if args.benchmarks:
        requested = set(args.benchmarks)
        selected = [case for case in CASES if case.name in requested]
        missing = requested - {case.name for case in selected}
        if missing:
            print(
                f"Unknown benchmark(s): {', '.join(sorted(missing))}",
                file=sys.stderr,
            )
            return 2

    if args.samples is not None and args.samples < 1:
        print("--samples must be at least 1", file=sys.stderr)
        return 2

    metadata = environment_metadata()
    print(
        f"WarPy40K {metadata['warpy40k_version']} | "
        f"{metadata['python_implementation']} {metadata['python_version']} | "
        f"{metadata['platform']}"
    )
    print("Timing is informational; compare runs on the same machine/configuration.\n")

    results = [run_case(case, args.samples) for case in selected]
    print_results(results)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "environment": metadata,
            "results": [asdict(result) for result in results],
        }
        args.json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"\nWrote {args.json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
