"""
Token definitions for the WarPy40K language.
"""

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    """Token types for WarPy40K language."""

    # Basic tokens
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto()

    # Control-flow and function keywords
    IF = auto()  # 'if'
    ELSE = auto()  # 'else'
    WHILE = auto()  # 'while'
    DEF = auto()  # 'def'
    RETURN = auto()  # 'return'

    # Native WarPy40K data constructors
    SQUAD = auto()  # 'Squad'
    DATASLATE = auto()  # 'Dataslate'

    # Warhammer 40K specific keywords
    INQUISITION = auto()  # 'Inquisition'
    EMPEROR = auto()  # 'Emperor'
    CHAOS = auto()  # 'Chaos'
    XENOS = auto()  # 'Xenos'
    HERETIC = auto()  # 'Heretic'
    PURGE = auto()  # 'Purge'
    EXTERMINATUS = auto()  # 'Exterminatus'
    BLESS = auto()  # 'Bless'
    CURSE = auto()  # 'Curse'
    FAITH = auto()  # 'Faith'
    WARP = auto()  # 'Warp'

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()

    # Comparison
    EQ = auto()
    NEQ = auto()
    GT = auto()
    LT = auto()
    GTE = auto()
    LTE = auto()

    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()

    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    DOT = auto()

    # Assignment
    ASSIGN = auto()

    # End of file
    EOF = auto()

    # Whitespace (ignored)
    WHITESPACE = auto()

    # Comments
    COMMENT = auto()


@dataclass
class Token:
    """Represents a token in the source code."""

    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        return (
            f"Token({self.type.name}, '{self.value}', "
            f"line={self.line}, col={self.column})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return (
            self.type == other.type
            and self.value == other.value
            and self.line == other.line
            and self.column == other.column
        )
