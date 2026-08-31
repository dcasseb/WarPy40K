"""Regression tests for WarPy40K v1.1 native data types."""

from warpy40k.interpreter import DataslateValue, Interpreter, SquadValue
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser


def execute(source: str):
    interpreter = Interpreter()
    ast = Parser(Lexer(source).tokenize()).parse()
    return interpreter.execute(ast)


def test_squad_literal_and_index_access():
    result = execute("s = Squad[10, 20, 30]; s[1]")
    assert result == 20


def test_nested_squad_dataslate_access():
    result = execute(
        'party = Squad[Dataslate{name: "Acolyte", health: 88}]; '
        "party[0].health"
    )
    assert result == 88


def test_squad_is_runtime_owned_value():
    result = execute("Squad[1, 2, 3]")
    assert isinstance(result, SquadValue)
    assert result.members == [1, 2, 3]
    assert repr(result) == "Squad[1, 2, 3]"


def test_deploy_extract_and_reassign_mutate_squad_explicitly():
    result = execute(
        "s = Squad[1, 2]; Deploy(s, 3); Reassign(s, 0, 9); "
        "Extract(s, 1); s"
    )
    assert isinstance(result, SquadValue)
    assert result.members == [9, 3]


def test_dataslate_literal_and_field_access():
    result = execute('marine = Dataslate{name: "Titus", health: 100}; marine.name')
    assert result == "Titus"


def test_dataslate_is_immutable_by_default():
    result = execute(
        'original = Dataslate{name: "Titus", health: 100}; '
        'updated = Inscribe(original, "health", 75); '
        "Squad[original.health, updated.health]"
    )
    assert isinstance(result, SquadValue)
    assert result.members == [100, 75]


def test_inscribe_can_add_a_new_field():
    result = execute(
        'marine = Dataslate{name: "Titus"}; '
        'veteran = Inscribe(marine, "rank", "Captain"); veteran.rank'
    )
    assert result == "Captain"


def test_erase_returns_new_dataslate():
    result = execute(
        'record = Dataslate{name: "Vharax", status: "Heretic"}; '
        'clean = Erase(record, "status"); len(clean)'
    )
    assert result == 1


def test_purge_understands_native_data_types():
    squad = execute("Purge Squad[1, 2, 3]")
    dataslate = execute('Purge Dataslate{name: "x"}')
    assert isinstance(squad, SquadValue) and len(squad) == 0
    assert isinstance(dataslate, DataslateValue) and len(dataslate) == 0


def test_structural_dataslate_equality():
    result = execute("Dataslate{x: 1, y: 2} == Dataslate{x: 1, y: 2}")
    assert result is True
