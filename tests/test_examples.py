"""Regression tests for runnable bundled examples."""

from pathlib import Path

import pytest

from warpy40k import evaluate

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.mark.parametrize(
    "filename",
    [
        "hello.wp40k",
        "control_flow.wp40k",
        "recursion.wp40k",
        "variables.wp40k",
        "warpy_demo.wp40k",
    ],
)
def test_noninteractive_example_executes(filename, capsys):
    source = (EXAMPLES / filename).read_text(encoding="utf-8")

    evaluate(source, use_global=False)

    assert capsys.readouterr().out


def test_calculator_example_uses_explicit_numeric_conversion(monkeypatch, capsys):
    answers = iter(["10", "5"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    source = (EXAMPLES / "calculator.wp40k").read_text(encoding="utf-8")

    evaluate(source, use_global=False)

    output = capsys.readouterr().out
    assert "15" in output
    assert "50" in output
    assert "2.0" in output
