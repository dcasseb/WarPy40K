#!/usr/bin/env python3
"""Measure cold and cached WarPy40K v1.5 Codex loading."""

from __future__ import annotations

import argparse
import statistics
import time
from typing import Callable, List, Tuple

from warpy40k.interpreter import Interpreter
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser

SOURCE = "Invoke clamp from Codex Core; clamp(15, 0, 10)"
EXPECTED = 10


def parse_source():
    return Parser(Lexer(SOURCE).tokenize()).parse()


def measure(
    callable_: Callable[[], int], warmups: int, samples: int
) -> Tuple[int, float]:
    result = 0
    for _ in range(warmups):
        result = callable_()

    timings: List[float] = []
    for _ in range(samples):
        start = time.perf_counter()
        result = callable_()
        timings.append(time.perf_counter() - start)
    return result, statistics.median(timings) * 1000.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=15)
    parser.add_argument("--warmups", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.samples < 1 or args.warmups < 0:
        raise SystemExit("samples must be >= 1 and warmups must be >= 0")

    ast = parse_source()

    def cold() -> int:
        value = Interpreter().execute(ast)
        if not isinstance(value, int) or isinstance(value, bool):
            raise RuntimeError(f"module benchmark returned {value!r}")
        return value

    cached_interpreter = Interpreter()
    cached_interpreter.execute(ast)

    def cached() -> int:
        value = cached_interpreter.execute(ast)
        if not isinstance(value, int) or isinstance(value, bool):
            raise RuntimeError(f"module benchmark returned {value!r}")
        return value

    cold_result, cold_ms = measure(cold, args.warmups, args.samples)
    cached_result, cached_ms = measure(cached, args.warmups, args.samples)
    if cold_result != EXPECTED or cached_result != EXPECTED:
        raise RuntimeError("Codex benchmark result mismatch")

    ratio = cold_ms / cached_ms if cached_ms > 0 else float("nan")
    print(f"cold module load : {cold_ms:.3f} ms median")
    print(f"cached import    : {cached_ms:.3f} ms median")
    print(f"cold/cached      : {ratio:.3f}x")
    print("Timing is informational; compare runs on the same machine/configuration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
