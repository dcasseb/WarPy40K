"""
Interpreter for the WarPy40K language.

Executes the Abstract Syntax Tree (AST) and produces results.
"""

import random
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from .ast import (
    ASTNode,
    BinaryOpNode,
    BlessExprNode,
    BlockNode,
    ChaosExprNode,
    CurseExprNode,
    EmperorExprNode,
    ExterminatusExprNode,
    FunctionCallNode,
    FunctionDefinitionNode,
    IdentifierNode,
    IfStatementNode,
    InquisitionExprNode,
    LiteralNode,
    Program,
    PurgeExprNode,
    ReturnStatementNode,
    UnaryOpNode,
    VariableAssignmentNode,
    VariableDeclarationNode,
    WhileLoopNode,
)


@dataclass
class UserFunction:
    """Runtime representation of a WarPy40K user-defined function."""

    name: str
    parameters: List[str]
    body: BlockNode
    closure: Tuple[Dict[str, Any], ...]


class _ReturnSignal(Exception):
    """Internal signal used to unwind execution when `return` is reached."""

    def __init__(self, value: Any) -> None:
        super().__init__()
        self.value = value


class Interpreter:
    """
    Interpreter for executing WarPy40K AST nodes.

    `environment` remains the public/global environment for compatibility.
    Function calls add temporary lexical scopes on top of it.
    """

    def __init__(self) -> None:
        """Initialize the interpreter."""
        self.environment: Dict[str, Any] = {}
        self._scopes: List[Dict[str, Any]] = [self.environment]
        self._function_depth = 0
        self._init_builtins()

    def _init_builtins(self) -> None:
        """Initialize built-in functions and constants."""
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
        """Convert a numeric value or decimal string to an integer."""
        if isinstance(value, (bool, int, float, str)):
            return int(value.strip() if isinstance(value, str) else value)
        raise TypeError("int() expects a number, Boolean, or decimal string")

    def _builtin_float(self, value: Any) -> float:
        """Convert a numeric value or decimal string to a float."""
        if isinstance(value, (bool, int, float, str)):
            return float(value.strip() if isinstance(value, str) else value)
        raise TypeError("float() expects a number, Boolean, or decimal string")

    def _builtin_str(self, value: Any) -> str:
        """Return the stable textual representation of a runtime value."""
        return str(value)

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
        elif isinstance(node, LiteralNode):
            return self._execute_literal(node)
        elif isinstance(node, IdentifierNode):
            return self._execute_identifier(node)
        elif isinstance(node, BinaryOpNode):
            return self._execute_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self._execute_unary_op(node)
        elif isinstance(node, VariableDeclarationNode):
            return self._execute_variable_declaration(node)
        elif isinstance(node, VariableAssignmentNode):
            return self._execute_variable_assignment(node)
        elif isinstance(node, FunctionDefinitionNode):
            return self._execute_function_definition(node)
        elif isinstance(node, FunctionCallNode):
            return self._execute_function_call(node)
        elif isinstance(node, IfStatementNode):
            return self._execute_if_statement(node)
        elif isinstance(node, WhileLoopNode):
            return self._execute_while_loop(node)
        elif isinstance(node, BlockNode):
            return self._execute_block(node)
        elif isinstance(node, ReturnStatementNode):
            return self._execute_return_statement(node)
        elif isinstance(node, InquisitionExprNode):
            return self._execute_inquisition_expr(node)
        elif isinstance(node, EmperorExprNode):
            return self._execute_emperor_expr(node)
        elif isinstance(node, ChaosExprNode):
            return self._execute_chaos_expr(node)
        elif isinstance(node, PurgeExprNode):
            return self._execute_purge_expr(node)
        elif isinstance(node, ExterminatusExprNode):
            return self._execute_exterminatus_expr(node)
        elif isinstance(node, BlessExprNode):
            return self._execute_bless_expr(node)
        elif isinstance(node, CurseExprNode):
            return self._execute_curse_expr(node)
        else:
            raise RuntimeError(
                f"No execution method for node type: {type(node).__name__}"
            )

    def _execute_program(self, node: Program) -> Any:
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result

    def _execute_literal(self, node: LiteralNode) -> Any:
        return node.value

    def _execute_identifier(self, node: IdentifierNode) -> Any:
        return self._lookup(node.name)

    def _execute_binary_op(self, node: BinaryOpNode) -> Any:
        left = self.execute(node.left)
        right = self.execute(node.right)
        operator = node.operator

        if operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        elif operator == "^":
            return left**right
        elif operator == "==":
            return left == right
        elif operator == "!=":
            return left != right
        elif operator == ">":
            return left > right
        elif operator == "<":
            return left < right
        elif operator == ">=":
            return left >= right
        elif operator == "<=":
            return left <= right
        elif operator == "AND" or operator == "&&":
            return left and right
        elif operator == "OR" or operator == "||":
            return left or right

        raise RuntimeError(f"Unknown operator: {operator}")

    def _execute_unary_op(self, node: UnaryOpNode) -> Any:
        operand = self.execute(node.operand)
        operator = node.operator

        if operator == "-":
            return -operand
        elif operator == "NOT" or operator == "!":
            return not operand

        raise RuntimeError(f"Unknown unary operator: {operator}")

    def _execute_variable_declaration(self, node: VariableDeclarationNode) -> Any:
        value = self.execute(node.value) if node.value is not None else None
        return self._define(node.name, value)

    def _execute_variable_assignment(self, node: VariableAssignmentNode) -> Any:
        value = self.execute(node.value)
        return self._define(node.name, value)

    def _execute_function_definition(
        self, node: FunctionDefinitionNode
    ) -> UserFunction:
        if not isinstance(node.body, BlockNode):
            raise RuntimeError("Function body must be a block")

        function = UserFunction(
            name=node.name,
            parameters=list(node.parameters),
            body=node.body,
            closure=tuple(self._scopes),
        )
        self._define(node.name, function)
        return function

    def _execute_function_call(self, node: FunctionCallNode) -> Any:
        func = self._lookup(node.name)
        args = [self.execute(arg) for arg in node.arguments]

        if isinstance(func, UserFunction):
            return self._call_user_function(func, args)
        elif callable(func):
            return func(*args)

        raise TypeError(f"'{node.name}' is not callable")

    def _call_user_function(self, function: UserFunction, args: List[Any]) -> Any:
        expected = len(function.parameters)
        received = len(args)
        if received != expected:
            raise TypeError(
                f"Function '{function.name}' expected {expected} "
                f"argument(s), got {received}"
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
        condition = self.execute(node.condition)

        if condition:
            return self.execute(node.then_branch)
        elif node.else_branch is not None:
            return self.execute(node.else_branch)

        return None

    def _execute_while_loop(self, node: WhileLoopNode) -> Any:
        result = None

        while self.execute(node.condition):
            result = self.execute(node.body)

        return result

    def _execute_block(self, node: BlockNode) -> Any:
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result

    def _execute_return_statement(self, node: ReturnStatementNode) -> Any:
        if self._function_depth == 0:
            raise RuntimeError("'return' can only be used inside a function")

        value = self.execute(node.value) if node.value is not None else None
        raise _ReturnSignal(value)

    def _execute_inquisition_expr(self, node: InquisitionExprNode) -> Any:
        if node.target is not None:
            return bool(self.execute(node.target))
        return True

    def _execute_emperor_expr(self, node: EmperorExprNode) -> Any:
        faith_factor = self._lookup("FAITH") / 100.0

        if node.target is not None:
            target_value = self.execute(node.target)
            if isinstance(target_value, (int, float)):
                return target_value * faith_factor
            return target_value

        return 1000

    def _execute_chaos_expr(self, node: ChaosExprNode) -> Any:
        corruption = self._lookup("CORRUPTION") / 100.0

        if node.target is not None:
            target_value = self.execute(node.target)
            if isinstance(target_value, (int, float)):
                chaos_factor = random.uniform(-corruption, corruption) * target_value
                return target_value + chaos_factor
            return target_value

        return random.random() * 100

    def _execute_purge_expr(self, node: PurgeExprNode) -> Any:
        target_value = self.execute(node.target)

        if isinstance(target_value, (int, float)):
            return 0
        elif isinstance(target_value, str):
            return ""
        elif isinstance(target_value, list):
            return []
        elif isinstance(target_value, dict):
            return {}
        else:
            return None

    def _execute_exterminatus_expr(self, node: ExterminatusExprNode) -> Any:
        if node.target is not None:
            self.execute(node.target)
            return None
        return "EXTERMINATUS"

    def _execute_bless_expr(self, node: BlessExprNode) -> Any:
        target_value = self.execute(node.target)

        if isinstance(target_value, (int, float)):
            return target_value + (target_value / 10)
        elif isinstance(target_value, str):
            return f"Blessed {target_value}"
        else:
            return target_value

    def _execute_curse_expr(self, node: CurseExprNode) -> Any:
        target_value = self.execute(node.target)

        if isinstance(target_value, (int, float)):
            return target_value * 0.9
        elif isinstance(target_value, str):
            return f"Cursed {target_value}"
        else:
            return target_value
