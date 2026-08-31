# Orders and Pattern Dispatch — WarPy40K 1.2

`Order` is WarPy40K's structured decision construct. It is intentionally more expressive than a traditional `switch`: clauses may match structured native values, bind pieces of those values, and apply guards.

## Basic dispatch

```text
Order action {
    When "1" {
        print("Boltgun")
    }

    When "2" {
        print("Chainsword")
    }

    Otherwise {
        print("Invalid order")
    }
}
```

Clauses are evaluated from top to bottom. The first matching `When` is executed and there is no fall-through.

## Literal patterns

Supported exact-value patterns include integers, floats, strings, Booleans, and negative numeric literals:

```text
Order threat {
    When 0 { print("Clear") }
    When -1 { print("Invalid auspex reading") }
    When 10 { print("Critical") }
}
```

## Wildcard

`_` matches any value without creating a binding:

```text
Order signal {
    When _ {
        print("Signal acknowledged")
    }
}
```

## Bindings

An identifier in a pattern captures the matched value:

```text
Order 42 {
    When value {
        print(value)
    }
}
```

`value` exists only while evaluating that clause's guard and body. If an outer variable has the same name, its previous value is restored afterward.

## Dataslate patterns

Dataslate patterns are partial structural matches. Fields not listed by the pattern are ignored:

```text
target = Dataslate{
    name: "Vharax",
    status: "Heretic",
    threat: 8
}

Order target {
    When Dataslate{status: "Heretic", threat: level} {
        print("Threat:", level)
    }

    Otherwise {
        print("Observe")
    }
}
```

A required field must exist and its nested pattern must match.

## Guards

A `When` may add an `if` guard. Pattern bindings are available to the guard:

```text
Order target {
    When Dataslate{status: "Heretic", threat: level} if level > 5 {
        print("Exterminatus review")
    }

    When Dataslate{status: "Heretic"} {
        print("Purge")
    }
}
```

If the structural pattern matches but the guard evaluates to false, matching continues with the next clause.

## Squad patterns

Squad patterns currently require the same number of members as the target Squad:

```text
formation = Squad["Titus", 100]

Order formation {
    When Squad[name, health] if health == 100 {
        print(name)
    }

    Otherwise {
        print("Formation mismatch")
    }
}
```

Rest/spread patterns are not part of v1.2.

## Otherwise and unmatched Orders

`Otherwise` is optional, may occur at most once, and must come after all `When` clauses. If no `When` matches and there is no `Otherwise`, the Order performs no action and produces `None` internally.

## Pattern restrictions

- a plain pattern identifier is a binding, not a variable lookup;
- duplicate binding names inside one pattern are rejected;
- duplicate Dataslate fields inside one pattern are rejected;
- `When` clauses cannot appear after `Otherwise`;
- `Order` is a statement in v1.2, not a first-class expression.

## Showcase

The official `examples/vault_of_vharax.wp40k` showcase uses `Order` for exploration and combat command dispatch. This makes the game a regression benchmark for both scalar command matching and the broader v1.2 runtime.
