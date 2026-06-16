"""
Lexer for the WarPy40K language.

Converts source code into tokens for parsing.
"""

import re
from typing import List, Optional

from .tokens import Token, TokenType


class Lexer:
    """
    Lexical analyzer for WarPy40K language.
    
    Converts source code string into a list of tokens.
    """
    
    def __init__(self, source: str):
        """
        Initialize the lexer with source code.
        
        Args:
            source: The source code to tokenize
        """
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code.
        
        Returns:
            List of tokens
        """
        while self.position < len(self.source):
            token = self.next_token()
            if token and token.type not in (TokenType.WHITESPACE, TokenType.COMMENT):
                self.tokens.append(token)
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def next_token(self) -> Optional[Token]:
        """
        Get the next token from the source.
        
        Returns:
            The next token, or None if at end of source
        """
        if self.position >= len(self.source):
            return None
        
        current_char = self.source[self.position]
        
        # Skip whitespace
        if current_char.isspace():
            return self._handle_whitespace()
        
        # Handle comments
        if current_char == '#':
            return self._handle_comment()
        
        # Handle strings
        if current_char == '"':
            return self._handle_string()
        
        # Handle numbers
        if current_char.isdigit():
            return self._handle_number()
        
        # Handle identifiers and keywords
        if current_char.isalpha() or current_char == '_':
            return self._handle_identifier()
        
        # Handle operators and punctuation
        return self._handle_operator(current_char)
    
    def _handle_whitespace(self) -> Token:
        """Handle whitespace characters."""
        start_line = self.line
        start_column = self.column
        
        while (self.position < len(self.source) and 
               self.source[self.position].isspace()):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
        
        return Token(TokenType.WHITESPACE, self.source[start_column-1:self.position], 
                     start_line, start_column)
    
    def _handle_comment(self) -> Token:
        """Handle single-line comments."""
        start_line = self.line
        start_column = self.column
        
        while (self.position < len(self.source) and 
               self.source[self.position] != '\n'):
            self.position += 1
            self.column += 1
        
        return Token(TokenType.COMMENT, self.source[start_column-1:self.position], 
                     start_line, start_column)
    
    def _handle_string(self) -> Token:
        """Handle string literals."""
        start_line = self.line
        start_column = self.column
        self.position += 1  # Skip opening quote
        self.column += 1
        
        string_value = ""
        while (self.position < len(self.source) and 
               self.source[self.position] != '"'):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            string_value += self.source[self.position]
            self.position += 1
        
        if self.position < len(self.source):
            self.position += 1  # Skip closing quote
            self.column += 1
        
        return Token(TokenType.STRING, string_value, start_line, start_column)
    
    def _handle_number(self) -> Token:
        """Handle numeric literals (integers and floats)."""
        start_line = self.line
        start_column = self.column
        
        has_decimal = False
        number_str = ""
        
        while (self.position < len(self.source) and 
               (self.source[self.position].isdigit() or 
                self.source[self.position] == '.')):
            if self.source[self.position] == '.':
                if has_decimal:
                    break  # Only one decimal point allowed
                has_decimal = True
            number_str += self.source[self.position]
            self.position += 1
            self.column += 1
        
        if has_decimal:
            return Token(TokenType.FLOAT, number_str, start_line, start_column)
        else:
            return Token(TokenType.INTEGER, number_str, start_line, start_column)
    
    def _handle_identifier(self) -> Token:
        """Handle identifiers and keywords."""
        start_line = self.line
        start_column = self.column
        
        identifier = ""
        while (self.position < len(self.source) and 
               (self.source[self.position].isalnum() or 
                self.source[self.position] == '_')):
            identifier += self.source[self.position]
            self.position += 1
            self.column += 1
        
        # Check if it's a boolean
        if identifier == 'True':
            return Token(TokenType.BOOLEAN, 'True', start_line, start_column)
        elif identifier == 'False':
            return Token(TokenType.BOOLEAN, 'False', start_line, start_column)
        
        # Check if it's a keyword
        keyword_map = {
            'Inquisition': TokenType.INQUISITION,
            'Emperor': TokenType.EMPEROR,
            'Chaos': TokenType.CHAOS,
            'Xenos': TokenType.XENOS,
            'Heretic': TokenType.HERETIC,
            'Purge': TokenType.PURGE,
            'Exterminatus': TokenType.EXTERMINATUS,
            'Bless': TokenType.BLESS,
            'Curse': TokenType.CURSE,
            'Faith': TokenType.FAITH,
            'Warp': TokenType.WARP,
            'AND': TokenType.AND,
            'OR': TokenType.OR,
            'NOT': TokenType.NOT,
        }
        
        token_type = keyword_map.get(identifier, TokenType.IDENTIFIER)
        return Token(token_type, identifier, start_line, start_column)
    
    def _handle_operator(self, current_char: str) -> Token:
        """Handle operators and punctuation."""
        start_line = self.line
        start_column = self.column
        
        # Two-character operators
        two_char_ops = {
            '==': TokenType.EQ,
            '!=': TokenType.NEQ,
            '>=': TokenType.GTE,
            '<=': TokenType.LTE,
            '&&': TokenType.AND,
            '||': TokenType.OR,
        }
        
        if (self.position + 1 < len(self.source) and 
            self.source[self.position:self.position+2] in two_char_ops):
            op = self.source[self.position:self.position+2]
            self.position += 2
            self.column += 2
            return Token(two_char_ops[op], op, start_line, start_column)
        
        # Single-character operators
        single_char_ops = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '^': TokenType.POWER,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ',': TokenType.COMMA,
            ';': TokenType.SEMICOLON,
            ':': TokenType.COLON,
            '=': TokenType.ASSIGN,
            '>': TokenType.GT,
            '<': TokenType.LT,
            '!': TokenType.NOT,
        }
        
        if current_char in single_char_ops:
            self.position += 1
            self.column += 1
            return Token(single_char_ops[current_char], current_char, 
                        start_line, start_column)
        
        # Unknown character
        raise SyntaxError(f"Unknown character: '{current_char}' at line {self.line}, column {self.column}")
        
        # Unknown character
        raise SyntaxError(f"Unknown character: '{current_char}' at line {self.line}, column {self.column}")
