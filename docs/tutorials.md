# WarPy40K Tutorials

This document provides step-by-step tutorials for creating programs with WarPy40K.

## 🏁 Your First Program

### Step 1: Install WarPy40K

```bash
git clone https://github.com/dcasseb/WarPy40K.git
cd WarPy40K
pip install -e .
```

### Step 2: Create a Simple Program

Create a file named `first_program.wp40k`:

```python
# My first WarPy40K program
print("For the Emperor!")
print("This is my first WarPy40K program")
```

### Step 3: Run Your Program

```bash
warpy40k first_program.wp40k
```

Expected output:
```
For the Emperor!
This is my first WarPy40K program
```

### Step 4: Try the REPL

```bash
warpy40k -i
```

Type some expressions:
```
>>> 1 + 2
3
>>> x = 10
10
>>> x * 2
20
>>> exit
May the Emperor protect you!
```

## 🧮 Basic Arithmetic Tutorial

### Lesson 1: Numbers and Operations

Create `arithmetic.wp40k`:

```python
# Basic arithmetic operations

# Addition
result = 5 + 3
print("5 + 3 =")
print(result)

# Subtraction
result = 10 - 4
print("10 - 4 =")
print(result)

# Multiplication
result = 7 * 6
print("7 * 6 =")
print(result)

# Division
result = 20 / 4
print("20 / 4 =")
print(result)

# Power
result = 2 ^ 3
print("2 ^ 3 =")
print(result)
```

Run it:
```bash
warpy40k arithmetic.wp40k
```

### Lesson 2: Operator Precedence

Create `precedence.wp40k`:

```python
# Operator precedence examples

# Multiplication before addition
result = 1 + 2 * 3
print("1 + 2 * 3 =")
print(result)  # Output: 7 (1 + (2 * 3))

# Use parentheses to override
result = (1 + 2) * 3
print("(1 + 2) * 3 =")
print(result)  # Output: 9

# Complex expression
result = 2 + 3 * 4 - 5 / 2
print("2 + 3 * 4 - 5 / 2 =")
print(result)
```

### Lesson 3: Variables

Create `variables.wp40k`:

```python
# Using variables

# Assign values
x = 10
y = 20

# Use variables in expressions
sum = x + y
product = x * y
difference = y - x
quotient = y / x

# Print results
print("x =")
print(x)
print("y =")
print(y)
print("x + y =")
print(sum)
print("x * y =")
print(product)
print("y - x =")
print(difference)
print("y / x =")
print(quotient)
```

## 🔄 Control Flow Tutorial

### Lesson 1: If Statements

Create `if_statements.wp40k`:

```python
# If statement examples

# Basic if
x = 10
if x > 5
    print("x is greater than 5")
else
    print("x is 5 or less")

# Nested if
a = 15
b = 10
if a > b
    if a > 20
        print("a is greater than 20")
    else
        print("a is between 10 and 20")
else
    print("a is 10 or less")

# Multiple conditions
age = 25
faith = 80
if age >= 18 AND faith > 50
    print("Adult and faithful")
else
    print("Not adult or not faithful")
```

### Lesson 2: Comparison Operators

Create `comparisons.wp40k`:

```python
# Comparison operators

a = 10
b = 20

# Equal
if a == 10
    print("a is 10")

# Not equal
if a != b
    print("a is not equal to b")

# Greater than
if b > a
    print("b is greater than a")

# Less than
if a < b
    print("a is less than b")

# Greater or equal
if b >= a
    print("b is greater or equal to a")

# Less or equal
if a <= b
    print("a is less or equal to b")
```

## 🌟 WarPy40K Expressions Tutorial

### Lesson 1: Inquisition

Create `inquisition_tutorial.wp40k`:

```python
# Inquisition - Truth and judgment

# Basic usage
result = Inquisition
print("Inquisition (no target) =")
print(result)  # Always True

# With target
result = Inquisition 42
print("Inquisition 42 =")
print(result)  # True (42 is truthy)

result = Inquisition 0
print("Inquisition 0 =")
print(result)  # False (0 is falsy)

# Practical use
faith_score = 75
if Inquisition faith_score
    print("The subject is faithful!")
else
    print("The subject is a heretic!")
```

### Lesson 2: Emperor

Create `emperor_tutorial.wp40k`:

```python
# Emperor - Divine power

# Basic usage
power = Emperor
print("Emperor (no target) =")
print(power)  # 1000

# With target
blessed = Emperor 100
print("Emperor 100 =")
print(blessed)  # 100.0

# With FAITH constant
result = Emperor FAITH
print("Emperor FAITH =")
print(result)  # 100.0

# Combined with Bless
result = Bless Emperor 50
print("Bless Emperor 50 =")
print(result)  # 55.0
```

### Lesson 3: Chaos

Create `chaos_tutorial.wp40k`:

```python
# Chaos - Corruption and randomness

# Basic usage
chaos_value = Chaos
print("Chaos (no target) =")
print(chaos_value)  # Random value

# With target
corrupted = Chaos 100
print("Chaos 100 =")
print(corrupted)  # 100 + random factor

# Multiple calls
value1 = Chaos
value2 = Chaos
print("First chaos value:")
print(value1)
print("Second chaos value:")
print(value2)
print("Are they different?")
print(value1 != value2)
```

### Lesson 4: Bless and Curse

Create `bless_curse_tutorial.wp40k`:

```python
# Bless and Curse - Modifications

# Bless examples
blessed_number = Bless 100
print("Bless 100 =")
print(blessed_number)  # 110.0

blessed_string = Bless "John"
print("Bless 'John' =")
print(blessed_string)  # "Blessed John"

# Curse examples
cursed_number = Curse 100
print("Curse 100 =")
print(cursed_number)  # 90.0

cursed_string = Curse "John"
print("Curse 'John' =")
print(cursed_string)  # "Cursed John"

# Combined
result = Bless Curse 100
print("Bless Curse 100 =")
print(result)  # 99.0 (100 * 0.9 * 1.1)
```

### Lesson 5: Purge and Exterminatus

Create `purge_tutorial.wp40k`:

```python
# Purge and Exterminatus - Destruction

# Purge examples
purged_number = Purge 42
print("Purge 42 =")
print(purged_number)  # 0

purged_string = Purge "heretic"
print("Purge 'heretic' =")
print(purged_string)  # ""

# Exterminatus examples
exterminatus_result = Exterminatus
print("Exterminatus (no target) =")
print(exterminatus_result)  # "EXTERMINATUS"

exterminatus_with_target = Exterminatus 100
print("Exterminatus 100 =")
print(exterminatus_with_target)  # None
```

## 🎮 Interactive Program Tutorial

### Lesson 1: Simple Input/Output

Create `simple_io.wp40k`:

```python
# Simple interactive program

print("Welcome to WarPy40K Interactive!")
name = input("What is your name? ")
print("Hello, " + name + "!")

age = input("How old are you? ")
print("You are " + age + " years old.")
```

### Lesson 2: Calculator Program

Create `calculator_tutorial.wp40k`:

```python
# Simple calculator

print("WarPy40K Calculator")
print("------------------")

a = input("Enter first number: ")
b = input("Enter second number: ")

# Convert to numbers (assuming valid input)
a_num = a * 1
b_num = b * 1

print("Results:")
print("Sum: ")
print(a_num + b_num)
print("Difference: ")
print(a_num - b_num)
print("Product: ")
print(a_num * b_num)
print("Quotient: ")
print(a_num / b_num)
```

### Lesson 3: Faith Checker

Create `faith_checker.wp40k`:

```python
# Faith checker program

print("Imperium Faith Checker")
print("----------------------")

name = input("Enter subject name: ")
faith_score = input("Enter faith score (0-100): ")

# Convert to number
faith_num = faith_score * 1

# Check faith
if Inquisition faith_num
    print(name + " is faithful to the Emperor!")
    blessed_score = Bless faith_num
    print("Blessed faith score: ")
    print(blessed_score)
else
    print(name + " is a HERETIC!")
    purged_score = Purge faith_num
    print("Purged faith score: ")
    print(purged_score)
```

## 🏆 Advanced Tutorial: Planet Management System

Create `planet_manager.wp40k`:

```python
# Planet Management System

print("=== Planet Management System ===")
print()

# Initialize planet
planet_name = input("Enter planet name: ")
population = POPULATION
faith_level = FAITH
corruption_level = CORRUPTION

print("Planet: " + planet_name)
print("Population: ")
print(population)
print("Faith Level: ")
print(faith_level)
print("Corruption Level: ")
print(corruption_level)
print()

# Check planet status
if Inquisition faith_level AND corruption_level < 10
    print(planet_name + " is LOYAL")
    blessed_pop = Bless Emperor population
    print("Blessed population: ")
    print(blessed_pop)
else
    print(planet_name + " is at RISK")
    if corruption_level > 50
        print("EXTERMINATUS recommended!")
        Exterminatus
    else
        print("Inquisition investigation required")
        inquisition_result = Inquisition Chaos
        print("Inquisition result: ")
        print(inquisition_result)
```

## 📚 Tutorial Summary

You've learned:

1. ✅ **Basic syntax** - Comments, print, variables
2. ✅ **Arithmetic** - Operations, precedence, expressions
3. ✅ **Control flow** - If/else statements, comparisons
4. ✅ **WarPy40K expressions** - All special keywords
5. ✅ **Interactive programs** - Input/output, user interaction
6. ✅ **Complete programs** - Combining all features

## 🎯 Next Steps

- **[Examples](examples.md)** - See complete example programs
- **[Language Reference](language_reference.md)** - Complete syntax guide
- **[WarPy40K Expressions](warpy_expressions.md)** - Detailed expression documentation
- Try creating your own programs!
