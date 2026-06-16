"""
Interpreter for the WarPy40K language.

Executes the Abstract Syntax Tree (AST) and produces results.
"""

import random
from typing import Any, Dict, List, Optional, Union

from .ast import (
    ASTNode, Program, LiteralNode, IdentifierNode, BinaryOpNode, 
    UnaryOpNode, VariableDeclarationNode, VariableAssignmentNode,
    FunctionCallNode, IfStatementNode, WhileLoopNode, BlockNode,
    ReturnStatementNode, InquisitionExprNode, EmperorExprNode,
    ChaosExprNode, PurgeExprNode, ExterminatusExprNode,
    BlessExprNode, CurseExprNode
)


class Interpreter:
    """
    Interpreter for executing WarPy40K AST nodes.
    """
    
    def __init__(self):
        """Initialize the interpreter."""
        self.environment: Dict[str, Any] = {}
        self._init_builtins()
    
    def _init_builtins(self) -> None:
        """Initialize built-in functions and constants."""
        # Warhammer 40K themed constants
        self.environment['FAITH'] = 100  # Default faith value
        self.environment['CORRUPTION'] = 0  # Default corruption level
        self.environment['POPULATION'] = 1000000  # Default population
        
        # Built-in functions
        self.environment['print'] = self._builtin_print
        self.environment['random'] = self._builtin_random
        self.environment['abs'] = abs
        self.environment['min'] = min
        self.environment['max'] = max
        self.environment['pow'] = pow
    
    def _builtin_print(self, *args: Any) -> None:
        """Built-in print function."""
        print(*args)
        return None
    
    def _builtin_random(self) -> float:
        """Built-in random function."""
        return random.random()
    
    def execute(self, node: ASTNode) -> Any:
        """
        Execute an AST node and return the result.
        
        Args:
            node: The AST node to execute
            
        Returns:
            The result of the execution
        """
        # Use isinstance to determine the node type and dispatch
        if isinstance(node, Program):
            return self._execute_program(node)
        elif isinstance(node, LiteralNode):
            return self._execute_literal(node)
        elif isinstance(node, IdentifierNode):
            return self._execute_identifier(node)
        elif isinstance(node, BinaryOpNode):
            return self._execute_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self._execute_unary_op(node)
        elif isinstance(node, VariableDeclarationNode):
            return self._execute_variable_declaration(node)
        elif isinstance(node, VariableAssignmentNode):
            return self._execute_variable_assignment(node)
        elif isinstance(node, FunctionCallNode):
            return self._execute_function_call(node)
        elif isinstance(node, IfStatementNode):
            return self._execute_if_statement(node)
        elif isinstance(node, WhileLoopNode):
            return self._execute_while_loop(node)
        elif isinstance(node, BlockNode):
            return self._execute_block(node)
        elif isinstance(node, ReturnStatementNode):
            return self._execute_return_statement(node)
        elif isinstance(node, InquisitionExprNode):
            return self._execute_inquisition_expr(node)
        elif isinstance(node, EmperorExprNode):
            return self._execute_emperor_expr(node)
        elif isinstance(node, ChaosExprNode):
            return self._execute_chaos_expr(node)
        elif isinstance(node, PurgeExprNode):
            return self._execute_purge_expr(node)
        elif isinstance(node, ExterminatusExprNode):
            return self._execute_exterminatus_expr(node)
        elif isinstance(node, BlessExprNode):
            return self._execute_bless_expr(node)
        elif isinstance(node, CurseExprNode):
            return self._execute_curse_expr(node)
        else:
            raise RuntimeError(f"No execution method for node type: {type(node).__name__}")
    
    def _execute_program(self, node: Program) -> Any:
        """Execute a program (list of statements)."""
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result
    
    def _execute_literal(self, node: LiteralNode) -> Any:
        """Execute a literal node."""
        return node.value
    
    def _execute_identifier(self, node: IdentifierNode) -> Any:
        """Execute an identifier node (variable lookup)."""
        if node.name in self.environment:
            return self.environment[node.name]
        else:
            raise NameError(f"Name '{node.name}' is not defined")
    
    def _execute_binary_op(self, node: BinaryOpNode) -> Any:
        """Execute a binary operation."""
        left = self.execute(node.left)
        right = self.execute(node.right)
        operator = node.operator
        
        # Arithmetic operations
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        elif operator == '^':
            return left ** right
        
        # Comparison operations
        elif operator == '==':
            return left == right
        elif operator == '!=':
            return left != right
        elif operator == '>':
            return left > right
        elif operator == '<':
            return left < right
        elif operator == '>=':
            return left >= right
        elif operator == '<=':
            return left <= right
        
        # Logical operations
        elif operator == 'AND' or operator == '&&':
            return left and right
        elif operator == 'OR' or operator == '||':
            return left or right
        
        raise RuntimeError(f"Unknown operator: {operator}")
    
    def _execute_unary_op(self, node: UnaryOpNode) -> Any:
        """Execute a unary operation."""
        operand = self.execute(node.operand)
        operator = node.operator
        
        if operator == '-':
            return -operand
        elif operator == 'NOT' or operator == '!':
            return not operand
        
        raise RuntimeError(f"Unknown unary operator: {operator}")
    
    def _execute_variable_declaration(self, node: VariableDeclarationNode) -> Any:
        """Execute a variable declaration."""
        value = None
        if node.value:
            value = self.execute(node.value)
        
        self.environment[node.name] = value
        return value
    
    def _execute_variable_assignment(self, node: VariableAssignmentNode) -> Any:
        """Execute a variable assignment."""
        value = self.execute(node.value)
        self.environment[node.name] = value
        return value
    
    def _execute_function_call(self, node: FunctionCallNode) -> Any:
        """Execute a function call."""
        if node.name not in self.environment:
            raise NameError(f"Function '{node.name}' is not defined")
        
        func = self.environment[node.name]
        
        # Evaluate arguments
        args = [self.execute(arg) for arg in node.arguments]
        
        # Call the function
        if callable(func):
            return func(*args)
        else:
            raise TypeError(f"'{node.name}' is not callable")
    
    def _execute_if_statement(self, node: IfStatementNode) -> Any:
        """Execute an if statement."""
        condition = self.execute(node.condition)
        
        if condition:
            return self.execute(node.then_branch)
        elif node.else_branch:
            return self.execute(node.else_branch)
        
        return None
    
    def _execute_while_loop(self, node: WhileLoopNode) -> Any:
        """Execute a while loop."""
        result = None
        
        while True:
            condition = self.execute(node.condition)
            if not condition:
                break
            result = self.execute(node.body)
        
        return result
    
    def _execute_block(self, node: BlockNode) -> Any:
        """Execute a block of statements."""
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result
    
    def _execute_return_statement(self, node: ReturnStatementNode) -> Any:
        """Execute a return statement."""
        if node.value:
            return self.execute(node.value)
        return None
    
    # WarPy40K Specific Executions
    
    def _execute_inquisition_expr(self, node: InquisitionExprNode) -> Any:
        """
        Execute Inquisition expression.
        
        Inquisition represents investigation/judgment.
        If target is provided, evaluates its truthiness.
        If no target, returns a high faith value.
        """
        if node.target:
            target_value = self.execute(node.target)
            # Inquisition judges the target - returns boolean based on truthiness
            return bool(target_value)
        else:
            # Default: Inquisition brings faith and order
            return True
    
    def _execute_emperor_expr(self, node: EmperorExprNode) -> Any:
        """
        Execute Emperor expression.
        
        Emperor represents divine power and protection.
        If target is provided, blesses it (multiplies by faith factor).
        If no target, returns a high value representing divine power.
        """
        faith_factor = self.environment.get('FAITH', 100) / 100.0
        
        if node.target:
            target_value = self.execute(node.target)
            if isinstance(target_value, (int, float)):
                return target_value * faith_factor
            else:
                # For non-numeric values, just return the target
                return target_value
        else:
            # Emperor's divine power
            return 1000
    
    def _execute_chaos_expr(self, node: ChaosExprNode) -> Any:
        """
        Execute Chaos expression.
        
        Chaos represents corruption and uncertainty.
        If target is provided, corrupts it (adds randomness).
        If no target, returns a random value representing chaos.
        """
        corruption = self.environment.get('CORRUPTION', 0) / 100.0
        
        if node.target:
            target_value = self.execute(node.target)
            if isinstance(target_value, (int, float)):
                # Add chaos/randomness
                chaos_factor = random.uniform(-corruption, corruption) * target_value
                return target_value + chaos_factor
            else:
                return target_value
        else:
            # Pure chaos
            return random.random() * 100
    
    def _execute_purge_expr(self, node: PurgeExprNode) -> Any:
        """
        Execute Purge expression.
        
        Purge represents destruction/removal.
        Sets the target to zero/None/empty.
        """
        target_value = self.execute(node.target)
        
        if isinstance(target_value, (int, float)):
            return 0
        elif isinstance(target_value, str):
            return ""
        elif isinstance(target_value, list):
            return []
        elif isinstance(target_value, dict):
            return {}
        else:
            return None
    
    def _execute_exterminatus_expr(self, node: ExterminatusExprNode) -> Any:
        """
        Execute Exterminatus expression.
        
        Exterminatus represents total annihilation.
        If target is provided, destroys it completely.
        If no target, returns a special value representing total destruction.
        """
        if node.target:
            # Exterminatus destroys everything - returns None
            self.execute(node.target)  # Execute for side effects
            return None
        else:
            # Total annihilation
            return "EXTERMINATUS"  # Special marker
    
    def _execute_bless_expr(self, node: BlessExprNode) -> Any:
        """
        Execute Bless expression.
        
        Bless represents positive modification.
        Increases the target value.
        """
        target_value = self.execute(node.target)
        
        if isinstance(target_value, (int, float)):
            # Bless increases by 10%
            return target_value * 1.1
        elif isinstance(target_value, str):
            # Bless adds a positive prefix
            return f"Blessed {target_value}"
        else:
            return target_value
    
    def _execute_curse_expr(self, node: CurseExprNode) -> Any:
        """
        Execute Curse expression.
        
        Curse represents negative modification.
        Decreases the target value.
        """
        target_value = self.execute(node.target)
        
        if isinstance(target_value, (int, float)):
            # Curse decreases by 10%
            return target_value * 0.9
        elif isinstance(target_value, str):
            # Curse adds a negative prefix
            return f"Cursed {target_value}"
        else:
            return target_value
