# WarPy40K Expressions

This document explains the special Warhammer 40K themed expressions available in WarPy40K.

## 🌟 Overview

WarPy40K includes special keywords that represent concepts from the Warhammer 40K universe. These expressions have unique behaviors that go beyond standard programming operations.

## 📜 Inquisition

### Syntax
```python
Inquisition [target]
```

### Description
Represents **truth, judgment, and investigation** from the Warhammer 40K universe. The Inquisition seeks out heresy and corruption, determining the truth of a matter.

### Behavior
- **Without target**: Returns `True` (the Inquisition always finds truth)
- **With target**: Evaluates the truthiness of the target and returns a boolean

### Examples
```python
# Without target - always returns True
result = Inquisition
print(result)  # Output: True

# With target - evaluates truthiness
result = Inquisition 42
print(result)  # Output: True (42 is truthy)

result = Inquisition 0
print(result)  # Output: False (0 is falsy)

result = Inquisition ""
print(result)  # Output: False (empty string is falsy)

# Use in conditionals
faith = 80
if Inquisition faith
    print("The subject is faithful!")
else
    print("The subject is a heretic!")
```

### Use Cases
- Checking if a value is truthy
- Making decisions based on faith/loyalty
- Validating input

## 👑 Emperor

### Syntax
```python
Emperor [target]
```

### Description
Represents **divine power, protection, and blessing** from the Emperor of Mankind. The Emperor is the god-like figure who provides power and protection to the Imperium.

### Behavior
- **Without target**: Returns `1000` (representing the Emperor's immense power)
- **With target**: Multiplies the target by the faith factor (FAITH / 100)

### Examples
```python
# Without target - returns divine power value
power = Emperor
print(power)  # Output: 1000

# With target - applies divine blessing
blessed = Emperor 100
print(blessed)  # Output: 100.0 (100 * 100/100)

# With FAITH constant
result = Emperor FAITH
print(result)  # Output: 100.0 (100 * 100/100)

# Combined with other operations
result = Emperor 50 + 10
print(result)  # Output: 60.0
```

### Use Cases
- Applying divine blessings to values
- Representing the Emperor's power in calculations
- Boosting important values

## 🌪️ Chaos

### Syntax
```python
Chaos [target]
```

### Description
Represents **corruption, randomness, and the unpredictable nature of the Warp**. Chaos brings uncertainty and unpredictability to the galaxy.

### Behavior
- **Without target**: Returns a random float between 0 and 100
- **With target**: Adds a random factor to the target based on the CORRUPTION level

### Examples
```python
# Without target - pure chaos
chaos_value = Chaos
print(chaos_value)  # Output: Random value between 0 and 100

# With target - adds corruption
corrupted = Chaos 100
print(corrupted)  # Output: 100 + random factor

# Multiple calls produce different results
value1 = Chaos
value2 = Chaos
print(value1 != value2)  # Usually True

# Use in simulations
# Simulate a battle with chaos factor
damage = 50 + Chaos 10
print(damage)
```

### Use Cases
- Adding randomness to simulations
- Representing corruption in calculations
- Creating unpredictable behavior

## 🔥 Purge

### Syntax
```python
Purge target
```

### Description
Represents **destruction and removal** of heretics, xenos, and other threats to the Imperium. The Inquisition often calls for purging when heresy is found.

### Behavior
- **Sets the target to zero/empty** based on its type
- Numbers become `0`
- Strings become `""`
- Lists become `[]`
- Dictionaries become `{}`

### Examples
```python
# Purge a number
result = Purge 42
print(result)  # Output: 0

# Purge a string
result = Purge "heretic"
print(result)  # Output: ""

# Use in cleanup
x = 100
x = Purge x
print(x)  # Output: 0
```

### Use Cases
- Resetting values
- Removing unwanted data
- Representing destruction in simulations

## ☠️ Exterminatus

### Syntax
```python
Exterminatus [target]
```

### Description
Represents **total annihilation and complete destruction**. Exterminatus is the ultimate sanction, used to completely destroy a planet or system that has fallen to Chaos.

### Behavior
- **Without target**: Returns the string `"EXTERMINATUS"`
- **With target**: Executes the target (for side effects) and returns `None`

### Examples
```python
# Without target
destruction = Exterminatus
print(destruction)  # Output: EXTERMINATUS

# With target - destroys and returns None
result = Exterminatus 42
print(result)  # Output: None

# Use in extreme cases
if corruption > 90
    Exterminatus  # Total annihilation!
    print("The planet has been exterminated")
```

### Use Cases
- Representing complete destruction
- Terminating programs or operations
- Extreme error handling

## 🙏 Bless

### Syntax
```python
Bless target
```

### Description
Represents **positive modification and divine favor**. Blessing increases the value or quality of something.

### Behavior
- **Numbers**: Increases by 10% (multiplies by 1.1)
- **Strings**: Adds the prefix `"Blessed "`
- **Other types**: Returns the target unchanged

### Examples
```python
# Bless a number
blessed = Bless 100
print(blessed)  # Output: 110.0

# Bless a string
blessed_name = Bless "John"
print(blessed_name)  # Output: "Blessed John"

# Bless the Emperor's power
power = Bless Emperor
print(power)  # Output: 1100.0 (1000 * 1.1)

# Multiple blessings
result = Bless Bless 100
print(result)  # Output: 121.0 (100 * 1.1 * 1.1)
```

### Use Cases
- Increasing values
- Adding positive modifiers
- Representing divine favor

## 💀 Curse

### Syntax
```python
Curse target
```

### Description
Represents **negative modification and corruption**. Cursing decreases the value or quality of something, often due to Chaos influence.

### Behavior
- **Numbers**: Decreases by 10% (multiplies by 0.9)
- **Strings**: Adds the prefix `"Cursed "`
- **Other types**: Returns the target unchanged

### Examples
```python
# Curse a number
cursed = Curse 100
print(cursed)  # Output: 90.0

# Curse a string
cursed_name = Curse "John"
print(cursed_name)  # Output: "Cursed John"

# Curse with Chaos
result = Curse Chaos
print(result)  # Output: Random value * 0.9

# Multiple curses
result = Curse Curse 100
print(result)  # Output: 81.0 (100 * 0.9 * 0.9)
```

### Use Cases
- Decreasing values
- Adding negative modifiers
- Representing corruption

## 🏛️ Built-in Constants

### FAITH
- **Value**: 100
- **Description**: Represents the default faith level in the Imperium
- **Usage**: Used in calculations involving faith and loyalty

```python
faith_level = FAITH
print(faith_level)  # Output: 100

# Use with Emperor
blessed = Emperor FAITH
print(blessed)  # Output: 100.0
```

### CORRUPTION
- **Value**: 0
- **Description**: Represents the default corruption level
- **Usage**: Used in calculations involving Chaos and corruption

```python
corruption_level = CORRUPTION
print(corruption_level)  # Output: 0

# Increase corruption
CORRUPTION = 10
# Now Chaos will have more effect
```

### POPULATION
- **Value**: 1000000
- **Description**: Represents a default planet population
- **Usage**: Used in population calculations and simulations

```python
planet_population = POPULATION
print(planet_population)  # Output: 1000000

# Bless a planet's population
blessed_population = Bless POPULATION
print(blessed_population)  # Output: 1100000.0
```

## 🎯 Practical Examples

### Faith Check System
```python
# Check if a subject is faithful
faith_score = 75

if Inquisition faith_score
    print("Subject is faithful!")
    blessed_score = Bless faith_score
    print("Blessed faith score:", blessed_score)
else
    print("Subject is a heretic!")
    purged_score = Purge faith_score
    print("Purged faith score:", purged_score)
```

### Planet Management
```python
# Simulate planet management
population = POPULATION
corruption = 5

# Check planet status
if Inquisition (Chaos population)
    print("Planet is stable")
else
    print("Planet needs attention")

# Apply Emperor's blessing
blessed_population = Bless Emperor population
print("Blessed population:", blessed_population)
```

### Battle Simulation
```python
# Simulate a battle
attack_power = 100
defense_power = 80

# Apply chaos factor to attack
chaos_attack = Chaos attack_power
print("Chaos attack power:", chaos_attack)

# Check if defense holds
if Inquisition (chaos_attack < defense_power)
    print("Defense holds!")
else
    print("Defense is breached!")
    # Purge the defenders
    Purge defense_power
```

## 📖 Summary Table

| Expression | Target | Returns | Description |
|------------|--------|---------|-------------|
| `Inquisition` | Optional | Boolean | Truth/judgment |
| `Emperor` | Optional | Number | Divine power |
| `Chaos` | Optional | Number | Corruption/randomness |
| `Purge` | Required | Zero/Empty | Destruction |
| `Exterminatus` | Optional | None/"EXTERMINATUS" | Total annihilation |
| `Bless` | Required | Increased value | Positive modification |
| `Curse` | Required | Decreased value | Negative modification |

## 🎓 Best Practices

1. **Use meaningful names**: Match the Warhammer 40K theme when appropriate
2. **Comment your code**: Explain what each WarPy40K expression represents
3. **Test edge cases**: WarPy40K expressions can have unexpected results
4. **Combine expressions**: Many expressions work well together

## 📚 Next Steps

- **[Tutorials](tutorials.md)** - Step-by-step programming guides
- **[Examples](examples.md)** - See complete example programs
- **[Language Reference](language_reference.md)** - Complete syntax guide
