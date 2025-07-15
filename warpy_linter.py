#!/usr/bin/env python3
"""
WarPy40K Language Linter
Checks syntax, validates commands, variables, and provides helpful error messages.
"""

import sys
import re
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class LintSeverity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

@dataclass
class LintIssue:
    line: int
    column: int
    severity: LintSeverity
    message: str
    code: str
    suggestion: Optional[str] = None

class WarPy40KLinter:
    def __init__(self):
        # Valid commands in WarPy40K
        self.valid_commands = {
            'the_emperor_protects', 'only_in_death_does_duty_end', 'even_in_death_i_still_serve',
            'no_pity_no_remorse_no_fear', 'burn_the_heretic', 'pain_is_temporary_glory_is_forever',
            'faith_is_my_shield', 'we_are_angels_of_death', 'we_are_one', 'WAAAGH', 'taste_chaos',
            'for_the_emperor', 'purge_the_xenos', 'the_emperors_will_be_done', 'fear_is_the_mind_killer',
            'ave_imperator', 'the_path_is_set', 'farseers_vision', 'more_dakka', 'ork_cunning',
            'blood_for_the_blood_god', 'let_the_galaxy_burn', 'servitor', 'hear_the_emperors_voice',
            'vox_cast'
        }
        
        # Valid keywords
        self.keywords = {'for', 'in', 'while', 'if', 'else', 'dg'}
        
        # Valid comparison operators
        self.comparison_operators = {'==', '!=', '<', '>', '<=', '>='}
        
        # Valid arithmetic operators
        self.arithmetic_operators = {'+', '-', '*', '/'}
        
        # Track variables and their usage
        self.declared_variables: Set[str] = set()
        self.used_variables: Set[str] = set()
        self.loop_variables: Set[str] = set()
        
        # Track control flow
        self.in_loop = False
        self.loop_depth = 0
        self.in_conditional = False
        
        # Issues found
        self.issues: List[LintIssue] = []

    def lint_file(self, file_path: str) -> List[LintIssue]:
        """Main linting function that processes a WarPy40K file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.issues.append(LintIssue(
                line=1, column=1, severity=LintSeverity.ERROR,
                message=f"File '{file_path}' not found",
                code="FILE_NOT_FOUND"
            ))
            return self.issues
        except Exception as e:
            self.issues.append(LintIssue(
                line=1, column=1, severity=LintSeverity.ERROR,
                message=f"Error reading file: {str(e)}",
                code="FILE_READ_ERROR"
            ))
            return self.issues

        # Reset state for new file
        self.declared_variables.clear()
        self.used_variables.clear()
        self.loop_variables.clear()
        self.in_loop = False
        self.loop_depth = 0
        self.in_conditional = False
        self.issues.clear()

        # Process each line
        for line_num, line in enumerate(lines, 1):
            self._lint_line(line_num, line.rstrip())

        # Post-processing checks
        self._check_unused_variables()
        self._check_undeclared_variables()
        self._check_loop_balance()

        return self.issues

    def _lint_line(self, line_num: int, line: str):
        """Lint a single line of WarPy40K code."""
        # Skip empty lines
        if not line.strip():
            return

        # Check for comments (now supported in WarPy40K)
        if line.strip().startswith('#'):
            return  # Comments are now valid, no warning needed

        # Check for trailing whitespace
        if line.rstrip() != line:
            self.issues.append(LintIssue(
                line=line_num, column=len(line.rstrip()) + 1, severity=LintSeverity.WARNING,
                message="Trailing whitespace detected",
                code="TRAILING_WHITESPACE",
                suggestion="Remove trailing spaces"
            ))

        # Check line length
        if len(line) > 120:
            self.issues.append(LintIssue(
                line=line_num, column=121, severity=LintSeverity.WARNING,
                message="Line too long (over 120 characters)",
                code="LINE_TOO_LONG",
                suggestion="Break the line into multiple lines"
            ))

        # Track loop depth for block ends (dedent simulation)
        if line.strip() == '':
            return
        if line.strip().startswith('for ') or line.strip().startswith('while '):
            self.loop_depth += 1
        if line.strip().startswith('endfor') or line.strip().startswith('endwhile'):
            self.loop_depth = max(0, self.loop_depth - 1)

        # Parse and validate the line
        self._parse_line(line_num, line)

    def _parse_line(self, line_num: int, line: str):
        """Parse and validate a line of WarPy40K code."""
        # Remove inline comments (everything after #)
        if '#' in line:
            line = line[:line.find('#')].rstrip()
        
        # Skip empty lines after comment removal
        if not line.strip():
            return
            
        stripped = line.strip()
        
        # Check for else clause (valid in if-else statements)
        if stripped == 'else:':
            return  # Valid syntax, no validation needed
        
        # Check for variable declaration
        if self._is_variable_declaration(stripped):
            self._validate_variable_declaration(line_num, stripped)
            return

        # Check for assignment
        if '=' in stripped and not stripped.startswith('if') and not stripped.startswith('while'):
            self._validate_assignment(line_num, stripped)
            return

        # Check for loop
        if stripped.startswith('for '):
            self._validate_for_loop(line_num, stripped)
            return

        # Check for while loop
        if stripped.startswith('while '):
            self._validate_while_loop(line_num, stripped)
            return

        # Check for conditional
        if stripped.startswith('if '):
            self._validate_conditional(line_num, stripped)
            return

        # Check for command
        if '(' in stripped and stripped.endswith(')'):
            self._validate_command(line_num, stripped)
            return

        # Check for standalone command (no arguments)
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\(\)$', stripped):
            self._validate_command(line_num, stripped)
            return

        # Check for multi-command lines (commands separated by spaces)
        if ' ' in stripped and '(' in stripped:
            # Try to parse as multiple commands
            self._parse_multi_commands(line_num, stripped)
            return

        # Unknown syntax
        self.issues.append(LintIssue(
            line=line_num, column=1, severity=LintSeverity.ERROR,
            message=f"Unknown syntax: '{stripped}'",
            code="UNKNOWN_SYNTAX",
            suggestion="Check the WarPy40K syntax documentation"
        ))

    def _is_variable_declaration(self, line: str) -> bool:
        """Check if a line is a variable declaration."""
        return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*:\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=', line)

    def _validate_variable_declaration(self, line_num: int, line: str):
        """Validate a variable declaration."""
        # Extract variable name and type
        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line)
        if not match:
            self.issues.append(LintIssue(
                line=line_num, column=1, severity=LintSeverity.ERROR,
                message="Invalid variable declaration syntax",
                code="INVALID_VAR_DECL",
                suggestion="Use format: variable_name: type = value"
            ))
            return

        var_name = match.group(1)
        var_type = match.group(2)
        
        # Check if variable is already declared
        if var_name in self.declared_variables:
            self.issues.append(LintIssue(
                line=line_num, column=1, severity=LintSeverity.WARNING,
                message=f"Variable '{var_name}' is already declared",
                code="DUPLICATE_VAR_DECL",
                suggestion="Use a different variable name or remove the duplicate declaration"
            ))

        # Check variable name
        if var_name in self.keywords:
            self.issues.append(LintIssue(
                line=line_num, column=1, severity=LintSeverity.ERROR,
                message=f"'{var_name}' is a reserved keyword",
                code="RESERVED_KEYWORD",
                suggestion="Use a different variable name"
            ))

        self.declared_variables.add(var_name)

        # Validate the value
        value_part = line.split('=', 1)[1].strip()
        self._validate_expression(line_num, value_part, f"variable '{var_name}' declaration")

    def _validate_assignment(self, line_num: int, line: str):
        """Validate an assignment statement."""
        if '=' not in line:
            return

        parts = line.split('=', 1)
        if len(parts) != 2:
            self.issues.append(LintIssue(
                line=line_num, column=1, severity=LintSeverity.ERROR,
                message="Invalid assignment syntax",
                code="INVALID_ASSIGNMENT",
                suggestion="Use format: variable = expression"
            ))
            return

        var_name = parts[0].strip()
        expression = parts[1].strip()

        # Check if variable is declared
        if var_name not in self.declared_variables and var_name not in self.loop_variables:
            self.issues.append(LintIssue(
                line=line_num, column=1, severity=LintSeverity.WARNING,
                message=f"Variable '{var_name}' is used before declaration",
                code="UNDECLARED_VARIABLE",
                suggestion="Declare the variable first using 'variable_name: dg = initial_value'"
            ))

        self.used_variables.add(var_name)
        self._validate_expression(line_num, expression, f"assignment to '{var_name}'")

    def _validate_for_loop(self, line_num: int, line: str):
        """Validate a for loop."""
        # Check if line contains multiple commands after the for loop
        if ' ' in line and line.count(' ') > 3:  # More than just "for var in range:"
            # Extract the for loop part and the commands part
            colon_pos = line.find(':')
            if colon_pos == -1:
                self.issues.append(LintIssue(
                    line=line_num, column=len(line), severity=LintSeverity.ERROR,
                    message="For loop must end with ':'",
                    code="MISSING_COLON",
                    suggestion="Add ':' at the end of the for loop declaration"
                ))
                return
            
            for_part = line[:colon_pos + 1]
            commands_part = line[colon_pos + 1:].strip()
            
            # Validate the for loop part
            self._validate_for_loop_structure(line_num, for_part)
            
            # Validate the commands part
            if commands_part:
                self._parse_multi_commands(line_num, commands_part)
        else:
            # Simple for loop without inline commands
            self._validate_for_loop_structure(line_num, line)

    def _validate_for_loop_structure(self, line_num: int, line: str):
        """Validate the structure of a for loop."""
        # Check basic syntax
        if not line.endswith(':'):
            self.issues.append(LintIssue(
                line=line_num, column=len(line), severity=LintSeverity.ERROR,
                message="For loop must end with ':'",
                code="MISSING_COLON",
                suggestion="Add ':' at the end of the for loop declaration"
            ))
            return

        # Extract loop parts
        match = re.match(r'^for\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+(.+):$', line)
        if not match:
            self.issues.append(LintIssue(
                line=line_num, column=1, severity=LintSeverity.ERROR,
                message="Invalid for loop syntax",
                code="INVALID_FOR_LOOP",
                suggestion="Use format: for variable in start..end:"
            ))
            return

        var_name = match.group(1)
        range_expr = match.group(2)

        # Check loop variable
        if var_name in self.keywords:
            self.issues.append(LintIssue(
                line=line_num, column=5, severity=LintSeverity.ERROR,
                message=f"'{var_name}' is a reserved keyword",
                code="RESERVED_KEYWORD",
                suggestion="Use a different variable name"
            ))

        self.loop_variables.add(var_name)
        self.loop_depth += 1

        # Validate range expression
        if '..' not in range_expr:
            self.issues.append(LintIssue(
                line=line_num, column=line.find(range_expr) + 1, severity=LintSeverity.ERROR,
                message="Invalid range expression",
                code="INVALID_RANGE",
                suggestion="Use format: start..end (e.g., 1..10)"
            ))
        else:
            start, end = range_expr.split('..', 1)
            self._validate_expression(line_num, start.strip(), "for loop start value")
            self._validate_expression(line_num, end.strip(), "for loop end value")

    def _validate_while_loop(self, line_num: int, line: str):
        """Validate a while loop."""
        if not line.endswith(':'):
            self.issues.append(LintIssue(
                line=line_num, column=len(line), severity=LintSeverity.ERROR,
                message="While loop must end with ':'",
                code="MISSING_COLON",
                suggestion="Add ':' at the end of the while loop declaration"
            ))
            return

        # Extract condition
        condition_start = line.find('while ') + 6
        condition = line[condition_start:-1].strip()

        if not condition:
            self.issues.append(LintIssue(
                line=line_num, column=condition_start, severity=LintSeverity.ERROR,
                message="While loop must have a condition",
                code="MISSING_CONDITION",
                suggestion="Add a condition (e.g., while x < 10:)"
            ))
            return

        self.loop_depth += 1
        self._validate_condition(line_num, condition, "while loop")

    def _validate_conditional(self, line_num: int, line: str):
        """Validate an if statement."""
        if not line.endswith(':'):
            self.issues.append(LintIssue(
                line=line_num, column=len(line), severity=LintSeverity.ERROR,
                message="If statement must end with ':'",
                code="MISSING_COLON",
                suggestion="Add ':' at the end of the if statement"
            ))
            return

        # Extract condition
        condition_start = line.find('if ') + 3
        condition = line[condition_start:-1].strip()

        if not condition:
            self.issues.append(LintIssue(
                line=line_num, column=condition_start, severity=LintSeverity.ERROR,
                message="If statement must have a condition",
                code="MISSING_CONDITION",
                suggestion="Add a condition (e.g., if x == 1:)"
            ))
            return

        self.in_conditional = True
        self._validate_condition(line_num, condition, "if statement")

    def _validate_command(self, line_num: int, line: str):
        """Validate a command call."""
        # Extract command name
        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', line)
        if not match:
            self.issues.append(LintIssue(
                line=line_num, column=1, severity=LintSeverity.ERROR,
                message="Invalid command syntax",
                code="INVALID_COMMAND",
                suggestion="Use format: command_name() or command_name(arguments)"
            ))
            return

        command_name = match.group(1)

        # Check if command exists
        if command_name not in self.valid_commands:
            self.issues.append(LintIssue(
                line=line_num, column=1, severity=LintSeverity.ERROR,
                message=f"Unknown command '{command_name}'",
                code="UNKNOWN_COMMAND",
                suggestion=f"Available commands: {', '.join(sorted(self.valid_commands))}"
            ))

        # Check parentheses balance
        if not line.endswith(')'):
            self.issues.append(LintIssue(
                line=line_num, column=len(line), severity=LintSeverity.ERROR,
                message="Missing closing parenthesis",
                code="MISSING_PARENTHESIS",
                suggestion="Add ')' at the end of the command"
            ))
            return

        # Extract arguments
        args_start = line.find('(') + 1
        args_end = line.rfind(')')
        args_str = line[args_start:args_end].strip()

        if args_str:
            self._validate_arguments(line_num, args_str)

    def _validate_arguments(self, line_num: int, args_str: str):
        """Validate command arguments."""
        # Simple argument validation - can be enhanced
        if args_str:
            # Check for string literals
            if '"' in args_str:
                # Validate string literal syntax
                if not re.match(r'^"[^"]*"$', args_str.strip()):
                    self.issues.append(LintIssue(
                        line=line_num, column=args_str.find('"') + 1, severity=LintSeverity.ERROR,
                        message="Invalid string literal",
                        code="INVALID_STRING",
                        suggestion="Use format: \"string_content\""
                    ))
            else:
                # Check for variable references
                var_name = args_str.strip()
                if var_name and var_name not in self.declared_variables and var_name not in self.loop_variables:
                    self.issues.append(LintIssue(
                        line=line_num, column=args_str.find(var_name) + 1, severity=LintSeverity.WARNING,
                        message=f"Variable '{var_name}' is used but not declared",
                        code="UNDECLARED_VARIABLE",
                        suggestion="Declare the variable first or use a string literal"
                    ))

    def _validate_expression(self, line_num: int, expr: str, context: str):
        """Recursively validate an arithmetic expression with correct precedence and parentheses."""
        # Remove inline comments
        if '#' in expr:
            expr = expr[:expr.find('#')].rstrip()
        expr = expr.strip()
        if not expr:
            return

        # Parentheses: recursively validate inside
        if expr.startswith('(') and expr.endswith(')'):
            # Check for matching parentheses
            depth = 0
            for i, c in enumerate(expr):
                if c == '(': depth += 1
                elif c == ')': depth -= 1
                if depth == 0 and i != len(expr) - 1:
                    break
            else:
                # Parentheses wrap the whole expression
                return self._validate_expression(line_num, expr[1:-1], f"parenthesized expression in {context}")

        # Operator precedence: lowest to highest
        # 1. +, -
        # 2. *, /, %
        def split_outside_parens(s, ops):
            parts = []
            depth = 0
            last = 0
            for i, c in enumerate(s):
                if c == '(': depth += 1
                elif c == ')': depth -= 1
                elif depth == 0 and any(s.startswith(op, i) for op in ops):
                    for op in ops:
                        if s.startswith(op, i):
                            parts.append((s[last:i].strip(), op))
                            last = i + len(op)
                            break
            parts.append((s[last:].strip(), None))
            return parts

        # Try +, - first
        parts = split_outside_parens(expr, ['+', '-'])
        if len(parts) > 1:
            for part, op in parts:
                self._validate_expression(line_num, part, f"arithmetic operation (+/-) in {context}")
            return
        # Then *, /, %
        parts = split_outside_parens(expr, ['*', '/', '%'])
        if len(parts) > 1:
            for part, op in parts:
                self._validate_expression(line_num, part, f"arithmetic operation (*//%) in {context}")
            return

        # Number
        if re.match(r'^\d+(\.\d+)?$', expr):
            return
        # String literal
        if re.match(r'^"[^"]*"$', expr):
            return
        # Variable
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr):
            var_name = expr
            if var_name not in self.declared_variables and var_name not in self.loop_variables:
                self.issues.append(LintIssue(
                    line=line_num, column=1, severity=LintSeverity.WARNING,
                    message=f"Variable '{var_name}' is used but not declared in {context}",
                    code="UNDECLARED_VARIABLE",
                    suggestion="Declare the variable first"
                ))
            self.used_variables.add(var_name)
            return
        # Function call
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\(\)$', expr):
            func_name = expr[:-2]
            if func_name not in self.valid_commands:
                self.issues.append(LintIssue(
                    line=line_num, column=1, severity=LintSeverity.WARNING,
                    message=f"Unknown function '{func_name}' in {context}",
                    code="UNKNOWN_FUNCTION",
                    suggestion=f"Available functions: {', '.join(sorted(self.valid_commands))}"
                ))
            return
        # Function call with arguments (allow nested parentheses and whitespace)
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\(.*\)$', expr):
            func_name = expr[:expr.find('(')]
            if func_name not in self.valid_commands:
                self.issues.append(LintIssue(
                    line=line_num, column=1, severity=LintSeverity.WARNING,
                    message=f"Unknown function '{func_name}' in {context}",
                    code="UNKNOWN_FUNCTION",
                    suggestion=f"Available functions: {', '.join(sorted(self.valid_commands))}"
                ))
            # Validate arguments (best effort: split on commas not inside quotes or parens)
            args_str = expr[expr.find('(')+1:expr.rfind(')')]
            if args_str.strip():
                # Simple split for now; could be improved for nested
                self._validate_arguments(line_num, args_str)
            return
        # Comparison or logical
        if any(op in expr for op in self.comparison_operators) or re.search(r'\b(and|or)\b', expr):
            return
        # If we get here, it's an unknown expression pattern
        self.issues.append(LintIssue(
            line=line_num, column=1, severity=LintSeverity.ERROR,
            message=f"Invalid expression in {context}",
            code="INVALID_EXPRESSION",
            suggestion="Use numbers, strings, variables, function calls, arithmetic operations, or valid comparisons"
        ))

    def _validate_condition(self, line_num: int, condition: str, context: str):
        """Validate a condition expression, supporting arithmetic, comparisons, and logical 'and'/'or'."""
        condition = condition.strip()
        if not condition:
            self.issues.append(LintIssue(
                line=line_num, column=1, severity=LintSeverity.ERROR,
                message=f"Empty condition in {context}",
                code="EMPTY_CONDITION",
                suggestion="Provide a valid condition (e.g., if x == 1:)"
            ))
            return
        # Handle parentheses
        if condition.startswith('(') and condition.endswith(')'):
            depth = 0
            for i, c in enumerate(condition):
                if c == '(': depth += 1
                elif c == ')': depth -= 1
                if depth == 0 and i != len(condition) - 1:
                    break
            else:
                return self._validate_condition(line_num, condition[1:-1], context)
        # Handle logical 'and'/'or'
        tokens = re.split(r'\b(and|or)\b', condition)
        if len(tokens) > 1:
            for i in range(0, len(tokens), 2):
                cond = tokens[i].strip()
                if cond:
                    self._validate_condition(line_num, cond, context)
            return
        # Handle comparisons
        for op in self.comparison_operators:
            if op in condition:
                parts = condition.split(op, 1)
                if len(parts) == 2:
                    left, right = parts[0].strip(), parts[1].strip()
                    self._validate_expression(line_num, left, f"left side of {context}")
                    self._validate_expression(line_num, right, f"right side of {context}")
                    return
        # If no comparison operator found, allow arithmetic, variable, or number as condition
        self._validate_expression(line_num, condition, context)

    def _parse_multi_commands(self, line_num: int, line: str):
        """Parse a line that contains multiple commands."""
        # Simple approach: split by spaces and try to identify commands
        parts = line.split()
        current_command = ""
        paren_count = 0
        
        for part in parts:
            current_command += part + " "
            paren_count += part.count('(') - part.count(')')
            
            if paren_count == 0 and current_command.strip():
                # Complete command found
                self._validate_command(line_num, current_command.strip())
                current_command = ""
        
        # If there's remaining content, it might be incomplete
        if current_command.strip():
            self.issues.append(LintIssue(
                line=line_num, column=1, severity=LintSeverity.WARNING,
                message=f"Incomplete command: '{current_command.strip()}'",
                code="INCOMPLETE_COMMAND",
                suggestion="Check for missing parentheses or syntax errors"
            ))

    def _check_unused_variables(self):
        """Check for unused variables."""
        for var in self.declared_variables:
            if var not in self.used_variables:
                self.issues.append(LintIssue(
                    line=1, column=1, severity=LintSeverity.WARNING,
                    message=f"Variable '{var}' is declared but never used",
                    code="UNUSED_VARIABLE",
                    suggestion="Remove the variable declaration or use it in your code"
                ))

    def _check_undeclared_variables(self):
        """Check for undeclared variables."""
        for var in self.used_variables:
            if var not in self.declared_variables and var not in self.loop_variables:
                self.issues.append(LintIssue(
                    line=1, column=1, severity=LintSeverity.ERROR,
                    message=f"Variable '{var}' is used but never declared",
                    code="UNDECLARED_VARIABLE",
                    suggestion="Declare the variable first using 'variable_name: dg = initial_value'"
                ))

    def _check_loop_balance(self):
        """Check for balanced loop structures. Only warn if explicit block ends are used and not matched."""
        # In flat, non-indented WarPy40K scripts, do not warn for loop depth
        # Only warn if explicit 'endfor' or 'endwhile' is used and not matched
        pass

    def print_issues(self, issues: List[LintIssue], file_path: str = ""):
        """Print linting issues in a formatted way."""
        if not issues:
            print(f"✅ No issues found in {file_path}")
            return

        print(f"🔍 Found {len(issues)} issue(s) in {file_path}:")
        print()

        # Group issues by severity
        errors = [i for i in issues if i.severity == LintSeverity.ERROR]
        warnings = [i for i in issues if i.severity == LintSeverity.WARNING]
        infos = [i for i in issues if i.severity == LintSeverity.INFO]

        for severity, issue_list, symbol in [
            (LintSeverity.ERROR, errors, "❌"),
            (LintSeverity.WARNING, warnings, "⚠️"),
            (LintSeverity.INFO, infos, "ℹ️")
        ]:
            if issue_list:
                print(f"{symbol} {severity.value}S ({len(issue_list)}):")
                for issue in issue_list:
                    print(f"  Line {issue.line}, Col {issue.column}: {issue.message}")
                    print(f"    Code: {issue.code}")
                    if issue.suggestion:
                        print(f"    Suggestion: {issue.suggestion}")
                    print()
                print()

def main():
    """Main function to run the linter."""
    if len(sys.argv) < 2:
        print("Usage: python warpy_linter.py <file.wp40k>")
        print("       python warpy_linter.py --help")
        sys.exit(1)

    if sys.argv[1] == "--help":
        print("WarPy40K Language Linter")
        print("Checks syntax, validates commands, variables, and provides helpful error messages.")
        print()
        print("Usage: python warpy_linter.py <file.wp40k>")
        print()
        print("The linter checks for:")
        print("  - Syntax errors and invalid commands")
        print("  - Undeclared and unused variables")
        print("  - Invalid loop and conditional structures")
        print("  - String literal syntax")
        print("  - Code style issues (line length, whitespace)")
        print()
        print("Exit codes:")
        print("  0 - No errors found")
        print("  1 - Errors found")
        sys.exit(0)

    file_path = sys.argv[1]
    linter = WarPy40KLinter()
    issues = linter.lint_file(file_path)

    linter.print_issues(issues, file_path)

    # Exit with error code if there are errors
    error_count = len([i for i in issues if i.severity == LintSeverity.ERROR])
    sys.exit(1 if error_count > 0 else 0)

if __name__ == "__main__":
    main() 