"""
Interpreter for the WarPy40K language.

Executes the Abstract Syntax Tree (AST) and produces results.
"""

import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .ast import (
    ASTNode,
    BinaryOpNode,
    BindingPatternNode,
    BlessExprNode,
    BlockNode,
    ChaosExprNode,
    CurseExprNode,
    DataslateLiteralNode,
    DataslatePatternNode,
    EmperorExprNode,
    ExterminatusExprNode,
    FieldAccessNode,
    FunctionCallNode,
    FunctionDefinitionNode,
    IdentifierNode,
    IfStatementNode,
    IndexAccessNode,
    InquisitionExprNode,
    LiteralNode,
    LiteralPatternNode,
    OrderStatementNode,
    PatternNode,
    Program,
    PurgeExprNode,
    ReturnStatementNode,
    SquadLiteralNode,
    SquadPatternNode,
    UnaryOpNode,
    VariableAssignmentNode,
    VariableDeclarationNode,
    WhileLoopNode,
    WildcardPatternNode,
)


@dataclass
class SquadValue:
    """Ordered mutable WarPy40K collection."""

    members: List[Any]

    def __len__(self) -> int:
        return len(self.members)

    def __repr__(self) -> str:
        return "Squad[" + ", ".join(repr(value) for value in self.members) + "]"


@dataclass(frozen=True)
class DataslateValue:
    """Immutable WarPy40K structured record."""

    fields: Tuple[Tuple[str, Any], ...]

    def __len__(self) -> int:
        return len(self.fields)

    def get(self, key: str) -> Any:
        for field_name, value in self.fields:
            if field_name == key:
                return value
        raise KeyError(f"Dataslate has no field '{key}'")

    def has(self, key: str) -> bool:
        return any(field_name == key for field_name, _ in self.fields)

    def inscribe(self, key: str, value: Any) -> "DataslateValue":
        updated = []
        found = False
        for field_name, field_value in self.fields:
            if field_name == key:
                updated.append((field_name, value))
                found = True
            else:
                updated.append((field_name, field_value))
        if not found:
            updated.append((key, value))
        return DataslateValue(tuple(updated))

    def erase(self, key: str) -> "DataslateValue":
        if not self.has(key):
            raise KeyError(f"Dataslate has no field '{key}'")
        return DataslateValue(
            tuple(
                (field_name, value)
                for field_name, value in self.fields
                if field_name != key
            )
        )

    def __repr__(self) -> str:
        body = ", ".join(f"{name}: {value!r}" for name, value in self.fields)
        return "Dataslate{" + body + "}"


@dataclass
class UserFunction:
    name: str
    parameters: List[str]
    body: BlockNode
    closure: Tuple[Dict[str, Any], ...]


class _ReturnSignal(Exception):
    def __init__(self, value: Any) -> None:
        super().__init__()
        self.value = value


class Interpreter:
    """Tree-walking interpreter for WarPy40K."""

    def __init__(self) -> None:
        self.environment: Dict[str, Any] = {}
        self._scopes: List[Dict[str, Any]] = [self.environment]
        self._function_depth = 0
        self._init_builtins()

    def _init_builtins(self) -> None:
        self.environment["FAITH"] = 100
        self.environment["CORRUPTION"] = 0
        self.environment["POPULATION"] = 1000000
        self.environment["True"] = True
        self.environment["False"] = False

        self.environment["print"] = self._builtin_print
        self.environment["input"] = self._builtin_input
        self.environment["random"] = self._builtin_random
        self.environment["abs"] = abs
        self.environment["min"] = min
        self.environment["max"] = max
        self.environment["pow"] = pow
        self.environment["len"] = len
        self.environment["range"] = range
        self.environment["int"] = self._builtin_int
        self.environment["float"] = self._builtin_float
        self.environment["str"] = self._builtin_str
        self.environment["exit"] = self._builtin_exit

        self.environment["Deploy"] = self._builtin_deploy
        self.environment["Extract"] = self._builtin_extract
        self.environment["Reassign"] = self._builtin_reassign
        self.environment["Inscribe"] = self._builtin_inscribe
        self.environment["Erase"] = self._builtin_erase

    def _builtin_print(self, *args: Any) -> None:
        print(*args)
        return None

    def _builtin_input(self, prompt: str = "") -> str:
        return input(prompt)

    def _builtin_exit(self, code: int = 0) -> None:
        import sys

        sys.exit(code)

    def _builtin_random(self) -> float:
        return random.random()

    def _builtin_int(self, value: Any) -> int:
        if isinstance(value, (bool, int, float, str)):
            return int(value.strip() if isinstance(value, str) else value)
        raise TypeError("int() expects a number, Boolean, or decimal string")

    def _builtin_float(self, value: Any) -> float:
        if isinstance(value, (bool, int, float, str)):
            return float(value.strip() if isinstance(value, str) else value)
        raise TypeError("float() expects a number, Boolean, or decimal string")

    def _builtin_str(self, value: Any) -> str:
        return str(value)

    def _require_squad(self, value: Any) -> SquadValue:
        if not isinstance(value, SquadValue):
            raise TypeError("operation expects a Squad value")
        return value

    def _require_dataslate(self, value: Any) -> DataslateValue:
        if not isinstance(value, DataslateValue):
            raise TypeError("operation expects a Dataslate value")
        return value

    def _builtin_deploy(self, squad: Any, value: Any) -> SquadValue:
        target = self._require_squad(squad)
        target.members.append(value)
        return target

    def _builtin_extract(self, squad: Any, index: Any = None) -> Any:
        target = self._require_squad(squad)
        if not target.members:
            raise IndexError("cannot Extract from an empty Squad")
        if index is None:
            return target.members.pop()
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("Squad index must be an integer")
        return target.members.pop(index)

    def _builtin_reassign(self, squad: Any, index: Any, value: Any) -> SquadValue:
        target = self._require_squad(squad)
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("Squad index must be an integer")
        target.members[index] = value
        return target

    def _builtin_inscribe(self, dataslate: Any, key: Any, value: Any) -> DataslateValue:
        target = self._require_dataslate(dataslate)
        if not isinstance(key, str):
            raise TypeError("Dataslate field name must be a string")
        return target.inscribe(key, value)

    def _builtin_erase(self, dataslate: Any, key: Any) -> DataslateValue:
        target = self._require_dataslate(dataslate)
        if not isinstance(key, str):
            raise TypeError("Dataslate field name must be a string")
        return target.erase(key)

    def _lookup(self, name: str) -> Any:
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Name '{name}' is not defined")

    def _define(self, name: str, value: Any) -> Any:
        self._scopes[-1][name] = value
        return value

    def execute(self, node: ASTNode) -> Any:
        if isinstance(node, Program):
            return self._execute_program(node)
        if isinstance(node, LiteralNode):
            return node.value
        if isinstance(node, IdentifierNode):
            return self._lookup(node.name)
        if isinstance(node, BinaryOpNode):
            return self._execute_binary_op(node)
        if isinstance(node, UnaryOpNode):
            return self._execute_unary_op(node)
        if isinstance(node, VariableDeclarationNode):
            return self._execute_variable_declaration(node)
        if isinstance(node, VariableAssignmentNode):
            return self._execute_variable_assignment(node)
        if isinstance(node, FunctionDefinitionNode):
            return self._execute_function_definition(node)
        if isinstance(node, FunctionCallNode):
            return self._execute_function_call(node)
        if isinstance(node, IfStatementNode):
            return self._execute_if_statement(node)
        if isinstance(node, WhileLoopNode):
            return self._execute_while_loop(node)
        if isinstance(node, OrderStatementNode):
            return self._execute_order_statement(node)
        if isinstance(node, BlockNode):
            return self._execute_block(node)
        if isinstance(node, ReturnStatementNode):
            return self._execute_return_statement(node)
        if isinstance(node, SquadLiteralNode):
            return SquadValue([self.execute(member) for member in node.members])
        if isinstance(node, DataslateLiteralNode):
            return DataslateValue(
                tuple((name, self.execute(value)) for name, value in node.fields)
            )
        if isinstance(node, IndexAccessNode):
            return self._execute_index_access(node)
        if isinstance(node, FieldAccessNode):
            return self._execute_field_access(node)
        if isinstance(node, InquisitionExprNode):
            return self._execute_inquisition_expr(node)
        if isinstance(node, EmperorExprNode):
            return self._execute_emperor_expr(node)
        if isinstance(node, ChaosExprNode):
            return self._execute_chaos_expr(node)
        if isinstance(node, PurgeExprNode):
            return self._execute_purge_expr(node)
        if isinstance(node, ExterminatusExprNode):
            return self._execute_exterminatus_expr(node)
        if isinstance(node, BlessExprNode):
            return self._execute_bless_expr(node)
        if isinstance(node, CurseExprNode):
            return self._execute_curse_expr(node)
        raise RuntimeError(f"No execution method for node type: {type(node).__name__}")

    def _execute_program(self, node: Program) -> Any:
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result

    def _execute_binary_op(self, node: BinaryOpNode) -> Any:
        left = self.execute(node.left)
        right = self.execute(node.right)
        operator = node.operator
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right
        if operator == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        if operator == "^":
            return left**right
        if operator == "==":
            return left == right
        if operator == "!=":
            return left != right
        if operator == ">":
            return left > right
        if operator == "<":
            return left < right
        if operator == ">=":
            return left >= right
        if operator == "<=":
            return left <= right
        if operator in ("AND", "&&"):
            return left and right
        if operator in ("OR", "||"):
            return left or right
        raise RuntimeError(f"Unknown operator: {operator}")

    def _execute_unary_op(self, node: UnaryOpNode) -> Any:
        operand = self.execute(node.operand)
        if node.operator == "-":
            return -operand
        if node.operator in ("NOT", "!"):
            return not operand
        raise RuntimeError(f"Unknown unary operator: {node.operator}")

    def _execute_variable_declaration(self, node: VariableDeclarationNode) -> Any:
        return self._define(
            node.name, self.execute(node.value) if node.value is not None else None
        )

    def _execute_variable_assignment(self, node: VariableAssignmentNode) -> Any:
        return self._define(node.name, self.execute(node.value))

    def _execute_function_definition(
        self, node: FunctionDefinitionNode
    ) -> UserFunction:
        if not isinstance(node.body, BlockNode):
            raise RuntimeError("Function body must be a block")
        function = UserFunction(
            node.name, list(node.parameters), node.body, tuple(self._scopes)
        )
        self._define(node.name, function)
        return function

    def _execute_function_call(self, node: FunctionCallNode) -> Any:
        func = self._lookup(node.name)
        args = [self.execute(arg) for arg in node.arguments]
        if isinstance(func, UserFunction):
            return self._call_user_function(func, args)
        if callable(func):
            return func(*args)
        raise TypeError(f"'{node.name}' is not callable")

    def _call_user_function(self, function: UserFunction, args: List[Any]) -> Any:
        if len(args) != len(function.parameters):
            raise TypeError(
                f"Function '{function.name}' expected {len(function.parameters)} "
                f"argument(s), got {len(args)}"
            )
        local_scope: Dict[str, Any] = dict(zip(function.parameters, args))
        previous_scopes = self._scopes
        self._scopes = list(function.closure) + [local_scope]
        self._function_depth += 1
        try:
            try:
                self.execute(function.body)
            except _ReturnSignal as signal:
                return signal.value
            return None
        finally:
            self._function_depth -= 1
            self._scopes = previous_scopes

    def _execute_if_statement(self, node: IfStatementNode) -> Any:
        if self.execute(node.condition):
            return self.execute(node.then_branch)
        if node.else_branch is not None:
            return self.execute(node.else_branch)
        return None

    def _execute_while_loop(self, node: WhileLoopNode) -> Any:
        result = None
        while self.execute(node.condition):
            result = self.execute(node.body)
        return result

    def _execute_order_statement(self, node: OrderStatementNode) -> Any:
        target = self.execute(node.target)
        for case in node.cases:
            bindings = self._match_pattern(case.pattern, target)
            if bindings is None:
                continue
            scope = self._scopes[-1]
            previous = {name: scope[name] for name in bindings if name in scope}
            absent = [name for name in bindings if name not in scope]
            scope.update(bindings)
            try:
                if case.guard is not None and not self.execute(case.guard):
                    continue
                return self.execute(case.body)
            finally:
                for name in absent:
                    scope.pop(name, None)
                scope.update(previous)
        if node.otherwise is not None:
            return self.execute(node.otherwise)
        return None

    def _match_pattern(
        self, pattern: PatternNode, value: Any
    ) -> Optional[Dict[str, Any]]:
        bindings: Dict[str, Any] = {}
        if self._match_into(pattern, value, bindings):
            return bindings
        return None

    def _match_into(
        self, pattern: PatternNode, value: Any, bindings: Dict[str, Any]
    ) -> bool:
        if isinstance(pattern, WildcardPatternNode):
            return True
        if isinstance(pattern, LiteralPatternNode):
            return value == pattern.value
        if isinstance(pattern, BindingPatternNode):
            bindings[pattern.name] = value
            return True
        if isinstance(pattern, DataslatePatternNode):
            if not isinstance(value, DataslateValue):
                return False
            snapshot = dict(bindings)
            for field_name, field_pattern in pattern.fields:
                if not value.has(field_name):
                    bindings.clear()
                    bindings.update(snapshot)
                    return False
                if not self._match_into(
                    field_pattern, value.get(field_name), bindings
                ):
                    bindings.clear()
                    bindings.update(snapshot)
                    return False
            return True
        if isinstance(pattern, SquadPatternNode):
            if not isinstance(value, SquadValue):
                return False
            if len(value.members) != len(pattern.members):
                return False
            snapshot = dict(bindings)
            for member_pattern, member_value in zip(pattern.members, value.members):
                if not self._match_into(member_pattern, member_value, bindings):
                    bindings.clear()
                    bindings.update(snapshot)
                    return False
            return True
        raise RuntimeError(f"Unknown pattern node: {type(pattern).__name__}")

    def _execute_block(self, node: BlockNode) -> Any:
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result

    def _execute_return_statement(self, node: ReturnStatementNode) -> Any:
        if self._function_depth == 0:
            raise RuntimeError("'return' can only be used inside a function")
        raise _ReturnSignal(
            self.execute(node.value) if node.value is not None else None
        )

    def _execute_index_access(self, node: IndexAccessNode) -> Any:
        target = self.execute(node.target)
        index = self.execute(node.index)
        if isinstance(target, SquadValue):
            if not isinstance(index, int) or isinstance(index, bool):
                raise TypeError("Squad index must be an integer")
            return target.members[index]
        if isinstance(target, str):
            if not isinstance(index, int) or isinstance(index, bool):
                raise TypeError("string index must be an integer")
            return target[index]
        raise TypeError("index access is supported only for Squad and string values")

    def _execute_field_access(self, node: FieldAccessNode) -> Any:
        target = self.execute(node.target)
        if not isinstance(target, DataslateValue):
            raise TypeError("field access is supported only for Dataslate values")
        return target.get(node.field_name)

    def _execute_inquisition_expr(self, node: InquisitionExprNode) -> Any:
        return bool(self.execute(node.target)) if node.target is not None else True

    def _execute_emperor_expr(self, node: EmperorExprNode) -> Any:
        faith_factor = self._lookup("FAITH") / 100.0
        if node.target is not None:
            target_value = self.execute(node.target)
            return (
                target_value * faith_factor
                if isinstance(target_value, (int, float))
                else target_value
            )
        return 1000

    def _execute_chaos_expr(self, node: ChaosExprNode) -> Any:
        corruption = self._lookup("CORRUPTION") / 100.0
        if node.target is not None:
            target_value = self.execute(node.target)
            if isinstance(target_value, (int, float)):
                return (
                    target_value
                    + random.uniform(-corruption, corruption) * target_value
                )
            return target_value
        return random.random() * 100

    def _execute_purge_expr(self, node: PurgeExprNode) -> Any:
        target_value = self.execute(node.target)
        if isinstance(target_value, (int, float)):
            return 0
        if isinstance(target_value, str):
            return ""
        if isinstance(target_value, SquadValue):
            return SquadValue([])
        if isinstance(target_value, DataslateValue):
            return DataslateValue(tuple())
        return None

    def _execute_exterminatus_expr(self, node: ExterminatusExprNode) -> Any:
        if node.target is not None:
            self.execute(node.target)
            return None
        return "EXTERMINATUS"

    def _execute_bless_expr(self, node: BlessExprNode) -> Any:
        target_value = self.execute(node.target)
        if isinstance(target_value, (int, float)):
            return target_value + target_value / 10
        if isinstance(target_value, str):
            return f"Blessed {target_value}"
        return target_value

    def _execute_curse_expr(self, node: CurseExprNode) -> Any:
        target_value = self.execute(node.target)
        if isinstance(target_value, (int, float)):
            return target_value * 0.9
        if isinstance(target_value, str):
            return f"Cursed {target_value}"
        return target_value
