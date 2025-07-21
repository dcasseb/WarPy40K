from lark import Lark, Transformer

def run_test(grammar, test_code, token_name):
    class MyTransformer(Transformer):
        def __default_token__(self, children):
            val = children[0]
            if hasattr(val, 'value'):
                val = val.value
            val = str(val)
            if val.startswith('"') and val.endswith('"'):
                result = val[1:-1]
            else:
                result = val
            return result
        def comando(self, children):
            return children
    parser = Lark(grammar, parser="lalr", transformer=MyTransformer())
    print(f"\n[TEST] Grammar: {token_name}\nCode: {test_code}")
    parser.parse(test_code)

# 1. MYSTRING in command, /"[^\"]*"/
grammar1 = r'''
start: comando
comando: "vox_cast" "(" MYSTRING ")"
MYSTRING : /"[^\"]*"/
%import common.WS
%ignore WS
'''
test_code1 = 'vox_cast("Hello, world!")'
run_test(grammar1, test_code1, "MYSTRING")

# 2. MYSTRING in command, /".+"/
grammar2 = r'''
start: comando
comando: "vox_cast" "(" MYSTRING ")"
MYSTRING : /".+"/
%import common.WS
%ignore WS
'''
test_code2 = 'vox_cast("Hello, world!")'
run_test(grammar2, test_code2, "MYSTRING")

# 3. Just a string as the start rule
grammar3 = r'''
start: MYSTRING
MYSTRING : /"[^\"]*"/
%import common.WS
%ignore WS
'''
test_code3 = '"Hello, world!"'
run_test(grammar3, test_code3, "MYSTRING") 