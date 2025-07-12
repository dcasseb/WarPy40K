from lark import Lark, Transformer, v_args
from lark import Tree, Token
import sys

# Unified grammar that matches the test files
warpy_grammar = r"""
start: programa

programa    : sentenca*

sentenca    : comando
            | declaracao
            | loop

declaracao  : identificador ":" tipo "=" chamada
tipo        : "dg" | "servitor" | "blob" | "psykers" | "void_shields"

comando     : NOME_COMANDO "(" [args] ")"

args        : expressao ("," expressao)*

chamada     : NOME_COMANDO "(" [args] ")"

comandos    : comando+
loop        : "for" identificador "in" expr_range ":" comandos

expr_range  : expressao ".." expressao

expressao   : numero
            | identificador
            | chamada
            | ESCAPED_STRING

NOME_COMANDO: "the_emperor_protects"|"only_in_death_does_duty_end"|"even_in_death_i_still_serve"|"no_pity_no_remorse_no_fear"|"burn_the_heretic"|"pain_is_temporary_glory_is_forever"|"faith_is_my_shield"|"we_are_angels_of_death"|"we_are_one"|"WAAAGH"|"taste_chaos"|"for_the_emperor"|"purge_the_xenos"|"the_emperors_will_be_done"|"fear_is_the_mind_killer"|"ave_imperator"|"the_path_is_set"|"farseers_vision"|"more_dakka"|"ork_cunning"|"blood_for_the_blood_god"|"let_the_galaxy_burn"|"servitor"
identificador: /[a-zA-Z_][a-zA-Z0-9_]*/
numero      : /\d+(\.\d+)?/

%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

# Command implementations
COMMANDS = {
    'the_emperor_protects': lambda: print("[LOG] The Emperor protects!"),
    'burn_the_heretic': lambda tgt: print(f"[ACTION] Burn the heretic: {tgt}"),
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
    'servitor': lambda: "servitor_instance"
}

# AST node definitions
class CommandNode:
    def __init__(self, name, args):
        print('DEBUG CommandNode:', name, args)
        self.name = name
        self.args = args
    
    def execute(self, context):
        handler = COMMANDS.get(self.name)
        if handler:
            try:
                # Resolve variables in arguments
                resolved_args = []
                for arg in self.args:
                    if isinstance(arg, str) and arg in context:
                        resolved_args.append(context[arg])
                    else:
                        resolved_args.append(arg)
                
                if resolved_args:
                    handler(*resolved_args)
                else:
                    handler()
            except TypeError:
                # Fallback for commands that don't take arguments
                handler()
        else:
            print(f"Unknown command: {self.name}")

class DeclarationNode:
    def __init__(self, varname, typename, callnode):
        self.varname = varname
        self.typename = typename
        self.callnode = callnode
    
    def execute(self, context):
        if isinstance(self.callnode, CommandNode):
            # Execute the call and store the result
            result = self.callnode.execute(context)
            context[self.varname] = result
        else:
            context[self.varname] = self.callnode
        print(f"[DECL] Variable {self.varname} of type {self.typename} declared")

class LoopNode:
    def __init__(self, varname, start, end, commands):
        self.varname = varname
        self.start = start
        self.end = end
        self.commands = commands
    
    def execute(self, context):
        print('DEBUG LoopNode:', self.varname, self.start, self.end, type(self.start), type(self.end))
        for i in range(int(self.start), int(self.end) + 1):
            context[self.varname] = i
            for cmd in self.commands:
                cmd.execute(context)

# Transformer to build AST
class WarpyTransformer(Transformer):
    def __init__(self):
        self.env = {}

    def _maybe_transform(self, val):
        return self.transform(val) if isinstance(val, Tree) else val

    def start(self, programa):
        return programa

    def programa(self, *sentencas):
        return list(sentencas)

    def sentenca(self, stmt):
        return stmt

    def declaracao(self, children):
        varname, typename, callnode = children
        return DeclarationNode(varname, typename, callnode)

    def comando(self, children):
        print('DEBUG comando:', children, [type(c) for c in children])
        name = str(children[0]) if children else None
        args = children[1] if len(children) > 1 else []
        return CommandNode(name, args)

    def chamada(self, children):
        print('DEBUG chamada:', children, [type(c) for c in children])
        name = str(children[0]) if children else None
        args = children[1] if len(children) > 1 else []
        return CommandNode(name, args)

    def expressao(self, val):
        return self._maybe_transform(val)

    def expr_range(self, children):
        start_tree, end_tree = children
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
        varname, range_tuple, comandos = children
        # comandos is a list of lists, flatten it
        if isinstance(comandos, list) and len(comandos) == 1 and isinstance(comandos[0], list):
            comandos = comandos[0]
        if not isinstance(range_tuple, tuple) or len(range_tuple) != 2:
            raise ValueError("Invalid loop range.")
        start, end = range_tuple
        return LoopNode(varname, start, end, comandos)

    def comandos(self, *cmds):
        return list(cmds)

    def args(self, first, *rest):
        return [first] + list(rest)

    def numero(self, children):
        print('DEBUG numero:', children)
        def extract_num(val):
            if isinstance(val, list):
                for v in val:
                    n = extract_num(v)
                    if n is not None:
                        return n
                return None
            if val is None:
                return None
            val_str = val.value if hasattr(val, 'value') else str(val)
            return int(val_str) if val_str.isdigit() else float(val_str)
        return extract_num(children)

    def identificador(self, children):
        print('DEBUG identificador:', children)
        def extract_str(val):
            if isinstance(val, list):
                for v in val:
                    s = extract_str(v)
                    if s is not None:
                        return s
                return None
            if val is None:
                return None
            return str(val.value) if hasattr(val, 'value') else str(val)
        return extract_str(children)

    def tipo(self, children):
        if not children:
            return None
        return children[0].value

    def ESCAPED_STRING(self, children):
        if not children:
            return None
        return children[0].value[1:-1]

def run_warpy_script(script_path: str):
    with open(script_path, 'r') as f:
        code = f.read()

    parser = Lark(warpy_grammar, parser='earley', start='start')
    parse_tree = parser.parse(code)

    transformer = WarpyTransformer()
    ast = transformer.transform(parse_tree)

    # Flatten the AST in case of nested lists
    def flatten(items):
        for x in items:
            if isinstance(x, list):
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
