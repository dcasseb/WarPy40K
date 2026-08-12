# WarPy40K 1.0 Official Showcase — The Vault of Vharax

`examples/vault_of_vharax.wp40k` is the official application showcase for WarPy40K 1.0.

It is a small terminal roguelike/RPG written entirely in WarPy40K source code. Its purpose is different from the Minsky-machine example: the Minsky interpreter demonstrates computational universality, while **The Vault of Vharax** demonstrates that the same language core can support a coherent interactive program with game state, rules, input, random events, combat, progression, and multiple endings.

## Run it

```bash
warpy40k examples/vault_of_vharax.wp40k
```

## Premise

You are an Inquisitorial acolyte descending through four sealed sectors beneath a dead forge-city. Each sector contains environmental risk and a hostile encounter. The final sector is controlled by Arch-Heretek Vharax.

The player manages five resources:

- `health` — reaching zero ends the run;
- `faith` — empowers Inquisition actions and sanctified events;
- `corruption` — reaching 100 destroys the character;
- `medicae` — limited healing charges;
- `relics` — recovered artifacts that contribute to the final score.

## Structure

The game contains four sectors:

1. **Ash Gate**
2. **Reliquary of Static**
3. **Choir of Rust**
4. **Throne of the Heretek**

Each sector has two phases.

### Exploration

The player can:

- advance immediately;
- search for supplies or relics;
- pray to recover Faith and reduce Corruption;
- withdraw from the vault.

Exploration is affected by `Chaos`, so the same strategic decision can lead to different outcomes.

### Combat

Combat is turn-based. Available actions are:

- **Boltgun** — reliable ranged damage;
- **Chainsword** — higher damage with greater exposure;
- **Inquisition** — a Faith-powered judgment strike that can backfire when Faith is insufficient relative to Corruption;
- **Medicae** — restore health at the cost of a finite charge and increased exposure during the turn.

After each surviving enemy encounter, the player gains a relic and partial recovery before advancing to the next sector.

## WarPy40K semantics used as game mechanics

The showcase deliberately uses the language's themed expressions as real mechanics rather than as decorative aliases.

### `Chaos`

```text
roll = Chaos;
```

`Chaos` drives encounter variance, search outcomes, environmental events, and combat damage.

### `Inquisition`

```text
if Inquisition (faith >= corruption + 10) {
    ...
}
```

`Inquisition` represents judgment: high Faith relative to Corruption allows a powerful combat action.

### `Bless`

```text
faith = min(100, Bless faith);
```

`Bless` strengthens Faith after sanctified discoveries and prayer.

### `Curse`

```text
health = Curse health;
```

`Curse` represents harmful transformations caused by traps and Warp exposure.

### `Emperor`

```text
health = min(100, health + Emperor 5);
```

`Emperor` participates in restorative effects during successful prayer.

### `Purge`

```text
corruption = Purge corruption;
```

Victory explicitly purges the remaining corruption state.

### `Exterminatus`

```text
final_protocol = Exterminatus;
```

The victorious ending uses the language-level annihilation marker as the vault's final sanction protocol.

## General language features exercised

The game is also a practical regression target for the core language:

- user-defined functions;
- lexical function scopes;
- function arguments and return values;
- mutable local state;
- nested `if` / `else`;
- unrestricted `while`;
- Boolean logic;
- strings and numbers;
- arithmetic and comparisons;
- calls to built-in functions;
- terminal input/output;
- nondeterministic execution through `Chaos`.

The game does **not** use Python `eval`, Python game logic, Python-side data structures, or a Python helper implementing the rules. Python only hosts the WarPy40K interpreter, exactly as it does for every `.wp40k` program.

## Why the game is intentionally small

WarPy40K 1.0 does not yet have native collection types such as the planned `Squad` and `Dataslate`. As a result, the showcase models the player's state with a small set of scalar values and generates enemies from the current sector instead of maintaining inventories or entity collections.

This limitation is useful: it establishes a concrete baseline for future versions. When v1.1 introduces native structured data, the same showcase can evolve toward:

- real inventories;
- equipment records;
- multiple enemies per encounter;
- persistent squads;
- procedural room collections;
- richer loot tables.

## Automated validation

`tests/test_showcase_v10.py` protects the showcase with three checks:

1. the complete source file must parse as a valid WarPy40K program;
2. gameplay helper functions must execute correctly inside the WarPy40K interpreter;
3. a deterministic full-program withdrawal session must start, accept input, traverse the main loop, and terminate normally.

This makes the showcase part of the language's regression suite rather than an untested example.

## Two complementary v1.0 showcases

WarPy40K 1.0 therefore ships with two different demonstrations:

| Showcase | Demonstrates |
|---|---|
| `minsky_universal.wp40k` | computational universality |
| `vault_of_vharax.wp40k` | practical interactive programming |

Together they answer two different questions:

- **Can WarPy40K express arbitrary computation?** — the Minsky interpreter demonstrates that it can under the usual theoretical model.
- **Can WarPy40K already be used to write an actual program with meaningful behavior?** — The Vault of Vharax demonstrates that it can.
