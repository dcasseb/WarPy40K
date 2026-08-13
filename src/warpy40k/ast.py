"""
Abstract Syntax Tree (AST) nodes for WarPy40K language.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Union


class NodeType(Enum):
    """Types of AST nodes."""

    PROGRAM = auto()
    EXPRESSION = auto()
    BINARY_OP = auto()
    UNARY_OP = auto()
    LITERAL = auto()
    IDENTIFIER = auto()
    VARIABLE_DECLARATION = auto()
    VARIABLE_ASSIGNMENT = auto()
    FUNCTION_DEFINITION = auto()
    FUNCTION_CALL = auto()
    IF_STATEMENT = auto()
    WHILE_LOOP = auto()
    BLOCK = auto()
    RETURN_STATEMENT = auto()

    # WarPy40K specific
    INQUISITION_EXPR = auto()
    EMPEROR_EXPR = auto()
    CHAOS_EXPR = auto()
    PURGE_EXPR = auto()
    EXTERMINATUS_EXPR = auto()
    BLESS_EXPR = auto()
    CURSE_EXPR = auto()


@dataclass
class ASTNode:
    """Base class for all AST nodes."""

    pass


@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""

    statements: List["ASTNode"] = field(default_factory=list)
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Program(statements={len(self.statements)})"


@dataclass
class LiteralNode(ASTNode):
    """Represents a literal value (number, string, boolean)."""

    value: Union[int, float, str, bool]
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Literal({type(self.value).__name__}: {self.value})"


@dataclass
class IdentifierNode(ASTNode):
    """Represents an identifier (variable name, function name)."""

    name: str
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Identifier({self.name})"


@dataclass
class BinaryOpNode(ASTNode):
    """Represents a binary operation (e.g., 1 + 2)."""

    left: ASTNode
    operator: str
    right: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"BinaryOp({self.left} {self.operator} {self.right})"


@dataclass
class UnaryOpNode(ASTNode):
    """Represents a unary operation (e.g., -5, NOT true)."""

    operator: str
    operand: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"UnaryOp({self.operator}{self.operand})"


@dataclass
class VariableDeclarationNode(ASTNode):
    """Represents a variable declaration."""

    name: str
    value: Optional[ASTNode] = None
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"VarDecl({self.name} = {self.value})"


@dataclass
class VariableAssignmentNode(ASTNode):
    """Represents a variable assignment."""

    name: str
    value: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"VarAssign({self.name} = {self.value})"


@dataclass
class FunctionDefinitionNode(ASTNode):
    """Represents a user-defined function."""

    name: str
    parameters: List[str]
    body: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"FunctionDef({self.name}, params={len(self.parameters)})"


@dataclass
class FunctionCallNode(ASTNode):
    """Represents a function call."""

    name: str
    arguments: List[ASTNode] = field(default_factory=list)
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"FunctionCall({self.name}, args={len(self.arguments)})"


@dataclass
class IfStatementNode(ASTNode):
    """Represents an if statement."""

    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"If({self.condition})"


@dataclass
class WhileLoopNode(ASTNode):
    """Represents a while loop."""

    condition: ASTNode
    body: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"While({self.condition})"


@dataclass
class BlockNode(ASTNode):
    """Represents a block of statements."""

    statements: List[ASTNode] = field(default_factory=list)
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Block({len(self.statements)} statements)"


@dataclass
class ReturnStatementNode(ASTNode):
    """Represents a return statement."""

    value: Optional[ASTNode] = None
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Return({self.value})"


# WarPy40K Specific Nodes


@dataclass
class InquisitionExprNode(ASTNode):
    """Represents an Inquisition expression - evaluates to truth/faith value."""

    target: Optional[ASTNode] = None
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Inquisition({self.target})"


@dataclass
class EmperorExprNode(ASTNode):
    """Represents an Emperor expression - divine protection/blessing."""

    target: Optional[ASTNode] = None
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Emperor({self.target})"


@dataclass
class ChaosExprNode(ASTNode):
    """Represents a Chaos expression - corruption/uncertainty."""

    target: Optional[ASTNode] = None
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Chaos({self.target})"


@dataclass
class PurgeExprNode(ASTNode):
    """Represents a Purge expression - destruction/removal."""

    target: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Purge({self.target})"


@dataclass
class ExterminatusExprNode(ASTNode):
    """Represents an Exterminatus expression - total annihilation."""

    target: Optional[ASTNode] = None
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Exterminatus({self.target})"


@dataclass
class BlessExprNode(ASTNode):
    """Represents a Bless expression - positive modification."""

    target: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Bless({self.target})"


@dataclass
class CurseExprNode(ASTNode):
    """Represents a Curse expression - negative modification."""

    target: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Curse({self.target})"
