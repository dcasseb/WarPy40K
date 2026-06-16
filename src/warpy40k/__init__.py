"""
WarPy40K - A toy language using Warhammer 40K universe expressions.

This package provides a simple interpreter for a custom language that
uses terminology and expressions from the Warhammer 40K universe.
"""

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .tokens import TokenType

__version__ = "0.1.0"
__all__ = ["Lexer", "Parser", "Interpreter", "TokenType"]


def evaluate(source: str) -> str:
    """
    Evaluate a WarPy40K expression and return the result.
    
    Args:
        source: The source code to evaluate
        
    Returns:
        The result of the evaluation as a string
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    return interpreter.execute(ast)
