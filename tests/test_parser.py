"""
Tests for the WarPy40K parser.
"""

import pytest

from warpy40k.lexer import Lexer
from warpy40k.parser import Parser
from warpy40k.ast import (
    Program, LiteralNode, IdentifierNode, BinaryOpNode, UnaryOpNode,
    VariableAssignmentNode, FunctionCallNode, InquisitionExprNode,
    EmperorExprNode, ChaosExprNode, PurgeExprNode, ExterminatusExprNode,
    BlessExprNode, CurseExprNode
)


class TestParser:
    """Test cases for the parser."""
    
    def _parse(self, source: str):
        """Helper to parse source code."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()
    
    def test_integer_literal(self):
        """Test parsing integer literal."""
        ast = self._parse("42")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], LiteralNode)
        assert ast.statements[0].value == 42
    
    def test_float_literal(self):
        """Test parsing float literal."""
        ast = self._parse("3.14")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], LiteralNode)
        assert ast.statements[0].value == 3.14
    
    def test_string_literal(self):
        """Test parsing string literal."""
        ast = self._parse('"hello"')
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], LiteralNode)
        assert ast.statements[0].value == "hello"
    
    def test_identifier(self):
        """Test parsing identifier."""
        ast = self._parse("myVar")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], IdentifierNode)
        assert ast.statements[0].name == "myVar"
    
    def test_binary_operation(self):
        """Test parsing binary operation."""
        ast = self._parse("1 + 2")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], BinaryOpNode)
        assert ast.statements[0].operator == "+"
        assert isinstance(ast.statements[0].left, LiteralNode)
        assert isinstance(ast.statements[0].right, LiteralNode)
        assert ast.statements[0].left.value == 1
        assert ast.statements[0].right.value == 2
    
    def test_operator_precedence(self):
        """Test operator precedence."""
        # Multiplication should have higher precedence than addition
        ast = self._parse("1 + 2 * 3")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], BinaryOpNode)
        assert ast.statements[0].operator == "+"
        assert isinstance(ast.statements[0].right, BinaryOpNode)
        assert ast.statements[0].right.operator == "*"
    
    def test_parentheses(self):
        """Test parentheses override precedence."""
        ast = self._parse("(1 + 2) * 3")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], BinaryOpNode)
        assert ast.statements[0].operator == "*"
        assert isinstance(ast.statements[0].left, BinaryOpNode)
        assert ast.statements[0].left.operator == "+"
    
    def test_unary_minus(self):
        """Test unary minus."""
        ast = self._parse("-42")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], UnaryOpNode)
        assert ast.statements[0].operator == "-"
        assert isinstance(ast.statements[0].operand, LiteralNode)
        assert ast.statements[0].operand.value == 42
    
    def test_unary_not(self):
        """Test unary NOT."""
        ast = self._parse("NOT true")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], UnaryOpNode)
        assert ast.statements[0].operator == "NOT"
    
    def test_variable_assignment(self):
        """Test variable assignment."""
        ast = self._parse("x = 42")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], VariableAssignmentNode)
        assert ast.statements[0].name == "x"
        assert isinstance(ast.statements[0].value, LiteralNode)
        assert ast.statements[0].value.value == 42
    
    def test_function_call(self):
        """Test function call."""
        ast = self._parse("print(42)")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], FunctionCallNode)
        assert ast.statements[0].name == "print"
        assert len(ast.statements[0].arguments) == 1
        assert isinstance(ast.statements[0].arguments[0], LiteralNode)
        assert ast.statements[0].arguments[0].value == 42
    
    def test_function_call_multiple_args(self):
        """Test function call with multiple arguments."""
        ast = self._parse("print(1, 2, 3)")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], FunctionCallNode)
        assert len(ast.statements[0].arguments) == 3
    
    def test_inquisition_expr(self):
        """Test Inquisition expression."""
        ast = self._parse("Inquisition")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], InquisitionExprNode)
        assert ast.statements[0].target is None
    
    def test_inquisition_with_target(self):
        """Test Inquisition expression with target."""
        ast = self._parse("Inquisition 42")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], InquisitionExprNode)
        assert isinstance(ast.statements[0].target, LiteralNode)
        assert ast.statements[0].target.value == 42
    
    def test_emperor_expr(self):
        """Test Emperor expression."""
        ast = self._parse("Emperor")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], EmperorExprNode)
    
    def test_chaos_expr(self):
        """Test Chaos expression."""
        ast = self._parse("Chaos")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], ChaosExprNode)
    
    def test_purge_expr(self):
        """Test Purge expression."""
        ast = self._parse("Purge 42")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], PurgeExprNode)
        assert isinstance(ast.statements[0].target, LiteralNode)
        assert ast.statements[0].target.value == 42
    
    def test_exterminatus_expr(self):
        """Test Exterminatus expression."""
        ast = self._parse("Exterminatus")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], ExterminatusExprNode)
    
    def test_bless_expr(self):
        """Test Bless expression."""
        ast = self._parse("Bless 42")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], BlessExprNode)
        assert isinstance(ast.statements[0].target, LiteralNode)
        assert ast.statements[0].target.value == 42
    
    def test_curse_expr(self):
        """Test Curse expression."""
        ast = self._parse("Curse 42")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], CurseExprNode)
        assert isinstance(ast.statements[0].target, LiteralNode)
        assert ast.statements[0].target.value == 42
    
    def test_complex_expression(self):
        """Test complex expression parsing."""
        ast = self._parse("Emperor + Inquisition 42 * Chaos")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        # Should be: Emperor + (Inquisition(42) * Chaos)
        assert isinstance(ast.statements[0], BinaryOpNode)
        assert ast.statements[0].operator == "+"
        assert isinstance(ast.statements[0].left, EmperorExprNode)
        assert isinstance(ast.statements[0].right, BinaryOpNode)
        assert ast.statements[0].right.operator == "*"
    
    def test_multiple_statements(self):
        """Test multiple statements."""
        ast = self._parse("x = 1\ny = 2")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 2
        assert isinstance(ast.statements[0], VariableAssignmentNode)
        assert isinstance(ast.statements[1], VariableAssignmentNode)
    
    def test_purge_requires_target(self):
        """Test that Purge requires a target."""
        with pytest.raises(SyntaxError):
            self._parse("Purge")
    
    def test_bless_requires_target(self):
        """Test that Bless requires a target."""
        with pytest.raises(SyntaxError):
            self._parse("Bless")
    
    def test_curse_requires_target(self):
        """Test that Curse requires a target."""
        with pytest.raises(SyntaxError):
            self._parse("Curse")
