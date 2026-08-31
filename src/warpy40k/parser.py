"""
Recursive-descent parser for the WarPy40K language.
"""

from typing import List, Optional, Set

from .ast import (
    ASTNode,
    BinaryOpNode,
    BindingPatternNode,
    BlessExprNode,
    BlockNode,
    ChaosExprNode,
    CurseExprNode,
    DataslateLiteralNode,
    DataslatePatternNode,
    EmperorExprNode,
    ExterminatusExprNode,
    FieldAccessNode,
    FunctionCallNode,
    FunctionDefinitionNode,
    IdentifierNode,
    IfStatementNode,
    IndexAccessNode,
    InquisitionExprNode,
    LiteralNode,
    LiteralPatternNode,
    OrderCaseNode,
    OrderStatementNode,
    PatternNode,
    Program,
    PurgeExprNode,
    ReturnStatementNode,
    SquadLiteralNode,
    SquadPatternNode,
    UnaryOpNode,
    VariableAssignmentNode,
    WhileLoopNode,
    WildcardPatternNode,
)
from .tokens import Token, TokenType


class Parser:
    """Recursive-descent parser for WarPy40K."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token: Optional[Token] = None
        self._advance()

    def _advance(self) -> None:
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
            self.position += 1
        else:
            self.current_token = None

    def _expect(self, token_type: TokenType, message: str = "") -> Token:
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self._advance()
            return token
        expected = token_type.name
        got = self.current_token.type.name if self.current_token else "EOF"
        line = self.current_token.line if self.current_token else "unknown"
        column = self.current_token.column if self.current_token else "unknown"
        raise SyntaxError(
            (message or f"Expected {expected}, got {got}")
            + f" at line {line}, column {column}"
        )

    def parse(self) -> Program:
        statements: List[ASTNode] = []
        while self.current_token and self.current_token.type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                statements.append(statement)
        return Program(statements)

    def _parse_statement(self) -> Optional[ASTNode]:
        token = self.current_token
        if token is None:
            return None
        if token.type == TokenType.IF:
            return self._parse_if_statement()
        if token.type == TokenType.WHILE:
            return self._parse_while_statement()
        if token.type == TokenType.DEF:
            return self._parse_function_definition()
        if token.type == TokenType.RETURN:
            return self._parse_return_statement()
        if token.type == TokenType.ORDER:
            return self._parse_order_statement()
        if token.type == TokenType.LBRACE:
            return self._parse_block()
        return self._parse_expression_statement()

    def _parse_if_statement(self) -> IfStatementNode:
        token = self.current_token
        assert token is not None
        self._advance()
        condition = self._parse_expression()
        then_branch = self._parse_statement()
        if then_branch is None:
            raise SyntaxError(
                f"if requires a body at line {token.line}, column {token.column}"
            )
        else_branch = None
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self._advance()
            else_branch = self._parse_statement()
            if else_branch is None:
                raise SyntaxError(
                    f"else requires a body at line {token.line}, column {token.column}"
                )
        return IfStatementNode(
            condition, then_branch, else_branch, token.line, token.column
        )

    def _parse_while_statement(self) -> WhileLoopNode:
        token = self.current_token
        assert token is not None
        self._advance()
        condition = self._parse_expression()
        body = self._parse_statement()
        if body is None:
            raise SyntaxError(
                f"while requires a body at line {token.line}, column {token.column}"
            )
        return WhileLoopNode(condition, body, token.line, token.column)

    def _parse_function_definition(self) -> FunctionDefinitionNode:
        def_token = self.current_token
        assert def_token is not None
        self._advance()
        name_token = self._expect(
            TokenType.IDENTIFIER, "Expected function name after 'def'"
        )
        self._expect(TokenType.LPAREN, "Expected '(' after function name")
        parameters: List[str] = []
        if self.current_token and self.current_token.type != TokenType.RPAREN:
            while True:
                parameter = self._expect(
                    TokenType.IDENTIFIER, "Expected parameter name"
                )
                parameters.append(parameter.value)
                if (
                    self.current_token is None
                    or self.current_token.type != TokenType.COMMA
                ):
                    break
                self._advance()
        self._expect(TokenType.RPAREN, "Expected ')' after function parameters")
        if not self.current_token or self.current_token.type != TokenType.LBRACE:
            raise SyntaxError(
                f"Function '{name_token.value}' requires a block body "
                f"at line {def_token.line}, column {def_token.column}"
            )
        body = self._parse_block()
        return FunctionDefinitionNode(
            name_token.value, parameters, body, def_token.line, def_token.column
        )

    def _parse_return_statement(self) -> ReturnStatementNode:
        token = self.current_token
        assert token is not None
        self._advance()
        value = None
        if self.current_token and self.current_token.type not in (
            TokenType.SEMICOLON,
            TokenType.RBRACE,
            TokenType.EOF,
        ):
            value = self._parse_expression()
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self._advance()
        return ReturnStatementNode(value, token.line, token.column)

    def _parse_order_statement(self) -> OrderStatementNode:
        token = self._expect(TokenType.ORDER)
        target = self._parse_expression()
        self._expect(TokenType.LBRACE, "Expected '{' after Order target")
        cases: List[OrderCaseNode] = []
        otherwise: Optional[ASTNode] = None
        saw_otherwise = False

        while self.current_token and self.current_token.type != TokenType.RBRACE:
            if self.current_token.type == TokenType.WHEN:
                if saw_otherwise:
                    raise SyntaxError("When cannot appear after Otherwise")
                when = self.current_token
                self._advance()
                bindings: Set[str] = set()
                pattern = self._parse_pattern(bindings)
                guard = None
                if self.current_token and self.current_token.type == TokenType.IF:
                    self._advance()
                    guard = self._parse_expression()
                body = self._parse_statement()
                if body is None:
                    raise SyntaxError("When requires a body")
                cases.append(OrderCaseNode(pattern, body, guard, when.line, when.column))
                continue
            if self.current_token.type == TokenType.OTHERWISE:
                if saw_otherwise:
                    raise SyntaxError("Order may contain only one Otherwise")
                self._advance()
                otherwise = self._parse_statement()
                if otherwise is None:
                    raise SyntaxError("Otherwise requires a body")
                saw_otherwise = True
                continue
            raise SyntaxError(
                "Order body accepts only When and Otherwise clauses "
                f"at line {self.current_token.line}, column {self.current_token.column}"
            )

        self._expect(TokenType.RBRACE, "Expected '}' after Order clauses")
        if not cases and otherwise is None:
            raise SyntaxError("Order requires at least one When or Otherwise clause")
        return OrderStatementNode(target, cases, otherwise, token.line, token.column)

    def _parse_pattern(self, bindings: Set[str]) -> PatternNode:
        token = self.current_token
        if token is None:
            raise SyntaxError("Unexpected end of input in pattern")
        if token.type == TokenType.MINUS:
            self._advance()
            number = self.current_token
            if number is None or number.type not in (TokenType.INTEGER, TokenType.FLOAT):
                raise SyntaxError("Negative pattern requires a numeric literal")
            self._advance()
            value = -int(number.value) if number.type == TokenType.INTEGER else -float(number.value)
            return LiteralPatternNode(value, token.line, token.column)
        if token.type == TokenType.INTEGER:
            self._advance()
            return LiteralPatternNode(int(token.value), token.line, token.column)
        if token.type == TokenType.FLOAT:
            self._advance()
            return LiteralPatternNode(float(token.value), token.line, token.column)
        if token.type == TokenType.STRING:
            self._advance()
            return LiteralPatternNode(token.value, token.line, token.column)
        if token.type == TokenType.BOOLEAN:
            self._advance()
            return LiteralPatternNode(token.value == "True", token.line, token.column)
        if token.type == TokenType.IDENTIFIER:
            self._advance()
            if token.value == "_":
                return WildcardPatternNode(token.line, token.column)
            if token.value in bindings:
                raise SyntaxError(f"Duplicate pattern binding '{token.value}'")
            bindings.add(token.value)
            return BindingPatternNode(token.value, token.line, token.column)
        if token.type == TokenType.DATASLATE:
            return self._parse_dataslate_pattern(bindings)
        if token.type == TokenType.SQUAD:
            return self._parse_squad_pattern(bindings)
        raise SyntaxError(
            f"Invalid Order pattern token {token.type.name} "
            f"at line {token.line}, column {token.column}"
        )

    def _parse_dataslate_pattern(self, bindings: Set[str]) -> DataslatePatternNode:
        token = self._expect(TokenType.DATASLATE)
        self._expect(TokenType.LBRACE, "Expected '{' after Dataslate pattern")
        fields = []
        seen = set()
        if self.current_token and self.current_token.type != TokenType.RBRACE:
            while True:
                if self.current_token.type == TokenType.IDENTIFIER:
                    key = self.current_token.value
                    self._advance()
                elif self.current_token.type == TokenType.STRING:
                    key = self.current_token.value
                    self._advance()
                else:
                    raise SyntaxError(
                        "Dataslate pattern field must be an identifier or string"
                    )
                if key in seen:
                    raise SyntaxError(f"Duplicate Dataslate pattern field '{key}'")
                seen.add(key)
                self._expect(TokenType.COLON, "Expected ':' after pattern field")
                fields.append((key, self._parse_pattern(bindings)))
                if not self.current_token or self.current_token.type != TokenType.COMMA:
                    break
                self._advance()
        self._expect(TokenType.RBRACE, "Expected '}' after Dataslate pattern")
        return DataslatePatternNode(fields, token.line, token.column)

    def _parse_squad_pattern(self, bindings: Set[str]) -> SquadPatternNode:
        token = self._expect(TokenType.SQUAD)
        self._expect(TokenType.LBRACKET, "Expected '[' after Squad pattern")
        members: List[PatternNode] = []
        if self.current_token and self.current_token.type != TokenType.RBRACKET:
            members.append(self._parse_pattern(bindings))
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self._advance()
                members.append(self._parse_pattern(bindings))
        self._expect(TokenType.RBRACKET, "Expected ']' after Squad pattern")
        return SquadPatternNode(members, token.line, token.column)

    def _parse_expression_statement(self) -> ASTNode:
        expr = self._parse_expression()
        if self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self._advance()
        return expr

    def _parse_expression(self) -> ASTNode:
        return self._parse_logical_or()

    def _parse_logical_or(self) -> ASTNode:
        left = self._parse_logical_and()
        while self.current_token and self.current_token.type == TokenType.OR:
            token = self.current_token
            self._advance()
            left = BinaryOpNode(
                left, token.value, self._parse_logical_and(), token.line, token.column
            )
        return left

    def _parse_logical_and(self) -> ASTNode:
        left = self._parse_comparison()
        while self.current_token and self.current_token.type == TokenType.AND:
            token = self.current_token
            self._advance()
            left = BinaryOpNode(
                left, token.value, self._parse_comparison(), token.line, token.column
            )
        return left

    def _parse_comparison(self) -> ASTNode:
        left = self._parse_addition()
        while self.current_token and self.current_token.type in (
            TokenType.EQ,
            TokenType.NEQ,
            TokenType.GT,
            TokenType.LT,
            TokenType.GTE,
            TokenType.LTE,
        ):
            token = self.current_token
            self._advance()
            left = BinaryOpNode(
                left, token.value, self._parse_addition(), token.line, token.column
            )
        return left

    def _parse_addition(self) -> ASTNode:
        left = self._parse_multiplication()
        while self.current_token and self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            token = self.current_token
            self._advance()
            left = BinaryOpNode(
                left,
                token.value,
                self._parse_multiplication(),
                token.line,
                token.column,
            )
        return left

    def _parse_multiplication(self) -> ASTNode:
        left = self._parse_power()
        while self.current_token and self.current_token.type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            token = self.current_token
            self._advance()
            left = BinaryOpNode(
                left, token.value, self._parse_power(), token.line, token.column
            )
        return left

    def _parse_power(self) -> ASTNode:
        left = self._parse_unary()
        if self.current_token and self.current_token.type == TokenType.POWER:
            token = self.current_token
            self._advance()
            return BinaryOpNode(
                left, token.value, self._parse_power(), token.line, token.column
            )
        return left

    def _parse_unary(self) -> ASTNode:
        if self.current_token and self.current_token.type in (
            TokenType.MINUS,
            TokenType.NOT,
        ):
            token = self.current_token
            self._advance()
            return UnaryOpNode(
                token.value, self._parse_unary(), token.line, token.column
            )
        return self._parse_postfix()

    def _parse_postfix(self) -> ASTNode:
        expr = self._parse_primary()
        while self.current_token:
            if self.current_token.type == TokenType.LBRACKET:
                token = self.current_token
                self._advance()
                index = self._parse_expression()
                self._expect(TokenType.RBRACKET, "Expected ']' after index")
                expr = IndexAccessNode(expr, index, token.line, token.column)
                continue
            if self.current_token.type == TokenType.DOT:
                token = self.current_token
                self._advance()
                field = self._expect(
                    TokenType.IDENTIFIER, "Expected field name after '.'"
                )
                expr = FieldAccessNode(expr, field.value, token.line, token.column)
                continue
            break
        return expr

    def _parse_primary(self) -> ASTNode:
        token = self.current_token
        if token is None:
            raise SyntaxError("Unexpected end of input")
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
            return LiteralNode(token.value == "True", token.line, token.column)
        if token.type == TokenType.IDENTIFIER:
            return self._parse_identifier_or_call()
        if token.type == TokenType.SQUAD:
            return self._parse_squad_literal()
        if token.type == TokenType.DATASLATE:
            return self._parse_dataslate_literal()
        if token.type == TokenType.LPAREN:
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "Expected closing parenthesis")
            return expr
        if token.type in (
            TokenType.INQUISITION,
            TokenType.EMPEROR,
            TokenType.CHAOS,
            TokenType.PURGE,
            TokenType.EXTERMINATUS,
            TokenType.BLESS,
            TokenType.CURSE,
        ):
            return self._parse_warpy_expr()
        raise SyntaxError(
            f"Unexpected token: {token.type.name} "
            f"at line {token.line}, column {token.column}"
        )

    def _parse_identifier_or_call(self) -> ASTNode:
        token = self._expect(TokenType.IDENTIFIER)
        name = token.value
        if self.current_token and self.current_token.type == TokenType.LPAREN:
            return self._parse_function_call(name, token.line, token.column)
        if self.current_token and self.current_token.type == TokenType.ASSIGN:
            self._advance()
            return VariableAssignmentNode(
                name, self._parse_expression(), token.line, token.column
            )
        return IdentifierNode(name, token.line, token.column)

    def _parse_function_call(
        self, name: str, line: int, column: int
    ) -> FunctionCallNode:
        self._expect(TokenType.LPAREN, "Expected '(' after function name")
        arguments: List[ASTNode] = []
        if self.current_token and self.current_token.type != TokenType.RPAREN:
            arguments.append(self._parse_expression())
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self._advance()
                arguments.append(self._parse_expression())
        self._expect(TokenType.RPAREN, "Expected closing parenthesis")
        return FunctionCallNode(name, arguments, line, column)

    def _parse_squad_literal(self) -> SquadLiteralNode:
        token = self._expect(TokenType.SQUAD)
        self._expect(TokenType.LBRACKET, "Expected '[' after Squad")
        members: List[ASTNode] = []
        if self.current_token and self.current_token.type != TokenType.RBRACKET:
            members.append(self._parse_expression())
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self._advance()
                members.append(self._parse_expression())
        self._expect(TokenType.RBRACKET, "Expected ']' after Squad members")
        return SquadLiteralNode(members, token.line, token.column)

    def _parse_dataslate_literal(self) -> DataslateLiteralNode:
        token = self._expect(TokenType.DATASLATE)
        self._expect(TokenType.LBRACE, "Expected '{' after Dataslate")
        fields = []
        seen = set()
        if self.current_token and self.current_token.type != TokenType.RBRACE:
            while True:
                if self.current_token.type == TokenType.IDENTIFIER:
                    key = self.current_token.value
                    self._advance()
                elif self.current_token.type == TokenType.STRING:
                    key = self.current_token.value
                    self._advance()
                else:
                    raise SyntaxError(
                        "Dataslate field name must be an identifier or string"
                    )
                if key in seen:
                    raise SyntaxError(f"Duplicate Dataslate field '{key}'")
                seen.add(key)
                self._expect(TokenType.COLON, "Expected ':' after Dataslate field name")
                fields.append((key, self._parse_expression()))
                if not self.current_token or self.current_token.type != TokenType.COMMA:
                    break
                self._advance()
        self._expect(TokenType.RBRACE, "Expected '}' after Dataslate fields")
        return DataslateLiteralNode(fields, token.line, token.column)

    def _parse_block(self) -> BlockNode:
        token = self._expect(TokenType.LBRACE, "Expected '{'")
        statements: List[ASTNode] = []
        while self.current_token and self.current_token.type not in (
            TokenType.RBRACE,
            TokenType.EOF,
        ):
            statement = self._parse_statement()
            if statement is not None:
                statements.append(statement)
        self._expect(TokenType.RBRACE, "Expected '}'")
        return BlockNode(statements, token.line, token.column)

    def _parse_warpy_expr(self) -> ASTNode:
        token = self.current_token
        assert token is not None
        parsers = {
            TokenType.INQUISITION: self._parse_inquisition_expr,
            TokenType.EMPEROR: self._parse_emperor_expr,
            TokenType.CHAOS: self._parse_chaos_expr,
            TokenType.PURGE: self._parse_purge_expr,
            TokenType.EXTERMINATUS: self._parse_exterminatus_expr,
            TokenType.BLESS: self._parse_bless_expr,
            TokenType.CURSE: self._parse_curse_expr,
        }
        return parsers[token.type]()

    def _has_optional_target(self) -> bool:
        return bool(
            self.current_token
            and self.current_token.type
            in (
                TokenType.INTEGER,
                TokenType.FLOAT,
                TokenType.STRING,
                TokenType.BOOLEAN,
                TokenType.IDENTIFIER,
                TokenType.SQUAD,
                TokenType.DATASLATE,
                TokenType.LPAREN,
                TokenType.MINUS,
                TokenType.NOT,
                TokenType.INQUISITION,
                TokenType.EMPEROR,
                TokenType.CHAOS,
                TokenType.PURGE,
                TokenType.EXTERMINATUS,
                TokenType.BLESS,
                TokenType.CURSE,
            )
        )

    def _parse_inquisition_expr(self) -> InquisitionExprNode:
        token = self.current_token
        assert token is not None
        self._advance()
        return InquisitionExprNode(
            self._parse_unary() if self._has_optional_target() else None,
            token.line,
            token.column,
        )

    def _parse_emperor_expr(self) -> EmperorExprNode:
        token = self.current_token
        assert token is not None
        self._advance()
        return EmperorExprNode(
            self._parse_unary() if self._has_optional_target() else None,
            token.line,
            token.column,
        )

    def _parse_chaos_expr(self) -> ChaosExprNode:
        token = self.current_token
        assert token is not None
        self._advance()
        return ChaosExprNode(
            self._parse_unary() if self._has_optional_target() else None,
            token.line,
            token.column,
        )

    def _parse_purge_expr(self) -> PurgeExprNode:
        token = self.current_token
        assert token is not None
        self._advance()
        if not self._has_optional_target():
            raise SyntaxError(
                f"Purge expression requires a target at line {token.line}"
            )
        return PurgeExprNode(self._parse_unary(), token.line, token.column)

    def _parse_exterminatus_expr(self) -> ExterminatusExprNode:
        token = self.current_token
        assert token is not None
        self._advance()
        return ExterminatusExprNode(
            self._parse_unary() if self._has_optional_target() else None,
            token.line,
            token.column,
        )

    def _parse_bless_expr(self) -> BlessExprNode:
        token = self.current_token
        assert token is not None
        self._advance()
        if not self._has_optional_target():
            raise SyntaxError(
                f"Bless expression requires a target at line {token.line}"
            )
        return BlessExprNode(self._parse_unary(), token.line, token.column)

    def _parse_curse_expr(self) -> CurseExprNode:
        token = self.current_token
        assert token is not None
        self._advance()
        if not self._has_optional_target():
            raise SyntaxError(
                f"Curse expression requires a target at line {token.line}"
            )
        return CurseExprNode(self._parse_unary(), token.line, token.column)
