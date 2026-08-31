"""
Abstract Syntax Tree (AST) nodes for WarPy40K language.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Tuple, Union


class NodeType(Enum):
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
    SQUAD_LITERAL = auto()
    DATASLATE_LITERAL = auto()
    INDEX_ACCESS = auto()
    FIELD_ACCESS = auto()

    INQUISITION_EXPR = auto()
    EMPEROR_EXPR = auto()
    CHAOS_EXPR = auto()
    PURGE_EXPR = auto()
    EXTERMINATUS_EXPR = auto()
    BLESS_EXPR = auto()
    CURSE_EXPR = auto()


@dataclass
class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    statements: List["ASTNode"] = field(default_factory=list)
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Program(statements={len(self.statements)})"


@dataclass
class LiteralNode(ASTNode):
    value: Union[int, float, str, bool]
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Literal({type(self.value).__name__}: {self.value})"


@dataclass
class IdentifierNode(ASTNode):
    name: str
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"Identifier({self.name})"


@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"BinaryOp({self.left} {self.operator} {self.right})"


@dataclass
class UnaryOpNode(ASTNode):
    operator: str
    operand: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"UnaryOp({self.operator}{self.operand})"


@dataclass
class VariableDeclarationNode(ASTNode):
    name: str
    value: Optional[ASTNode] = None
    line: int = 1
    column: int = 1


@dataclass
class VariableAssignmentNode(ASTNode):
    name: str
    value: ASTNode
    line: int = 1
    column: int = 1


@dataclass
class FunctionDefinitionNode(ASTNode):
    name: str
    parameters: List[str]
    body: ASTNode
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"FunctionDef({self.name}, params={len(self.parameters)})"


@dataclass
class FunctionCallNode(ASTNode):
    name: str
    arguments: List[ASTNode] = field(default_factory=list)
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"FunctionCall({self.name}, args={len(self.arguments)})"


@dataclass
class IfStatementNode(ASTNode):
    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None
    line: int = 1
    column: int = 1


@dataclass
class WhileLoopNode(ASTNode):
    condition: ASTNode
    body: ASTNode
    line: int = 1
    column: int = 1


@dataclass
class BlockNode(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)
    line: int = 1
    column: int = 1


@dataclass
class ReturnStatementNode(ASTNode):
    value: Optional[ASTNode] = None
    line: int = 1
    column: int = 1


@dataclass
class SquadLiteralNode(ASTNode):
    members: List[ASTNode] = field(default_factory=list)
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"SquadLiteral({len(self.members)} members)"


@dataclass
class DataslateLiteralNode(ASTNode):
    fields: List[Tuple[str, ASTNode]] = field(default_factory=list)
    line: int = 1
    column: int = 1

    def __repr__(self) -> str:
        return f"DataslateLiteral({len(self.fields)} fields)"


@dataclass
class IndexAccessNode(ASTNode):
    target: ASTNode
    index: ASTNode
    line: int = 1
    column: int = 1


@dataclass
class FieldAccessNode(ASTNode):
    target: ASTNode
    field_name: str
    line: int = 1
    column: int = 1


@dataclass
class InquisitionExprNode(ASTNode):
    target: Optional[ASTNode] = None
    line: int = 1
    column: int = 1


@dataclass
class EmperorExprNode(ASTNode):
    target: Optional[ASTNode] = None
    line: int = 1
    column: int = 1


@dataclass
class ChaosExprNode(ASTNode):
    target: Optional[ASTNode] = None
    line: int = 1
    column: int = 1


@dataclass
class PurgeExprNode(ASTNode):
    target: ASTNode
    line: int = 1
    column: int = 1


@dataclass
class ExterminatusExprNode(ASTNode):
    target: Optional[ASTNode] = None
    line: int = 1
    column: int = 1


@dataclass
class BlessExprNode(ASTNode):
    target: ASTNode
    line: int = 1
    column: int = 1


@dataclass
class CurseExprNode(ASTNode):
    target: ASTNode
    line: int = 1
    column: int = 1
