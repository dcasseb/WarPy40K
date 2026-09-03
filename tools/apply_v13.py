"""One-shot repository migration that implements WarPy40K v1.3."""

from pathlib import Path


def replace(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"pattern not found in {path}: {old[:80]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


# AST
replace(
    "src/warpy40k/ast.py",
    "    ORDER_STATEMENT = auto()\n    SQUAD_LITERAL = auto()",
    "    ORDER_STATEMENT = auto()\n    WARP_STATEMENT = auto()\n    SQUAD_LITERAL = auto()",
)
replace(
    "src/warpy40k/ast.py",
    "@dataclass\nclass SquadLiteralNode(ASTNode):",
    "@dataclass\nclass WarpStatementNode(ASTNode):\n"
    "    seed: ASTNode\n"
    "    body: ASTNode\n"
    "    line: int = 1\n"
    "    column: int = 1\n\n\n"
    "@dataclass\nclass SquadLiteralNode(ASTNode):",
)

# Parser
replace(
    "src/warpy40k/parser.py",
    "    VariableAssignmentNode,\n    WhileLoopNode,",
    "    VariableAssignmentNode,\n    WarpStatementNode,\n    WhileLoopNode,",
)
replace(
    "src/warpy40k/parser.py",
    "        if token.type == TokenType.ORDER:\n"
    "            return self._parse_order_statement()\n"
    "        if token.type == TokenType.LBRACE:",
    "        if token.type == TokenType.ORDER:\n"
    "            return self._parse_order_statement()\n"
    "        if token.type == TokenType.WARP:\n"
    "            return self._parse_warp_statement()\n"
    "        if token.type == TokenType.LBRACE:",
)
replace(
    "src/warpy40k/parser.py",
    "    def _parse_function_definition(self) -> FunctionDefinitionNode:\n",
    "    def _parse_warp_statement(self) -> WarpStatementNode:\n"
    "        token = self._expect(TokenType.WARP)\n"
    "        seed_keyword = self._expect(\n"
    "            TokenType.IDENTIFIER, \"Expected 'seed' after Warp\"\n"
    "        )\n"
    "        if seed_keyword.value != \"seed\":\n"
    "            raise SyntaxError(\n"
    "                f\"Expected 'seed' after Warp at line {seed_keyword.line}, \"\n"
    "                f\"column {seed_keyword.column}\"\n"
    "            )\n"
    "        seed = self._parse_expression()\n"
    "        if not self.current_token or self.current_token.type != TokenType.LBRACE:\n"
    "            raise SyntaxError(\n"
    "                f\"Warp requires a block body at line {token.line}, \"\n"
    "                f\"column {token.column}\"\n"
    "            )\n"
    "        body = self._parse_block()\n"
    "        if self.current_token and self.current_token.type == TokenType.SEMICOLON:\n"
    "            self._advance()\n"
    "        return WarpStatementNode(seed, body, token.line, token.column)\n\n"
    "    def _parse_function_definition(self) -> FunctionDefinitionNode:\n",
)

# Interpreter
replace(
    "src/warpy40k/interpreter.py",
    "    VariableDeclarationNode,\n    WhileLoopNode,",
    "    VariableDeclarationNode,\n    WarpStatementNode,\n    WhileLoopNode,",
)
replace(
    "src/warpy40k/interpreter.py",
    "    def __init__(self) -> None:\n"
    "        self.environment: Dict[str, Any] = {}\n"
    "        self._scopes: List[Dict[str, Any]] = [self.environment]\n"
    "        self._function_depth = 0\n"
    "        self._init_builtins()",
    "    def __init__(self, warp_replay: Optional[List[float]] = None) -> None:\n"
    "        self.environment: Dict[str, Any] = {}\n"
    "        self._scopes: List[Dict[str, Any]] = [self.environment]\n"
    "        self._function_depth = 0\n"
    "        self._warp_random_stack: List[random.Random] = []\n"
    "        self._warp_trace: List[float] = []\n"
    "        self._warp_replay = (\n"
    "            list(warp_replay) if warp_replay is not None else None\n"
    "        )\n"
    "        self._warp_replay_index = 0\n"
    "        self._init_builtins()\n\n"
    "    @property\n"
    "    def warp_trace(self) -> List[float]:\n"
    "        \"\"\"Return normalized random draws made inside Warp regions.\"\"\"\n"
    "        return list(self._warp_trace)\n\n"
    "    @property\n"
    "    def warp_replay_complete(self) -> bool:\n"
    "        \"\"\"Whether every supplied replay draw has been consumed.\"\"\"\n"
    "        return (\n"
    "            self._warp_replay is not None\n"
    "            and self._warp_replay_index == len(self._warp_replay)\n"
    "        )",
)
replace(
    "src/warpy40k/interpreter.py",
    "    def _builtin_random(self) -> float:\n        return random.random()",
    "    def _draw_random(self) -> float:\n"
    "        if not self._warp_random_stack:\n"
    "            return random.random()\n"
    "        if self._warp_replay is not None:\n"
    "            if self._warp_replay_index >= len(self._warp_replay):\n"
    "                raise RuntimeError(\n"
    "                    \"Warp replay exhausted before execution completed\"\n"
    "                )\n"
    "            value = self._warp_replay[self._warp_replay_index]\n"
    "            self._warp_replay_index += 1\n"
    "            if not isinstance(value, (int, float)) or isinstance(value, bool):\n"
    "                raise TypeError(\"Warp replay values must be numeric\")\n"
    "            value = float(value)\n"
    "            if not 0.0 <= value < 1.0:\n"
    "                raise ValueError(\n"
    "                    \"Warp replay values must be in [0.0, 1.0)\"\n"
    "                )\n"
    "        else:\n"
    "            value = self._warp_random_stack[-1].random()\n"
    "        self._warp_trace.append(value)\n"
    "        return value\n\n"
    "    def _draw_uniform(self, low: float, high: float) -> float:\n"
    "        return low + (high - low) * self._draw_random()\n\n"
    "    def _builtin_random(self) -> float:\n"
    "        return self._draw_random()",
)
replace(
    "src/warpy40k/interpreter.py",
    "        if isinstance(node, OrderStatementNode):\n"
    "            return self._execute_order_statement(node)\n"
    "        if isinstance(node, BlockNode):",
    "        if isinstance(node, OrderStatementNode):\n"
    "            return self._execute_order_statement(node)\n"
    "        if isinstance(node, WarpStatementNode):\n"
    "            return self._execute_warp_statement(node)\n"
    "        if isinstance(node, BlockNode):",
)
replace(
    "src/warpy40k/interpreter.py",
    "    def _execute_order_statement(self, node: OrderStatementNode) -> Any:\n",
    "    def _execute_warp_statement(self, node: WarpStatementNode) -> Any:\n"
    "        seed = self.execute(node.seed)\n"
    "        if not isinstance(seed, int) or isinstance(seed, bool):\n"
    "            raise TypeError(\"Warp seed must be an integer\")\n"
    "        self._warp_random_stack.append(random.Random(seed))\n"
    "        try:\n"
    "            return self.execute(node.body)\n"
    "        finally:\n"
    "            self._warp_random_stack.pop()\n\n"
    "    def _execute_order_statement(self, node: OrderStatementNode) -> Any:\n",
)
replace(
    "src/warpy40k/interpreter.py",
    "                    target_value\n"
    "                    + random.uniform(-corruption, corruption) * target_value\n"
    "                )",
    "                    target_value\n"
    "                    + self._draw_uniform(-corruption, corruption) * target_value\n"
    "                )",
)
replace(
    "src/warpy40k/interpreter.py",
    "        return random.random() * 100",
    "        return self._draw_random() * 100",
)

# Version metadata
replace("src/warpy40k/__init__.py", '__version__ = "1.2.0"', '__version__ = "1.3.0"')
replace("pyproject.toml", 'version = "1.2.0"', 'version = "1.3.0"')

# Changelog
changelog = Path("CHANGELOG.md")
text = changelog.read_text(encoding="utf-8")
heading = "# Changelog\n\nAll notable changes to WarPy40K are recorded here.\n\n"
entry = """## 1.3.0 — 2026-09-03

### Added

- Explicit `Warp seed <integer> { ... }` nondeterministic regions.
- Region-local deterministic random streams shared by `Chaos` and `random()`.
- Nested Warp regions with independent streams and correct parent restoration.
- Runtime Warp trace recording through `Interpreter.warp_trace`.
- Deterministic replay through `Interpreter(warp_replay=...)`.

### Semantics

- A Warp seed expression is evaluated exactly once on region entry.
- Seeds must be integers; Booleans, floats, and strings are rejected.
- Functions called from inside a Warp region consume the active region stream.
- Nested Warp draws do not perturb the parent region stream.
- Runtime errors and returns restore the previous Warp stream through cleanup.
- `Chaos` and `random()` outside Warp preserve legacy global randomness.
- `seed` remains an ordinary identifier outside contextual `Warp seed` syntax.

### Replay

- Warp traces store normalized random draws in execution order.
- Replaying a trace reproduces decisions independently of the new region seed.
- Replay exhaustion and invalid values fail instead of generating fresh entropy.

"""
if entry not in text:
    if heading not in text:
        raise SystemExit("CHANGELOG heading not found")
    changelog.write_text(text.replace(heading, heading + entry, 1), encoding="utf-8")

# Documentation
Path("docs/warp_effect_model.md").write_text(
    """# Warp Effect Model

WarPy40K v1.3 makes nondeterminism explicit and replayable.

## Syntax

```text
Warp seed 42 {
    roll = Chaos
    sample = random()
}
```

`seed` is contextual syntax after `Warp`; it remains a normal identifier elsewhere. The seed expression is evaluated exactly once and must produce an integer. Booleans are rejected.

## Deterministic region-local streams

Entering a Warp region creates a fresh deterministic random stream. Every `Chaos` draw and built-in `random()` call inside that dynamic region consumes the same stream. Functions invoked from the region therefore participate in the same deterministic sequence.

The same program, inputs, and Warp seed produce the same random decisions. Code outside Warp retains legacy process-global randomness for 1.x compatibility.

## Nesting

```text
Warp seed 10 {
    first = random()
    Warp seed 99 {
        nested = Chaos
    }
    second = random()
}
```

Nested Warp regions own independent streams. A nested draw does not perturb the parent stream. Structured cleanup restores the previous stream even when execution exits through an error or function return.

## Record and replay

The reference interpreter exposes normalized decisions:

```python
interpreter = Interpreter()
interpreter.execute(ast)
trace = interpreter.warp_trace
```

They can be replayed later:

```python
replay = Interpreter(warp_replay=trace)
replay.execute(ast)
assert replay.warp_replay_complete
```

Replay consumes recorded normalized draws instead of generating new ones. The seed is still evaluated and validated, but the supplied trace determines outcomes. Exhausted, nonnumeric, or out-of-range traces fail explicitly.

Recording decisions instead of Python `random.Random` internal state gives future Forge runtimes a portable semantic contract without requiring CPython RNG compatibility.

## Performance rule

Warp bookkeeping is constant-time per draw: an active-stack lookup plus one append or indexed read when recording/replaying. Replay never reparses source or rebuilds the AST per decision.

## Compatibility

WarPy40K 1.3 does not make all randomness deterministic. Existing `Chaos` and `random()` outside Warp continue to behave as in earlier 1.x versions. Programs requiring reproducibility should place nondeterministic logic inside explicit Warp regions.
""",
    encoding="utf-8",
)

index = Path("docs/index.md")
text = index.read_text(encoding="utf-8")
if "[Warp Effect Model](warp_effect_model.md)" not in text:
    marker = "## Language\n"
    link = (
        "\n- [Warp Effect Model](warp_effect_model.md) — deterministic "
        "nondeterminism, trace recording, and replay.\n"
    )
    text = text.replace(marker, marker + link, 1) if marker in text else text + link
text = text.replace(
    "The next planned release is **v1.3 — The Warp Effect Model**.",
    "**v1.3 — The Warp Effect Model is implemented.**",
)
index.write_text(text, encoding="utf-8")

roadmap = Path("docs/roadmap.md")
text = roadmap.read_text(encoding="utf-8")
text = text.replace(
    "## v1.3 — The Warp Effect Model",
    "## v1.3 — The Warp Effect Model ✅",
)
roadmap.write_text(text, encoding="utf-8")

# One-shot migration artifacts should not survive the implementation commit.
Path(".github/workflows/release-v1.2.0.yml").unlink(missing_ok=True)
Path(".github/workflows/bootstrap-v1.3.yml").unlink(missing_ok=True)
Path("tools/apply_v13.py").unlink(missing_ok=True)
