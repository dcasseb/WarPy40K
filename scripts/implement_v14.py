from pathlib import Path


def replace(path, old, new):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"pattern not found in {path}: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


replace(
    "src/warpy40k/parser.py",
    "    ChaosExprNode,\n    CurseExprNode,",
    "    ChaosExprNode,\n    ContractAssertionNode,\n    ContractClauseNode,\n    CurseExprNode,",
)
replace(
    "src/warpy40k/parser.py",
    "        if token.type == TokenType.WARP:\n            return self._parse_warp_statement()\n        if token.type == TokenType.LBRACE:",
    "        if token.type == TokenType.WARP:\n            return self._parse_warp_statement()\n        if token.type == TokenType.INQUISITION and self._next_identifier_is(\"Assert\"):\n            return self._parse_contract_assertion()\n        if token.type == TokenType.LBRACE:",
)
replace(
    "src/warpy40k/parser.py",
    "    def _parse_if_statement(self) -> IfStatementNode:\n",
    "    def _next_identifier_is(self, value: str) -> bool:\n        if self.position >= len(self.tokens):\n            return False\n        token = self.tokens[self.position]\n        return token.type == TokenType.IDENTIFIER and token.value == value\n\n    def _parse_contract_assertion(self) -> ContractAssertionNode:\n        token = self._expect(TokenType.INQUISITION)\n        marker = self._expect(TokenType.IDENTIFIER, \"Expected 'Assert' after Inquisition\")\n        if marker.value != \"Assert\":\n            raise SyntaxError(\n                f\"Expected 'Assert' after Inquisition at line {marker.line}, \"\n                f\"column {marker.column}\"\n            )\n        condition = self._parse_expression()\n        if self.current_token and self.current_token.type == TokenType.SEMICOLON:\n            self._advance()\n        return ContractAssertionNode(condition, token.line, token.column)\n\n    def _parse_if_statement(self) -> IfStatementNode:\n",
)

old_function_tail = '''        self._expect(TokenType.RPAREN, "Expected ')' after function parameters")
        if not self.current_token or self.current_token.type != TokenType.LBRACE:
            raise SyntaxError(
                f"Function '{name_token.value}' requires a block body "
                f"at line {def_token.line}, column {def_token.column}"
            )
        body = self._parse_block()
        return FunctionDefinitionNode(
            name_token.value, parameters, body, def_token.line, def_token.column
        )'''
new_function_tail = '''        self._expect(TokenType.RPAREN, "Expected ')' after function parameters")
        requires: List[ContractClauseNode] = []
        ensures: List[ContractClauseNode] = []
        while self.current_token and self.current_token.type == TokenType.INQUISITION:
            clause_token = self.current_token
            if self.position >= len(self.tokens):
                break
            marker = self.tokens[self.position]
            if marker.type != TokenType.IDENTIFIER or marker.value not in (
                "Requires",
                "Ensures",
            ):
                break
            self._advance()
            self._advance()
            condition = self._parse_expression()
            clause = ContractClauseNode(
                condition,
                marker.value.lower(),
                clause_token.line,
                clause_token.column,
            )
            if marker.value == "Requires":
                requires.append(clause)
            else:
                ensures.append(clause)
        if not self.current_token or self.current_token.type != TokenType.LBRACE:
            raise SyntaxError(
                f"Function '{name_token.value}' requires a block body "
                f"at line {def_token.line}, column {def_token.column}"
            )
        body = self._parse_block()
        return FunctionDefinitionNode(
            name_token.value,
            parameters,
            body,
            def_token.line,
            def_token.column,
            requires,
            ensures,
        )'''
replace("src/warpy40k/parser.py", old_function_tail, new_function_tail)

replace(
    "src/warpy40k/interpreter.py",
    "    ChaosExprNode,\n    CurseExprNode,",
    "    ChaosExprNode,\n    ContractAssertionNode,\n    ContractClauseNode,\n    CurseExprNode,",
)
replace(
    "src/warpy40k/interpreter.py",
    "class UserFunction:\n    name: str\n    parameters: List[str]\n    body: BlockNode\n    closure: Tuple[Dict[str, Any], ...]",
    "class UserFunction:\n    name: str\n    parameters: List[str]\n    body: BlockNode\n    closure: Tuple[Dict[str, Any], ...]\n    requires: Tuple[ContractClauseNode, ...] = tuple()\n    ensures: Tuple[ContractClauseNode, ...] = tuple()",
)
replace(
    "src/warpy40k/interpreter.py",
    "class _ReturnSignal(Exception):\n",
    "class ContractViolation(RuntimeError):\n    \"\"\"Raised when an enabled Inquisition contract evaluates false.\"\"\"\n\n\nclass _ReturnSignal(Exception):\n",
)
replace(
    "src/warpy40k/interpreter.py",
    "    def __init__(self, warp_replay: Optional[List[float]] = None) -> None:\n",
    "    def __init__(\n        self,\n        warp_replay: Optional[List[float]] = None,\n        contracts_enabled: bool = True,\n    ) -> None:\n",
)
replace(
    "src/warpy40k/interpreter.py",
    "        self._warp_replay_index = 0\n        self._init_builtins()",
    "        self._warp_replay_index = 0\n        self.contracts_enabled = contracts_enabled\n        self._init_builtins()",
)
replace(
    "src/warpy40k/interpreter.py",
    "        if isinstance(node, WarpStatementNode):\n            return self._execute_warp_statement(node)\n        if isinstance(node, BlockNode):",
    "        if isinstance(node, WarpStatementNode):\n            return self._execute_warp_statement(node)\n        if isinstance(node, ContractAssertionNode):\n            return self._execute_contract_assertion(node)\n        if isinstance(node, BlockNode):",
)
replace(
    "src/warpy40k/interpreter.py",
    "        function = UserFunction(\n            node.name, list(node.parameters), node.body, tuple(self._scopes)\n        )",
    "        function = UserFunction(\n            node.name,\n            list(node.parameters),\n            node.body,\n            tuple(self._scopes),\n            tuple(node.requires),\n            tuple(node.ensures),\n        )",
)

old_call = '''        local_scope: Dict[str, Any] = dict(zip(function.parameters, args))
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
            self._scopes = previous_scopes'''
new_call = '''        local_scope: Dict[str, Any] = dict(zip(function.parameters, args))
        previous_scopes = self._scopes
        self._scopes = list(function.closure) + [local_scope]
        self._function_depth += 1
        try:
            if self.contracts_enabled:
                for clause in function.requires:
                    self._check_contract(clause, "precondition", function.name)
            try:
                self.execute(function.body)
                result = None
            except _ReturnSignal as signal:
                result = signal.value
            if self.contracts_enabled:
                had_result = "result" in local_scope
                previous_result = local_scope.get("result")
                local_scope["result"] = result
                try:
                    for clause in function.ensures:
                        self._check_contract(clause, "postcondition", function.name)
                finally:
                    if had_result:
                        local_scope["result"] = previous_result
                    else:
                        local_scope.pop("result", None)
            return result
        finally:
            self._function_depth -= 1
            self._scopes = previous_scopes'''
replace("src/warpy40k/interpreter.py", old_call, new_call)

replace(
    "src/warpy40k/interpreter.py",
    "    def _execute_if_statement(self, node: IfStatementNode) -> Any:\n",
    '''    def _contract_values(self, condition: ASTNode) -> str:
        names: List[str] = []

        def visit(value: Any) -> None:
            if isinstance(value, IdentifierNode):
                if value.name not in names:
                    names.append(value.name)
                return
            if isinstance(value, ASTNode):
                for field_value in vars(value).values():
                    visit(field_value)
                return
            if isinstance(value, (list, tuple)):
                for item in value:
                    visit(item)

        visit(condition)
        rendered = []
        for name in names:
            try:
                rendered.append(f"{name}={self._lookup(name)!r}")
            except NameError:
                pass
        return ", ".join(rendered)

    def _check_contract(
        self, clause: ContractClauseNode, kind: str, function_name: str
    ) -> None:
        if bool(self.execute(clause.condition)):
            return
        values = self._contract_values(clause.condition)
        detail = f"; values: {values}" if values else ""
        raise ContractViolation(
            f"Inquisition {kind} failed in function '{function_name}' "
            f"at line {clause.line}, column {clause.column}: "
            f"{clause.condition!r}{detail}"
        )

    def _execute_contract_assertion(self, node: ContractAssertionNode) -> bool:
        if not self.contracts_enabled:
            return True
        if bool(self.execute(node.condition)):
            return True
        values = self._contract_values(node.condition)
        detail = f"; values: {values}" if values else ""
        raise ContractViolation(
            f"Inquisition assertion failed at line {node.line}, "
            f"column {node.column}: {node.condition!r}{detail}"
        )

    def _execute_if_statement(self, node: IfStatementNode) -> Any:
''',
)

replace("src/warpy40k/__init__.py", '__version__ = "1.3.0"', '__version__ = "1.4.0"')
replace("pyproject.toml", 'version = "1.3.0"', 'version = "1.4.0"')
replace(
    "src/warpy40k/__init__.py",
    "from .interpreter import Interpreter",
    "from .interpreter import ContractViolation, Interpreter",
)
replace(
    "src/warpy40k/__init__.py",
    '    "Interpreter",\n',
    '    "Interpreter",\n    "ContractViolation",\n',
)

Path("docs/inquisition_contracts.md").write_text(
    """# Inquisition Contracts

WarPy40K v1.4 turns judgment into executable specification.

## Assertions

```text
Inquisition Assert health > 0
```

False enabled assertions raise `ContractViolation` with source location, condition, and relevant identifier values.

## Preconditions and postconditions

```text
def heal(health, amount)
Inquisition Requires health > 0
Inquisition Requires amount > 0
Inquisition Ensures result >= health
{
    return health + amount
}
```

`Requires` runs after argument binding and before the body. `Ensures` runs after the return value is known and may reference parameters plus temporary `result`.

## Optional checking

`Interpreter(contracts_enabled=False)` disables condition evaluation entirely.

## Compatibility

Existing `Inquisition value` Boolean judgment remains intact. `Assert`, `Requires`, and `Ensures` are contextual identifiers, not global reserved words.

## Performance

Contract-enabled and contract-disabled execution should be benchmarked separately so validation overhead remains explicit.
""",
    encoding="utf-8",
)

p = Path("CHANGELOG.md")
text = p.read_text(encoding="utf-8")
marker = "# Changelog\n\nAll notable changes to WarPy40K are recorded here.\n\n"
entry = """## 1.4.0 — 2026-09-04

### Added

- `Inquisition Assert <condition>` executable assertions.
- Function `Inquisition Requires <condition>` preconditions.
- Function `Inquisition Ensures <condition>` postconditions with temporary `result`.
- `ContractViolation` diagnostics with relevant values.
- Optional checking through `Interpreter(contracts_enabled=False)`.

"""
if marker in text and entry not in text:
    p.write_text(text.replace(marker, marker + entry, 1), encoding="utf-8")

p = Path("docs/roadmap.md")
p.write_text(
    p.read_text(encoding="utf-8").replace(
        "## v1.4 — Inquisition Contracts\n",
        "## v1.4 — Inquisition Contracts ✅\n",
        1,
    ),
    encoding="utf-8",
)

p = Path("README.md")
text = p.read_text(encoding="utf-8").replace(
    "**Current version: 1.3.0**",
    "**Current version: 1.4.0**",
    1,
)
heading = "## Core language\n"
section = """## WarPy40K 1.4 — Inquisition Contracts

Version **1.4.0** adds executable assertions plus function preconditions and postconditions. Contract checking can be disabled through `Interpreter(contracts_enabled=False)`. See [`docs/inquisition_contracts.md`](docs/inquisition_contracts.md).

"""
if section not in text and heading in text:
    text = text.replace(heading, section + heading, 1)
p.write_text(text, encoding="utf-8")

p = Path("docs/index.md")
text = p.read_text(encoding="utf-8")
if "inquisition_contracts.md" not in text:
    text += "\n- [Inquisition Contracts](inquisition_contracts.md) — assertions, preconditions, postconditions, and optional runtime checking.\n"
p.write_text(text, encoding="utf-8")

Path(".github/workflows/bootstrap-v1.4.yml").unlink(missing_ok=True)
Path("scripts/implement_v14.py").unlink(missing_ok=True)
