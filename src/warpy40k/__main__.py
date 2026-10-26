#!/usr/bin/env python3
"""
Main entry point for WarPy40K interpreter.

Allows running WarPy40K code from the command line.
"""

import argparse
import sys
from pathlib import Path

from . import WarPy40KError, evaluate
from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser


def main() -> None:
    """Main entry point for the WarPy40K interpreter."""
    parser = argparse.ArgumentParser(
        description="WarPy40K - A toy language using Warhammer 40K universe expressions"
    )
    parser.add_argument("file", nargs="?", help="WarPy40K source file to execute")
    parser.add_argument(
        "-c", "--code", type=str, help="Execute a single line of WarPy40K code"
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Start interactive REPL mode"
    )
    parser.add_argument(
        "--tokens", action="store_true", help="Display tokens instead of executing"
    )
    parser.add_argument(
        "--ast", action="store_true", help="Display AST instead of executing"
    )

    parser.add_argument(
        "--grant",
        action="append",
        choices=[
            "console",
            "file_read",
            "file_write",
            "environment",
            "process",
            "time",
        ],
        default=[],
        help="Grant a named host effect capability (repeatable)",
    )
    parser.add_argument(
        "--strict-effects",
        action="store_true",
        help="Require Sanction regions for console and process effects too",
    )
    parser.add_argument(
        "--file-root",
        type=Path,
        help="Host-authorized root for file_read/file_write effects",
    )
    args = parser.parse_args()
    options = {
        "granted_effects": args.grant,
        "strict_effects": args.strict_effects,
        "file_root": args.file_root,
    }

    if args.interactive:
        repl(**options)
    elif args.code:
        execute_code(args.code, args.tokens, args.ast, **options)
    elif args.file:
        execute_file(args.file, args.tokens, args.ast, **options)
    else:
        repl(**options)


def execute_code(
    source: str,
    show_tokens: bool = False,
    show_ast: bool = False,
    print_result: bool = True,
    granted_effects=None,
    strict_effects: bool = False,
    file_root=None,
    module_paths=None,
) -> None:
    """Execute a string of WarPy40K code."""

    try:
        if show_tokens:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            for token in tokens:
                if token.type.name != "EOF":
                    print(token)
            return

        if show_ast:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            print(ast)
            return

        if granted_effects or strict_effects or file_root or module_paths:
            runtime = Interpreter(
                granted_effects=granted_effects,
                strict_effects=strict_effects,
                file_root=file_root,
                module_paths=module_paths,
            )
            result = runtime.execute(Parser(Lexer(source).tokenize()).parse())
        else:
            result = evaluate(source, use_global=False)
        if print_result and result is not None:
            print(result)
    except WarPy40KError as e:
        print(f"WarPy40K Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


def execute_file(
    filename: str,
    show_tokens: bool = False,
    show_ast: bool = False,
    granted_effects=None,
    strict_effects: bool = False,
    file_root=None,
) -> None:
    """Parse and execute a complete WarPy40K source file exactly once."""

    try:
        source = Path(filename).read_text(encoding="utf-8")
        execute_code(
            source,
            show_tokens,
            show_ast,
            print_result=False,
            granted_effects=granted_effects,
            strict_effects=strict_effects,
            file_root=file_root,
            module_paths=[Path(filename).resolve().parent],
        )
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def repl(granted_effects=None, strict_effects=False, file_root=None) -> None:
    """Start an interactive REPL for WarPy40K."""

    print("WarPy40K Interactive REPL")
    print("Type 'exit' or 'quit' to exit")
    print("Type 'help' for information")
    print("Type 'reset' to clear all variables")
    print()

    # Reset interpreter for fresh REPL session
    runtime = Interpreter(
        granted_effects=granted_effects,
        strict_effects=strict_effects,
        file_root=file_root,
    )

    while True:
        try:
            prompt = ">>> "
            code = input(prompt)

            if code.strip().lower() in ("exit", "quit", "q"):
                print("May the Emperor protect you!")
                break

            if code.strip().lower() in ("help", "?"):
                print_help()
                continue

            if code.strip().lower() in ("reset", "clear"):
                runtime = Interpreter(
                    granted_effects=granted_effects,
                    strict_effects=strict_effects,
                    file_root=file_root,
                )
                print("All variables cleared. The Emperor's will be done.")
                continue

            if not code.strip():
                continue

            # Execute the code (use_global=True to maintain state)
            result = runtime.execute(Parser(Lexer(code).tokenize()).parse())
            if result is not None:
                print(result)

        except KeyboardInterrupt:
            print("\nUse 'exit' or 'quit' to exit")
        except WarPy40KError as e:
            print(f"WarPy40K Error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Unexpected Error: {e}", file=sys.stderr)


def print_help() -> None:
    """Print help information."""
    print("WarPy40K Language Help")
    print("=" * 40)
    print()
    print("Basic Syntax:")
    print("  1 + 2           # Addition")
    print("  x = 5           # Variable assignment")
    print("  print(x)        # Function call")
    print()
    print("Warhammer 40K Expressions:")
    print("  Inquisition     # Truth/judgment")
    print("  Emperor         # Divine power")
    print("  Chaos           # Corruption/randomness")
    print("  Purge x         # Destroy/remove x")
    print("  Exterminatus x  # Total annihilation")
    print("  Bless x         # Positive modification")
    print("  Curse x         # Negative modification")
    print()
    print("Built-in Constants:")
    print("  FAITH, CORRUPTION, POPULATION")
    print()
    print("Built-in Functions:")
    print("  print(x), input(prompt), int(x), float(x), str(x)")
    print("  random(), abs(x), min(x,y), max(x,y), pow(x,y)")


if __name__ == "__main__":
    main()
