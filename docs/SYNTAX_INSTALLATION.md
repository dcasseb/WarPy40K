# WarPy40K Syntax Highlighting - Complete Installation Guide

This guide covers installing syntax highlighting for WarPy40K in both VS Code and Sublime Text.

## 🎨 VS Code Extension

### ✅ **Already Installed!**
The VS Code extension has been successfully installed on your machine.

### **Features:**
- Complete syntax highlighting for all WarPy40K constructs
- Custom "WarPy40K Dark" theme with Warhammer 40K inspired colors
- Auto-completion and file association
- Support for all language features

### **Testing VS Code:**
1. Open VS Code
2. Create a new file with `.wp40k` extension
3. Type some WarPy40K code:
   ```warpy40k
   # Test syntax highlighting
   i: dg = 0
   for i in 1..5:
       the_emperor_protects()
       if i > 3:
           for_the_emperor()
   ```

### **Using the WarPy40K Dark Theme:**
1. Press `Ctrl+K Ctrl+T` (or `Cmd+K Cmd+T` on Mac)
2. Select "WarPy40K Dark" from the theme list

## 🎨 Sublime Text Extension

### ✅ **Already Installed!**
The Sublime Text syntax highlighting has been successfully installed on your machine.

### **Features:**
- Complete syntax highlighting for all WarPy40K constructs
- Automatic file association for `.wp40k` files
- Support for all language features

### **Testing Sublime Text:**
1. Open Sublime Text 4
2. Create a new file with `.wp40k` extension
3. Type some WarPy40K code:
   ```warpy40k
   # Test syntax highlighting
   i: dg = 0
   for i in 1..5:
       the_emperor_protects()
       if i > 3:
           for_the_emperor()
   ```

### **Manual Syntax Selection (if needed):**
1. Open a `.wp40k` file
2. Go to **View → Syntax → User → WarPy40K**
3. Or press **Ctrl+Shift+P** and type "Set Syntax: WarPy40K"

## 🎯 **What You Should See**

Both editors should highlight:
- **Comments** (`#`) in green
- **Commands** (`the_emperor_protects`, `for_the_emperor`, etc.) in function color
- **Keywords** (`for`, `while`, `if`, `else`, `in`) in control flow color
- **Variables** (`i`, `counter`) in variable color
- **Types** (`dg`, `servitor`, `blob`, `psykers`, `void_shields`) in storage type color
- **Numbers** (`0`, `1`, `5`) in number color
- **Operators** (`+`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `..`, `:`) in operator color
- **Strings** (`"heretic"`) in string color

## 🔧 **Troubleshooting**

### VS Code Issues:
1. **Extension not working**: Restart VS Code
2. **No syntax highlighting**: Check if file has `.wp40k` extension
3. **Theme not available**: Check if extension is properly installed

### Sublime Text Issues:
1. **Syntax not appearing**: Restart Sublime Text
2. **Manual selection needed**: Use View → Syntax → User → WarPy40K
3. **Wrong colors**: Try a different color scheme

## 📁 **File Locations**

### VS Code Extension:
- **Installed**: `~/.vscode/extensions/warpy40k-syntax-0.1.0/`
- **Source**: `warpy40k-syntax/`

### Sublime Text Syntax:
- **Syntax file**: `~/.config/sublime-text/Packages/User/WarPy40K.sublime-syntax`
- **Settings file**: `~/.config/sublime-text/Packages/User/WarPy40K.sublime-settings`
- **Source**: `warpy40k-sublime/`

## 🚀 **Quick Test Commands**

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

## 🎉 **Success!**

Both VS Code and Sublime Text now have full syntax highlighting support for WarPy40K! You can write WarPy40K code with beautiful syntax highlighting in either editor.

---

**For the Emperor!** 🛡️ 