"""Regression tests for the WarPy40K v1.0 official showcase."""

import random
from pathlib import Path

from warpy40k.ast import Program
from warpy40k.interpreter import Interpreter
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser

ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = ROOT / "examples" / "vault_of_vharax.wp40k"
SOURCE = SHOWCASE.read_text(encoding="utf-8")
DEFINITIONS_ONLY = SOURCE.rsplit("launch_inquisitor();", 1)[0]


def parse(source: str) -> Program:
    return Parser(Lexer(source).tokenize()).parse()


def execute(interpreter: Interpreter, source: str):
    return interpreter.execute(parse(source))


def test_showcase_is_valid_warpy40k_source():
    ast = parse(SOURCE)
    assert isinstance(ast, Program)
    assert len(ast.statements) >= 10


def test_showcase_helper_rules_execute_in_warpy40k():
    interpreter = Interpreter()
    execute(interpreter, DEFINITIONS_ONLY)

    assert execute(interpreter, "sector_name(1)") == "Ash Gate"
    assert execute(interpreter, "sector_name(4)") == "Throne of the Heretek"
    assert execute(interpreter, "enemy_name(4)") == "Arch-Heretek Vharax"
    assert execute(interpreter, "enemy_health(1)") == 44
    assert execute(interpreter, "enemy_health(4)") == 96


def test_complete_showcase_withdrawal_session(monkeypatch, capsys):
    # A deterministic full-program smoke test. The player withdraws at the
    # first strategic choice, which exercises startup, function definitions,
    # the main game loop, input, branching, status output, and termination.
    monkeypatch.setattr("builtins.input", lambda prompt="": "4")
    random.seed(1)

    interpreter = Interpreter()
    execute(interpreter, SOURCE)

    output = capsys.readouterr().out
    assert "WARPY40K: THE VAULT OF VHARAX" in output
    assert "Sector 1 : Ash Gate" in output
    assert "WITHDRAWAL: You seal the vault behind you." in output
    assert "Extraction score:" in output


def test_complete_showcase_victory_session(monkeypatch, capsys):
    monkeypatch.setattr(random, "random", lambda: 0.5)

    def choose(prompt=""):
        if "Choose your approach" in prompt:
            return "1"
        return "2"

    monkeypatch.setattr("builtins.input", choose)
    execute(Interpreter(), SOURCE)

    output = capsys.readouterr().out
    assert "Sector 4 : Throne of the Heretek" in output
    assert "VICTORY: VHARAX HAS BEEN JUDGED." in output
    assert "Vault sanction: EXTERMINATUS" in output
    assert "Final score:" in output


def test_complete_showcase_defeat_session(monkeypatch, capsys):
    source = SOURCE.replace("health = 100;", "health = 1;", 1)
    monkeypatch.setattr(random, "random", lambda: 0.5)

    def choose(prompt=""):
        if "Choose your approach" in prompt:
            return "1"
        return "1"

    monkeypatch.setattr("builtins.input", choose)
    execute(Interpreter(), source)

    output = capsys.readouterr().out
    assert "DEFEAT: Your duty ends beneath the forge-city." in output
    assert "Relics recovered before death: 0" in output


def test_complete_showcase_corruption_session(monkeypatch, capsys):
    source = SOURCE.replace("corruption = 5;", "corruption = 99;", 1)
    monkeypatch.setattr(random, "random", lambda: 0.0)

    def choose(prompt=""):
        if "Choose your approach" in prompt:
            return "1"
        return "1"

    monkeypatch.setattr("builtins.input", choose)
    execute(Interpreter(), source)

    output = capsys.readouterr().out
    assert "A Warp pulse rolls through the corridor." in output
    assert "Your identity dissolves into the Warp." in output
    assert "DEFEAT: Your duty ends beneath the forge-city." in output


def test_invalid_action_and_empty_medicae_cost_no_turn(monkeypatch, capsys):
    source = SOURCE.replace("health = 100;", "health = 1;", 1)
    source = source.replace("medicae = 2;", "medicae = 0;", 1)
    actions = iter(["invalid", "4", "1"])
    monkeypatch.setattr(random, "random", lambda: 0.5)

    def choose(prompt=""):
        if "Choose your approach" in prompt:
            return "1"
        return next(actions)

    monkeypatch.setattr("builtins.input", choose)
    execute(Interpreter(), source)

    output = capsys.readouterr().out
    assert "Invalid order. Hesitation costs no turn." in output
    assert "No medicae charges remain." in output
    assert output.count("Scrap Cultist strikes for") == 1
