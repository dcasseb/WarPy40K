# Destaque de Sintaxe WarPy40K para VS Code

Uma extensão do Visual Studio Code que fornece destaque de sintaxe rico para a linguagem de programação WarPy40K.

> Veja o [README principal do WarPy40K](../README.md) para recursos da linguagem, interpretador e uso do linter.

## Recursos

- Destaque de sintaxe para arquivos `.wp40k`
- Suporte para todas as construções da linguagem WarPy40K:
  - Comandos (ex: `the_emperor_protects`, `for_the_emperor`)
  - Declarações e atribuições de variáveis
  - Construções de loop (`for`, `while`)
  - Declarações condicionais (`if`, `else`)
  - Tipos de dados (`dg`, `servitor`, `blob`, `psykers`, `void_shields`)
  - Operadores (`+`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `..`, `:`)
  - Strings e números

## Instalação

### Método 1: Instalar a partir do VSIX (Recomendado)

1. Baixe o arquivo `warpy40k-syntax-*.vsix` mais recente dos releases ou construa localmente.
2. No VS Code, pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac) e selecione `Extensions: Install from VSIX...`.
3. Selecione o arquivo `.vsix`.
4. Abra um arquivo `.wp40k` para ver o destaque de sintaxe.

### Método 2: Instalação de Desenvolvimento

1. Clone o repositório e abra a pasta `warpy40k-syntax` no VS Code.
2. Press `F5` to launch an Extension Development Host window.
3. Open a `.wp40k` file to test the highlighting.

## Language Features

### Commands
```warpy40k
the_emperor_protects()
for_the_emperor()
burn_the_heretic("heretic")
```

### Variable Declarations
```warpy40k
i: dg = 0
name: servitor = "servant"
```

### Assignments
```warpy40k
i = i + 1
counter = 42
```

### Loops
```warpy40k
for i in 1..10:
    the_emperor_protects()

while x < 5:
    x = x + 1
```

### Conditionals
```warpy40k
if i > 0:
    for_the_emperor()
else:
    burn_the_heretic("traitor")
```

## Color Scheme

The extension uses your current VS Code color theme. Language elements are highlighted with distinct scopes:
- **Commands**: Function color
- **Keywords**: Control flow color
- **Types**: Storage type color
- **Variables**: Variable color
- **Strings**: String color
- **Numbers**: Number color
- **Operators**: Operator color

## Troubleshooting & FAQ

**Q: Syntax highlighting doesn't appear?**
- Make sure the extension is installed and enabled.
- Open a `.wp40k` file (or set the language mode to WarPy40K manually).
- Reload VS Code if needed.

**Q: How do I set the language mode manually?**
- Click the language indicator in the bottom right and select `WarPy40K`.

**Q: Can I customize the colors?**
- Yes! Add custom rules to your VS Code color theme using the provided scopes (see `syntaxes/warpy40k.tmLanguage.json`).

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Edit `syntaxes/warpy40k.tmLanguage.json` or related files
3. Test with a `.wp40k` file
4. Submit a pull request

## Support

If you encounter issues:
- Check the VS Code output/console for errors
- Create an issue on the GitHub repository
- Include the WarPy40K code that causes the problem

## License

This extension is part of the WarPy40K project. See `LICENSE` for details.

---

*For the Emperor!* 🛡️ 