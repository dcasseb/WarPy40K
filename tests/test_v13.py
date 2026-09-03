"""Regression tests for WarPy40K v1.3 Warp effect semantics."""

import pytest

from warpy40k.ast import WarpStatementNode
from warpy40k.interpreter import Interpreter, SquadValue
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser


def parse(source: str):
    return Parser(Lexer(source).tokenize()).parse()


def execute(source: str, interpreter=None):
    runtime = interpreter or Interpreter()
    return runtime.execute(parse(source))


def test_warp_parses_as_explicit_statement_node():
    program = parse("Warp seed 42 { value = Chaos; }")
    assert len(program.statements) == 1
    assert isinstance(program.statements[0], WarpStatementNode)


def test_same_seed_replays_identical_chaos_sequence():
    source = (
        "Warp seed 42 { "
        "result = Squad[Chaos, random(), Chaos]; "
        "}; result"
    )
    first = execute(source)
    second = execute(source)
    assert isinstance(first, SquadValue)
    assert isinstance(second, SquadValue)
    assert first.members == second.members


def test_different_seed_can_produce_different_trace():
    first = execute("Warp seed 41 { result = Squad[Chaos, random()]; }; result")
    second = execute("Warp seed 42 { result = Squad[Chaos, random()]; }; result")
    assert isinstance(first, SquadValue)
    assert isinstance(second, SquadValue)
    assert first.members != second.members


def test_numeric_chaos_is_deterministic_inside_seeded_warp():
    source = "CORRUPTION = 100; Warp seed 7 { result = Chaos 100; }; result"
    assert execute(source) == execute(source)


def test_nested_warp_does_not_perturb_parent_stream():
    plain = execute(
        "Warp seed 77 { "
        "first = random(); second = random(); "
        "result = Squad[first, second]; "
        "}; result"
    )
    nested = execute(
        "Warp seed 77 { "
        "first = random(); "
        "Warp seed 999 { ignored = Squad[Chaos, random(), Chaos]; }; "
        "second = random(); result = Squad[first, second]; "
        "}; result"
    )
    assert isinstance(plain, SquadValue)
    assert isinstance(nested, SquadValue)
    assert plain.members == nested.members


def test_seed_expression_is_evaluated_exactly_once():
    result = execute(
        "counter = Squad[0]; "
        "def choose_seed() { "
        "Reassign(counter, 0, counter[0] + 1); return 42; "
        "} "
        "Warp seed choose_seed() { value = Chaos; }; counter[0]"
    )
    assert result == 1


@pytest.mark.parametrize("seed", ["True", "1.5", '"forty-two"'])
def test_warp_rejects_non_integer_seed(seed):
    with pytest.raises(TypeError, match="Warp seed must be an integer"):
        execute(f"Warp seed {seed} {{ value = Chaos; }}")


def test_warp_stack_is_restored_after_runtime_error():
    interpreter = Interpreter()
    with pytest.raises(NameError):
        execute("Warp seed 42 { missing_name; }", interpreter)
    assert interpreter._warp_random_stack == []


def test_function_called_inside_warp_uses_same_local_stream():
    direct = execute(
        "Warp seed 123 { "
        "first = random(); second = random(); "
        "result = Squad[first, second]; "
        "}; result"
    )
    through_function = execute(
        "def draw() { return random(); } "
        "Warp seed 123 { "
        "first = random(); second = draw(); "
        "result = Squad[first, second]; "
        "}; result"
    )
    assert isinstance(direct, SquadValue)
    assert isinstance(through_function, SquadValue)
    assert direct.members == through_function.members


def test_recorded_warp_trace_can_be_replayed_with_different_seed():
    recorded = Interpreter()
    source = "Warp seed 42 { result = Squad[Chaos, random(), Chaos]; }; result"
    expected = execute(source, recorded)

    replay = Interpreter(warp_replay=recorded.warp_trace)
    actual = execute(
        "Warp seed 999 { result = Squad[Chaos, random(), Chaos]; }; result",
        replay,
    )

    assert isinstance(expected, SquadValue)
    assert isinstance(actual, SquadValue)
    assert actual.members == expected.members
    assert replay.warp_replay_complete


def test_warp_replay_exhaustion_is_reported():
    interpreter = Interpreter(warp_replay=[0.25])
    with pytest.raises(RuntimeError, match="Warp replay exhausted"):
        execute("Warp seed 1 { first = random(); second = random(); }", interpreter)


def test_seed_identifier_remains_available_outside_warp_syntax():
    assert execute("seed = 17; seed") == 17
