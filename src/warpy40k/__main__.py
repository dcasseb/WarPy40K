#!/usr/bin/env python3
"""
Main entry point for WarPy40K interpreter.

Allows running WarPy40K code from the command line.
"""

import sys
import argparse

from . import evaluate
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


def main():
    """Main entry point for the WarPy40K interpreter."""
    parser = argparse.ArgumentParser(
        description="WarPy40K - A toy language using Warhammer 40K universe expressions"
    )
    parser.add_argument(
        'file',
        nargs='?',
        help='WarPy40K source file to execute'
    )
    parser.add_argument(
        '-c', '--code',
        type=str,
        help='Execute a single line of WarPy40K code'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Start interactive REPL mode'
    )
    parser.add_argument(
        '--tokens',
        action='store_true',
        help='Display tokens instead of executing'
    )
    parser.add_argument(
        '--ast',
        action='store_true',
        help='Display AST instead of executing'
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        repl()
    elif args.code:
        execute_code(args.code, args.tokens, args.ast)
    elif args.file:
        execute_file(args.file, args.tokens, args.ast)
    else:
        # Default to REPL if no arguments
        repl()


def execute_code(source: str, show_tokens: bool = False, show_ast: bool = False) -> None:
    """Execute a string of WarPy40K code."""
    try:
        if show_tokens:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            for token in tokens:
                if token.type.name != 'EOF':
                    print(token)
            return
        
        if show_ast:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            print(ast)
            return
        
        result = evaluate(source)
        if result is not None:
            print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def execute_file(filename: str, show_tokens: bool = False, show_ast: bool = False) -> None:
    """Execute a WarPy40K source file."""
    try:
        with open(filename, 'r') as f:
            source = f.read()
        execute_code(source, show_tokens, show_ast)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def repl() -> None:
    """Start an interactive REPL for WarPy40K."""
    print("WarPy40K Interactive REPL")
    print("Type 'exit' or 'quit' to exit")
    print("Type 'help' for information")
    print()
    
    interpreter = Interpreter()
    
    while True:
        try:
            prompt = ">>> "
            code = input(prompt)
            
            if code.strip().lower() in ('exit', 'quit', 'q'):
                print("May the Emperor protect you!")
                break
            
            if code.strip().lower() in ('help', '?'):
                print_help()
                continue
            
            if not code.strip():
                continue
            
            # Execute the code
            result = evaluate(code)
            if result is not None:
                print(result)
                
        except KeyboardInterrupt:
            print("\nUse 'exit' or 'quit' to exit")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


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
    print("  print(x), random(), abs(x), min(x,y), max(x,y), pow(x,y)")


if __name__ == "__main__":
    main()
