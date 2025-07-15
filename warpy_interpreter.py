from lark import Lark, Transformer, v_args
from lark import Tree, Token
import sys

# Unified grammar that matches the test files
warpy_grammar = r"""
start: programa

programa    : sentenca*

sentenca    : comando
            | declaracao
            | atribuicao
            | loop
            | loop_while
            | condicional
            | COMMENT

declaracao  : identificador ":" tipo "=" expressao
atribuicao  : identificador "=" expressao

tipo        : "dg" | "servitor" | "blob" | "psykers" | "void_shields"

comando     : NOME_COMANDO "(" [args] ")"

args        : expressao ("," expressao)*

chamada     : NOME_COMANDO "(" [args] ")"

comandos    : sentenca+
loop        : FOR identificador IN expr_range ":" comandos
loop_while  : WHILE expressao ":" comandos
condicional : IF expressao ":" comandos [ELSE ":" comandos]

expr_range  : expressao ".." expressao

expressao   : termo expressao_rest
expressao_rest : PLUS termo expressao_rest
              | MINUS termo expressao_rest
              | ""  

termo       : fator termo_rest
termo_rest  : STAR fator termo_rest
           | SLASH fator termo_rest
           | PERCENT fator termo_rest
           | ""

fator       : numero
            | identificador
            | chamada
            | ESCAPED_STRING
            | comparacao
            | "(" expressao ")"

comparacao  : expressao op_comparacao expressao
op_comparacao: "==" | "!=" | "<" | ">" | "<=" | ">="

NOME_COMANDO: "the_emperor_protects"|"only_in_death_does_duty_end"|"even_in_death_i_still_serve"|"no_pity_no_remorse_no_fear"|"burn_the_heretic"|"pain_is_temporary_glory_is_forever"|"faith_is_my_shield"|"we_are_angels_of_death"|"we_are_one"|"WAAAGH"|"taste_chaos"|"for_the_emperor"|"purge_the_xenos"|"the_emperors_will_be_done"|"fear_is_the_mind_killer"|"ave_imperator"|"the_path_is_set"|"farseers_vision"|"more_dakka"|"ork_cunning"|"blood_for_the_blood_god"|"let_the_galaxy_burn"|"servitor"|"hear_the_emperors_voice"|"vox_cast"
IF: "if"
ELSE: "else"
FOR: "for"
IN: "in"
WHILE: "while"
identificador: /[a-zA-Z_][a-zA-Z0-9_]*/
numero      : /\d+(\.\d+)?/
COMMENT     : /#[^\n]*/

ESCAPED_STRING : /"[^\"]*"/

PLUS: "+"
MINUS: "-"
STAR: "*"
SLASH: "/"
PERCENT: "%"

%import common.WS
%ignore WS
"""

# Command implementations
COMMANDS = {
    'the_emperor_protects': lambda: print("[LOG] The Emperor protects!"),
    'burn_the_heretic': lambda tgt=None: print(f"[FIB] {tgt}" if tgt is not None else "[FIB]"),
    'for_the_emperor': lambda: print("[IMPERIUM] For the Emperor!"),
    'purge_the_xenos': lambda tgt: print(f"[ACTION] Xenos purged: {tgt}!"),
    'the_emperors_will_be_done': lambda: print("[IMPERIUM] The Emperor's will is fulfilled."),
    'fear_is_the_mind_killer': lambda: print("[LOG] Fear suppressed."),
    'ave_imperator': lambda: print("Ave Imperator! Glory to the Emperor!"),
    'we_are_one': lambda: print("[UNITY] We are one."),
    'WAAAGH': lambda: print("[WAAAGH!] The orks rally!"),
    'taste_chaos': lambda: print("[CORRUPTION] Warp corrupts your soul."),
    'the_path_is_set': lambda: print("[ELDAR] The path is set. We proceed."),
    'farseers_vision': lambda: print("[ELDAR] The Farseer foresees..."),
    'more_dakka': lambda: print("[ORKS] More dakka! Fire everything!"),
    'ork_cunning': lambda: print("[ORKS] Cunning plan!"),
    'blood_for_the_blood_god': lambda: print("[CHAOS] Blood for the Blood God!"),
    'let_the_galaxy_burn': lambda: print("[CHAOS] The galaxy burns!"),
    'only_in_death_does_duty_end': lambda: print("[LOG] Only in death does duty end."),
    'even_in_death_i_still_serve': lambda: print("[LOG] Even in death, I still serve!"),
    'no_pity_no_remorse_no_fear': lambda: print("[LOG] No pity, no remorse, no fear!"),
    'pain_is_temporary_glory_is_forever': lambda: print("[LOG] Pain is temporary, glory is forever."),
    'faith_is_my_shield': lambda: print("[LOG] Faith is my shield!"),
    'we_are_angels_of_death': lambda: print("[LOG] We are the Angels of Death!"),
    'servitor': lambda: "servitor_instance",
    'hear_the_emperors_voice': lambda prompt=None: hear_the_emperors_voice_impl(prompt),
    'vox_cast': lambda msg=None: print(f"[VOX] {str(msg) if msg is not None else ''}"),
}

def hear_the_emperors_voice_impl(prompt=None):
    try:
        return input(prompt if prompt else "")
    except (EOFError, KeyboardInterrupt):
        print("[LOG] Input interrupted. Returning empty string.")
        return ""

def flatten_args(args):
    flat = []
    for arg in args:
        if isinstance(arg, list):
            flat.extend(flatten_args(arg))
        else:
            flat.append(arg)
    return flat

def unwrap(val):
    while isinstance(val, list) and len(val) == 1:
        val = val[0]
    return val

# AST node definitions
class CommandNode:
    def __init__(self, name, args):
        self.name = name
        self.args = flatten_args(args)
    
    def execute(self, context):
        handler = COMMANDS.get(self.name)
        if handler:
            try:
                # TODO: [vox_cast] Debug print for vox_cast call
                if self.name == 'vox_cast':
                    print(f"[DEBUG] vox_cast called with args: {self.args}")
                # Resolve variables and evaluate expressions in arguments
                resolved_args = []
                for arg in self.args:
                    if isinstance(arg, str) and arg in context:
                        resolved_args.append(context[arg])
                    elif isinstance(arg, (SumNode, SubtractionNode, MultiplicationNode, DivisionNode, ModuloNode)):
                        resolved_args.append(arg.evaluate(context))
                    elif isinstance(arg, ComparisonNode):
                        resolved_args.append(arg.evaluate(context))
                    else:
                        resolved_args.append(arg)
                # TODO: [vox_cast] Debug print for resolved vox_cast arguments
                if self.name == 'vox_cast':
                    print(f"[DEBUG] vox_cast resolved_args: {resolved_args}")
                if resolved_args:
                    return handler(*resolved_args)
                else:
                    return handler()
            except TypeError:
                # Fallback for commands that don't take arguments
                return handler()
        else:
            print(f"Unknown command: {self.name}")
            return None

class DeclarationNode:
    def __init__(self, varname, typename, callnode):
        self.varname = varname
        self.typename = typename
        self.callnode = callnode
    
    def execute(self, context):
        value = self.callnode
        # If the value is a CommandNode, execute it and store the result
        if isinstance(value, CommandNode):
            result = value.execute(context)
            value = result
        # If type is dg and value is a string, try to convert to int or float
        if self.typename == "dg" and isinstance(value, str):
            try:
                if "." in value:
                    value = float(value)
                else:
                    value = int(value)
            except Exception:
                raise ValueError(f"Cannot convert input '{value}' to a number for variable '{self.varname}' of type dg.")
        elif self.typename == "dg" and value is None:
            raise ValueError(f"Input for variable '{self.varname}' of type dg was empty or invalid.")
        elif isinstance(value, (SumNode, SubtractionNode, MultiplicationNode, DivisionNode, ModuloNode)):
            value = value.evaluate(context)
        context[self.varname] = value
        print(f"[DECL] Variable {self.varname} of type {self.typename} declared")

class LoopNode:
    def __init__(self, varname, start, end, commands):
        self.varname = varname
        self.start = start
        self.end = end
        self.commands = commands
    
    def execute(self, context):
        def _resolve(val, context):
            if isinstance(val, list):
                if len(val) == 1:
                    return _resolve(val[0], context)
                raise ValueError("Unexpected list value in loop range")
            if isinstance(val, str) and val in context:
                return context[val]
            return val
        start = _resolve(self.start, context)
        end = _resolve(self.end, context)
        for i in range(int(start), int(end) + 1):
            context[self.varname] = i
            for cmd in self.commands:
                cmd.execute(context)

class ConditionalNode:
    def __init__(self, condition, then_commands, else_commands=None):
        self.condition = condition
        # Only keep executable nodes
        self.then_commands = [cmd for cmd in then_commands if hasattr(cmd, 'execute')]
        self.else_commands = [cmd for cmd in else_commands if hasattr(cmd, 'execute')] if else_commands else None
    
    def execute(self, context):
        # Evaluate condition
        condition_result = self._evaluate_condition(self.condition, context)
        if condition_result:
            for cmd in self.then_commands:
                cmd.execute(context)
        elif self.else_commands:
            for cmd in self.else_commands:
                cmd.execute(context)
    
    def _evaluate_condition(self, condition, context):
        if isinstance(condition, ComparisonNode):
            return condition.evaluate(context)
        # For simple values, treat as truthy/falsy
        return bool(condition)

class ComparisonNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def evaluate(self, context):
        left_val = self._resolve_value(self.left, context)
        right_val = self._resolve_value(self.right, context)
        
        if self.operator == "==":
            return left_val == right_val
        elif self.operator == "!=":
            return left_val != right_val
        elif self.operator == "<":
            return left_val < right_val
        elif self.operator == ">":
            return left_val > right_val
        elif self.operator == "<=":
            return left_val <= right_val
        elif self.operator == ">=":
            return left_val >= right_val
        return False
    
    def _resolve_value(self, value, context):
        if isinstance(value, str) and value in context:
            return context[value]
        elif isinstance(value, (SumNode, SubtractionNode, MultiplicationNode, DivisionNode, ModuloNode)):
            return value.evaluate(context)
        return value

class WhileNode:
    def __init__(self, condition, commands):
        self.condition = condition
        self.commands = commands
    def execute(self, context):
        # Avalia a condição e executa enquanto for verdadeira
        while self._evaluate_condition(self.condition, context):
            for cmd in self.commands:
                cmd.execute(context)
    def _evaluate_condition(self, condition, context):
        if isinstance(condition, ComparisonNode):
            return condition.evaluate(context)
        return bool(condition)

class AssignmentNode:
    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr
    def execute(self, context):
        value = self._eval_expr(self.expr, context)
        context[self.varname] = value
    def _eval_expr(self, expr, context):
        if isinstance(expr, (SumNode, SubtractionNode, MultiplicationNode, DivisionNode, ModuloNode)):
            return expr.evaluate(context)
        if isinstance(expr, ComparisonNode):
            return expr.evaluate(context)
        if isinstance(expr, str) and expr in context:
            return context[expr]
        return expr

class SumNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, context):
        left_val = self._resolve(self.left, context)
        right_val = self._resolve(self.right, context)
        return left_val + right_val
    def _resolve(self, val, context):
        if isinstance(val, str) and val in context:
            return context[val]
        if isinstance(val, (SumNode, SubtractionNode, MultiplicationNode, DivisionNode, ModuloNode)):
            return val.evaluate(context)
        return val

class SubtractionNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, context):
        left_val = self._resolve(self.left, context)
        right_val = self._resolve(self.right, context)
        return left_val - right_val
    def _resolve(self, val, context):
        if isinstance(val, str) and val in context:
            return context[val]
        if isinstance(val, (SumNode, SubtractionNode, MultiplicationNode, DivisionNode, ModuloNode)):
            return val.evaluate(context)
        return val

class MultiplicationNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, context):
        left_val = self._resolve(self.left, context)
        right_val = self._resolve(self.right, context)
        return left_val * right_val
    def _resolve(self, val, context):
        if isinstance(val, str) and val in context:
            return context[val]
        if isinstance(val, (SumNode, SubtractionNode, MultiplicationNode, DivisionNode, ModuloNode)):
            return val.evaluate(context)
        return val

class DivisionNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, context):
        left_val = self._resolve(self.left, context)
        right_val = self._resolve(self.right, context)
        if right_val == 0:
            raise ValueError("Division by zero")
        return left_val / right_val
    def _resolve(self, val, context):
        if isinstance(val, str) and val in context:
            return context[val]
        if isinstance(val, (SumNode, SubtractionNode, MultiplicationNode, DivisionNode, ModuloNode)):
            return val.evaluate(context)
        return val

class ModuloNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, context):
        left_val = self._resolve(self.left, context)
        right_val = self._resolve(self.right, context)
        if right_val == 0:
            raise ValueError("Modulo by zero")
        return left_val % right_val
    def _resolve(self, val, context):
        if isinstance(val, str) and val in context:
            return context[val]
        if isinstance(val, (SumNode, SubtractionNode, MultiplicationNode, DivisionNode, ModuloNode)):
            return val.evaluate(context)
        return val

# Transformer to build AST
class WarpyTransformer(Transformer):
    def __init__(self):
        self.env = {}

    def _maybe_transform(self, val):
        return self.transform(val) if isinstance(val, Tree) else val

    def start(self, programa):
        return programa

    def programa(self, *sentencas):
        return sentencas

    def sentenca(self, stmt):
        return stmt

    def declaracao(self, children):
        varname, typename, expr = map(unwrap, children)
        return DeclarationNode(varname, typename, expr)

    def atribuicao(self, children):
        varname, expr = map(unwrap, children)
        return AssignmentNode(varname, expr)

    def comando(self, children):
        name = str(unwrap(children[0])) if children else None
        args = unwrap(children[1]) if len(children) > 1 else []
        if not isinstance(args, list):
            args = [args]
        print(f"[DEBUG] comando: name={name}, args={args}")
        return CommandNode(name, args)

    def chamada(self, children):
        name = str(unwrap(children[0])) if children else None
        args = unwrap(children[1]) if len(children) > 1 else []
        if not isinstance(args, list):
            args = [args]
        return CommandNode(name, args)

    def expressao(self, val):
        return self._maybe_transform(val)

    def soma(self, children):
        left, right = map(unwrap, children)
        return SumNode(left, right)

    def subtracao(self, children):
        left, right = map(unwrap, children)
        return SubtractionNode(left, right)

    def termo(self, val):
        return self._maybe_transform(val)

    def multiplicacao(self, children):
        left, right = map(unwrap, children)
        return MultiplicationNode(left, right)

    def divisao(self, children):
        left, right = map(unwrap, children)
        return DivisionNode(left, right)

    def modulo(self, children):
        left, right = map(unwrap, children)
        return ModuloNode(left, right)

    def fator(self, val):
        return self._maybe_transform(val)

    def expr_range(self, children):
        start_tree, end_tree = map(unwrap, children)
        start = self._maybe_transform(start_tree)
        end = self._maybe_transform(end_tree)
        
        # Extract the actual numeric values from lists if needed
        def extract_num(val):
            if isinstance(val, list):
                if len(val) == 1:
                    return extract_num(val[0])
                return None
            if hasattr(val, 'value'):
                val_str = val.value
                return int(val_str) if val_str.isdigit() else float(val_str)
            return val
        
        start = extract_num(start)
        end = extract_num(end)
        
        # Only allow numbers or identifiers (not CommandNode)
        if isinstance(start, CommandNode) or isinstance(end, CommandNode):
            raise ValueError("Loop range must be a number or variable, not a command.")
        return (start, end)

    def loop(self, children):
        # children[0] is FOR token, children[1] is identificador, children[2] is IN token, children[3] is expr_range, children[4] is comandos
        varname = unwrap(children[1])
        range_tuple = unwrap(children[3])
        comandos = unwrap(children[4])
        # comandos is a list of lists, flatten it
        if isinstance(comandos, list) and len(comandos) == 1 and isinstance(comandos[0], list):
            comandos = comandos[0]
        if not isinstance(range_tuple, tuple) or len(range_tuple) != 2:
            raise ValueError("Invalid loop range.")
        start, end = range_tuple
        return LoopNode(varname, start, end, comandos)

    def loop_while(self, children):
        # children[0] is WHILE token, children[1] is [condition], children[2] is [commands]
        condition = unwrap(children[1][0]) if isinstance(children[1], list) and children[1] else unwrap(children[1])
        commands = unwrap(children[2]) if len(children) > 2 else []
        return WhileNode(condition, commands)

    def condicional(self, children):
        i = 0
        if isinstance(children[i], Token) and children[i].type == 'IF':
            i += 1
        condition_expr = unwrap(children[i])
        i += 1
        if isinstance(children[i], Token) and children[i].type == ':':
            i += 1
        then_commands = unwrap(children[i])
        i += 1
        else_commands = None
        if len(children) > i and isinstance(children[i], Token) and children[i].type == 'ELSE':
            i += 1
            if isinstance(children[i], Token) and children[i].type == ':':
                i += 1
            else_commands = unwrap(children[i])
        # Ensure then_commands and else_commands are always lists
        if then_commands is not None and not isinstance(then_commands, list):
            then_commands = [then_commands]
        if else_commands is not None and not isinstance(else_commands, list):
            else_commands = [else_commands]
        if isinstance(then_commands, list) and len(then_commands) == 1 and isinstance(then_commands[0], list):
            then_commands = then_commands[0]
        if isinstance(else_commands, list) and len(else_commands) == 1 and isinstance(else_commands[0], list):
            else_commands = else_commands[0]
        return ConditionalNode(condition_expr, then_commands, else_commands)

    def comparacao(self, children):
        left, operator, right = map(unwrap, children)
        return ComparisonNode(left, operator, right)

    def op_comparacao(self, children):
        if not children:
            return None
        return str(children[0])

    def comandos(self, *stmts):
        def flatten(items):
            for x in items:
                if isinstance(x, list):
                    yield from flatten(x)
                else:
                    yield x
        statements = []
        for stmt in flatten(stmts):
            if hasattr(stmt, 'execute') and not isinstance(stmt, ComparisonNode):
                statements.append(stmt)
        # Always return a list, even for a single item
        if not isinstance(statements, list):
            statements = [statements]
        return statements

    def args(self, *args):
        # Always return a flat list of arguments
        flat_args = []
        for arg in args:
            if isinstance(arg, list):
                flat_args.extend(arg)
            else:
                flat_args.append(arg)
        return flat_args

    def numero(self, children):
        children = unwrap(children)
        val_str = children.value if hasattr(children, 'value') else str(children)
        return int(val_str) if val_str.isdigit() else float(val_str)

    def identificador(self, children):
        children = unwrap(children)
        return str(children.value) if hasattr(children, 'value') else str(children)

    def tipo(self, children):
        if not children:
            return None
        return str(children[0])

    def ESCAPED_STRING(self, children):
        val = children[0]
        if hasattr(val, 'value'):
            val = val.value
        val = str(val)
        if val.startswith('"') and val.endswith('"'):
            return val[1:-1]
        return val

    def COMMENT(self, children):
        # Comments are ignored during execution
        return None

def run_warpy_script(script_path: str):
    # TEMP: Use a hardcoded string for testing
    code = 'vox_cast("Hello, world!")'
    # with open(script_path, 'r') as f:
    #     code = f.read()

    parser = Lark(warpy_grammar, parser='earley', start='start')
    parse_tree = parser.parse(code)

    transformer = WarpyTransformer()
    ast = transformer.transform(parse_tree)

    # Flatten the AST in case of nested lists
    def flatten(items):
        for x in items:
            if isinstance(x, (list, tuple)):
                yield from flatten(x)
            else:
                yield x

    context = {}
    for stmt in flatten(ast):
        if hasattr(stmt, 'execute'):
            stmt.execute(context)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python warpy_interpreter.py <file.wp40k>")
        sys.exit(1)

    script_file = sys.argv[1]
    run_warpy_script(script_file)
