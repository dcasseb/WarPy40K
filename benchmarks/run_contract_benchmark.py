#!/usr/bin/env python3
"""Measure WarPy40K v1.4 runtime-contract overhead."""

from __future__ import annotations

import argparse
import gc
import statistics
import sys
import time
from pathlib import Path
from typing import Callable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from warpy40k.interpreter import Interpreter  # noqa: E402
from warpy40k.lexer import Lexer  # noqa: E402
from warpy40k.parser import Parser  # noqa: E402

SOURCE = """
def accumulate(limit)
Inquisition Requires limit >= 0
Inquisition Ensures result >= 0
{
    i = 0;
    total = 0;
    while i < limit {
        total = total + i;
        i = i + 1;
    }
    return total;
}

j = 0;
result = 0;
while j < 250 {
    result = accumulate(40);
    j = j + 1;
}
result;
"""
EXPECTED = 780


def measure(
    callable_: Callable[[], int], warmups: int, samples: int
) -> Tuple[int, float]:
    result = 0
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

    return result, statistics.median(timings) * 1000.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=15)
    parser.add_argument("--warmups", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.samples < 1 or args.warmups < 0:
        print("samples must be >= 1 and warmups must be >= 0", file=sys.stderr)
        return 2

    ast = Parser(Lexer(SOURCE).tokenize()).parse()

    def execute(enabled: bool) -> int:
        value = Interpreter(contracts_enabled=enabled).execute(ast)
        if not isinstance(value, int) or isinstance(value, bool):
            raise RuntimeError(f"contract benchmark returned non-integer {value!r}")
        return value

    enabled_result, enabled_ms = measure(
        lambda: execute(True), args.warmups, args.samples
    )
    disabled_result, disabled_ms = measure(
        lambda: execute(False), args.warmups, args.samples
    )

    if enabled_result != EXPECTED or disabled_result != EXPECTED:
        raise RuntimeError(
            "contract benchmark result mismatch: "
            f"enabled={enabled_result}, disabled={disabled_result}, expected={EXPECTED}"
        )

    overhead = enabled_ms / disabled_ms if disabled_ms > 0 else float("nan")
    print(f"contracts enabled : {enabled_ms:.3f} ms median")
    print(f"contracts disabled: {disabled_ms:.3f} ms median")
    print(f"enabled/disabled  : {overhead:.3f}x")
    print("Timing is informational; compare runs on the same machine/configuration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
