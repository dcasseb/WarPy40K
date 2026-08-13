# WarPy40K Examples

This document provides complete example programs with explanations.

## 📁 Included Examples

The WarPy40K repository includes several example programs in the `examples/` directory:

### 1. hello.wp40k
Simple "Hello World" program demonstrating basic output.

**Code:**
```python
# WarPy40K Example: Hello World
# This is a simple program that demonstrates basic output

print("Welcome to the WarPy40K language!")
print("For the Emperor!")
```

**Run:**
```bash
warpy40k examples/hello.wp40k
```

**Output:**
```
Welcome to the WarPy40K language!
For the Emperor!
```

---

### 2. calculator.wp40k
Interactive calculator demonstrating variables, arithmetic, and user input.

**Code:**
```python
# WarPy40K Example: Simple Calculator
# Demonstrates variables, arithmetic, and user input

print("Simple WarPy40K Calculator")
print("--------------------------")

a = input("Enter first number: ")
b = input("Enter second number: ")

# Convert to numbers (assuming user enters valid integers)
a_num = int(a)
b_num = int(b)

print("Results:")
print("Sum:", a_num + b_num)
print("Difference:", a_num - b_num)
print("Product:", a_num * b_num)
print("Quotient:", a_num / b_num)
```

**Run:**
```bash
warpy40k examples/calculator.wp40k
```

**Example Session:**
```
Simple WarPy40K Calculator
--------------------------
Enter first number: 10
Enter second number: 5
Results:
Sum: 15
Difference: 5
Product: 50
Quotient: 2.0
```

---

### 3. variables.wp40k
Demonstrates variable usage and arithmetic operations.

**Code:**
```python
# WarPy40K Example: Variables and Arithmetic
# Demonstrates variable usage and arithmetic operations

# Variable assignments
x = 10
y = 20
z = 5

# Arithmetic operations
sum = x + y
product = x * y
difference = y - x
quotient = y / x

print("Variables and Arithmetic:")
print("  x =")
print(x)
print("  y =")
print(y)
print("  z =")
print(z)
print("  x + y =")
print(sum)
print("  x * y =")
print(product)
print("  y - x =")
print(difference)
print("  y / x =")
print(quotient)

# Power operation
power = x ^ z
print("  x ^ z =")
print(power)

# Using variables in expressions
result = (x + y) * z
print("  (x + y) * z =")
print(result)
```

**Run:**
```bash
warpy40k examples/variables.wp40k
```

**Output:**
```
Variables and Arithmetic:
  x =
10
  y =
20
  z =
5
  x + y =
30
  x * y =
200
  y - x =
10
  y / x =
2.0
  x ^ z =
100000
  (x + y) * z =
150
```

---

### 4. warpy_demo.wp40k
Demonstrates all WarPy40K specific expressions.

**Code:**
```python
# WarPy40K Example: Warhammer 40K Themed Demo
# Demonstrates all WarPy40K specific expressions

print("=== WarPy40K Theme Demo ===")
print()

# Inquisition - Truth and judgment
print("Inquisition (truth/judgment):")
faithful = Inquisition FAITH
print("  Inquisition FAITH =")
print(faithful)
heretic = Inquisition 0
print("  Inquisition 0 =")
print(heretic)
print()

# Emperor - Divine power
print("Emperor (divine power):")
blessed = Emperor 100
print("  Emperor 100 =")
print(blessed)
power = Emperor
print("  Emperor (no target) =")
print(power)
print()

# Chaos - Corruption and randomness
print("Chaos (corruption/randomness):")
corrupted = Chaos 100
print("  Chaos 100 =")
print(corrupted)
pure_chaos = Chaos
print("  Chaos (no target) =")
print(pure_chaos)
print()

# Bless and Curse - Modifications
print("Bless and Curse (modifications):")
blessed_value = Bless 100
print("  Bless 100 =")
print(blessed_value)
cursed_value = Curse 100
print("  Curse 100 =")
print(cursed_value)
print()

# Purge and Exterminatus - Destruction
print("Purge and Exterminatus (destruction):")
purged = Purge 42
print("  Purge 42 =")
print(purged)
exterminated = Exterminatus 100
print("  Exterminatus 100 =")
print(exterminated)
print()

# Combined expressions
print("Combined expressions:")
result = Bless Emperor 50
print("  Bless Emperor 50 =")
print(result)

judgment = Inquisition Chaos
print("  Inquisition Chaos =")
print(judgment)

print()
print("=== Demo Complete ===")
```

**Run:**
```bash
warpy40k examples/warpy_demo.wp40k
```

**Output:** (values may vary due to Chaos randomness)
```
=== WarPy40K Theme Demo ===

Inquisition (truth/judgment):
  Inquisition FAITH =
True
  Inquisition 0 =
False

Emperor (divine power):
  Emperor 100 =
100.0
  Emperor (no target) =
1000

Chaos (corruption/randomness):
  Chaos 100 =
100.0
  Chaos (no target) =
75.31826593382571

Bless and Curse (modifications):
  Bless 100 =
110.00000000000001
  Curse 100 =
90.0

Purge and Exterminatus (destruction):
  Purge 42 =
0
  Exterminatus 100 =
None

Combined expressions:
  Bless Emperor 50 =
55.00000000000001
  Inquisition Chaos =
True

=== Demo Complete ===
```

---

### 5. control_flow.wp40k
Demonstrates if/else functionality.

**Code:**
```python
# WarPy40K Example: Control Flow
# Demonstrates if/else functionality

print("=== Control Flow Demo ===")
print()

# If statement example
print("If statement example:")
x = 10
if x > 5
    print("x is greater than 5")
else
    print("x is 5 or less")

print()

# Nested if example
print("Nested if example:")
y = 15
if x > 5
    if y > 10
        print("Both x > 5 and y > 10")
    else
        print("x > 5 but y <= 10")
else
    print("x <= 5")

print()

# Combined example with WarPy40K expressions
print("Combined example with WarPy40K:")
faith = 80
if Inquisition faith
    print("The subject is faithful!")
else
    print("The subject is a heretic!")

print()

# Test with false condition
heresy = 0
if Inquisition heresy
    print("This should not print")
else
    print("The Emperor protects the faithful!")

print()

# Complex condition
print("Complex condition:")
a = 10
b = 20
if a > 5 AND b < 30
    print("Complex condition passed!")
else
    print("Complex condition failed!")

print()
print("=== Demo Complete ===")
```

**Run:**
```bash
warpy40k examples/control_flow.wp40k
```

**Output:**
```
=== Control Flow Demo ===

If statement example:
x is greater than 5

Nested if example:
Both x > 5 and y > 10

Combined example with WarPy40K:
The subject is faithful!
The Emperor protects the faithful!

Complex condition:
Complex condition passed!

=== Demo Complete ===
```

---

## 🎯 Complete Example Programs

Here are some additional example programs you can create:

### 1. Faith Checker Program

**File:** `faith_checker.wp40k`

```python
# Faith Checker Program

print("Imperium Faith Checker")
print("----------------------")

name = input("Enter subject name: ")
faith_score = input("Enter faith score (0-100): ")

# Convert to number
faith_num = int(faith_score)

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

**How it works:**
1. Asks for a subject name and faith score
2. Uses `Inquisition` to check if the faith score is truthy
3. If faithful, applies `Bless` to increase the score
4. If heretic, applies `Purge` to reset the score to 0

---

### 2. Planet Management System

**File:** `planet_manager.wp40k`

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

**How it works:**
1. Takes planet name as input
2. Uses built-in constants for population, faith, and corruption
3. Checks planet status using `Inquisition` and comparisons
4. Applies `Bless Emperor` for loyal planets
5. Recommends `Exterminatus` for highly corrupted planets

---

### 3. Battle Simulator

**File:** `battle_simulator.wp40k`

```python
# Battle Simulator

print("=== WarPy40K Battle Simulator ===")
print()

# Get army sizes
imperial_army = input("Enter Imperial Army size: ")
chaos_army = input("Enter Chaos Army size: ")

# Convert to numbers
imperial_num = int(imperial_army)
chaos_num = int(chaos_army)

# Apply modifiers
imperial_power = Bless Emperor imperial_num
chaos_power = Curse Chaos chaos_num

print("Imperial Power: ")
print(imperial_power)
print("Chaos Power: ")
print(chaos_power)
print()

# Determine outcome
if imperial_power > chaos_power
    print("IMPERIUM VICTORY!")
    print("The Emperor protects!")
else
    print("CHAOS VICTORY!")
    print("The galaxy burns!")
```

**How it works:**
1. Takes army sizes as input
2. Applies `Bless Emperor` to Imperial army (boosts by faith)
3. Applies `Curse Chaos` to Chaos army (reduces with randomness)
4. Compares the powers to determine the winner

---

### 4. Inquisition Trial

**File:** `inquisition_trial.wp40k`

```python
# Inquisition Trial

print("=== Inquisition Trial ===")
print()

# Get subject information
subject_name = input("Enter subject name: ")
faith = input("Enter faith level (0-100): ")
loyalty = input("Enter loyalty score (0-100): ")

# Convert to numbers
faith_num = int(faith)
loyalty_num = int(loyalty)

# Trial by Inquisition
print()
print("Trial Results:")
print("-------------")

# Check faith
if Inquisition faith_num
    print("✓ Faith: PASSED")
else
    print("✗ Faith: FAILED")

# Check loyalty
if Inquisition loyalty_num
    print("✓ Loyalty: PASSED")
else
    print("✗ Loyalty: FAILED")

# Final judgment
if Inquisition faith_num AND Inquisition loyalty_num
    print()
    print("VERDICT: INNOCENT")
    blessed_subject = Bless subject_name
    print("Blessed subject: ")
    print(blessed_subject)
else
    print()
    print("VERDICT: HERETIC")
    purged_subject = Purge subject_name
    print("Purged subject: ")
    print(purged_subject)
    print()
    print("EXTERMINATUS!")
    Exterminatus
```

**How it works:**
1. Takes subject name, faith, and loyalty as input
2. Uses `Inquisition` to check each attribute
3. Provides a verdict based on both checks
4. Applies `Bless` for innocent subjects, `Purge` and `Exterminatus` for heretics

---

## 📚 Example Program Templates

### Template 1: Simple Script

```python
# Simple WarPy40K Script Template

# Import constants (if needed)
# FAITH, CORRUPTION, POPULATION are built-in

# Define variables
variable1 = value1
variable2 = value2

# Perform operations
result = operation1 + operation2

# Output results
print("Result:")
print(result)
```

### Template 2: Interactive Program

```python
# Interactive WarPy40K Program Template

print("Program Title")
print("-------------")

# Get user input
input1 = input("Prompt 1: ")
input2 = input("Prompt 2: ")

# Process input
# Convert to numbers if needed: num = int(input1)

# Perform calculations
result = calculation

# Output results
print("Results:")
print(result)
```

### Template 3: Conditional Program

```python
# Conditional WarPy40K Program Template

# Get input
value = input("Enter value: ")

# Convert if needed
num = int(value)

# Check conditions
if condition1
    # Do something
    result = action1
else
    # Do something else
    result = action2

# Output
print(result)
```

### Template 4: WarPy40K Themed Program

```python
# WarPy40K Themed Program Template

# Use WarPy40K expressions
faith_check = Inquisition FAITH
emperor_power = Emperor 100
chaos_factor = Chaos

# Combine with standard operations
result = Bless (emperor_power + chaos_factor)

# Use in conditionals
if Inquisition result
    print("Success!")
else
    print("Failure!")
```

---

## 🎯 Tips for Writing Good WarPy40K Programs

1. **Start simple**: Begin with basic print statements and arithmetic
2. **Use comments**: Explain what your code does
3. **Test frequently**: Run your program often to catch errors
4. **Use meaningful names**: Match the Warhammer 40K theme when appropriate
5. **Keep it short**: WarPy40K is designed for small programs
6. **Have fun**: Embrace the Warhammer 40K theme!

---

## 📖 Next Steps

- **[Tutorials](tutorials.md)** - Step-by-step programming guides
- **[Language Reference](language_reference.md)** - Complete syntax guide
- **[WarPy40K Expressions](warpy_expressions.md)** - Detailed expression documentation
- Try creating your own programs!
