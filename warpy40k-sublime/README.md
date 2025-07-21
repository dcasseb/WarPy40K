# Destaque de Sintaxe WarPy40K para Sublime Text

Uma definição de sintaxe do Sublime Text que fornece destaque de sintaxe rico para a linguagem de programação WarPy40K.

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

### Método 1: Usando o Script de Instalação (Recomendado)
```bash
cd warpy40k-sublime
chmod +x install.sh
./install.sh
```

### Método 2: Instalação Manual

#### macOS
```bash
cp WarPy40K.sublime-syntax ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/User/
cp WarPy40K.sublime-settings ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/User/
```

#### Windows
```bash
cp WarPy40K.sublime-syntax %APPDATA%\Sublime Text 3\Packages\User\
cp WarPy40K.sublime-settings %APPDATA%\Sublime Text 3\Packages\User\
```

#### Linux
```bash
cp WarPy40K.sublime-syntax ~/.config/sublime-text-3/Packages/User/
cp WarPy40K.sublime-settings ~/.config/sublime-text-3/Packages/User/
```

## Testing

1. Open Sublime Text
2. Create a new file with `.wp40k` extension
3. Add some WarPy40K code:

```warpy40k
# Test the syntax highlighting
i: dg = 0
for i in 1..5:
    the_emperor_protects()
    if i > 3:
        for_the_emperor()
    else:
        burn_the_heretic("test")
```

4. You should see syntax highlighting for:
   - Comments in green
   - Commands in function color
   - Keywords (for, if, else) in control flow color
   - Variables in variable color
   - Types (dg) in storage type color
   - Numbers in number color
   - Operators in operator color

## Manual Syntax Selection

If syntax highlighting doesn't appear automatically:

1. Open a `.wp40k` file
2. Go to **View → Syntax → User → WarPy40K**
3. Or press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) and type "Set Syntax: WarPy40K"

## Customization

You can customize the colors by:
1. Going to **Preferences → Settings**
2. Adding custom color scheme rules to your user settings
3. Using scope names like:
   - `entity.name.function.warpy40k` for commands
   - `keyword.control.warpy40k` for keywords
   - `storage.type.warpy40k` for types
   - `variable.other.warpy40k` for variables

## Troubleshooting & FAQ

**Q: Syntax highlighting doesn't appear?**
- Make sure the files are in the correct User packages directory
- Restart Sublime Text
- Check if the syntax appears in View → Syntax → User

**Q: Colors not appearing as expected?**
- Try a different color scheme (Preferences → Color Scheme)
- Check if your theme supports the scope names
- Restart Sublime Text

**Q: How do I uninstall?**
- Delete `WarPy40K.sublime-syntax` and `WarPy40K.sublime-settings` from your User packages directory
- Restart Sublime Text

## File Structure

- `WarPy40K.sublime-syntax` - Main syntax definition file
- `WarPy40K.sublime-settings` - File association settings
- `install.sh` - Automated installation script
- `README.md` - This documentation

## Contributing

To contribute to the syntax highlighting:
1. Fork the repository
2. Make your changes to `WarPy40K.sublime-syntax`
3. Test with a `.wp40k` file
4. Submit a pull request

## Support

If you encounter any issues:
1. Check the Sublime Text console for errors
2. Create an issue on the GitHub repository
3. Include the WarPy40K code that's causing problems

---

*For the Emperor!* 🛡️ 