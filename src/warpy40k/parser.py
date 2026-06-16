"""
Parser for the WarPy40K language.

Converts tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional, Union

from .tokens import Token, TokenType
from .ast import (
    ASTNode, Program, LiteralNode, IdentifierNode, BinaryOpNode, 
    UnaryOpNode, VariableDeclarationNode, VariableAssignmentNode,
    FunctionCallNode, IfStatementNode, WhileLoopNode, BlockNode,
    ReturnStatementNode, InquisitionExprNode, EmperorExprNode,
    ChaosExprNode, PurgeExprNode, ExterminatusExprNode,
    BlessExprNode, CurseExprNode
)


class Parser:
    """
    Recursive descent parser for WarPy40K language.
    """
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize the parser with tokens.
        
        Args:
            tokens: List of tokens from the lexer
        """
        self.tokens = tokens
        self.position = 0
        self.current_token: Optional[Token] = None
        self._advance()
    
    def _advance(self) -> None:
        """Advance to the next token."""
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
            self.position += 1
        else:
            self.current_token = None
    
    def _peek(self) -> Optional[Token]:
        """Peek at the next token without consuming it."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    def _expect(self, token_type: TokenType, message: str = "") -> Token:
        """
        Expect a specific token type.
        
        Args:
            token_type: The expected token type
            message: Custom error message
            
        Returns:
            The current token
            
        Raises:
            SyntaxError: If the current token doesn't match the expected type
        """
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self._advance()
            return token
        
        expected = token_type.name
        got = self.current_token.type.name if self.current_token else "EOF"
        error_msg = message or f"Expected {expected}, got {got}"
        
        line = self.current_token.line if self.current_token else "unknown"
        column = self.current_token.column if self.current_token else "unknown"
        
        raise SyntaxError(f"{error_msg} at line {line}, column {column}")
    
    def parse(self) -> Program:
        """
        Parse the entire token stream into a Program AST node.
        
        Returns:
            The root Program node
        """
        statements: List[ASTNode] = []
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            statement = self._parse_statement()
            if statement:
                statements.append(statement)
        
        return Program(statements)
    
    def _parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement."""
        token = self.current_token
        
        if not token:
            return None
        
        # Handle if statements
        if token.type == TokenType.IDENTIFIER and token.value.lower() == 'if':
            return self._parse_if_statement()
        
        # Handle while loops (commented out for now - needs more work)
        # if token.type == TokenType.IDENTIFIER and token.value.lower() == 'while':
        #     return self._parse_while_statement()
        
        # Handle WarPy40K specific expressions
        if token.type == TokenType.INQUISITION:
            return self._parse_inquisition_expr()
        elif token.type == TokenType.EMPEROR:
            return self._parse_emperor_expr()
        elif token.type == TokenType.CHAOS:
            return self._parse_chaos_expr()
        elif token.type == TokenType.PURGE:
            return self._parse_purge_expr()
        elif token.type == TokenType.EXTERMINATUS:
            return self._parse_exterminatus_expr()
        elif token.type == TokenType.BLESS:
            return self._parse_bless_expr()
        elif token.type == TokenType.CURSE:
            return self._parse_curse_expr()
        
        # Handle variable declaration/assignment
        if token.type == TokenType.IDENTIFIER:
            # Check if it's a variable declaration (var x = 5) or assignment (x = 5)
            # For now, we'll treat all as expressions
            return self._parse_expression_statement()
        
        # Handle other statement types
        if token.type == TokenType.LBRACE:
            return self._parse_block()
        
        # Default to expression statement
        return self._parse_expression_statement()
    
    def _parse_if_statement(self) -> IfStatementNode:
        """Parse an if statement: if condition then_branch else else_branch"""
        # Consume 'if' token
        self._advance()
        
        # Parse condition
        condition = self._parse_expression()
        
        # Parse then branch
        then_branch = self._parse_statement()
        
        # Check for else
        else_branch = None
        if (self.current_token and 
            self.current_token.type == TokenType.IDENTIFIER and
            self.current_token.value.lower() == 'else'):
            self._advance()
            else_branch = self._parse_statement()
        
        return IfStatementNode(condition, then_branch, else_branch, 
                               self.current_token.line if self.current_token else 1,
                               self.current_token.column if self.current_token else 1)
    
    def _parse_while_statement(self) -> WhileLoopNode:
        """Parse a while statement: while condition body"""
        # Consume 'while' token
        self._advance()
        
        # Parse condition
        condition = self._parse_expression()
        
        # Parse body
        body = self._parse_statement()
        
        return WhileLoopNode(condition, body,
                           self.current_token.line if self.current_token else 1,
                           self.current_token.column if self.current_token else 1)
    
    def _parse_expression_statement(self) -> ASTNode:
        """Parse an expression statement."""
        expr = self._parse_expression()
        
        # Optional semicolon
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self._advance()
        
        return expr
    
    def _parse_expression(self) -> ASTNode:
        """Parse an expression."""
        return self._parse_logical_or()
    
    def _parse_logical_or(self) -> ASTNode:
        """Parse logical OR expressions."""
        left = self._parse_logical_and()
        
        while (self.current_token and 
               self.current_token.type in (TokenType.OR,)):
            op_token = self.current_token
            self._advance()
            right = self._parse_logical_and()
            left = BinaryOpNode(left, op_token.value, right, 
                               op_token.line, op_token.column)
        
        return left
    
    def _parse_logical_and(self) -> ASTNode:
        """Parse logical AND expressions."""
        left = self._parse_comparison()
        
        while (self.current_token and 
               self.current_token.type in (TokenType.AND,)):
            op_token = self.current_token
            self._advance()
            right = self._parse_comparison()
            left = BinaryOpNode(left, op_token.value, right, 
                               op_token.line, op_token.column)
        
        return left
    
    def _parse_comparison(self) -> ASTNode:
        """Parse comparison expressions."""
        left = self._parse_addition()
        
        while (self.current_token and 
               self.current_token.type in (TokenType.EQ, TokenType.NEQ, 
                                           TokenType.GT, TokenType.LT, 
                                           TokenType.GTE, TokenType.LTE)):
            op_token = self.current_token
            self._advance()
            right = self._parse_addition()
            left = BinaryOpNode(left, op_token.value, right, 
                               op_token.line, op_token.column)
        
        return left
    
    def _parse_addition(self) -> ASTNode:
        """Parse addition and subtraction expressions."""
        left = self._parse_multiplication()
        
        while (self.current_token and 
               self.current_token.type in (TokenType.PLUS, TokenType.MINUS)):
            op_token = self.current_token
            self._advance()
            right = self._parse_multiplication()
            left = BinaryOpNode(left, op_token.value, right, 
                               op_token.line, op_token.column)
        
        return left
    
    def _parse_multiplication(self) -> ASTNode:
        """Parse multiplication, division, and power expressions."""
        left = self._parse_power()
        
        while (self.current_token and 
               self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE)):
            op_token = self.current_token
            self._advance()
            right = self._parse_power()
            left = BinaryOpNode(left, op_token.value, right, 
                               op_token.line, op_token.column)
        
        return left
    
    def _parse_power(self) -> ASTNode:
        """Parse power expressions (right-associative)."""
        left = self._parse_unary()
        
        while (self.current_token and 
               self.current_token.type == TokenType.POWER):
            op_token = self.current_token
            self._advance()
            right = self._parse_power()  # Right-associative
            left = BinaryOpNode(left, op_token.value, right, 
                               op_token.line, op_token.column)
        
        return left
    
    def _parse_unary(self) -> ASTNode:
        """Parse unary expressions."""
        if (self.current_token and 
            self.current_token.type in (TokenType.MINUS, TokenType.NOT)):
            op_token = self.current_token
            self._advance()
            operand = self._parse_unary()
            return UnaryOpNode(op_token.value, operand, 
                              op_token.line, op_token.column)
        
        return self._parse_primary()
    
    def _parse_primary(self) -> ASTNode:
        """Parse primary expressions (literals, identifiers, parentheses, etc.)."""
        token = self.current_token
        
        if not token:
            raise SyntaxError("Unexpected end of input")
        
        # Handle literals
        if token.type == TokenType.INTEGER:
            self._advance()
            return LiteralNode(int(token.value), token.line, token.column)
        
        if token.type == TokenType.FLOAT:
            self._advance()
            return LiteralNode(float(token.value), token.line, token.column)
        
        if token.type == TokenType.STRING:
            self._advance()
            return LiteralNode(token.value, token.line, token.column)
        
        if token.type == TokenType.BOOLEAN:
            self._advance()
            return LiteralNode(token.value == 'True', token.line, token.column)
        
        # Handle identifiers
        if token.type == TokenType.IDENTIFIER:
            return self._parse_identifier_or_call()
        
        # Handle parentheses
        if token.type == TokenType.LPAREN:
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "Expected closing parenthesis")
            return expr
        
        # Handle WarPy40K keywords as primary expressions
        if token.type in (TokenType.INQUISITION, TokenType.EMPEROR, TokenType.CHAOS,
                          TokenType.PURGE, TokenType.EXTERMINATUS, TokenType.BLESS,
                          TokenType.CURSE):
            return self._parse_warpy_expr()
        
        raise SyntaxError(f"Unexpected token: {token.type.name} at line {token.line}, column {token.column}")
    
    def _parse_identifier_or_call(self) -> ASTNode:
        """Parse an identifier or function call."""
        token = self.current_token
        if token.type != TokenType.IDENTIFIER:
            raise SyntaxError(f"Expected identifier, got {token.type.name}")
        
        name = token.value
        line = token.line
        column = token.column
        self._advance()
        
        # Check for function call
        if self.current_token and self.current_token.type == TokenType.LPAREN:
            return self._parse_function_call(name, line, column)
        
        # Check for assignment
        if self.current_token and self.current_token.type == TokenType.ASSIGN:
            self._advance()
            value = self._parse_expression()
            return VariableAssignmentNode(name, value, line, column)
        
        return IdentifierNode(name, line, column)
    
    def _parse_function_call(self, name: str, line: int, column: int) -> FunctionCallNode:
        """Parse a function call."""
        self._expect(TokenType.LPAREN, "Expected '(' after function name")
        
        arguments: List[ASTNode] = []
        
        if self.current_token and self.current_token.type != TokenType.RPAREN:
            arguments.append(self._parse_expression())
            
            while (self.current_token and 
                   self.current_token.type == TokenType.COMMA):
                self._advance()
                arguments.append(self._parse_expression())
        
        self._expect(TokenType.RPAREN, "Expected closing parenthesis")
        
        return FunctionCallNode(name, arguments, line, column)
    
    def _parse_block(self) -> BlockNode:
        """Parse a block of statements."""
        line = self.current_token.line if self.current_token else 1
        column = self.current_token.column if self.current_token else 1
        
        self._expect(TokenType.LBRACE, "Expected '{'")
        
        statements: List[ASTNode] = []
        
        while (self.current_token and 
               self.current_token.type != TokenType.RBRACE and 
               self.current_token.type != TokenType.EOF):
            statement = self._parse_statement()
            if statement:
                statements.append(statement)
        
        self._expect(TokenType.RBRACE, "Expected '}'")
        
        return BlockNode(statements, line, column)
    
    def _parse_warpy_expr(self) -> ASTNode:
        """Parse WarPy40K specific expressions."""
        token = self.current_token
        
        if token.type == TokenType.INQUISITION:
            return self._parse_inquisition_expr()
        elif token.type == TokenType.EMPEROR:
            return self._parse_emperor_expr()
        elif token.type == TokenType.CHAOS:
            return self._parse_chaos_expr()
        elif token.type == TokenType.PURGE:
            return self._parse_purge_expr()
        elif token.type == TokenType.EXTERMINATUS:
            return self._parse_exterminatus_expr()
        elif token.type == TokenType.BLESS:
            return self._parse_bless_expr()
        elif token.type == TokenType.CURSE:
            return self._parse_curse_expr()
        
        raise SyntaxError(f"Unknown WarPy40K expression: {token.type.name}")
    
    def _parse_inquisition_expr(self) -> InquisitionExprNode:
        """Parse Inquisition expression."""
        token = self.current_token
        self._advance()
        
        # Inquisition can have an optional target
        target = None
        if (self.current_token and 
            self.current_token.type not in (TokenType.SEMICOLON, TokenType.RBRACE, 
                                             TokenType.EOF, TokenType.COMMA)):
            target = self._parse_expression()
        
        return InquisitionExprNode(target, token.line, token.column)
    
    def _parse_emperor_expr(self) -> EmperorExprNode:
        """Parse Emperor expression."""
        token = self.current_token
        self._advance()
        
        target = None
        if (self.current_token and 
            self.current_token.type not in (TokenType.SEMICOLON, TokenType.RBRACE, 
                                             TokenType.EOF, TokenType.COMMA)):
            target = self._parse_expression()
        
        return EmperorExprNode(target, token.line, token.column)
    
    def _parse_chaos_expr(self) -> ChaosExprNode:
        """Parse Chaos expression."""
        token = self.current_token
        self._advance()
        
        target = None
        if (self.current_token and 
            self.current_token.type not in (TokenType.SEMICOLON, TokenType.RBRACE, 
                                             TokenType.EOF, TokenType.COMMA)):
            target = self._parse_expression()
        
        return ChaosExprNode(target, token.line, token.column)
    
    def _parse_purge_expr(self) -> PurgeExprNode:
        """Parse Purge expression."""
        token = self.current_token
        self._advance()
        
        # Purge requires a target
        if not self.current_token or self.current_token.type in (TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
            raise SyntaxError(f"Purge expression requires a target at line {token.line}")
        
        target = self._parse_expression()
        return PurgeExprNode(target, token.line, token.column)
    
    def _parse_exterminatus_expr(self) -> ExterminatusExprNode:
        """Parse Exterminatus expression."""
        token = self.current_token
        self._advance()
        
        target = None
        if (self.current_token and 
            self.current_token.type not in (TokenType.SEMICOLON, TokenType.RBRACE, 
                                             TokenType.EOF, TokenType.COMMA)):
            target = self._parse_expression()
        
        return ExterminatusExprNode(target, token.line, token.column)
    
    def _parse_bless_expr(self) -> BlessExprNode:
        """Parse Bless expression."""
        token = self.current_token
        self._advance()
        
        # Bless requires a target
        if not self.current_token or self.current_token.type in (TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
            raise SyntaxError(f"Bless expression requires a target at line {token.line}")
        
        target = self._parse_expression()
        return BlessExprNode(target, token.line, token.column)
    
    def _parse_curse_expr(self) -> CurseExprNode:
        """Parse Curse expression."""
        token = self.current_token
        self._advance()
        
        # Curse requires a target
        if not self.current_token or self.current_token.type in (TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
            raise SyntaxError(f"Curse expression requires a target at line {token.line}")
        
        target = self._parse_expression()
        return CurseExprNode(target, token.line, token.column)
