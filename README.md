# WarPy40K

A Warhammer 40K-themed toy programming language and interpreter, designed for fun, learning, and extensibility. WarPy40K features a custom syntax, unique commands, and robust tooling including a linter and syntax highlighting extensions for VS Code and Sublime Text.

## Features

- **Custom Language**: Warhammer 40K-inspired syntax and commands
- **Arithmetic Operations**: Full support for addition (+), subtraction (-), multiplication (*), division (/), and modulo (%) with proper operator precedence
- **Control Flow**: If-else conditionals, for loops, and while loops
- **Variables**: Typed variable declarations and assignments
- **Interpreter**: Execute `.wp40k` scripts directly with Python
- **Linter**: Comprehensive static analysis for syntax, variables, and style ([see linter docs](./LINTER_README.md))
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

- **Linter**: See [LINTER_README.md](./LINTER_README.md) for error codes, integration, and advanced usage.
- **Syntax Highlighting**:
  - VS Code: See `warpy40k-syntax/README.md`
  - Sublime Text: See `warpy40k-sublime/README.md`

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