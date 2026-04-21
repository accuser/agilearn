---
title: Structural pattern matching in context
---

# Structural pattern matching in context

`match`/`case` arrived in Python 3.10 (October 2021) and it's still finding its place in everyday code. If you've used a `switch` statement in C, Java, or JavaScript, your first instinct with `match` is probably wrong — it's a different tool with a different purpose.

## What it actually is

`match` does two things at once: it **destructures** a value (pulling it apart into named pieces) and it **branches** on what it found. That combination is what makes it more than a glorified `if`/`elif` chain.

Consider the difference:

```python
# if/elif — branching only
if isinstance(event, dict) and "type" in event:
    if event["type"] == "click":
        x = event.get("x")
        y = event.get("y")
        handle_click(x, y)
    elif event["type"] == "keypress":
        key = event.get("key")
        handle_key(key)

# match — branching and destructuring together
match event:
    case {"type": "click", "x": x, "y": y}:
        handle_click(x, y)
    case {"type": "keypress", "key": key}:
        handle_key(key)
```

The second form doesn't save lines for the sake of it. It says, in one place: "I'm expecting shapes that look like this, and here's what to do when I find each one." The pattern *is* the check.

## How it differs from `switch`

A C-style `switch` does one thing: it dispatches on a single value. It's `if x == 1 ... elif x == 2 ...` with nicer syntax. Some languages add fall-through, some don't. That's the whole story.

`match`/`case` dispatches on **shape** rather than value:

- literal values (`case 404:`)
- sequences of a given length (`case [x, y]:`)
- sequences with a known prefix and rest (`case [first, *rest]:`)
- dicts with required keys (`case {"type": "click"}:`)
- instances of a class with attributes in certain states (`case Point(x=0):`)
- unions of the above (`case 1 | 2 | 3:`)
- with optional guards (`case (x, y) if x == y:`)

It's closer to pattern matching in Haskell, OCaml, or Rust than to `switch` in C.

## When it earns its place

Pattern matching is a clear win when:

- **You're handling structured data with a type/kind field.** Parsing JSON responses, dispatching on message types, or handling ASTs are the classic fits.
- **You'd otherwise write nested `isinstance` + attribute access.** `match point: case Point(x=x, y=y):` is much cleaner than `if isinstance(point, Point): x, y = point.x, point.y`.
- **The branches form a closed set.** If you can enumerate all the cases at the point of the `match`, you get exhaustive handling with little ceremony.

## When it doesn't

Not every conditional benefits from becoming a `match`. Reach for `if`/`elif` when:

- **You're testing a single expression for one of a handful of values**, and the values aren't structured. `if x == 1 ... elif x == 2:` is perfectly readable; `match x:` adds ceremony without benefit.
- **Your conditions involve arithmetic or method calls** on the subject. `match` patterns check structure; `if score > 0.8 and score <= 1.0:` isn't something `match` can express naturally.
- **You need to compare against runtime values bound to local names.** Bare names in `case` patterns capture, they don't compare — `case CONSTANT:` binds `CONSTANT`, it doesn't test equality. You'd need a dotted name or a guard (`case x if x == CONSTANT:`).
- **The reader will expect C-style `switch` semantics** and be confused. If your audience is all new to `match`, the learning curve may outweigh the clarity win for small cases.

## Dict dispatch as a third option

Between `if`/`elif` and `match` sits a pattern worth remembering: **dict dispatch**.

```python
HANDLERS = {
    "click": handle_click,
    "keypress": handle_key,
}
handler = HANDLERS.get(event["type"], handle_unknown)
handler(event)
```

This works well when each branch is a simple function call keyed on a value, and the cases can be extended at runtime (plugin-style). It doesn't help when you need destructuring or guards — that's when `match` wins.

See the [Choose between if/elif chains, dict dispatch, and match/case](../recipes/choose-between-conditional-patterns.ipynb) recipe for the judgement call in practice.

## What to take away

`match` is a destructuring-and-branching tool. Use it when you have structured data and want to pick it apart while deciding what to do. Don't use it as a fancier `if`/`elif` for flat value comparisons — that's not what it's for, and the patterns syntax (especially the capture-not-compare behaviour of bare names) has enough sharp edges that "just use `if`" is often the right call.

## Further reading

- [`match`/`case` syntax](../reference/match-case-syntax.md) — every pattern type at a glance.
- [PEP 634](https://peps.python.org/pep-0634/) — the specification.
- [PEP 636](https://peps.python.org/pep-0636/) — the tutorial-style rationale from the authors.
