# Linter da Linguagem WarPy40K

Um linter abrangente para a linguagem de programação WarPy40K. Verifica sintaxe, valida comandos e variáveis, e fornece mensagens de erro úteis para qualidade robusta de código.

> Veja o [README.md](../README.md) principal para visão geral do projeto, uso do interpretador e realce de sintaxe.

## Recursos

- **Validação de Sintaxe**: Garante que as regras de sintaxe do WarPy40K, estrutura de comandos, declarações de variáveis, atribuições, loops e condicionais estejam corretas.
- **Validação de Comandos**: Verifica se todos os comandos existem no conjunto de comandos WarPy40K, verifica sintaxe de argumentos e valida literais de string e referências de variáveis.
- **Análise de Variáveis**: Rastreia declarações e uso de variáveis, detecta variáveis não declaradas/não utilizadas e valida nomes contra palavras-chave reservadas.
- **Análise de Fluxo de Controle**: Valida estruturas de loop for/while, declarações de variáveis de loop e expressões condicionais.
- **Validação de Expressões Aritméticas**: Valida operações aritméticas (+, -, *, /, %) com precedência adequada de operadores e parênteses.
- **Verificações de Estilo de Código**: Detecta espaços em branco finais, linhas longas e comentários não suportados.

## Instalação

O linter é um script Python independente. Requer Python 3.6+ e nenhuma dependência extra.

```bash
chmod +x warpy_linter.py
python3 warpy_linter.py tests/test_fibonacci.wp40k
```

## Uso

```bash
python3 warpy_linter.py tests/test_fibonacci.wp40k
```

Para ajuda:
```bash
python3 warpy_linter.py --help
```

### Códigos de Saída
- `0` - Nenhum erro encontrado (avisos ainda podem estar presentes)
- `1` - Erros encontrados

## Códigos de Erro e Mensagens

### ❌ ERROS (Devem ser corrigidos)

| Código | Descrição | Exemplo | Correção |
|--------|-----------|---------|----------|
| `UNKNOWN_SYNTAX` | Sintaxe inválida | `sintaxe_invalida_aqui` | Consulte a documentação de sintaxe do WarPy40K |
| `UNKNOWN_COMMAND` | Comando não existe | `comando_desconhecido()` | Use comandos WarPy40K válidos |
| `MISSING_COLON` | Loop sem dois pontos | `for i in 1..5` | Adicione `:` no final |
| `INVALID_CONDITION` | Condição inválida | `while condicao_invalida:` | Use operadores de comparação |
| `UNDECLARED_VARIABLE` | Variável usada antes da declaração | `x = var_nao_declarada` | Declare a variável primeiro |
| `RESERVED_KEYWORD` | Usando palavra-chave reservada | `for: dg = 0` | Use nome de variável diferente |
| `INVALID_VAR_DECL` | Declaração de variável inválida | `var_ruim: tipo_invalido = 123` | Use `variavel: tipo = valor` |
| `MISSING_PARENTHESIS` | Parênteses de fechamento ausente | `the_emperor_protects(` | Adicione `)` |
| `INVALID_STRING` | Literal de string inválida | `"string_nao_fechada` | Feche a string com `"` |
| `EMPTY_EXPRESSION` | Expressão vazia | `x = ` | Forneça expressão válida |
| `INVALID_ARITHMETIC` | Expressão aritmética inválida | `x = a / 0` | Verifique divisão por zero ou operações inválidas |

### ⚠️ AVISOS (Devem ser revisados)

| Código | Descrição | Exemplo | Correção |
|--------|-----------|---------|----------|
| `TRAILING_WHITESPACE` | Espaços finais | `command() ` | Remova espaços finais |
| `LINE_TOO_LONG` | Linha > 120 caracteres | Linha muito longa... | Divida em múltiplas linhas |
| `UNUSED_VARIABLE` | Variável declarada mas não usada | `x: dg = 0` | Use a variável ou remova |
| `UNDECLARED_VARIABLE` | Variável usada mas não declarada | `x = alguma_var` | Declare a variável primeiro |
| `INCOMPLETE_COMMAND` | Comando parece incompleto | `command(` | Verifique parênteses ausentes ou erros de sintaxe |

### ℹ️ INFO (Informativo)

| Código | Descrição | Exemplo |
|--------|-----------|---------|
| `INCOMPLETE_COMMAND` | Comando parece incompleto | `command(` |

## Exemplos

### ✅ Código WarPy40K Válido
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

# Operações aritméticas
x: dg = 10
y: dg = 3
z: dg = x * y + 2  # 32
remainder: dg = x % y  # 1
```

### ❌ Código com Erros
```warpy40k
invalid_syntax_here
unknown_command()
for i in 1..5  # Dois pontos ausentes
while invalid_condition:  # Condição inválida
    for_the_emperor()
x = undeclared_var  # Variável não declarada
```

## Integração

### Integração VS Code
Adicione às suas configurações do VS Code para linting automático:

```json
{
    "files.associations": {
        "*.wp40k": "plaintext"
    },
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": false,
    "python.linting.mypyEnabled": false,
    "python.linting.customLinterEnabled": true,
    "python.linting.customLinterPath": "./warpy_linter.py",
    "python.linting.customLinterArgs": ["${file}"]
}
```

### Git Hooks
Adicione ao seu hook pre-commit:

```bash
#!/bin/bash
# .git/hooks/pre-commit

for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.wp40k$'); do
    python3 warpy_linter.py "$file"
    if [ $? -ne 0 ]; then
        echo "Linting falhou para $file"
        exit 1
    fi
done
```

## Configuração

O linter foi projetado para ser leve e não requer arquivos de configuração. Todas as regras são incorporadas e seguem as especificações da linguagem WarPy40K.

## Solução de Problemas e FAQ

**P: Quais operações aritméticas são suportadas?**
R: WarPy40K suporta adição (+), subtração (-), multiplicação (*), divisão (/) e módulo (%) com precedência adequada de operadores e parênteses.

**P: Posso usar o linter no meu editor ou CI?**
R: Sim! Veja a seção de integração acima para VS Code e Git hooks.

## Contribuindo

Para estender o linter:
1. Adicione novos métodos de validação à classe `WarPy40KLinter`
2. Atualize o conjunto `valid_commands` com novos comandos
3. Adicione novos códigos de erro à classe `LintIssue`
4. Atualize esta documentação

## Licença

Este linter faz parte do projeto WarPy40K e segue os mesmos termos de licença. Veja `LICENSE` para detalhes.

---

*Pelo Imperador!* 🛡️ 