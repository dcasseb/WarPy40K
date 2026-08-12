"""
WarPy40K - A Warhammer 40K-inspired interpreted programming language.

This package provides the lexer, parser, AST interpreter, and Python API
for the WarPy40K language.
"""

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .tokens import TokenType

__version__ = "1.0.0"
__all__ = [
    "Lexer",
    "Parser",
    "Interpreter",
    "TokenType",
    "evaluate",
    "reset_interpreter",
    "WarPy40KError",
]


class WarPy40KError(Exception):
    """Custom exception for WarPy40K errors."""

    def __init__(self, message: str, line: int = 1, column: int = 1):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Error at line {line}, column {column}: {message}")


_global_interpreter = None


def get_interpreter() -> Interpreter:
    """Get the global interpreter instance, creating it if necessary."""
    global _global_interpreter
    if _global_interpreter is None:
        _global_interpreter = Interpreter()
    return _global_interpreter


def reset_interpreter() -> None:
    """Reset the global interpreter (clears all variables and state)."""
    global _global_interpreter
    _global_interpreter = Interpreter()


def evaluate(source: str, use_global: bool = True):
    """Evaluate WarPy40K source code and return the result."""
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = get_interpreter() if use_global else Interpreter()
        return interpreter.execute(ast)
    except WarPy40KError:
        raise
    except SyntaxError as e:
        error_msg = str(e)
        line = 1
        column = 1

        if "line" in error_msg and "column" in error_msg:
            parts = error_msg.split()
            try:
                line_idx = parts.index("line") + 1
                line = int(parts[line_idx].rstrip(','))
                column_idx = parts.index("column") + 1
                column = int(parts[column_idx])
            except (ValueError, IndexError):
                pass

        raise WarPy40KError(f"Syntax error: {error_msg}", line, column) from e
    except NameError as e:
        raise WarPy40KError(str(e), 1, 1) from e
    except ZeroDivisionError as e:
        raise WarPy40KError(str(e), 1, 1) from e
    except Exception as e:
        raise WarPy40KError(str(e), 1, 1) from e
