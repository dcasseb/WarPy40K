"""Integration tests for the WarPy40K command-line entry point."""

import sys

import pytest

from warpy40k import __main__ as cli


def test_execute_file_runs_complete_source_exactly_once(tmp_path, capsys):
    program = tmp_path / "single_pass.wp40k"
    program.write_text(
        'print("side effect")\n'
        "def identity(value) { return value }\n"
        "print(identity(42))\n",
        encoding="utf-8",
    )

    cli.execute_file(str(program))

    output = capsys.readouterr().out
    assert output.count("side effect") == 1
    assert output.count("42") == 1


def test_execute_file_does_not_echo_the_last_expression(tmp_path, capsys):
    program = tmp_path / "script.wp40k"
    program.write_text("40 + 2\n", encoding="utf-8")

    cli.execute_file(str(program))

    assert capsys.readouterr().out == ""


def test_execute_file_supports_utf8_and_numeric_conversion(
    tmp_path, monkeypatch, capsys
):
    program = tmp_path / "conversao.wp40k"
    program.write_text(
        'valor = int(input("Número: "))\nprint("Áquila", valor + 1)\n',
        encoding="utf-8",
    )
    monkeypatch.setattr("builtins.input", lambda prompt="": "41")

    cli.execute_file(str(program))

    assert "Áquila 42" in capsys.readouterr().out


def test_execute_code_can_show_tokens_and_ast(capsys):
    cli.execute_code("1 + 2", show_tokens=True)
    token_output = capsys.readouterr().out
    assert "INTEGER" in token_output

    cli.execute_code("1 + 2", show_ast=True)
    ast_output = capsys.readouterr().out
    assert "Program" in ast_output


def test_execute_file_reports_missing_path(tmp_path, capsys):
    missing = tmp_path / "missing.wp40k"

    with pytest.raises(SystemExit, match="1"):
        cli.execute_file(str(missing))

    assert "not found" in capsys.readouterr().err


def test_main_dispatches_inline_code(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["warpy40k", "-c", "20 + 22"])

    cli.main()

    assert capsys.readouterr().out.strip() == "42"
