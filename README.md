# WarPy40K

É uma linguagem DSL de programação e interpretador "toy" com tema de Warhammer 40K, projetada para diversão, aprendizado e extensibilidade. WarPy40K apresenta sintaxe personalizada, comandos exclusivos e ferramentas robustas, incluindo um linter e extensões de destaque de sintaxe para VS Code e Sublime Text.

## Sobre o Universo Warhammer 40K

### O Que é Warhammer 40,000?

Warhammer 40,000 (também conhecido como Warhammer 40K ou WH40K) é um universo de ficção científica criado pela Games Workshop em 1987. Ambientado no ano 40,000 (daí o nome), é um futuro sombrio onde "há apenas guerra" (*"In the grim darkness of the far future, there is only war"*).

### O Universo

O universo de Warhammer 40K é caracterizado por:

- **Imperium of Man**: Um império galáctico totalitário liderado pelo God-Emperor of Mankind, que governa milhões de mundos através de uma burocracia massiva e opressiva
- **Space Marines**: Guerreiros geneticamente modificados, os Adeptus Astartes, conhecidos como "Angels of Death"
- **Chaos**: Forças demoníacas da Warp (uma dimensão paralela) que corrompem e destroem
- **Xenos**: Raças alienígenas como Orks (criaturas brutais obcecadas com guerra), Eldar (antiga raça psíquica), Tyranids (enxame devorador), entre outros
- **Technological Decay**: A humanidade perdeu muito conhecimento tecnológico, tratando máquinas como objetos religiosos
- **Grimdark**: O universo é intencionalmente sombrio, onde não há "mocinhos" verdadeiros e a sobrevivência é uma luta constante

### O Jogo de Tabuleiro

Warhammer 40,000 é um jogo de estratégia em miniatura onde:

1. **Exércitos**: Cada jogador monta um exército escolhendo entre diferentes facções (Space Marines, Orks, Chaos, Eldar, etc.)
2. **Miniaturas**: Jogadores compram, montam e pintam miniaturas detalhadas representando soldados, veículos e criaturas
3. **Regras**: Sistema complexo de regras para movimento, combate, habilidades especiais e magia (poderes psíquicos)
4. **Dados**: Usa principalmente dados de 6 faces (d6) para determinar acertos, ferimentos e saves
5. **Turnos**: Jogadores alternam turnos movendo suas unidades, atirando e combatendo corpo-a-corpo
6. **Objetivos**: Vitória através de eliminação do inimigo ou controle de objetivos no tabuleiro
7. **Customização**: Listas de exército altamente customizáveis com diferentes unidades, equipamentos e estratégias

### Elementos Temáticos no WarPy40K

Nossa linguagem de programação incorpora elementos autênticos do universo Warhammer 40K:

#### Tipos de Dados Temáticos
- **`dg`** (Digit): Números, representando dados e cálculos táticos
- **`servitor`**: Referência aos servitors (humanos lobotomizados que operam máquinas)
- **`blob`**: Inspirado nas "blob squads" (grandes grupos de guardsmen imperiais)
- **`psykers`**: Referência aos psykers (humanos com poderes psíquicos)
- **`void_shields`**: Sistema de proteção de naves espaciais imperiais

#### Comandos Inspirados no Lore
- **`the_emperor_protects`**: Frase icônica de proteção imperial
- **`burn_the_heretic`**: Usado para output/print, referenciando a purificação de hereges
- **`vox_cast`**: Sistema de comunicação imperial para input/output
- **`WAAAGH`**: Grito de guerra dos Orks
- **`blood_for_the_blood_god`**: Invocação do Chaos God Khorne
- **`for_the_emperor`**: Grito de batalha dos Space Marines

### Objetivo do WarPy40K

O projeto WarPy40K tem múltiplos objetivos educacionais e recreativos:

#### Objetivos Educacionais
1. **Aprendizado de Compiladores**: Demonstrar conceitos de análise léxica, sintática e semântica
2. **Design de Linguagens**: Explorar como criar uma linguagem de programação com identidade própria
3. **Análise Estática**: Implementar um linter funcional para detecção de erros
4. **Tooling**: Desenvolver ferramentas auxiliares como syntax highlighting

#### Objetivos Recreativos
1. **Imersão Temática**: Permitir que fãs de Warhammer 40K programem usando vocabulário familiar
2. **Comunidade**: Criar uma ponte entre comunidades de programação e gaming
3. **Criatividade**: Inspirar projetos únicos que combinem hobbies diferentes

#### Objetivos Técnicos
1. **Funcionalidade Completa**: Suportar estruturas de controle, variáveis tipadas e operações aritméticas
2. **Extensibilidade**: Arquitetura que permite fácil adição de novos comandos e tipos
3. **Qualidade**: Código limpo, bem documentado e testado
4. **Acessibilidade**: Ferramentas que facilitam o uso (linter, syntax highlighting, exemplos)

### Por Que Warhammer 40K?

A escolha do universo Warhammer 40K para esta linguagem não é por acaso:

1. **Vocabulário Rico**: O universo possui terminologia técnica extensa que se adapta bem a conceitos de programação
2. **Comunidade Apaixonada**: Fãs de 40K apreciam referências autênticas e detalhadas ao lore
3. **Estética Distintiva**: A estética "grimdark" cria uma identidade visual e conceitual única
4. **Complexidade**: O universo é complexo o suficiente para inspirar funcionalidades avançadas
5. **Nostalgia e Diversão**: Combina o aprendizado técnico com elementos lúdicos familiares

O WarPy40K não é apenas uma linguagem de programação - é uma homenagem a um universo rico e uma ferramenta educacional que torna o aprendizado de compiladores mais envolvente e memorável.

*"Knowledge is power, guard it well."* - Adeptus Mechanicus

## Features

- **Linguagem Personalizada**: Sintaxe e comandos inspirados no Warhammer 40K
- **Operações Aritméticas**: Suporte completo para adição (+), subtração (-), multiplicação (*), divisão (/) e módulo (%) com a devida precedência de operadores
- **Fluxo de Controle**: Condicionais if-else, loops for e while
- **Variáveis**: Declarações e atribuições de variáveis tipadas
- **Interpretador**: Executa scripts `.wp40k` diretamente com Python
- **Linter**: Análise estática abrangente de sintaxe, variáveis e estilo ([consulte a documentação do linter](./docs/LINTER_README.md))
- **Destaque de Sintaxe**: Extensões oficiais para VS Code e Sublime Text
- **Arquivos de Teste**: Scripts de exemplo para aprendizado e validação
  
## Instalação

1. Instale as dependências:
   ```bash
   pip install lark-parser
   ```

2. Clone o repositório:
   ```bash
   git clone https://github.com/YOUR-USERNAME/WarPy40K.git
   cd WarPy40K
   ```

## Uso

To run a WarPy40K script:
```bash
python3 warpy_interpreter.py tests/test_fibonacci.wp40k
```

To lint a script:
```bash
python3 warpy_linter.py tests/test_fibonacci.wp40k
```

## Exemplo

```warpy40k
# Operações aritméticas básicas
a: dg = 10
b: dg = 3
c: dg = 2

# Adição e subtração
result1: dg = a + b      # 13
result2: dg = a - b      # 7

# Multiplicação e divisão
result3: dg = a * b      # 30
result4: dg = a / b      # 3.333...

# Operação módulo
result5: dg = a % b      # 1

# Expressões complexas com precedência
complex: dg = a + b * c  # 16 (não é 26 devido à precedência)

# Parênteses para substituir a precedência
paren: dg = (a + b) * c  # 26

# Sequência de Fibonacci com aritmética
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

- **Linter**: Veja [LINTER_README.md](./docs/LINTER_README.md) para erros de código, integração, e uso avançado.
- **Syntax Highlighting**:
  - VS Code: Veja `warpy40k-syntax/README.md`
  - Sublime Text: Veja `warpy40k-sublime/README.md`

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
