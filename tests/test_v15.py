"""Regression tests for WarPy40K v1.5 Codex modules."""

from pathlib import Path

import pytest

from warpy40k.ast import ExportNode, ImportNode
from warpy40k.interpreter import Interpreter, ModuleLoadError, SquadValue
from warpy40k.lexer import Lexer
from warpy40k.parser import Parser


def parse(source: str):
    return Parser(Lexer(source).tokenize()).parse()


def execute(source: str, module_paths=None, interpreter=None):
    runtime = interpreter or Interpreter(module_paths=module_paths)
    return runtime.execute(parse(source))


def write_module(root: Path, name: str, source: str) -> Path:
    path = root / f"{name}.wp40k"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def test_codex_import_and_export_parse_as_explicit_nodes():
    program = parse("Invoke add from Codex Math; Codex Export add;")
    assert isinstance(program.statements[0], ImportNode)
    assert program.statements[0].name == "add"
    assert program.statements[0].module == "Math"
    assert isinstance(program.statements[1], ExportNode)
    assert program.statements[1].name == "add"


def test_imported_function_executes_with_module_local_private_helper(tmp_path):
    write_module(
        tmp_path,
        "Math",
        """
def hidden(value) { return value + 1; }
def double_after_increment(value) { return hidden(value) * 2; }
Codex Export double_after_increment;
""",
    )
    result = execute(
        "Invoke double_after_increment from Codex Math; "
        "double_after_increment(4)",
        [tmp_path],
    )
    assert result == 10


def test_private_module_names_do_not_leak_into_importing_scope(tmp_path):
    write_module(
        tmp_path,
        "Vault",
        "secret = 99; public = 7; Codex Export public;",
    )
    interpreter = Interpreter(module_paths=[tmp_path])
    assert execute("Invoke public from Codex Vault; public", interpreter=interpreter) == 7
    with pytest.raises(NameError, match="secret"):
        execute("secret", interpreter=interpreter)


def test_import_of_non_exported_name_is_rejected(tmp_path):
    write_module(tmp_path, "Vault", "secret = 99;")
    with pytest.raises(ModuleLoadError, match="does not export 'secret'"):
        execute("Invoke secret from Codex Vault", [tmp_path])


def test_export_of_undefined_name_is_rejected(tmp_path):
    write_module(tmp_path, "Broken", "Codex Export missing;")
    with pytest.raises(ModuleLoadError, match="cannot export undefined name 'missing'"):
        execute("Invoke missing from Codex Broken", [tmp_path])


def test_repeated_import_reuses_cached_module_state(tmp_path):
    write_module(
        tmp_path,
        "State",
        "state = Squad[0]; Codex Export state;",
    )
    interpreter = Interpreter(module_paths=[tmp_path])
    result = execute(
        "Invoke state from Codex State; "
        "Reassign(state, 0, 5); "
        "Invoke state from Codex State; "
        "state",
        interpreter=interpreter,
    )
    assert isinstance(result, SquadValue)
    assert result.members == [5]
    assert interpreter.module_cache_size == 1


def test_nested_module_import_resolves_relative_to_calling_codex(tmp_path):
    nested = tmp_path / "campaign"
    write_module(nested, "Numbers", "answer = 42; Codex Export answer;")
    write_module(
        nested,
        "Mission",
        "Invoke answer from Codex Numbers; "
        "def report() { return answer; } "
        "Codex Export report;",
    )
    result = execute(
        'Invoke report from Codex "campaign/Mission"; report()',
        [tmp_path],
    )
    assert result == 42


def test_import_inside_exported_function_keeps_module_origin(tmp_path):
    nested = tmp_path / "campaign"
    write_module(nested, "Numbers", "answer = 42; Codex Export answer;")
    write_module(
        nested,
        "Mission",
        "def report() { Invoke answer from Codex Numbers; return answer; } "
        "Codex Export report;",
    )
    result = execute(
        'Invoke report from Codex "campaign/Mission"; report()',
        [tmp_path],
    )
    assert result == 42


def test_circular_module_import_is_reported(tmp_path):
    write_module(
        tmp_path,
        "Alpha",
        "Invoke beta from Codex Beta; alpha = 1; Codex Export alpha;",
    )
    write_module(
        tmp_path,
        "Beta",
        "Invoke alpha from Codex Alpha; beta = 2; Codex Export beta;",
    )
    with pytest.raises(ModuleLoadError, match="Circular Codex import"):
        execute("Invoke alpha from Codex Alpha", [tmp_path])


def test_module_search_path_order_is_deterministic(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    write_module(first, "Choice", "value = 1; Codex Export value;")
    write_module(second, "Choice", "value = 2; Codex Export value;")
    assert execute("Invoke value from Codex Choice; value", [first, second]) == 1


def test_absolute_and_parent_traversal_module_specs_are_rejected(tmp_path):
    with pytest.raises(ModuleLoadError, match="unsafe Codex module path"):
        execute('Invoke value from Codex "../Secret"', [tmp_path])
    with pytest.raises(ModuleLoadError, match="unsafe Codex module path"):
        execute('Invoke value from Codex "/tmp/Secret"', [tmp_path])


def test_python_modules_are_not_imported_as_codices(tmp_path):
    with pytest.raises(ModuleLoadError, match="Codex 'os' was not found"):
        execute("Invoke path from Codex os", [tmp_path])


def test_core_stdlib_uses_same_codex_abstraction():
    assert execute("Invoke identity from Codex Core; identity(17)") == 17
    assert execute("Invoke clamp from Codex Core; clamp(15, 0, 10)") == 10


def test_contextual_module_words_remain_normal_identifiers():
    result = execute(
        "Invoke = 1; Codex = 2; Export = 3; from = 4; "
        "Invoke + Codex + Export + from"
    )
    assert result == 10
