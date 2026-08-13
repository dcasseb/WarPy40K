"""Regression tests for WarPy40K v0.9 language features."""

import pytest

from warpy40k import WarPy40KError, evaluate, reset_interpreter
from warpy40k.ast import FunctionDefinitionNode, ReturnStatementNode, WhileLoopNode
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser
from warpy40k.tokens import TokenType


def parse(source: str):
    return Parser(Lexer(source).tokenize()).parse()


def setup_function():
    reset_interpreter()


def test_control_flow_keywords_are_real_tokens():
    tokens = Lexer("if else while def return").tokenize()
    assert [token.type for token in tokens[:-1]] == [
        TokenType.IF,
        TokenType.ELSE,
        TokenType.WHILE,
        TokenType.DEF,
        TokenType.RETURN,
    ]


def test_while_parses_to_loop_node():
    ast = parse("while x < 3 { x = x + 1 }")
    assert isinstance(ast.statements[0], WhileLoopNode)


def test_function_and_return_parse_to_ast_nodes():
    ast = parse("def identity(x) { return x }")
    function = ast.statements[0]
    assert isinstance(function, FunctionDefinitionNode)
    assert function.name == "identity"
    assert function.parameters == ["x"]
    assert isinstance(function.body.statements[0], ReturnStatementNode)


def test_while_executes_multiple_iterations():
    result = evaluate("""
        x = 0
        while x < 5 {
            x = x + 1
        }
        x
        """)
    assert result == 5


def test_user_defined_function_call():
    result = evaluate("""
        def add(a, b) {
            return a + b
        }
        add(20, 22)
        """)
    assert result == 42


def test_function_parameters_are_local():
    result = evaluate("""
        x = 99
        def identity(x) {
            return x
        }
        identity(42)
        x
        """)
    assert result == 99


def test_recursive_factorial():
    result = evaluate("""
        def factorial(n) {
            if n <= 1 {
                return 1
            }
            return n * factorial(n - 1)
        }
        factorial(6)
        """)
    assert result == 720


def test_recursive_fibonacci():
    result = evaluate("""
        def fib(n) {
            if n <= 1 {
                return n
            }
            return fib(n - 1) + fib(n - 2)
        }
        fib(10)
        """)
    assert result == 55


def test_return_unwinds_from_inside_while():
    result = evaluate("""
        def first_at_least(limit) {
            x = 0
            while True {
                if x >= limit {
                    return x
                }
                x = x + 1
            }
        }
        first_at_least(7)
        """)
    assert result == 7


def test_function_arity_is_validated():
    with pytest.raises(WarPy40KError, match="expected 2 argument"):
        evaluate("""
            def add(a, b) { return a + b }
            add(1)
            """)


def test_return_outside_function_is_rejected():
    with pytest.raises(WarPy40KError, match="inside a function"):
        evaluate("return 42")
