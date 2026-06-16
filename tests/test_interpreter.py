"""
Tests for the WarPy40K interpreter.
"""

import pytest

from warpy40k import evaluate
from warpy40k.interpreter import Interpreter
from warpy40k.ast import (
    Program, LiteralNode, IdentifierNode, BinaryOpNode, UnaryOpNode,
    VariableAssignmentNode, FunctionCallNode, InquisitionExprNode,
    EmperorExprNode, ChaosExprNode, PurgeExprNode, ExterminatusExprNode,
    BlessExprNode, CurseExprNode
)


class TestInterpreter:
    """Test cases for the interpreter."""
    
    def test_integer_literal(self):
        """Test integer literal evaluation."""
        result = evaluate("42")
        assert result == 42
    
    def test_float_literal(self):
        """Test float literal evaluation."""
        result = evaluate("3.14")
        assert result == 3.14
    
    def test_string_literal(self):
        """Test string literal evaluation."""
        result = evaluate('"hello"')
        assert result == "hello"
    
    def test_addition(self):
        """Test addition."""
        result = evaluate("1 + 2")
        assert result == 3
    
    def test_subtraction(self):
        """Test subtraction."""
        result = evaluate("5 - 3")
        assert result == 2
    
    def test_multiplication(self):
        """Test multiplication."""
        result = evaluate("2 * 3")
        assert result == 6
    
    def test_division(self):
        """Test division."""
        result = evaluate("6 / 2")
        assert result == 3.0
    
    def test_power(self):
        """Test power operation."""
        result = evaluate("2 ^ 3")
        assert result == 8
    
    def test_unary_minus(self):
        """Test unary minus."""
        result = evaluate("-42")
        assert result == -42
    
    def test_comparison_eq(self):
        """Test equality comparison."""
        result = evaluate("1 == 1")
        assert result == True
        result = evaluate("1 == 2")
        assert result == False
    
    def test_comparison_neq(self):
        """Test not equal comparison."""
        result = evaluate("1 != 2")
        assert result == True
        result = evaluate("1 != 1")
        assert result == False
    
    def test_comparison_gt(self):
        """Test greater than comparison."""
        result = evaluate("2 > 1")
        assert result == True
        result = evaluate("1 > 2")
        assert result == False
    
    def test_comparison_lt(self):
        """Test less than comparison."""
        result = evaluate("1 < 2")
        assert result == True
        result = evaluate("2 < 1")
        assert result == False
    
    def test_variable_assignment(self):
        """Test variable assignment."""
        result = evaluate("x = 42")
        assert result == 42
    
    def test_variable_lookup(self):
        """Test variable lookup."""
        # First assign, then lookup
        evaluate("x = 42")
        result = evaluate("x")
        assert result == 42
    
    def test_builtin_print(self, capsys):
        """Test built-in print function."""
        evaluate('print("hello")')
        captured = capsys.readouterr()
        assert "hello" in captured.out
    
    def test_builtin_random(self):
        """Test built-in random function."""
        result = evaluate("random()")
        assert isinstance(result, float)
        assert 0 <= result <= 1
    
    def test_builtin_abs(self):
        """Test built-in abs function."""
        result = evaluate("abs(-42)")
        assert result == 42
    
    def test_builtin_min(self):
        """Test built-in min function."""
        result = evaluate("min(1, 2, 3)")
        assert result == 1
    
    def test_builtin_max(self):
        """Test built-in max function."""
        result = evaluate("max(1, 2, 3)")
        assert result == 3
    
    def test_builtin_pow(self):
        """Test built-in pow function."""
        result = evaluate("pow(2, 3)")
        assert result == 8
    
    def test_builtin_constants(self):
        """Test built-in constants."""
        result = evaluate("FAITH")
        assert result == 100
        result = evaluate("CORRUPTION")
        assert result == 0
        result = evaluate("POPULATION")
        assert result == 1000000
    
    def test_inquisition_expr(self):
        """Test Inquisition expression."""
        result = evaluate("Inquisition")
        assert result == True
    
    def test_inquisition_with_target(self):
        """Test Inquisition expression with target."""
        result = evaluate("Inquisition 42")
        assert result == True
        result = evaluate("Inquisition 0")
        assert result == False
    
    def test_emperor_expr(self):
        """Test Emperor expression."""
        result = evaluate("Emperor")
        assert result == 1000
    
    def test_emperor_with_target(self):
        """Test Emperor expression with target."""
        result = evaluate("Emperor 100")
        assert result == 100.0  # 100 * (100/100) = 100
    
    def test_chaos_expr(self):
        """Test Chaos expression."""
        result = evaluate("Chaos")
        assert isinstance(result, float)
        assert 0 <= result <= 100
    
    def test_purge_expr(self):
        """Test Purge expression."""
        result = evaluate("Purge 42")
        assert result == 0
        result = evaluate('Purge "hello"')
        assert result == ""
    
    def test_exterminatus_expr(self):
        """Test Exterminatus expression."""
        result = evaluate("Exterminatus")
        assert result == "EXTERMINATUS"
        result = evaluate("Exterminatus 42")
        assert result is None
    
    def test_bless_expr(self):
        """Test Bless expression."""
        result = evaluate("Bless 100")
        assert result == 110.0  # 100 * 1.1
        result = evaluate('Bless "hello"')
        assert result == "Blessed hello"
    
    def test_curse_expr(self):
        """Test Curse expression."""
        result = evaluate("Curse 100")
        assert result == 90.0  # 100 * 0.9
        result = evaluate('Curse "hello"')
        assert result == "Cursed hello"
    
    def test_complex_expression(self):
        """Test complex expression evaluation."""
        result = evaluate("2 + 3 * 4")
        assert result == 14  # 2 + (3 * 4)
    
    def test_parentheses(self):
        """Test parentheses override precedence."""
        result = evaluate("(2 + 3) * 4")
        assert result == 20
    
    def test_multiple_statements(self):
        """Test multiple statements."""
        result = evaluate("x = 1\ny = 2\nx + y")
        assert result == 3
    
    def test_logical_and(self):
        """Test logical AND."""
        result = evaluate("True AND False")
        assert result == False
        result = evaluate("True AND True")
        assert result == True
    
    def test_logical_or(self):
        """Test logical OR."""
        result = evaluate("True OR False")
        assert result == True
        result = evaluate("False OR False")
        assert result == False
    
    def test_logical_not(self):
        """Test logical NOT."""
        result = evaluate("NOT True")
        assert result == False
        result = evaluate("NOT False")
        assert result == True
    
    def test_combined_warpy_expr(self):
        """Test combined WarPy40K expressions."""
        result = evaluate("Bless Emperor 100")
        # Emperor 100 = 100 * 1.0 = 100, then Bless 100 = 100 * 1.1 = 110
        assert result == 110.0
