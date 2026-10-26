"""v1.6 Sanction capability and compatibility tests."""

import pytest

from warpy40k.interpreter import EffectViolation, Interpreter
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser


def run(source, **kwargs):
    interpreter = Interpreter(**kwargs)
    result = interpreter.execute(Parser(Lexer(source).tokenize()).parse())
    return result, interpreter


def test_pure_execution_requires_no_effects():
    assert run("def add(a, b) { return a + b; } add(4, 5)", strict_effects=True)[0] == 9


def test_unsanctioned_time_is_denied():
    with pytest.raises(EffectViolation, match="time"):
        run("Clock()", granted_effects=["time"])


def test_host_must_grant_requested_capability():
    with pytest.raises(EffectViolation, match="not granted"):
        run("Sanction time { Clock() }")


def test_time_sanction_and_restoration():
    result, _ = run(
        "Sanction time { Clock() }", granted_effects=["time"], strict_effects=True
    )
    assert isinstance(result, float)
    with pytest.raises(EffectViolation):
        run(
            "Sanction time { Clock() } Clock()",
            granted_effects=["time"],
            strict_effects=True,
        )


def test_nested_sanction_cannot_escalate():
    with pytest.raises(EffectViolation, match="Nested"):
        run(
            "Sanction console { Sanction console, time { Clock() } }",
            granted_effects=["time", "console"],
        )


def test_file_access_confined_to_host_root(tmp_path):
    result, _ = run(
        'Sanction file_write, file_read { WriteFile("log.txt", "hello"); ' 
        'ReadFile("log.txt") }',
        granted_effects=["file_read", "file_write"],
        file_root=tmp_path,
        strict_effects=True,
    )
    assert result == "hello"
    assert (tmp_path / "log.txt").read_text() == "hello"
    with pytest.raises(EffectViolation, match="Unsafe"):
        run(
            'Sanction file_read { ReadFile("../secrets.txt") }',
            granted_effects=["file_read"],
            file_root=tmp_path,
        )


def test_symlink_cannot_escape_file_root(tmp_path):
    outside = tmp_path.parent / "outside-warpy-effects.txt"
    outside.write_text("secret")
    (tmp_path / "link.txt").symlink_to(outside)
    try:
        with pytest.raises(EffectViolation, match="escapes"):
            run(
                'Sanction file_read { ReadFile("link.txt") }',
                granted_effects=["file_read"],
                file_root=tmp_path,
            )
    finally:
        outside.unlink()


def test_environment_requires_permission(monkeypatch):
    monkeypatch.setenv("WARPY_TEST_ENV", "value")
    assert (
        run(
            'Sanction environment { GetEnv("WARPY_TEST_ENV") }',
            granted_effects=["environment"],
        )[0]
        == "value"
    )


def test_strict_mode_denies_ambient_print(capsys):
    with pytest.raises(EffectViolation, match="console"):
        run('print("no")', strict_effects=True)
    assert capsys.readouterr().out == ""


def test_legacy_print_remains_supported(capsys):
    run('print("legacy")')
    assert capsys.readouterr().out == "legacy\n"


def test_strict_print_inside_console_sanction(capsys):
    run(
        'Sanction console { print("allowed") }',
        granted_effects=["console"],
        strict_effects=True,
    )
    assert capsys.readouterr().out == "allowed\n"


def test_nested_function_uses_active_sanction():
    result, _ = run(
        "def now() { return Clock(); } Sanction time { now() }",
        granted_effects=["time"],
        strict_effects=True,
    )
    assert isinstance(result, float)


def test_sanction_words_are_contextual_identifiers():
    assert run("Sanction = 6; Sanction + 1")[0] == 7


def test_invalid_grants_are_rejected_before_execution():
    with pytest.raises(ValueError, match="Unknown host capability"):
        Interpreter(granted_effects=["network"])


def test_sanction_cleanup_on_runtime_error():
    runtime = Interpreter(granted_effects=["time"], strict_effects=True)
    with pytest.raises(ZeroDivisionError):
        runtime.execute(Parser(Lexer("Sanction time { 1 / 0 }").tokenize()).parse())
    with pytest.raises(EffectViolation):
        runtime.execute(Parser(Lexer("Clock()").tokenize()).parse())


def test_loaded_codex_cannot_bypass_host_sanction(tmp_path):
    (tmp_path / "ClockMod.wp40k").write_text(
        "def read_clock() { return Clock(); } Codex Export read_clock;"
    )
    runtime = Interpreter(
        granted_effects=["time"],
        strict_effects=True,
        module_paths=[tmp_path],
    )
    program = Parser(
        Lexer(
            "Invoke read_clock from Codex ClockMod; " "Sanction time { read_clock() }"
        ).tokenize()
    ).parse()
    assert isinstance(runtime.execute(program), float)
    with pytest.raises(EffectViolation, match="time"):
        runtime.execute(Parser(Lexer("read_clock()").tokenize()).parse())


def test_imported_codex_cannot_implicitly_elevate(tmp_path):
    (tmp_path / "Escalation.wp40k").write_text(
        "Sanction time { Clock() }; value = 1; Codex Export value;"
    )
    with pytest.raises(EffectViolation, match="not granted"):
        run(
            "Invoke value from Codex Escalation",
            module_paths=[tmp_path],
            strict_effects=True,
        )


def test_cli_effect_options(tmp_path, capsys):
    from warpy40k.__main__ import execute_code

    execute_code(
        'Sanction console { print("approved") }',
        print_result=False,
        granted_effects=["console"],
        strict_effects=True,
    )
    assert capsys.readouterr().out == "approved\n"
