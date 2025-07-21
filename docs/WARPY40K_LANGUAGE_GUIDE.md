# Guia da Linguagem WarPy40K

## Introdução

**WarPy40K** é uma linguagem de programação experimental inspirada no universo Warhammer 40.000. Ela foi projetada para ser divertida, legível e expressiva, com um conjunto único de comandos e uma sintaxe simples e acessível. Este guia cobre todos os aspectos da linguagem, desde variáveis e tipos até loops, condicionais e o conjunto completo de comandos.

---

## 1. Estrutura de Arquivo e Execução de Código

- Arquivos fonte WarPy40K usam a extensão `.wp40k`.
- Você pode executar um script com:
  ```bash
  python3 warpy_interpreter.py tests/your_script.wp40k
  ```
- Verifique seu código para erros e estilo:
  ```bash
  python3 warpy_linter.py tests/your_script.wp40k
  ```

---

## 2. Visão Geral da Sintaxe da Linguagem

### 2.1. Declarações

Um programa WarPy40K é uma sequência de **declarações**. Cada declaração pode ser:
- Uma declaração de variável
- Uma atribuição
- Uma chamada de comando
- Um loop (`for` ou `while`)
- Um condicional (`if`/`else`)

### 2.2. Comentários

- Comentários começam com `#` e continuam até o final da linha.
- Comentários são ignorados durante a execução e podem ser usados para documentação.
- Exemplo:
  ```warpy40k
  # Este é um comentário
  i: dg = 0  # Inicializar contador
  ```

---

## 3. Variáveis e Tipos

### 3.1. Declaração

Declare uma variável com um tipo e valor inicial:
```warpy40k
nome_variavel: tipo = valor
```
- Exemplo:
  ```warpy40k
  i: dg = 0
  name: servitor = "imperial_servant"
  power: psykers = 100
  ```

#### Tipos Suportados

| Tipo         | Descrição                          | Valor de Exemplo   |
|--------------|------------------------------------|--------------------|
| `dg`         | Número genérico (inteiro/float)    | `0`, `42`, `3.14`  |
| `servitor`   | String ou identificador            | `"servant"`        |
| `blob`       | Dados arbitrários (string/número)  | `"data"`, `123`    |
| `psykers`    | Número, frequentemente para poder psíquico | `100`              |
| `void_shields` | Booleano ou status               | `true`, `false`    |

### 3.2. Atribuição

Atribua um novo valor a uma variável existente:
```warpy40k
nome_variavel = expressão
```
- Exemplo:
  ```warpy40k
  i = i + 1
  name = "new_name"
  ```

---

## 4. Expressões

### 4.1. Literais

- **Números:** `0`, `42`, `3.14`
- **Strings:** `"hello world"`
- **Booleanos:** `true`, `false` (como valores para `void_shields`)

### 4.2. Variáveis

- Use nomes de variáveis diretamente em expressões:
  ```warpy40k
  result = i + power
  ```

### 4.3. Operações Aritméticas

WarPy40K suporta um conjunto completo de operações aritméticas com precedência adequada de operadores:

#### Operadores Básicos

| Operador | Descrição | Exemplo | Resultado |
|----------|-----------|---------|-----------|
| `+` | Adição | `a + b` | Soma de a e b |
| `-` | Subtração | `a - b` | Diferença de a e b |
| `*` | Multiplicação | `a * b` | Produto de a e b |
| `/` | Divisão | `a / b` | Quociente de a dividido por b |
| `%` | Módulo | `a % b` | Resto de a dividido por b |

#### Exemplos

```warpy40k
# Aritmética básica
a: dg = 10
b: dg = 3
c: dg = 2

sum: dg = a + b        # 13
diff: dg = a - b       # 7
product: dg = a * b    # 30
quotient: dg = a / b   # 3.333...
remainder: dg = a % b  # 1
```

#### Precedência de Operadores

Operadores aritméticos seguem regras de precedência padrão (maior para menor):

1. **Parênteses** `()` - Precedência mais alta
2. **Multiplicação** `*`, **Divisão** `/`, **Módulo** `%` - Mesma precedência
3. **Adição** `+`, **Subtração** `-` - Mesma precedência

```warpy40k
# Exemplos de precedência
result1: dg = 2 + 3 * 4    # 14 (não 20)
result2: dg = (2 + 3) * 4  # 20
result3: dg = 10 / 2 + 3   # 8 (não 2)
result4: dg = 10 % 3 + 1   # 2
```

#### Expressões Complexas

Você pode combinar múltiplas operações em uma única expressão:

```warpy40k
# Aritmética complexa
x: dg = 5
y: dg = 2
z: dg = 3

# Múltiplas operações
result: dg = x * y + z     # 13 (5 * 2 + 3)
result2: dg = x + y * z    # 11 (5 + 2 * 3)
result3: dg = (x + y) * z  # 21 ((5 + 2) * 3)

# Usando módulo
remainder: dg = x % y      # 1
power: dg = x * x % 3      # 1 (25 % 3)
```

#### Notas sobre Divisão e Módulo

- **Divisão** (`/`) sempre retorna um resultado float, mesmo para divisão de inteiros
- **Módulo** (`%`) funciona com inteiros e floats
- Divisão por zero causará um erro de execução
- Módulo por zero causará um erro de execução

```warpy40k
# Exemplos de divisão
a: dg = 10
b: dg = 3

div: dg = a / b        # 3.3333333333333335
mod: dg = a % b        # 1

# Aritmética com float
c: dg = 10.5
d: dg = 2.5

float_div: dg = c / d  # 4.2
float_mod: dg = c % d  # 0.5
```

### 4.4. Comparações

- Operadores suportados: `==`, `!=`, `<`, `>`, `<=`, `>=`
  ```warpy40k
  if i >= 0:
      ...
  ```

### 4.5. Operadores Lógicos

- Use `and` e `or` para combinar condições:
  ```warpy40k
  if i > 0 and power < 100:
      ...
  ```

---

## 5. Comandos

Comandos são o coração do WarPy40K, cada um inspirado no lore de Warhammer 40K. Eles são chamados como funções, com ou sem argumentos.

### 5.1. Sintaxe de Comandos

```warpy40k
nome_comando()
nome_comando(argumento)
```

### 5.2. Lista Completa de Comandos

| Comando                        | Exemplo de Uso                       | Descrição/Efeito (implementação padrão)                   |
|--------------------------------|--------------------------------------|------------------------------------------------------------|
| `the_emperor_protects()`       | `the_emperor_protects()`             | Registra: The Emperor protects!                           |
| `only_in_death_does_duty_end()`| `only_in_death_does_duty_end()`      | Registra: Only in death does duty end.                    |
| `even_in_death_i_still_serve()`| `even_in_death_i_still_serve()`      | Registra: Even in death, I still serve!                   |
| `no_pity_no_remorse_no_fear()` | `no_pity_no_remorse_no_fear()`       | Registra: No pity, no remorse, no fear!                   |
| `burn_the_heretic(arg)`        | `burn_the_heretic("traitor")`        | Registra: Burn the heretic: arg                           |
| `pain_is_temporary_glory_is_forever()` | ... | Registra: Pain is temporary, glory is forever.            |
| `faith_is_my_shield()`         | `faith_is_my_shield()`               | Registra: Faith is my shield!                             |
| `we_are_angels_of_death()`     | `we_are_angels_of_death()`           | Registra: We are the Angels of Death!                     |
| `we_are_one()`                 | `we_are_one()`                       | Registra: We are one.                                     |
| `WAAAGH()`                     | `WAAAGH()`                           | Registra: The orks rally!                                 |
| `taste_chaos()`                | `taste_chaos()`                      | Registra: Warp corrupts your soul.                        |
| `for_the_emperor()`            | `for_the_emperor()`                  | Registra: For the Emperor!                                |
| `purge_the_xenos(arg)`         | `purge_the_xenos("xenos")`           | Registra: Xenos purged: arg!                              |
| `the_emperors_will_be_done()`  | `the_emperors_will_be_done()`        | Registra: The Emperor's will is fulfilled.                |
| `fear_is_the_mind_killer()`    | `fear_is_the_mind_killer()`          | Registra: Fear suppressed.                                |
| `ave_imperator()`              | `ave_imperator()`                    | Registra: Ave Imperator! Glory to the Emperor!            |
| `the_path_is_set()`            | `the_path_is_set()`                  | Registra: The path is set. We proceed.                    |
| `farseers_vision()`            | `farseers_vision()`                  | Registra: The Farseer foresees...                         |
| `more_dakka()`                 | `more_dakka()`                       | Registra: More dakka! Fire everything!                    |
| `ork_cunning()`                | `ork_cunning()`                      | Registra: Cunning plan!                                   |
| `blood_for_the_blood_god()`    | `blood_for_the_blood_god()`          | Registra: Blood for the Blood God!                        |
| `let_the_galaxy_burn()`        | `let_the_galaxy_burn()`              | Registra: The galaxy burns!                               |
| `servitor()`                   | `servitor()`                         | Retorna: "servitor_instance" (para uso avançado)         |
| `vox_cast(msg)`                | `vox_cast("message")`                | Imprime mensagem com prefixo [VOX] (estilo Warhammer 40K) |

---

## 6. Fluxo de Controle

### 6.1. Loops For

Itere sobre um intervalo de números:
```warpy40k
for i in 1..5:
    the_emperor_protects()
```
- A variável do loop (`i`) assume valores do início ao fim (inclusive).

### 6.2. Loops While

Repita enquanto uma condição for verdadeira:
```warpy40k
while i < 10:
    for_the_emperor()
    i = i + 1
```

### 6.3. Condicionais

Ramifique seu código com `if` e `else`:
```warpy40k
if power > 50:
    the_emperors_will_be_done()
    ave_imperator()
else:
    fear_is_the_mind_killer()
    burn_the_heretic("weak_psyker")
```
- Você pode aninhar declarações `if` e usar operadores lógicos.

---

## 7. Exemplo: Sequência de Fibonacci

```warpy40k
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

---

## 8. Recursos Avançados

- **Loops Aninhados:** Você pode aninhar loops `for` e `while`.
- **Condicionais Encadeados:** Use `and`/`or` para condições complexas.
- **Concatenação de Strings:** Use `+` para concatenar strings (ex: `"heretic_" + str(i)`).
- **Todos os comandos podem ser chamados com ou sem argumentos conforme especificado.**

---

## 9. Linting e Melhores Práticas

- Use o linter para capturar erros e questões de estilo antes de executar seu código.
- Evite usar variáveis não declaradas.
- Mantenha linhas com menos de 120 caracteres para legibilidade.
- Use comentários para documentar seu código e explicar lógica complexa.

---

## 10. Suporte de Editores

- **VS Code:** Instale a extensão de sintaxe WarPy40K para destaque completo e suporte a temas.
- **Sublime Text:** Use a definição de sintaxe fornecida para destaque rico.

---

## 11. Estrutura do Projeto

Um projeto WarPy40K típico pode parecer com:
```
WarPy40K/
  warpy_interpreter.py
  warpy_linter.py
  tests/
    your_script.wp40k
  warpy40k-syntax/
  warpy40k-sublime/
  ...
```

---

## 12. Leitura Adicional

- Veja o `README.md` para instalação e uso.
- Veja o `LINTER_README.md` para códigos de erro e integração.
- Explore o diretório `tests/` para mais scripts de exemplo.

---

## 13. Referência Rápida

### Declaração de Variável
```warpy40k
x: dg = 10
```
### Atribuição
```warpy40k
x = x + 1
```
### Loop For
```warpy40k
for i in 1..5:
    command()
```
### Loop While
```warpy40k
while x < 10:
    command()
```
### If/Else
```warpy40k
if x > 0:
    command()
else:
    other_command()
```
### Chamada de Comando
```warpy40k
the_emperor_protects()
burn_the_heretic("traitor")
```

---

## 14. Dicas

- Use nomes de variáveis significativos.
- Use o linter para verificar seu código antes de executar.
- Explore o conjunto de comandos para saída divertida e temática.
- Tente combinar loops, condicionais e comandos para criar scripts interessantes!

---

*Pelo Imperador!* 