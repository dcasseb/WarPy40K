"""Informational v1.6 capability-check overhead benchmark."""

import argparse
import statistics
import time

from warpy40k.interpreter import Interpreter
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser

PURE = """
value = 0
i = 0
while i < 3000 {
    value = value + 1
    i = i + 1
}
"""
EFFECTS = """
i = 0
while i < 250 {
    Sanction time { last = Clock() }
    i = i + 1
}
"""


def parse(text):
    return Parser(Lexer(text).tokenize()).parse()


def time_case(ast, effects, samples, warmups):
    values = []
    for i in range(samples + warmups):
        runtime = Interpreter(granted_effects=["time"], strict_effects=effects)
        start = time.perf_counter()
        runtime.execute(ast)
        elapsed = (time.perf_counter() - start) * 1000
        if i >= warmups:
            values.append(elapsed)
    return statistics.median(values)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=9)
    parser.add_argument("--warmups", type=int, default=2)
    args = parser.parse_args()
    if args.samples < 1 or args.warmups < 0:
        parser.error("samples must be positive and warmups nonnegative")
    pure = parse(PURE)
    effects = parse(EFFECTS)
    p_legacy = time_case(pure, False, args.samples, args.warmups)
    p_strict = time_case(pure, True, args.samples, args.warmups)
    e_sanction = time_case(effects, True, args.samples, args.warmups)
    print(f"pure legacy: {p_legacy:.3f} ms")
    print(f"pure strict: {p_strict:.3f} ms")
    print(f"sanctioned time workload: {e_sanction:.3f} ms")
    print("Timings informational only; no latency threshold in shared CI.")


if __name__ == "__main__":
    main()
