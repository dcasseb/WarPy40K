"""Regression tests for WarPy40K v1.2 Order pattern dispatch."""

import pytest

from warpy40k.interpreter import Interpreter
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser


def execute(source: str):
    interpreter = Interpreter()
    ast = Parser(Lexer(source).tokenize()).parse()
    return interpreter.execute(ast)


def test_order_literal_dispatch_uses_first_match():
    result = execute(
        'choice = "2"; result = "none"; '
        'Order choice { '
        'When "1" { result = "boltgun"; } '
        'When "2" { result = "chainsword"; } '
        'When "2" { result = "duplicate"; } '
        'Otherwise { result = "invalid"; } '
        '}; result'
    )
    assert result == "chainsword"


def test_order_otherwise_handles_no_match():
    result = execute(
        'choice = "9"; result = "none"; '
        'Order choice { When "1" { result = "known"; } '
        'Otherwise { result = "unknown"; } }; result'
    )
    assert result == "unknown"


def test_dataslate_pattern_is_partial_and_binds_fields():
    result = execute(
        'target = Dataslate{status: "Heretic", threat: 8, name: "Vharax"}; '
        'result = "none"; '
        'Order target { '
        'When Dataslate{status: "Heretic", threat: level} { result = level; } '
        'Otherwise { result = -1; } '
        '}; result'
    )
    assert result == 8


def test_order_guard_can_use_pattern_binding():
    result = execute(
        'target = Dataslate{status: "Heretic", threat: 3}; result = "none"; '
        'Order target { '
        'When Dataslate{status: "Heretic", threat: level} if level > 5 '
        '{ result = "exterminatus"; } '
        'When Dataslate{status: "Heretic"} { result = "purge"; } '
        'Otherwise { result = "observe"; } '
        '}; result'
    )
    assert result == "purge"


def test_squad_pattern_matches_exact_shape_and_binds():
    result = execute(
        'formation = Squad["Titus", 100]; result = "none"; '
        'Order formation { '
        'When Squad[name, health] if health == 100 { result = name; } '
        'Otherwise { result = "broken"; } '
        '}; result'
    )
    assert result == "Titus"


def test_wildcard_pattern_matches_without_binding():
    result = execute(
        'value = 42; result = 0; '
        'Order value { When _ { result = 7; } }; result'
    )
    assert result == 7


def test_pattern_binding_scope_does_not_leak():
    with pytest.raises(NameError):
        execute('Order 42 { When captured { print(captured); } }; captured')


def test_order_without_otherwise_returns_none_when_unmatched():
    result = execute('Order 9 { When 1 { 10; } }')
    assert result is None


def test_duplicate_pattern_binding_is_rejected():
    with pytest.raises(SyntaxError, match="Duplicate pattern binding"):
        execute('Order Squad[1, 2] { When Squad[x, x] { x; } }')


def test_when_after_otherwise_is_rejected():
    with pytest.raises(SyntaxError, match="When cannot appear after Otherwise"):
        execute('Order 1 { Otherwise { 0; } When 1 { 1; } }')
