#!/usr/bin/env python3
"""
Simple test runner for WarPy40K project.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from warpy40k import evaluate, reset_interpreter
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser
from warpy40k.interpreter import Interpreter
from warpy40k.tokens import TokenType
from warpy40k.ast import (
    Program, LiteralNode, IdentifierNode, BinaryOpNode, UnaryOpNode,
    VariableAssignmentNode, FunctionCallNode, InquisitionExprNode,
    EmperorExprNode, ChaosExprNode, PurgeExprNode, ExterminatusExprNode,
    BlessExprNode, CurseExprNode
)


def test_lexer():
    """Test the lexer."""
    print("Testing Lexer...")
    
    # Test integer
    lexer = Lexer("42")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == "42"
    
    # Test float
    lexer = Lexer("3.14")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.FLOAT
    assert tokens[0].value == "3.14"
    
    # Test string
    lexer = Lexer('"hello"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "hello"
    
    # Test WarPy40K keywords
    lexer = Lexer("Inquisition Emperor Chaos")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.INQUISITION
    assert tokens[1].type == TokenType.EMPEROR
    assert tokens[2].type == TokenType.CHAOS
    
    print("✓ Lexer tests passed")


def test_parser():
    """Test the parser."""
    print("Testing Parser...")
    
    # Test simple expression
    lexer = Lexer("1 + 2")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], BinaryOpNode)
    
    # Test WarPy40K expressions
    lexer = Lexer("Inquisition")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast.statements[0], InquisitionExprNode)
    
    lexer = Lexer("Bless 100")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast.statements[0], BlessExprNode)
    
    print("✓ Parser tests passed")


def test_interpreter():
    """Test the interpreter."""
    print("Testing Interpreter...")
    
    # Test arithmetic
    assert evaluate("1 + 2") == 3
    assert evaluate("2 * 3") == 6
    assert evaluate("10 / 2") == 5.0
    assert evaluate("2 ^ 3") == 8
    
    # Test WarPy40K expressions
    assert evaluate("Inquisition") == True
    assert evaluate("Emperor") == 1000
    assert abs(evaluate("Bless 100") - 110.0) < 0.001
    assert abs(evaluate("Curse 100") - 90.0) < 0.001
    assert evaluate("Purge 42") == 0
    assert isinstance(evaluate("Chaos"), float)
    
    # Test variables - use same interpreter for variable persistence
    from warpy40k.interpreter import Interpreter
    from warpy40k.lexer import Lexer
    from warpy40k.parser import Parser
    
    interpreter = Interpreter()
    lexer = Lexer("x = 42")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter.execute(ast)
    
    lexer = Lexer("x")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert interpreter.execute(ast) == 42
    
    # Test built-in functions
    assert evaluate("abs(-42)") == 42
    assert evaluate("min(1, 2, 3)") == 1
    assert evaluate("max(1, 2, 3)") == 3
    
    print("✓ Interpreter tests passed")


def test_complex_expressions():
    """Test complex expressions."""
    print("Testing Complex Expressions...")
    
    # Test operator precedence
    assert evaluate("2 + 3 * 4") == 14  # 2 + (3 * 4)
    assert evaluate("(2 + 3) * 4") == 20
    
    # Test combined WarPy40K expressions
    result = evaluate("Bless Emperor 100")
    assert abs(result - 110.0) < 0.001
    
    # Test logical operations
    assert evaluate("True AND False") == False
    assert evaluate("True OR False") == True
    assert evaluate("NOT True") == False
    
    print("✓ Complex expression tests passed")


def test_control_flow():
    """Test control flow (if/else)."""
    print("Testing Control Flow...")
    
    # Test if/else with global interpreter
    reset_interpreter()
    
    # Set up a variable
    evaluate("x = 10")
    
    # Test if statement
    result = evaluate("if x > 5\n    y = 1\nelse\n    y = 0")
    # The result is the value of the last statement in the executed branch
    assert result == 1
    
    # Check that y was set
    y_value = evaluate("y")
    assert y_value == 1
    
    # Test else branch
    reset_interpreter()
    evaluate("x = 3")
    result = evaluate("if x > 5\n    y = 1\nelse\n    y = 0")
    assert result == 0
    y_value = evaluate("y")
    assert y_value == 0
    
    print("✓ Control flow tests passed")


def main():
    """Run all tests."""
    print("Running WarPy40K Tests")
    print("=" * 40)
    
    try:
        test_lexer()
        test_parser()
        test_interpreter()
        test_complex_expressions()
        test_control_flow()
        
        print("=" * 40)
        print("🎉 All tests passed!")
        return 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
