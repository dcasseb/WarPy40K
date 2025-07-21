# WarPy40K Destaque de Sintaxe - Guia Completo de Instalação

Este guia cobre a instalação do destaque de sintaxe para WarPy40K no VS Code e Sublime Text.

## 🎨 Extensão VS Code

### ✅ **Já Instalada!**
A extensão do VS Code foi instalada com sucesso em sua máquina.

### **Recursos:**
- Destaque de sintaxe completo para todas as construções WarPy40K
- Tema personalizado "WarPy40K Dark" com cores inspiradas em Warhammer 40K
- Auto-completar e associação de arquivos
- Suporte para todos os recursos da linguagem

### **Testando VS Code:**
1. Abra o VS Code
2. Crie um novo arquivo com extensão `.wp40k`
3. Digite algum código WarPy40K:
   ```warpy40k
   # Teste de destaque de sintaxe
   i: dg = 0
   for i in 1..5:
       the_emperor_protects()
       if i > 3:
           for_the_emperor()
   ```

### **Usando o Tema WarPy40K Dark:**
1. Pressione `Ctrl+K Ctrl+T` (ou `Cmd+K Cmd+T` no Mac)
2. Selecione "WarPy40K Dark" da lista de temas

## 🎨 Extensão Sublime Text

### ✅ **Já Instalada!**
O destaque de sintaxe do Sublime Text foi instalado com sucesso em sua máquina.

### **Recursos:**
- Destaque de sintaxe completo para todas as construções WarPy40K
- Associação automática de arquivos para arquivos `.wp40k`
- Suporte para todos os recursos da linguagem

### **Testando Sublime Text:**
1. Abra o Sublime Text 4
2. Crie um novo arquivo com extensão `.wp40k`
3. Digite algum código WarPy40K:
   ```warpy40k
   # Teste de destaque de sintaxe
   i: dg = 0
   for i in 1..5:
       the_emperor_protects()
       if i > 3:
           for_the_emperor()
   ```

### **Seleção Manual de Sintaxe (se necessário):**
1. Abra um arquivo `.wp40k`
2. Vá para **View → Syntax → User → WarPy40K**
3. Ou pressione **Ctrl+Shift+P** e digite "Set Syntax: WarPy40K"

## 🎯 **O Que Você Deve Ver**

Ambos os editores devem destacar:
- **Comentários** (`#`) em verde
- **Comandos** (`the_emperor_protects`, `for_the_emperor`, etc.) na cor de função
- **Palavras-chave** (`for`, `while`, `if`, `else`, `in`) na cor de fluxo de controle
- **Variáveis** (`i`, `counter`) na cor de variável
- **Tipos** (`dg`, `servitor`, `blob`, `psykers`, `void_shields`) na cor de tipo de armazenamento
- **Números** (`0`, `1`, `5`) na cor de número
- **Operadores** (`+`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `..`, `:`) na cor de operador
- **Strings** (`"heretic"`) na cor de string

## 🔧 **Solução de Problemas**

### Problemas do VS Code:
1. **Extensão não funcionando**: Reinicie o VS Code
2. **Sem destaque de sintaxe**: Verifique se o arquivo tem extensão `.wp40k`
3. **Tema não disponível**: Verifique se a extensão está instalada corretamente

### Problemas do Sublime Text:
1. **Sintaxe não aparecendo**: Reinicie o Sublime Text
2. **Seleção manual necessária**: Use View → Syntax → User → WarPy40K
3. **Cores erradas**: Tente um esquema de cores diferente

## 📁 **Localização dos Arquivos**

### Extensão VS Code:
- **Instalada**: `~/.vscode/extensions/warpy40k-syntax-0.1.0/`
- **Fonte**: `warpy40k-syntax/`

### Sintaxe Sublime Text:
- **Arquivo de sintaxe**: `~/.config/sublime-text/Packages/User/WarPy40K.sublime-syntax`
- **Arquivo de configurações**: `~/.config/sublime-text/Packages/User/WarPy40K.sublime-settings`
- **Fonte**: `warpy40k-sublime/`

## 🚀 **Comandos de Teste Rápido**

### VS Code:
```bash
cd warpy40k-syntax
code test-syntax.wp40k
```

### Sublime Text:
```bash
cd warpy40k-sublime
subl test-syntax.wp40k
```

## 🎉 **Sucesso!**

Tanto o VS Code quanto o Sublime Text agora têm suporte completo de destaque de sintaxe para WarPy40K! Você pode escrever código WarPy40K com belo destaque de sintaxe em qualquer editor.

---

**Pelo Imperador!** 🛡️ 