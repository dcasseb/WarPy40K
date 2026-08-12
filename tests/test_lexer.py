"""
Tests for the WarPy40K lexer.
"""

import pytest

from warpy40k.lexer import Lexer
from warpy40k.tokens import TokenType


class TestLexer:
    """Test cases for the lexer."""

    def test_integer_token(self):
        """Test integer tokenization."""
        lexer = Lexer("42")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.INTEGER
        assert tokens[0].value == "42"
        assert tokens[1].type == TokenType.EOF

    def test_float_token(self):
        """Test float tokenization."""
        lexer = Lexer("3.14")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.FLOAT
        assert tokens[0].value == "3.14"

    def test_string_token(self):
        """Test string tokenization."""
        lexer = Lexer('"hello"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello"

    def test_identifier_token(self):
        """Test identifier tokenization."""
        lexer = Lexer("myVar")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "myVar"

    def test_operators(self):
        """Test operator tokenization."""
        lexer = Lexer("+ - * / ^")
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.POWER,
            TokenType.EOF,
        ]
        for i, expected in enumerate(expected_types):
            assert tokens[i].type == expected

    def test_comparison_operators(self):
        """Test comparison operator tokenization."""
        lexer = Lexer("== != > < >= <=")
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.EQ,
            TokenType.NEQ,
            TokenType.GT,
            TokenType.LT,
            TokenType.GTE,
            TokenType.LTE,
            TokenType.EOF,
        ]
        for i, expected in enumerate(expected_types):
            assert tokens[i].type == expected

    def test_logical_operators(self):
        """Test logical operator tokenization."""
        lexer = Lexer("AND OR NOT && || !")
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.AND,
            TokenType.OR,
            TokenType.NOT,
            TokenType.AND,
            TokenType.OR,
            TokenType.NOT,
            TokenType.EOF,
        ]
        for i, expected in enumerate(expected_types):
            assert tokens[i].type == expected

    def test_punctuation(self):
        """Test punctuation tokenization in source order."""
        lexer = Lexer("(){};,:=")
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.LPAREN,
            TokenType.RPAREN,
            TokenType.LBRACE,
            TokenType.RBRACE,
            TokenType.SEMICOLON,
            TokenType.COMMA,
            TokenType.COLON,
            TokenType.ASSIGN,
            TokenType.EOF,
        ]
        for i, expected in enumerate(expected_types):
            assert tokens[i].type == expected

    def test_whitespace_ignored(self):
        """Test that whitespace is ignored."""
        lexer = Lexer("  42  ")
        tokens = lexer.tokenize()
        assert len(tokens) == 2
        assert tokens[0].type == TokenType.INTEGER
        assert tokens[1].type == TokenType.EOF

    def test_comments_ignored(self):
        """Test that comments, like whitespace, are omitted from parser tokens."""
        lexer = Lexer("42 # This is a comment")
        tokens = lexer.tokenize()
        assert len(tokens) == 2
        assert tokens[0].type == TokenType.INTEGER
        assert tokens[0].value == "42"
        assert tokens[1].type == TokenType.EOF

    def test_warpy_keywords(self):
        """Test Warhammer 40K keyword tokenization."""
        keywords = [
            ("Inquisition", TokenType.INQUISITION),
            ("Emperor", TokenType.EMPEROR),
            ("Chaos", TokenType.CHAOS),
            ("Xenos", TokenType.XENOS),
            ("Heretic", TokenType.HERETIC),
            ("Purge", TokenType.PURGE),
            ("Exterminatus", TokenType.EXTERMINATUS),
            ("Bless", TokenType.BLESS),
            ("Curse", TokenType.CURSE),
            ("Faith", TokenType.FAITH),
            ("Warp", TokenType.WARP),
        ]

        for keyword, token_type in keywords:
            lexer = Lexer(keyword)
            tokens = lexer.tokenize()
            assert tokens[0].type == token_type
            assert tokens[0].value == keyword

    def test_complex_expression(self):
        """Test tokenization of a complex expression."""
        lexer = Lexer("Inquisition Emperor + Chaos 42")
        tokens = lexer.tokenize()
        expected_types = [
            TokenType.INQUISITION,
            TokenType.EMPEROR,
            TokenType.PLUS,
            TokenType.CHAOS,
            TokenType.INTEGER,
            TokenType.EOF,
        ]
        for i, expected in enumerate(expected_types):
            assert tokens[i].type == expected

    def test_line_and_column_tracking(self):
        """Test line and column tracking."""
        lexer = Lexer("42\n100")
        tokens = lexer.tokenize()
        assert tokens[0].line == 1
        assert tokens[0].column == 1
        assert tokens[1].line == 2
        assert tokens[1].column == 1

    def test_empty_input(self):
        """Test empty input."""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_unknown_character(self):
        """Test unknown character raises error."""
        lexer = Lexer("42 @ 100")
        with pytest.raises(SyntaxError):
            lexer.tokenize()
