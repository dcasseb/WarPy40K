# Warp Effect Model

WarPy40K v1.3 makes nondeterminism explicit and replayable.

## Syntax

```text
Warp seed 42 {
    roll = Chaos
    sample = random()
}
```

`seed` is contextual syntax after `Warp`; it remains a normal identifier elsewhere. The seed expression is evaluated exactly once and must produce an integer. Booleans are rejected.

## Deterministic region-local streams

Entering a Warp region creates a fresh deterministic random stream. Every `Chaos` draw and built-in `random()` call inside that dynamic region consumes the same stream. Functions invoked from the region therefore participate in the same deterministic sequence.

The same program, inputs, and Warp seed produce the same random decisions. Code outside Warp retains legacy process-global randomness for 1.x compatibility.

## Nesting

```text
Warp seed 10 {
    first = random()
    Warp seed 99 {
        nested = Chaos
    }
    second = random()
}
```

Nested Warp regions own independent streams. A nested draw does not perturb the parent stream. Structured cleanup restores the previous stream even when execution exits through an error or function return.

## Record and replay

The reference interpreter exposes normalized decisions:

```python
interpreter = Interpreter()
interpreter.execute(ast)
trace = interpreter.warp_trace
```

They can be replayed later:

```python
replay = Interpreter(warp_replay=trace)
replay.execute(ast)
assert replay.warp_replay_complete
```

Replay consumes recorded normalized draws instead of generating new ones. The seed is still evaluated and validated, but the supplied trace determines outcomes. Exhausted, nonnumeric, or out-of-range traces fail explicitly.

Recording decisions instead of Python `random.Random` internal state gives future Forge runtimes a portable semantic contract without requiring CPython RNG compatibility.

## Performance rule

Warp bookkeeping is constant-time per draw: an active-stack lookup plus one append or indexed read when recording/replaying. Replay never reparses source or rebuilds the AST per decision.

## Compatibility

WarPy40K 1.3 does not make all randomness deterministic. Existing `Chaos` and `random()` outside Warp continue to behave as in earlier 1.x versions. Programs requiring reproducibility should place nondeterministic logic inside explicit Warp regions.
