# WarPy40K

A Warhammer 40K-themed toy programming language and interpreter, designed for fun, learning, and extensibility. WarPy40K features a custom syntax, unique commands, and robust tooling including a linter and syntax highlighting extensions for VS Code and Sublime Text.

## Features

- **Custom Language**: Warhammer 40K-inspired syntax and commands
- **Arithmetic Operations**: Full support for addition (+), subtraction (-), multiplication (*), division (/), and modulo (%) with proper operator precedence
- **Control Flow**: If-else conditionals, for loops, and while loops
- **Variables**: Typed variable declarations and assignments
- **Interpreter**: Execute `.wp40k` scripts directly with Python
- **Linter**: Comprehensive static analysis for syntax, variables, and style ([see linter docs](./docs/LINTER_README.md))
- **Syntax Highlighting**: Official extensions for VS Code and Sublime Text
- **Test Files**: Example scripts for learning and validation

## Installation

1. Install dependencies:
   ```bash
   pip install lark-parser
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/WarPy40K.git
   cd WarPy40K
   ```

## Integrantes

- Nome: [Seu Nome] - Matrícula: [Sua Matrícula] - Turma: [Sua Turma]

## Usage

To run a WarPy40K script:
```bash
python3 warpy_interpreter.py tests/test_fibonacci.wp40k
```

To lint a script:
```bash
python3 warpy_linter.py tests/test_fibonacci.wp40k
```

## Example

```warpy40k
# Basic arithmetic operations
a: dg = 10
b: dg = 3
c: dg = 2

# Addition and subtraction
result1: dg = a + b      # 13
result2: dg = a - b      # 7

# Multiplication and division
result3: dg = a * b      # 30
result4: dg = a / b      # 3.333...

# Modulo operation
result5: dg = a % b      # 1

# Complex expressions with precedence
complex: dg = a + b * c  # 16 (not 26 due to precedence)

# Parentheses to override precedence
paren: dg = (a + b) * c  # 26

# Fibonacci sequence with arithmetic
start: dg = 0
end: dg = 5

a: dg = 0
b: dg = 1
i: dg = 0
c: dg = 0

if start == 0:
    burn_the_heretic(a)

for i in 1..end:
    c = a + b
    a = b
    b = c
    if i >= start and i <= end:
        burn_the_heretic(a)
```

## Tooling

- **Linter**: See [LINTER_README.md](./docs/LINTER_README.md) for error codes, integration, and advanced usage.
- **Syntax Highlighting**:
  - VS Code: See `warpy40k-syntax/README.md`
  - Sublime Text: See `warpy40k-sublime/README.md`

## Referências

Este projeto foi desenvolvido utilizando as seguintes referências e tecnologias:

- **Lark Parser**: Biblioteca Python para parsing e análise sintática. Utilizada como base para implementar a análise léxica e sintática da linguagem WarPy40K. Site oficial: [https://github.com/lark-parser/lark](https://github.com/lark-parser/lark)
- **Warhammer 40K Universe**: Inspiração temática para nomes de comandos, tipos de dados e estética geral da linguagem. Propriedade da Games Workshop.
- **Crafting Interpreters**: Conceitos fundamentais de design de linguagens de programação e implementação de interpretadores, especialmente para estruturas de AST e avaliação de expressões.
- **Python Official Documentation**: Referência para implementação do interpretador e estruturas de dados.

### Contribuições Originais

- **Gramática WarPy40K**: Sintaxe completamente original inspirada no universo Warhammer 40K
- **Sistema de Tipos Temáticos**: Tipos de dados únicos (`dg`, `servitor`, `blob`, `psykers`, `void_shields`)
- **Comandos Temáticos**: Set completo de comandos inspirados no lore do Warhammer 40K
- **Linter Integrado**: Sistema de análise estática customizado para a linguagem
- **Extensões de Syntax Highlighting**: Plugins originais para VS Code e Sublime Text

## Estrutura do Código

O projeto está organizado nos seguintes módulos principais:

### Arquivos Principais

- **`warpy_interpreter.py`**: Contém o interpretador principal e todas as etapas de compilação
  - **Análise Léxica**: Definida na gramática Lark (linhas 6-65) com tokens, palavras-chave e operadores
  - **Análise Sintática**: Parser Lark automaticamente constrói a AST baseada na gramática EBNF
  - **Análise Semântica**: Implementada nas classes de nós AST (linhas 117-350) com verificação de tipos e contexto
  - **Interpretação/Execução**: Método `evaluate()` e `execute()` em cada nó AST (linhas 350-600)

- **`warpy_linter.py`**: Análise estática e detecção de erros
  - Verificação de sintaxe, variáveis não declaradas, tipos incompatíveis
  - Sistema de códigos de erro estruturado

- **`warpy_grammar.py`**: Definição da gramática em formato isolado para reutilização

### Estruturas de Dados Principais

- **AST Nodes**: Classes para representar diferentes construções da linguagem
  - `CommandNode`: Execução de comandos
  - `DeclarationNode`: Declaração de variáveis
  - `AssignmentNode`: Atribuição de valores
  - `LoopNode`/`WhileLoopNode`: Estruturas de repetição
  - `ConditionalNode`: Estruturas condicionais
  - Nós de expressões aritméticas (`SumNode`, `SubtractionNode`, etc.)

- **Context**: Dicionário para armazenamento de variáveis e estado durante execução

### Etapas de Compilação

1. **Análise Léxica**: Lark tokeniza o código fonte baseado na gramática
2. **Análise Sintática**: Lark constrói a AST automaticamente
3. **Transformação**: `WarpyTransformer` converte a AST Lark em nós customizados
4. **Análise Semântica**: Verificação de tipos e contexto durante a transformação
5. **Interpretação**: Execução através do método `execute()` do nó raiz

## Bugs/Limitações/Problemas Conhecidos

### Limitações Atuais

1. **Sistema de Tipos Simples**: Apenas verificação básica de tipos, sem inferência automática
2. **Escopo de Variáveis**: Apenas escopo global, sem suporte a escopos locais em funções
3. **Estruturas de Dados**: Não há suporte para arrays, structs ou objetos complexos
4. **Funções Definidas pelo Usuário**: Apenas comandos pré-definidos, sem definição de funções customizadas
5. **Sistema de Módulos**: Não há suporte para importação de outros arquivos WarPy40K

### Problemas Conhecidos

1. **Tratamento de Erros**: Algumas mensagens de erro poderiam ser mais específicas
2. **Performance**: Para scripts muito grandes, a interpretação pode ser lenta
3. **Depuração**: Falta de ferramentas de debug integradas

### Melhorias Incrementais Sugeridas

1. **Melhor Tratamento de Erros**: Adicionar números de linha nas mensagens de erro
2. **Escopo de Variáveis**: Implementar pilha de contextos para escopos aninhados
3. **Novos Tipos**: Adicionar tipos `array` e `map` para estruturas de dados
4. **Modo Debug**: Adicionar flag `--debug` para execução passo-a-passo
5. **Otimizações**: Cache de AST para arquivos não modificados
6. **Documentação**: Melhorar documentação inline e exemplos

## Project Structure

- `warpy_interpreter.py`: Interpreter and runtime logic
- `warpy_linter.py`: Linter for static analysis
- `tests/`: Example scripts including arithmetic tests
- `warpy40k-syntax/`: VS Code syntax highlighting extension
- `warpy40k-sublime/`: Sublime Text syntax highlighting extension

## Contributing

Contributions are welcome! Please see the linter and syntax extension READMEs for extension guidelines.

## License

This project is licensed under the same terms as the WarPy40K project. See `LICENSE` for details.

---

*For the Emperor!*

```text
                                                                                                                                                             
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@@@@        @@@@@@@@@@@@   @@@@@@@@@@@@        @@@@@@@@  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@           
            @@@@@@                 @@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@        @@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@                 @@@@@@            
               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@               
                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@        @@@@@@ @@@@@@@@@@@@@@@@@@@  @@@@@        @@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
                 @@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@         @       @@@@@@@@@@@@@@@       @         @@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@                 
                   @@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@               @@@@@@@@@@@@@@@@@               @@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@                   
                          @@@@@@@@@@@@@@@@@@@@  @@@@@@@@@@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@@@@@@@@@  @@@@@@@@@@@@@@@@@@@@                          
                       @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@                       
                         @@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@                         
                           @@@@@      @@@@@@@@@@@  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@@@@@@@       @@@@                           
                                  @@@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@                                  
                               @@@@@@@@@@@@@   @@@@@@@ @@@@@@@@@@@@@@@ @@@@@@@@@@@@@@@@@@@@@@@ @@@@@@@@@ @@@@@ @@@@@@@   @@@@@@@@@@@@@                               
                                 @@@@@@@@    @@@@@@@  @@@@@@@@@@@@@@@ @@@@@@@@@@@@@@@@@@@@@@@@@ @@@@@@@@@ @@@@@@ @@@@@@@    @@@@@@@@                                 
                                   @@@     @@@@@@@@ @@@@@@@@@@@@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@@@@@@@@@@ @@@@@@@@     @@@                                   
                                         @@@@@@@@  @@@@@@@ @@@@@     @@@@@ @@@@@@@@@@@@@@@@@@@@@     @@@@@ @@@@@@@  @@@@@@@@                                         
                                         @@@@@@@  @@@@@@@ @@@@@         @@@@@@@@@@@@@@@@@@@@@         @@@@@ @@@@@@@  @@@@@@@                                         
                                            @@   @@@@@@@  @@             @@@@@@@@@@@@@@@@@@@             @@  @@@@@@@   @@                                            
                                                 @@@@@@                  @@@@@@@@@@@@@@@@@@@                  @@@@@@                                                 
                                                                        @@@@@@@@@@@@@@@@@@@@@                                                                        
                                                                       @@@@@@@@@@@@@@@@@@@@@@@                                                                       
                                                                      @@@@@ @@@@@@@@@@@@@@@@@@@   @                                                                  
                                                                 @@@@@@@@  @@@@@@@@@@@@@@@ @@@@@@@@@@                                                                
                                                                 @@@@@@@@   @@@@@@@@@@@@@@  @@@@@ @@                                                                 
                                                                 @@@@@ @@@@  @@@@@@@@@@@ @@@@@ @@@ @                                                                 
                                                                 @@@@  @@@     @@@@@@@   @@@@@ @@@@                                                                  
                                                                 @@@ @@          @@@             @@@                                                                 
                                                                @@@@                            @@@@                                                                 
                                                                   @@                          @@                                                                    