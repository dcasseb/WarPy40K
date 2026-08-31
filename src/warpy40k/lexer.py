"""
Lexer for the WarPy40K language.

Converts source code into tokens for parsing.
"""

from typing import List, Optional

from .tokens import Token, TokenType


class Lexer:
    """Lexical analyzer for WarPy40K language."""

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code."""
        while self.position < len(self.source):
            token = self.next_token()
            if token and token.type not in (TokenType.WHITESPACE, TokenType.COMMENT):
                self.tokens.append(token)

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def next_token(self) -> Optional[Token]:
        if self.position >= len(self.source):
            return None

        current_char = self.source[self.position]

        if current_char.isspace():
            return self._handle_whitespace()
        if current_char == "#":
            return self._handle_comment()
        if current_char == '"':
            return self._handle_string()
        if current_char.isdigit():
            return self._handle_number()
        if current_char.isalpha() or current_char == "_":
            return self._handle_identifier()
        return self._handle_operator(current_char)

    def _handle_whitespace(self) -> Token:
        start_line = self.line
        start_column = self.column
        start_position = self.position

        while self.position < len(self.source) and self.source[self.position].isspace():
            if self.source[self.position] == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1

        return Token(
            TokenType.WHITESPACE,
            self.source[start_position : self.position],
            start_line,
            start_column,
        )

    def _handle_comment(self) -> Token:
        start_line = self.line
        start_column = self.column
        start_position = self.position

        while self.position < len(self.source) and self.source[self.position] != "\n":
            self.position += 1
            self.column += 1

        return Token(
            TokenType.COMMENT,
            self.source[start_position : self.position],
            start_line,
            start_column,
        )

    def _handle_string(self) -> Token:
        start_line = self.line
        start_column = self.column
        self.position += 1
        self.column += 1

        string_value = ""
        while self.position < len(self.source) and self.source[self.position] != '"':
            if self.source[self.position] == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            string_value += self.source[self.position]
            self.position += 1

        if self.position >= len(self.source):
            raise SyntaxError(
                f"Unterminated string at line {start_line}, column {start_column}"
            )

        self.position += 1
        self.column += 1
        return Token(TokenType.STRING, string_value, start_line, start_column)

    def _handle_number(self) -> Token:
        start_line = self.line
        start_column = self.column
        has_decimal = False
        number_str = ""

        while self.position < len(self.source) and (
            self.source[self.position].isdigit() or self.source[self.position] == "."
        ):
            if self.source[self.position] == ".":
                if has_decimal:
                    break
                has_decimal = True
            number_str += self.source[self.position]
            self.position += 1
            self.column += 1

        token_type = TokenType.FLOAT if has_decimal else TokenType.INTEGER
        return Token(token_type, number_str, start_line, start_column)

    def _handle_identifier(self) -> Token:
        start_line = self.line
        start_column = self.column
        identifier = ""

        while self.position < len(self.source) and (
            self.source[self.position].isalnum() or self.source[self.position] == "_"
        ):
            identifier += self.source[self.position]
            self.position += 1
            self.column += 1

        if identifier == "True":
            return Token(TokenType.BOOLEAN, "True", start_line, start_column)
        if identifier == "False":
            return Token(TokenType.BOOLEAN, "False", start_line, start_column)

        keyword_map = {
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "def": TokenType.DEF,
            "return": TokenType.RETURN,
            "Squad": TokenType.SQUAD,
            "Dataslate": TokenType.DATASLATE,
            "Inquisition": TokenType.INQUISITION,
            "Emperor": TokenType.EMPEROR,
            "Chaos": TokenType.CHAOS,
            "Xenos": TokenType.XENOS,
            "Heretic": TokenType.HERETIC,
            "Purge": TokenType.PURGE,
            "Exterminatus": TokenType.EXTERMINATUS,
            "Bless": TokenType.BLESS,
            "Curse": TokenType.CURSE,
            "Faith": TokenType.FAITH,
            "Warp": TokenType.WARP,
            "AND": TokenType.AND,
            "OR": TokenType.OR,
            "NOT": TokenType.NOT,
        }

        return Token(
            keyword_map.get(identifier, TokenType.IDENTIFIER),
            identifier,
            start_line,
            start_column,
        )

    def _handle_operator(self, current_char: str) -> Token:
        start_line = self.line
        start_column = self.column

        two_char_ops = {
            "==": TokenType.EQ,
            "!=": TokenType.NEQ,
            ">=": TokenType.GTE,
            "<=": TokenType.LTE,
            "&&": TokenType.AND,
            "||": TokenType.OR,
        }

        if (
            self.position + 1 < len(self.source)
            and self.source[self.position : self.position + 2] in two_char_ops
        ):
            op = self.source[self.position : self.position + 2]
            self.position += 2
            self.column += 2
            return Token(two_char_ops[op], op, start_line, start_column)

        single_char_ops = {
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.MULTIPLY,
            "/": TokenType.DIVIDE,
            "^": TokenType.POWER,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            "{": TokenType.LBRACE,
            "}": TokenType.RBRACE,
            "[": TokenType.LBRACKET,
            "]": TokenType.RBRACKET,
            ",": TokenType.COMMA,
            ";": TokenType.SEMICOLON,
            ":": TokenType.COLON,
            ".": TokenType.DOT,
            "=": TokenType.ASSIGN,
            ">": TokenType.GT,
            "<": TokenType.LT,
            "!": TokenType.NOT,
        }

        if current_char in single_char_ops:
            self.position += 1
            self.column += 1
            return Token(
                single_char_ops[current_char], current_char, start_line, start_column
            )

        raise SyntaxError(
            f"Unknown character: '{current_char}' at line {self.line}, "
            f"column {self.column}"
        )
