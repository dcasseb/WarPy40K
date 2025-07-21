# Referência de Comandos WarPy40K

Este documento fornece uma referência completa de todos os comandos disponíveis na linguagem de programação WarPy40K. Imprima esta página para ter uma referência útil ao escrever scripts WarPy40K!

## Índice

1. [Categorias de Comandos](#categorias-de-comandos)
2. [Lista Completa de Comandos](#lista-completa-de-comandos)
3. [Exemplos de Uso de Comandos](#exemplos-de-uso-de-comandos)
4. [Função de Entrada](#função-de-entrada)
5. [Categorias de Comandos por Facção](#categorias-de-comandos-por-facção)

---

## Categorias de Comandos

Os comandos WarPy40K são organizados em várias categorias temáticas baseadas no universo Warhammer 40.000:

- **Comandos Imperiais**: Leais ao Imperador
- **Comandos do Caos**: Corrompidos pela Warp
- **Comandos Ork**: Brutais e astutos
- **Comandos Eldar**: Antigos e misteriosos
- **Comandos Gerais**: Utilitários universais
- **Função de Entrada**: Interação com usuário

---

## Lista Completa de Comandos

| Comando | Categoria | Uso | Efeito | Argumentos |
|---------|-----------|-----|--------|------------|
| `the_emperor_protects()` | Imperial | `the_emperor_protects()` | Registra: "The Emperor protects!" | Nenhum |
| `only_in_death_does_duty_end()` | Imperial | `only_in_death_does_duty_end()` | Registra: "Only in death does duty end." | Nenhum |
| `even_in_death_i_still_serve()` | Imperial | `even_in_death_i_still_serve()` | Registra: "Even in death, I still serve!" | Nenhum |
| `no_pity_no_remorse_no_fear()` | Imperial | `no_pity_no_remorse_no_fear()` | Registra: "No pity, no remorse, no fear!" | Nenhum |
| `pain_is_temporary_glory_is_forever()` | Imperial | `pain_is_temporary_glory_is_forever()` | Registra: "Pain is temporary, glory is forever." | Nenhum |
| `faith_is_my_shield()` | Imperial | `faith_is_my_shield()` | Registra: "Faith is my shield!" | Nenhum |
| `we_are_angels_of_death()` | Imperial | `we_are_angels_of_death()` | Registra: "We are the Angels of Death!" | Nenhum |
| `for_the_emperor()` | Imperial | `for_the_emperor()` | Registra: "For the Emperor!" | Nenhum |
| `the_emperors_will_be_done()` | Imperial | `the_emperors_will_be_done()` | Registra: "The Emperor's will is fulfilled." | Nenhum |
| `ave_imperator()` | Imperial | `ave_imperator()` | Registra: "Ave Imperator! Glory to the Emperor!" | Nenhum |
| `burn_the_heretic(arg)` | Imperial | `burn_the_heretic("traitor")` | Registra: "Burn the heretic: [arg]" | String/Expressão |
| `purge_the_xenos(arg)` | Imperial | `purge_the_xenos("alien")` | Registra: "Xenos purged: [arg]!" | String/Expressão |
| `fear_is_the_mind_killer()` | Imperial | `fear_is_the_mind_killer()` | Registra: "Fear suppressed." | Nenhum |
| `we_are_one()` | Geral | `we_are_one()` | Registra: "We are one." | Nenhum |
| `WAAAGH()` | Ork | `WAAAGH()` | Registra: "The orks rally!" | Nenhum |
| `more_dakka()` | Ork | `more_dakka()` | Registra: "More dakka! Fire everything!" | Nenhum |
| `ork_cunning()` | Ork | `ork_cunning()` | Registra: "Cunning plan!" | Nenhum |
| `taste_chaos()` | Caos | `taste_chaos()` | Registra: "Warp corrupts your soul." | Nenhum |
| `blood_for_the_blood_god()` | Caos | `blood_for_the_blood_god()` | Registra: "Blood for the Blood God!" | Nenhum |
| `let_the_galaxy_burn()` | Caos | `let_the_galaxy_burn()` | Registra: "The galaxy burns!" | Nenhum |
| `the_path_is_set()` | Eldar | `the_path_is_set()` | Registra: "The path is set. We proceed." | Nenhum |
| `farseers_vision()` | Eldar | `farseers_vision()` | Registra: "The Farseer foresees..." | Nenhum |
| `servitor()` | Geral | `servitor()` | Retorna: "servitor_instance" | Nenhum |
| `hear_the_emperors_voice(prompt)` | Entrada | `hear_the_emperors_voice("Enter name:")` | Solicita entrada do usuário | String opcional |
| `vox_cast(msg)` | Geral | `vox_cast("message")` | Imprime mensagem com prefixo [VOX] (estilo Warhammer 40K) | String/Expressão |

---

## Exemplos de Uso de Comandos

### Chamadas Básicas de Comandos
```warpy40k
# Comandos simples sem argumentos
the_emperor_protects()
for_the_emperor()
WAAAGH()

# Comandos com argumentos string
burn_the_heretic("traitor")
purge_the_xenos("tyranid")

# Comandos com argumentos de variáveis
target: servitor = "heretic"
burn_the_heretic(target)
```

### Comandos em Variáveis
```warpy40k
# Armazenar resultado de comando em variável
result: servitor = servitor()

# Usar entrada na declaração de variável
name: servitor = hear_the_emperors_voice("Enter your name:")
```

### Comandos em Expressões
```warpy40k
# Usar entrada em expressões aritméticas
count: dg = hear_the_emperors_voice("Enter count:")
result: dg = count + 5

# Usar entrada em condicionais
power: dg = hear_the_emperors_voice("Enter power level:")
if power > 50:
    the_emperors_will_be_done()
else:
    fear_is_the_mind_killer()
```

### Comandos em Loops
```warpy40k
# Comandos em loops for
for i in 1..5:
    burn_the_heretic("heretic_" + str(i))
    the_emperor_protects()

# Comandos em loops while
counter: dg = 3
while counter > 0:
    for_the_emperor()
    counter = counter - 1
```

### Comandos em Condicionais
```warpy40k
# Escolha Imperial vs Caos
loyalty: dg = hear_the_emperors_voice("Enter loyalty level (1-100):")

if loyalty >= 50:
    the_emperor_protects()
    for_the_emperor()
    ave_imperator()
else:
    taste_chaos()
    blood_for_the_blood_god()
    let_the_galaxy_burn()
```

---

## Função de Entrada

A função `hear_the_emperors_voice()` é a forma principal de obter entrada do usuário em WarPy40K:

### Sintaxe
```warpy40k
hear_the_emperors_voice()                    # Usa prompt padrão
hear_the_emperors_voice("Custom prompt:")    # Usa prompt personalizado
```

### Exemplos de Uso
```warpy40k
# Entrada básica
name: servitor = hear_the_emperors_voice("Enter your name:")

# Entrada numérica (automaticamente convertida para tipo dg)
age: dg = hear_the_emperors_voice("Enter your age:")

# Entrada em expressões
count: dg = hear_the_emperors_voice("Enter count:")
total: dg = count * 2 + 10

# Entrada em condicionais
power: dg = hear_the_emperors_voice("Enter power level:")
if power > 75:
    the_emperors_will_be_done()
elif power > 25:
    faith_is_my_shield()
else:
    fear_is_the_mind_killer()
```

### Conversão de Tipo
- Quando usado com variáveis do tipo `dg`, strings de entrada são automaticamente convertidas para números
- Conversões inválidas (entrada não numérica para tipo `dg`) causarão erros de execução
- Entrada vazia para tipo `dg` causará erros de execução

---

## Categorias de Comandos por Facção

### Comandos Imperiais (Leais ao Imperador)
```warpy40k
the_emperor_protects()           # The Emperor protects!
only_in_death_does_duty_end()    # Only in death does duty end.
even_in_death_i_still_serve()    # Even in death, I still serve!
no_pity_no_remorse_no_fear()     # No pity, no remorse, no fear!
pain_is_temporary_glory_is_forever()  # Pain is temporary, glory is forever.
faith_is_my_shield()             # Faith is my shield!
we_are_angels_of_death()         # We are the Angels of Death!
for_the_emperor()                # For the Emperor!
the_emperors_will_be_done()      # The Emperor's will is fulfilled.
ave_imperator()                  # Ave Imperator! Glory to the Emperor!
burn_the_heretic(arg)            # Burn the heretic: [arg]
purge_the_xenos(arg)             # Xenos purged: [arg]!
fear_is_the_mind_killer()        # Fear suppressed.
```

### Comandos do Caos (Corrompidos pela Warp)
```warpy40k
taste_chaos()                    # Warp corrupts your soul.
blood_for_the_blood_god()        # Blood for the Blood God!
let_the_galaxy_burn()            # The galaxy burns!
```

### Comandos Ork (Brutais e Astutos)
```warpy40k
WAAAGH()                         # The orks rally!
more_dakka()                     # More dakka! Fire everything!
ork_cunning()                    # Cunning plan!
```

### Comandos Eldar (Antigos e Misteriosos)
```warpy40k
the_path_is_set()                # The path is set. We proceed.
farseers_vision()                # The Farseer foresees...
```

### Comandos Gerais (Universais)
```warpy40k
we_are_one()                     # We are one.
servitor()                       # Returns "servitor_instance"
hear_the_emperors_voice(prompt)  # User input function
```

---

## Cartão de Referência Rápida

### Comandos Mais Comuns
```warpy40k
the_emperor_protects()           # Comando Imperial básico
for_the_emperor()                # Grito de guerra Imperial
burn_the_heretic("target")       # Ação Imperial
WAAAGH()                         # Rally Ork
taste_chaos()                    # Corrupção do Caos
hear_the_emperors_voice()        # Obter entrada do usuário
```

### Padrões de Comandos
```warpy40k
# Comando simples
command_name()

# Comando com argumento
command_name("argument")
command_name(variable)

# Comando em variável
result: servitor = servitor()

# Comando em expressão
input: dg = hear_the_emperors_voice("Prompt:")
```

---

## Dicas para Usar Comandos

1. **Escolha Tematicamente**: Use comandos Imperiais para programas leais, Caos para temas de corrupção, etc.
2. **Combine com Lógica**: Use comandos em condicionais e loops para comportamento dinâmico
3. **Interação do Usuário**: Use `hear_the_emperors_voice()` para programas interativos
4. **Tratamento de Erros**: Comandos com argumentos lidarão com conversão de tipo automaticamente
5. **Depuração**: Comandos imprimem seus efeitos, tornando-os úteis para rastreamento de fluxo do programa

---

*Pelo Imperador! A linguagem WarPy40K serve ao Império da Humanidade.* 