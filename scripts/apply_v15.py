from pathlib import Path


def replace(path, old, new):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"pattern not found in {path}: {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# AST nodes.
replace(
    "src/warpy40k/ast.py",
    "    CONTRACT_ASSERTION = auto()\n    SQUAD_LITERAL = auto()",
    "    CONTRACT_ASSERTION = auto()\n    IMPORT = auto()\n    EXPORT = auto()\n    SQUAD_LITERAL = auto()",
)
replace(
    "src/warpy40k/ast.py",
    "@dataclass\nclass FunctionDefinitionNode(ASTNode):",
    '''@dataclass
class ImportNode(ASTNode):
    name: str
    module: str
    line: int = 1
    column: int = 1


@dataclass
class ExportNode(ASTNode):
    name: str
    line: int = 1
    column: int = 1


@dataclass
class FunctionDefinitionNode(ASTNode):''',
)

# Parser imports and contextual statements.
replace(
    "src/warpy40k/parser.py",
    "    ExterminatusExprNode,\n    FieldAccessNode,",
    "    ExterminatusExprNode,\n    ExportNode,\n    FieldAccessNode,",
)
replace(
    "src/warpy40k/parser.py",
    "    InquisitionExprNode,\n    LiteralNode,",
    "    InquisitionExprNode,\n    ImportNode,\n    LiteralNode,",
)
replace(
    "src/warpy40k/parser.py",
    '''        if token.type == TokenType.INQUISITION and self._next_identifier_is("Assert"):
            return self._parse_contract_assertion()
        if token.type == TokenType.LBRACE:''',
    '''        if token.type == TokenType.INQUISITION and self._next_identifier_is("Assert"):
            return self._parse_contract_assertion()
        if token.type == TokenType.IDENTIFIER and token.value == "Invoke":
            return self._parse_import_statement()
        if token.type == TokenType.IDENTIFIER and token.value == "Codex":
            return self._parse_export_statement()
        if token.type == TokenType.LBRACE:''',
)
replace(
    "src/warpy40k/parser.py",
    "    def _parse_contract_assertion(self) -> ContractAssertionNode:\n",
    '''    def _parse_import_statement(self) -> ImportNode:
        token = self._expect(TokenType.IDENTIFIER)
        name = self._expect(TokenType.IDENTIFIER, "Expected imported name after Invoke")
        from_token = self._expect(TokenType.IDENTIFIER, "Expected 'from' after import name")
        if from_token.value != "from":
            raise SyntaxError(
                f"Expected 'from' after imported name at line {from_token.line}, "
                f"column {from_token.column}"
            )
        codex = self._expect(TokenType.IDENTIFIER, "Expected 'Codex' after from")
        if codex.value != "Codex":
            raise SyntaxError(
                f"Expected 'Codex' after from at line {codex.line}, "
                f"column {codex.column}"
            )
        module = self.current_token
        if module is None or module.type not in (TokenType.IDENTIFIER, TokenType.STRING):
            raise SyntaxError("Expected Codex module name")
        self._advance()
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self._advance()
        return ImportNode(name.value, module.value, token.line, token.column)

    def _parse_export_statement(self) -> ExportNode:
        token = self._expect(TokenType.IDENTIFIER)
        marker = self._expect(TokenType.IDENTIFIER, "Expected 'Export' after Codex")
        if marker.value != "Export":
            raise SyntaxError(
                f"Expected 'Export' after Codex at line {marker.line}, "
                f"column {marker.column}"
            )
        name = self._expect(TokenType.IDENTIFIER, "Expected name after Codex Export")
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self._advance()
        return ExportNode(name.value, token.line, token.column)

    def _parse_contract_assertion(self) -> ContractAssertionNode:
''',
)

# Interpreter imports and module support.
replace(
    "src/warpy40k/interpreter.py",
    "import random\nfrom dataclasses import dataclass\nfrom typing import Any, Dict, List, Optional, Tuple",
    "import random\nfrom dataclasses import dataclass\nfrom pathlib import Path\nfrom typing import Any, Dict, List, Optional, Set, Tuple",
)
replace(
    "src/warpy40k/interpreter.py",
    "    ExterminatusExprNode,\n    FieldAccessNode,",
    "    ExterminatusExprNode,\n    ExportNode,\n    FieldAccessNode,",
)
replace(
    "src/warpy40k/interpreter.py",
    "    InquisitionExprNode,\n    LiteralNode,",
    "    InquisitionExprNode,\n    ImportNode,\n    LiteralNode,",
)
replace(
    "src/warpy40k/interpreter.py",
    '''class UserFunction:
    name: str
    parameters: List[str]
    body: BlockNode
    closure: Tuple[Dict[str, Any], ...]
    requires: Tuple[ContractClauseNode, ...] = tuple()
    ensures: Tuple[ContractClauseNode, ...] = tuple()''',
    '''class UserFunction:
    name: str
    parameters: List[str]
    body: BlockNode
    closure: Tuple[Dict[str, Any], ...]
    requires: Tuple[ContractClauseNode, ...] = tuple()
    ensures: Tuple[ContractClauseNode, ...] = tuple()
    module_origin: Optional[Path] = None''',
)
replace(
    "src/warpy40k/interpreter.py",
    '''class ContractViolation(RuntimeError):
    """Raised when an enabled Inquisition contract evaluates false."""
''',
    '''class ContractViolation(RuntimeError):
    """Raised when an enabled Inquisition contract evaluates false."""


class ModuleLoadError(RuntimeError):
    """Raised when a Codex cannot be resolved or exported safely."""


@dataclass
class ModuleRecord:
    path: Path
    exports: Dict[str, Any]
''',
)
replace(
    "src/warpy40k/interpreter.py",
    '''    def __init__(
        self,
        warp_replay: Optional[List[float]] = None,
        contracts_enabled: bool = True,
    ) -> None:''',
    '''    def __init__(
        self,
        warp_replay: Optional[List[float]] = None,
        contracts_enabled: bool = True,
        module_paths: Optional[List[Path]] = None,
    ) -> None:''',
)
replace(
    "src/warpy40k/interpreter.py",
    '''        self.contracts_enabled = contracts_enabled
        self._init_builtins()''',
    '''        self.contracts_enabled = contracts_enabled
        self.module_paths = [Path(path).resolve() for path in (module_paths or [])]
        self._module_cache: Dict[Path, ModuleRecord] = {}
        self._module_loading: Set[Path] = set()
        self._module_origin_stack: List[Path] = []
        self._declared_exports: List[str] = []
        self._init_builtins()''',
)
replace(
    "src/warpy40k/interpreter.py",
    '''    @property
    def warp_trace(self) -> List[float]:''',
    '''    @property
    def module_cache_size(self) -> int:
        return len(self._module_cache)

    @property
    def warp_trace(self) -> List[float]:''',
)
replace(
    "src/warpy40k/interpreter.py",
    '''        if isinstance(node, ContractAssertionNode):
            return self._execute_contract_assertion(node)
        if isinstance(node, BlockNode):''',
    '''        if isinstance(node, ContractAssertionNode):
            return self._execute_contract_assertion(node)
        if isinstance(node, ImportNode):
            return self._execute_import(node)
        if isinstance(node, ExportNode):
            return self._execute_export(node)
        if isinstance(node, BlockNode):''',
)
replace(
    "src/warpy40k/interpreter.py",
    '''            tuple(node.requires),
            tuple(node.ensures),
        )''',
    '''            tuple(node.requires),
            tuple(node.ensures),
            self._module_origin_stack[-1] if self._module_origin_stack else None,
        )''',
)
replace(
    "src/warpy40k/interpreter.py",
    '''        self._scopes = list(function.closure) + [local_scope]
        self._function_depth += 1
        try:''',
    '''        self._scopes = list(function.closure) + [local_scope]
        self._function_depth += 1
        if function.module_origin is not None:
            self._module_origin_stack.append(function.module_origin)
        try:''',
)
replace(
    "src/warpy40k/interpreter.py",
    '''        finally:
            self._function_depth -= 1
            self._scopes = previous_scopes

    def _contract_values''',
    '''        finally:
            if function.module_origin is not None:
                self._module_origin_stack.pop()
            self._function_depth -= 1
            self._scopes = previous_scopes

    def _validate_module_spec(self, module: str) -> Path:
        spec = Path(module)
        if spec.is_absolute() or ".." in spec.parts:
            raise ModuleLoadError(f"unsafe Codex module path: {module!r}")
        if spec.suffix and spec.suffix != ".wp40k":
            raise ModuleLoadError("Codex modules must use the .wp40k extension")
        return spec if spec.suffix else spec.with_suffix(".wp40k")

    def _resolve_module(self, module: str) -> Path:
        spec = self._validate_module_spec(module)
        roots: List[Path] = []
        if self._module_origin_stack:
            roots.append(self._module_origin_stack[-1])
        roots.extend(self.module_paths)
        roots.append(Path(__file__).resolve().parent / "stdlib")
        seen: Set[Path] = set()
        for root in roots:
            root = root.resolve()
            if root in seen:
                continue
            seen.add(root)
            candidate = (root / spec).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                continue
            if candidate.is_file():
                return candidate
        raise ModuleLoadError(f"Codex '{module}' was not found")

    def _load_module(self, module: str) -> ModuleRecord:
        path = self._resolve_module(module)
        if path in self._module_cache:
            return self._module_cache[path]
        if path in self._module_loading:
            chain = " -> ".join(
                [item.stem for item in self._module_loading] + [path.stem]
            )
            raise ModuleLoadError(f"Circular Codex import detected: {chain}")
        self._module_loading.add(path)
        try:
            from .lexer import Lexer
            from .parser import Parser

            source = path.read_text(encoding="utf-8")
            ast = Parser(Lexer(source).tokenize()).parse()
            child = Interpreter(
                contracts_enabled=self.contracts_enabled,
                module_paths=self.module_paths,
            )
            child._module_cache = self._module_cache
            child._module_loading = self._module_loading
            child._module_origin_stack = [path.parent]
            child.execute(ast)
            exports: Dict[str, Any] = {}
            for name in child._declared_exports:
                try:
                    exports[name] = child._lookup(name)
                except NameError as exc:
                    raise ModuleLoadError(
                        f"Codex '{module}' cannot export undefined name '{name}'"
                    ) from exc
            record = ModuleRecord(path, exports)
            self._module_cache[path] = record
            return record
        finally:
            self._module_loading.discard(path)

    def _execute_import(self, node: ImportNode) -> Any:
        record = self._load_module(node.module)
        if node.name not in record.exports:
            raise ModuleLoadError(
                f"Codex '{node.module}' does not export '{node.name}'"
            )
        return self._define(node.name, record.exports[node.name])

    def _execute_export(self, node: ExportNode) -> Any:
        try:
            value = self._lookup(node.name)
        except NameError as exc:
            raise ModuleLoadError(
                f"Codex cannot export undefined name '{node.name}'"
            ) from exc
        if node.name not in self._declared_exports:
            self._declared_exports.append(node.name)
        return value

    def _contract_values''',
)

# Version and package data.
replace("src/warpy40k/__init__.py", '__version__ = "1.4.0"', '__version__ = "1.5.0"')
replace(
    "src/warpy40k/__init__.py",
    "from .interpreter import ContractViolation, Interpreter",
    "from .interpreter import ContractViolation, Interpreter, ModuleLoadError",
)
replace(
    "src/warpy40k/__init__.py",
    '    "ContractViolation",\n',
    '    "ContractViolation",\n    "ModuleLoadError",\n',
)
replace("pyproject.toml", 'version = "1.4.0"', 'version = "1.5.0"')
p = Path("pyproject.toml")
text = p.read_text(encoding="utf-8")
if "[tool.setuptools.package-data]" not in text:
    text += '\n[tool.setuptools.package-data]\nwarpy40k = ["stdlib/*.wp40k"]\n'
p.write_text(text, encoding="utf-8")

# Docs.
Path("docs/codex_modules.md").write_text(
    '''# Codex Modules\n\nWarPy40K v1.5 introduces explicit file modules called Codices.\n\n## Import and export\n\n```text\nInvoke clamp from Codex Core\nvalue = clamp(15, 0, 10)\n```\n\nA module exposes names explicitly:\n\n```text\ndef add(a, b) { return a + b; }\nprivate_value = 99\nCodex Export add\n```\n\nOnly exported names cross the module boundary. Module-private variables and helpers remain available to exported functions through their lexical closure.\n\n## Resolution\n\nA Codex name maps deterministically to a `.wp40k` file. Resolution order is:\n\n1. the directory of the currently executing Codex;\n2. configured `module_paths`, in order;\n3. the bundled WarPy40K standard-library directory.\n\nAbsolute paths, parent traversal (`..`), and non-`.wp40k` module extensions are rejected. WarPy40K never delegates Codex loading to Python imports.\n\nString module specs allow nested paths:\n\n```text\nInvoke report from Codex "campaign/Mission"\n```\n\n## Cache\n\nEach resolved module path is evaluated at most once per interpreter. Repeated imports reuse the same exported values. Circular imports fail with `ModuleLoadError`.\n\n## Standard library\n\nThe first bundled Codex is `Core.wp40k`, containing `identity` and `clamp`. It is loaded through exactly the same parser/runtime abstraction as user Codices.\n\n## Python API\n\n```python\nInterpreter(module_paths=[Path("modules")])\n```\n\nThe order of `module_paths` is significant and deterministic.\n''',
    encoding="utf-8",
)

p = Path("docs/roadmap.md")
text = p.read_text(encoding="utf-8").replace(
    "## v1.5 — Codex Modules\n", "## v1.5 — Codex Modules ✅\n", 1
)
p.write_text(text, encoding="utf-8")

p = Path("CHANGELOG.md")
text = p.read_text(encoding="utf-8")
marker = "# Changelog\n\nAll notable changes to WarPy40K are recorded here.\n\n"
entry = '''## 1.5.0 — 2026-09-16\n\n### Added\n\n- `Invoke name from Codex Module` explicit imports.\n- `Codex Export name` explicit module exports.\n- module-local execution scopes and lexical closure preservation for exported functions.\n- deterministic relative/search-path/stdlib resolution for `.wp40k` Codices.\n- per-interpreter module cache and circular-import diagnostics.\n- bundled `Core` standard-library Codex using the same module abstraction.\n- safe rejection of absolute paths, parent traversal, arbitrary extensions, and Python imports.\n\n'''
if entry not in text:
    p.write_text(text.replace(marker, marker + entry, 1), encoding="utf-8")

p = Path("docs/index.md")
text = p.read_text(encoding="utf-8")
if "codex_modules.md" not in text:
    text += "\n- [Codex Modules](codex_modules.md) — explicit modules, exports, deterministic resolution, and caching.\n"
p.write_text(text, encoding="utf-8")
