"""Regression tests for WarPy40K v1.4 Inquisition contracts."""

import pytest

from warpy40k.interpreter import ContractViolation, Interpreter
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser


def parse(source: str):
    return Parser(Lexer(source).tokenize()).parse()


def execute(source: str, interpreter=None):
    runtime = interpreter or Interpreter()
    return runtime.execute(parse(source))


def test_inquisition_expression_remains_boolean_judgment():
    assert execute("value = Inquisition 42; value") is True
    assert execute("value = Inquisition 0; value") is False


def test_inquisition_assert_passes_and_returns_true():
    assert execute("health = 10; Inquisition Assert health > 0") is True


def test_inquisition_assert_failure_reports_location_and_condition():
    with pytest.raises(ContractViolation) as exc:
        execute("health = 0;\nInquisition Assert health > 0")
    message = str(exc.value)
    assert "assertion" in message
    assert "line 2" in message
    assert "health" in message
    assert "0" in message


def test_function_requires_is_checked_before_body():
    source = (
        "counter = Squad[0]; "
        "def heal(amount) "
        "Inquisition Requires amount > 0 "
        "{ Reassign(counter, 0, counter[0] + 1); return amount; } "
        "heal(0)"
    )
    with pytest.raises(ContractViolation, match="precondition"):
        execute(source)


def test_function_requires_can_use_parameters():
    source = (
        "def divide(total, count) "
        "Inquisition Requires count > 0 "
        "{ return total / count; } "
        "divide(10, 2)"
    )
    assert execute(source) == 5


def test_function_ensures_can_use_result_and_parameters():
    source = (
        "def heal(amount) "
        "Inquisition Requires amount > 0 "
        "Inquisition Ensures result >= amount "
        "{ return amount + 10; } "
        "heal(5)"
    )
    assert execute(source) == 15


def test_function_ensures_failure_reports_function_and_result():
    source = (
        "def broken(amount) "
        "Inquisition Ensures result > amount "
        "{ return amount; } "
        "broken(5)"
    )
    with pytest.raises(ContractViolation) as exc:
        execute(source)
    message = str(exc.value)
    assert "postcondition" in message
    assert "broken" in message
    assert "result=5" in message


def test_multiple_requires_and_ensures_are_supported():
    source = (
        "def clamp(value, low, high) "
        "Inquisition Requires low <= high "
        "Inquisition Requires value >= low "
        "Inquisition Ensures result >= low "
        "Inquisition Ensures result <= high "
        "{ if value > high { return high; } return value; } "
        "clamp(8, 0, 5)"
    )
    assert execute(source) == 5


def test_contracts_can_be_disabled_without_evaluating_conditions():
    source = (
        "counter = Squad[0]; "
        "def check(value) "
        "Inquisition Requires Reassign(counter, 0, counter[0] + 1) == counter "
        "{ return value; } "
        "result = check(7); Squad[result, counter[0]]"
    )
    result = execute(source, Interpreter(contracts_enabled=False))
    assert result.members == [7, 0]


def test_disabled_assertion_does_not_evaluate_condition():
    source = (
        "counter = Squad[0]; "
        "Inquisition Assert Reassign(counter, 0, 1) == counter; "
        "counter[0]"
    )
    assert execute(source, Interpreter(contracts_enabled=False)) == 0


def test_postcondition_runs_for_implicit_none_result():
    source = (
        "def noop() " "Inquisition Ensures result == result " "{ value = 1; } " "noop()"
    )
    assert execute(source) is None


def test_result_binding_does_not_leak_after_function_call():
    with pytest.raises(NameError):
        execute(
            "def identity(x) Inquisition Ensures result == x { return x; } "
            "identity(3); result"
        )
