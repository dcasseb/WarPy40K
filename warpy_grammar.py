from lark import Lark, Transformer, v_args

# Versão simplificada da gramática sem indentação complexa
warpy_grammar = r"""
programa    : sentenca*

sentenca    : comando
            | declaracao
            | loop

comando     : nome_comando "(" [args] ")"

nome_comando: "the_emperor_protects"
            | "only_in_death_does_duty_end"
            | "even_in_death_i_still_serve"
            | "no_pity_no_remorse_no_fear"
            | "burn_the_heretic"
            | "pain_is_temporary_glory_is_forever"
            | "faith_is_my_shield"
            | "we_are_angels_of_death"
            | "we_are_one"
            | "WAAAGH"
            | "taste_chaos"
            | "for_the_emperor"
            | "purge_the_xenos"
            | "the_emperors_will_be_done"
            | "fear_is_the_mind_killer"
            | "ave_imperator"
            | "the_path_is_set"
            | "farseers_vision"
            | "more_dakka"
            | "ork_cunning"
            | "blood_for_the_blood_god"
            | "let_the_galaxy_burn"
            | "servitor"

args        : expressao ("," expressao)*

declaracao  : identificador ":" tipo "=" expressao
tipo        : "dg" | "servitor" | "blob" | "psykers" | "void_shields"

loop        : "for" identificador "in" expr_range ":" comando+

expr_range  : expressao ".." expressao

expressao   : numero | identificador | chamada | string
chamada     : nome_comando "(" [args] ")"
string      : "\"" texto "\""

texto       : /[^"]+/
identificador: /[a-zA-Z_][a-zA-Z0-9_]*/
numero      : /\d+(\.\d+)?/

%import common.WS
%ignore WS
"""

# Comandos disponíveis
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

@v_args(inline=True)
class WarPyTransformer(Transformer):
    def __init__(self):
        self.env = {}

    def programa(self, *sentencas):
        for sentenca in sentencas:
            if sentenca:
                self._execute(sentenca)
        return sentencas

    def sentenca(self, stmt):
        return stmt

    def comando(self, nome_comando, *args):
        return ('cmd', str(nome_comando), args if args else ())

    def declaracao(self, identificador, tipo, expressao):
        return ('decl', str(identificador), str(tipo), expressao)

    def loop(self, identificador, expr_range, *comandos):
        return ('loop', str(identificador), expr_range, comandos)

    def expr_range(self, start, end):
        return range(int(start), int(end) + 1)

    def expressao(self, value):
        return value

    def numero(self, tok):
        return float(tok) if '.' in str(tok) else int(tok)

    def identificador(self, tok):
        var_name = str(tok)
        return self.env.get(var_name, var_name)

    def chamada(self, nome_comando, *args):
        return ('call', str(nome_comando), args if args else ())

    def nome_comando(self, tok):
        return str(tok)

    def tipo(self, tok):
        return str(tok)

    def args(self, *args):
        return args

    def _execute(self, stmt):
        if isinstance(stmt, tuple):
            if stmt[0] == 'cmd':
                _, name, args = stmt
                handler = COMMANDS.get(name)
                if handler:
                    try:
                        if args:
                            # Resolver variáveis nos argumentos
                            resolved_args = []
                            for arg in args:
                                if isinstance(arg, str) and arg in self.env:
                                    resolved_args.append(self.env[arg])
                                else:
                                    resolved_args.append(arg)
                            handler(*resolved_args)
                        else:
                            handler()
                    except TypeError:
                        handler()
                else:
                    print(f"Unknown command: {name}")
            
            elif stmt[0] == 'call':
                _, name, args = stmt
                handler = COMMANDS.get(name)
                if handler:
                    try:
                        if args:
                            return handler(*args)
                        else:
                            return handler()
                    except TypeError:
                        return handler()
            
            elif stmt[0] == 'decl':
                _, name, tipo, value = stmt
                # Executar chamada se for uma chamada de função
                if isinstance(value, tuple) and value[0] == 'call':
                    actual_value = self._execute(value)
                    self.env[name] = actual_value
                else:
                    self.env[name] = value
                print(f"[DECL] Variable {name} of type {tipo} declared")
            
            elif stmt[0] == 'loop':
                _, var_name, expr_range, comandos = stmt
                for i in expr_range:
                    self.env[var_name] = i
                    for comando in comandos:
                        if comando:
                            self._execute(comando)


# Classe do indentador não é necessária para esta versão simplificada
class WarPyIndenter:
    pass