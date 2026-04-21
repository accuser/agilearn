---
title: match/case syntax
---

# `match`/`case` syntax

Every pattern type available in Python's structural pattern matching (Python 3.10+), at a glance. For the tutorial walkthrough, see [Pattern matching with match/case](../learn/03-pattern-matching-with-match-case.ipynb).

## Basic shape

```python
match subject:
    case pattern_1:
        ...
    case pattern_2:
        ...
    case _:
        ...   # wildcard — matches anything
```

The subject is evaluated once. Cases are tried in order; the first match wins.

## Pattern types

### Literal patterns

Match exact values. Literals compare with `==`, except `None`, `True`, and `False`, which compare with `is`.

```python
match status:
    case 200:    print("OK")
    case 404:    print("Not Found")
    case "pending": print("waiting")
    case None:   print("no status")
```

### Capture patterns

A bare name *binds* the matched value — it's not a comparison.

```python
match point:
    case (0, 0):
        print("origin")
    case (x, y):            # x and y are bound to the values
        print(f"at ({x}, {y})")
```

Use `_` as the capture name when you don't need the value — it's the wildcard.

### Sequence patterns

Match tuples, lists, and other sequences (but not strings or bytes).

```python
match items:
    case []:                print("empty")
    case [x]:               print(f"one: {x}")
    case [x, y]:            print(f"two: {x}, {y}")
    case [x, *rest]:        print(f"{x} and {len(rest)} more")
```

Fixed-length, variable-length with `*rest`, and positional binding all work.

### Mapping patterns

Match dicts. Keys are compared by `==`; only the specified keys need to be present.

```python
match config:
    case {"host": host, "port": port}:
        connect(host, port)
    case {"host": host}:
        connect(host, default_port)
    case {}:
        raise ValueError("config is empty")
```

Extra keys in the subject are ignored. Use `**rest` to capture them.

### Class patterns

Match instances of a class and bind attributes by name or position.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

match shape:
    case Point(x=0, y=0):
        print("origin")
    case Point(x=x, y=y):
        print(f"at ({x}, {y})")
```

For positional matching, a class needs `__match_args__` (dataclasses set this automatically).

### OR patterns

Combine patterns with `|` — matches if any alternative matches.

```python
match day:
    case "Saturday" | "Sunday":
        print("weekend")
    case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
        print("weekday")
```

All alternatives must bind the same names (or none).

### Guarded patterns

Add an `if` guard to a case — it must evaluate to truthy for the case to match.

```python
match point:
    case (x, y) if x == y:
        print("on the diagonal")
    case (x, y):
        print(f"at ({x}, {y})")
```

The guard runs only after the pattern structure matches.

### AS patterns

Bind a name to a pattern with `as` — useful when you want both the destructured parts and the whole.

```python
match command:
    case ("move", direction) as cmd:
        log(cmd)           # the full tuple
        do_move(direction) # the captured piece
```

### Wildcard

`_` matches anything and binds nothing. Convention for the default case.

```python
match value:
    case 0:
        print("zero")
    case _:
        print("something else")
```

## Gotchas

- **Bare names capture**, they don't compare. `case CONSTANT:` will bind `CONSTANT` to whatever the subject is, even if `CONSTANT` is defined elsewhere. To compare against a constant, use a dotted name (`case module.CONSTANT:`) or wrap in parentheses with a literal.
- **Strings are not sequences** for matching purposes — `case [a, b, c]:` does *not* match the string `"abc"`.
- **No fall-through.** Unlike `switch` in C-family languages, once a case matches, the `match` block ends. You don't need `break`.

## Related pages

- [Structural pattern matching in context](../concepts/structural-pattern-matching-in-context.md) — when to reach for `match`/`case` and when not to.
- [Choose between if/elif chains, dict dispatch, and match/case](../recipes/choose-between-conditional-patterns.ipynb) — the judgement call.
