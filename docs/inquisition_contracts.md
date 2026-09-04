# Inquisition Contracts

WarPy40K v1.4 turns judgment into executable specification.

## Assertions

```text
Inquisition Assert health > 0
```

False enabled assertions raise `ContractViolation` with source location, condition, and relevant identifier values.

## Preconditions and postconditions

```text
def heal(health, amount)
Inquisition Requires health > 0
Inquisition Requires amount > 0
Inquisition Ensures result >= health
{
    return health + amount
}
```

`Requires` runs after argument binding and before the body. `Ensures` runs after the return value is known and may reference parameters plus temporary `result`.

## Optional checking

`Interpreter(contracts_enabled=False)` disables condition evaluation entirely.

## Compatibility

Existing `Inquisition value` Boolean judgment remains intact. `Assert`, `Requires`, and `Ensures` are contextual identifiers, not global reserved words.

## Performance

Contract-enabled and contract-disabled execution should be benchmarked separately so validation overhead remains explicit.
