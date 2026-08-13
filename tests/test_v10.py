"""WarPy40K v1.0 constructive Turing-completeness tests."""

from pathlib import Path

import pytest

from warpy40k import evaluate, reset_interpreter

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "minsky_universal.wp40k"


def setup_function():
    reset_interpreter()


def test_universal_minsky_example_executes():
    source = EXAMPLE.read_text(encoding="utf-8")
    result = evaluate(source, use_global=False)
    assert result == 7


def test_minsky_interpreter_runs_a_different_encoded_program():
    source = EXAMPLE.read_text(encoding="utf-8")

    # Load the universal interpreter and its helper functions, then append
    # another machine. This one increments C1 twice and halts:
    #   1: INC C1 -> 2
    #   2: INC C1 -> 0
    # Starting C1=40 must therefore halt with C1=42.
    source += """

FIELD_BASE_2 = 5
PROGRAM_BASE_2 = 20
machine_i1 = encode_inc(1, 2, FIELD_BASE_2)
machine_i2 = encode_inc(1, 0, FIELD_BASE_2)
machine_program = place_instruction(machine_i1, 1, PROGRAM_BASE_2) +
    place_instruction(machine_i2, 2, PROGRAM_BASE_2)
run_minsky(machine_program, PROGRAM_BASE_2, FIELD_BASE_2, 1, 40, 0, 0, False)
"""

    result = evaluate(source, use_global=False)
    assert result == 42


def test_minsky_zero_branch():
    source = EXAMPLE.read_text(encoding="utf-8")

    # 1: DECJZ C1, nonzero -> 2, zero -> 0
    # 2: INC C2 -> 0
    # With C1=0 the zero branch must halt immediately, leaving C1=0.
    source += """

FIELD_BASE_3 = 5
PROGRAM_BASE_3 = 20
branch_i1 = encode_decjz(1, 2, 0, FIELD_BASE_3)
branch_i2 = encode_inc(2, 0, FIELD_BASE_3)
branch_program = place_instruction(branch_i1, 1, PROGRAM_BASE_3) +
    place_instruction(branch_i2, 2, PROGRAM_BASE_3)
run_minsky(branch_program, PROGRAM_BASE_3, FIELD_BASE_3, 1, 0, 99, 0, False)
"""

    result = evaluate(source, use_global=False)
    assert result == 0


def test_minsky_step_guard_can_bound_non_halting_programs():
    source = EXAMPLE.read_text(encoding="utf-8")

    # 1: INC C1 -> 1 is deliberately non-halting.
    source += """

FIELD_BASE_4 = 5
PROGRAM_BASE_4 = 20
loop_i1 = encode_inc(1, 1, FIELD_BASE_4)
loop_program = place_instruction(loop_i1, 1, PROGRAM_BASE_4)
run_minsky(loop_program, PROGRAM_BASE_4, FIELD_BASE_4, 1, 0, 0, 10, False)
"""

    result = evaluate(source, use_global=False)
    assert result == -1


def test_minsky_halt_opcode_preserves_counter_one():
    source = EXAMPLE.read_text(encoding="utf-8")
    source += """

run_minsky(0, 20, 5, 0, 17, 23, 0, False)
"""

    assert evaluate(source, use_global=False) == 17


def test_minsky_increment_and_nonzero_decrement_for_counter_two():
    source = EXAMPLE.read_text(encoding="utf-8")
    source += """

FIELD_BASE_5 = 5
PROGRAM_BASE_5 = 20
c2_i1 = encode_inc(2, 2, FIELD_BASE_5)
c2_i2 = encode_decjz(2, 3, 0, FIELD_BASE_5)
c2_i3 = encode_inc(1, 0, FIELD_BASE_5)
c2_program = place_instruction(c2_i1, 1, PROGRAM_BASE_5) +
    place_instruction(c2_i2, 2, PROGRAM_BASE_5) +
    place_instruction(c2_i3, 3, PROGRAM_BASE_5)
run_minsky(c2_program, PROGRAM_BASE_5, FIELD_BASE_5, 1, 0, 0, 0, False)
"""

    assert evaluate(source, use_global=False) == 1


def test_minsky_nonzero_decrement_for_counter_one():
    source = EXAMPLE.read_text(encoding="utf-8")
    source += """

FIELD_BASE_6 = 5
PROGRAM_BASE_6 = 20
c1_i1 = encode_decjz(1, 0, 2, FIELD_BASE_6)
c1_program = place_instruction(c1_i1, 1, PROGRAM_BASE_6)
run_minsky(c1_program, PROGRAM_BASE_6, FIELD_BASE_6, 1, 2, 0, 0, False)
"""

    assert evaluate(source, use_global=False) == 1


def test_minsky_rejects_invalid_encoded_opcode():
    source = EXAMPLE.read_text(encoding="utf-8")
    source += """

INVALID_FIELD_BASE = 6
INVALID_PROGRAM_BASE = 20
invalid_program = place_instruction(5, 1, INVALID_PROGRAM_BASE)
run_minsky(invalid_program, INVALID_PROGRAM_BASE, INVALID_FIELD_BASE, 1, 0, 0, 0, False)
"""

    assert evaluate(source, use_global=False) == -2


@pytest.mark.parametrize(
    "arguments",
    [
        "-1, 20, 5, 0, 0, 0, 0, False",
        "0, 0, 5, 0, 0, 0, 0, False",
        "0, 20, 4, 0, 0, 0, 0, False",
        "0, 20, 5, -1, 0, 0, 0, False",
        "0, 20, 5, 0, -1, 0, 0, False",
        "0, 20, 5, 0, 0, -1, 0, False",
        "0, 20, 5, 0, 0, 0, -1, False",
    ],
)
def test_minsky_rejects_invalid_configuration(arguments):
    source = EXAMPLE.read_text(encoding="utf-8")
    source += f"\nrun_minsky({arguments})\n"

    assert evaluate(source, use_global=False) == -3
