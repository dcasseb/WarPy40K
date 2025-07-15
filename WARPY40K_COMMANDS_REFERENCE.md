# WarPy40K Commands Reference

This document provides a complete reference of all commands available in the WarPy40K programming language. Print this page for a handy reference while writing WarPy40K scripts!

## Table of Contents

1. [Command Categories](#command-categories)
2. [Complete Command List](#complete-command-list)
3. [Command Usage Examples](#command-usage-examples)
4. [Input Function](#input-function)
5. [Command Categories by Faction](#command-categories-by-faction)

---

## Command Categories

WarPy40K commands are organized into several thematic categories based on the Warhammer 40,000 universe:

- **Imperial Commands**: Loyal to the Emperor
- **Chaos Commands**: Corrupted by the Warp
- **Ork Commands**: Brutal and cunning
- **Eldar Commands**: Ancient and mysterious
- **General Commands**: Universal utility
- **Input Function**: User interaction

---

## Complete Command List

| Command | Category | Usage | Effect | Arguments |
|---------|----------|-------|--------|-----------|
| `the_emperor_protects()` | Imperial | `the_emperor_protects()` | Logs: "The Emperor protects!" | None |
| `only_in_death_does_duty_end()` | Imperial | `only_in_death_does_duty_end()` | Logs: "Only in death does duty end." | None |
| `even_in_death_i_still_serve()` | Imperial | `even_in_death_i_still_serve()` | Logs: "Even in death, I still serve!" | None |
| `no_pity_no_remorse_no_fear()` | Imperial | `no_pity_no_remorse_no_fear()` | Logs: "No pity, no remorse, no fear!" | None |
| `pain_is_temporary_glory_is_forever()` | Imperial | `pain_is_temporary_glory_is_forever()` | Logs: "Pain is temporary, glory is forever." | None |
| `faith_is_my_shield()` | Imperial | `faith_is_my_shield()` | Logs: "Faith is my shield!" | None |
| `we_are_angels_of_death()` | Imperial | `we_are_angels_of_death()` | Logs: "We are the Angels of Death!" | None |
| `for_the_emperor()` | Imperial | `for_the_emperor()` | Logs: "For the Emperor!" | None |
| `the_emperors_will_be_done()` | Imperial | `the_emperors_will_be_done()` | Logs: "The Emperor's will is fulfilled." | None |
| `ave_imperator()` | Imperial | `ave_imperator()` | Logs: "Ave Imperator! Glory to the Emperor!" | None |
| `burn_the_heretic(arg)` | Imperial | `burn_the_heretic("traitor")` | Logs: "Burn the heretic: [arg]" | String/Expression |
| `purge_the_xenos(arg)` | Imperial | `purge_the_xenos("alien")` | Logs: "Xenos purged: [arg]!" | String/Expression |
| `fear_is_the_mind_killer()` | Imperial | `fear_is_the_mind_killer()` | Logs: "Fear suppressed." | None |
| `we_are_one()` | General | `we_are_one()` | Logs: "We are one." | None |
| `WAAAGH()` | Ork | `WAAAGH()` | Logs: "The orks rally!" | None |
| `more_dakka()` | Ork | `more_dakka()` | Logs: "More dakka! Fire everything!" | None |
| `ork_cunning()` | Ork | `ork_cunning()` | Logs: "Cunning plan!" | None |
| `taste_chaos()` | Chaos | `taste_chaos()` | Logs: "Warp corrupts your soul." | None |
| `blood_for_the_blood_god()` | Chaos | `blood_for_the_blood_god()` | Logs: "Blood for the Blood God!" | None |
| `let_the_galaxy_burn()` | Chaos | `let_the_galaxy_burn()` | Logs: "The galaxy burns!" | None |
| `the_path_is_set()` | Eldar | `the_path_is_set()` | Logs: "The path is set. We proceed." | None |
| `farseers_vision()` | Eldar | `farseers_vision()` | Logs: "The Farseer foresees..." | None |
| `servitor()` | General | `servitor()` | Returns: "servitor_instance" | None |
| `hear_the_emperors_voice(prompt)` | Input | `hear_the_emperors_voice("Enter name:")` | Prompts for user input | Optional string |

---

## Command Usage Examples

### Basic Command Calls
```warpy40k
# Simple commands without arguments
the_emperor_protects()
for_the_emperor()
WAAAGH()

# Commands with string arguments
burn_the_heretic("traitor")
purge_the_xenos("tyranid")

# Commands with variable arguments
target: servitor = "heretic"
burn_the_heretic(target)
```

### Commands in Variables
```warpy40k
# Store command result in variable
result: servitor = servitor()

# Use input in variable declaration
name: servitor = hear_the_emperors_voice("Enter your name:")
```

### Commands in Expressions
```warpy40k
# Use input in arithmetic expressions
count: dg = hear_the_emperors_voice("Enter count:")
result: dg = count + 5

# Use input in conditionals
power: dg = hear_the_emperors_voice("Enter power level:")
if power > 50:
    the_emperors_will_be_done()
else:
    fear_is_the_mind_killer()
```

### Commands in Loops
```warpy40k
# Commands in for loops
for i in 1..5:
    burn_the_heretic("heretic_" + str(i))
    the_emperor_protects()

# Commands in while loops
counter: dg = 3
while counter > 0:
    for_the_emperor()
    counter = counter - 1
```

### Commands in Conditionals
```warpy40k
# Imperial vs Chaos choice
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

## Input Function

The `hear_the_emperors_voice()` function is the primary way to get user input in WarPy40K:

### Syntax
```warpy40k
hear_the_emperors_voice()                    # Uses default prompt
hear_the_emperors_voice("Custom prompt:")    # Uses custom prompt
```

### Usage Examples
```warpy40k
# Basic input
name: servitor = hear_the_emperors_voice("Enter your name:")

# Numeric input (automatically converted for dg type)
age: dg = hear_the_emperors_voice("Enter your age:")

# Input in expressions
count: dg = hear_the_emperors_voice("Enter count:")
total: dg = count * 2 + 10

# Input in conditionals
power: dg = hear_the_emperors_voice("Enter power level:")
if power > 75:
    the_emperors_will_be_done()
elif power > 25:
    faith_is_my_shield()
else:
    fear_is_the_mind_killer()
```

### Type Conversion
- When used with `dg` type variables, input strings are automatically converted to numbers
- Invalid conversions (non-numeric input for `dg` type) will cause runtime errors
- Empty input for `dg` type will cause runtime errors

---

## Command Categories by Faction

### Imperial Commands (Loyal to the Emperor)
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

### Chaos Commands (Corrupted by the Warp)
```warpy40k
taste_chaos()                    # Warp corrupts your soul.
blood_for_the_blood_god()        # Blood for the Blood God!
let_the_galaxy_burn()            # The galaxy burns!
```

### Ork Commands (Brutal and Cunning)
```warpy40k
WAAAGH()                         # The orks rally!
more_dakka()                     # More dakka! Fire everything!
ork_cunning()                    # Cunning plan!
```

### Eldar Commands (Ancient and Mysterious)
```warpy40k
the_path_is_set()                # The path is set. We proceed.
farseers_vision()                # The Farseer foresees...
```

### General Commands (Universal)
```warpy40k
we_are_one()                     # We are one.
servitor()                       # Returns "servitor_instance"
hear_the_emperors_voice(prompt)  # User input function
```

---

## Quick Reference Card

### Most Common Commands
```warpy40k
the_emperor_protects()           # Basic Imperial command
for_the_emperor()                # Imperial rallying cry
burn_the_heretic("target")       # Imperial action
WAAAGH()                         # Ork rally
taste_chaos()                    # Chaos corruption
hear_the_emperors_voice()        # Get user input
```

### Command Patterns
```warpy40k
# Simple command
command_name()

# Command with argument
command_name("argument")
command_name(variable)

# Command in variable
result: servitor = servitor()

# Command in expression
input: dg = hear_the_emperors_voice("Prompt:")
```

---

## Tips for Using Commands

1. **Choose Thematically**: Use Imperial commands for loyalist programs, Chaos for corruption themes, etc.
2. **Combine with Logic**: Use commands in conditionals and loops for dynamic behavior
3. **User Interaction**: Use `hear_the_emperors_voice()` for interactive programs
4. **Error Handling**: Commands with arguments will handle type conversion automatically
5. **Debugging**: Commands print their effects, making them useful for program flow tracking

---

*For the Emperor! The WarPy40K language serves the Imperium of Man.* 