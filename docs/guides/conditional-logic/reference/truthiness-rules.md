---
title: Truthiness rules
---

# Truthiness rules

The canonical list of what Python treats as truthy or falsy in a boolean context — that is, anywhere a value is used inside `if`, `while`, `and`, `or`, `not`, `filter`, or `bool()`.

## The falsy values

Python has a small, fixed set of values that are considered falsy:

| Category          | Falsy values |
|-------------------|--------------|
| The `None` object | `None` |
| Booleans          | `False` |
| Numbers           | `0`, `0.0`, `0j`, `Decimal(0)`, `Fraction(0, 1)` |
| Empty sequences   | `""`, `()`, `[]`, `range(0)` |
| Empty mappings    | `{}` |
| Empty sets        | `set()`, `frozenset()` |
| Empty bytes       | `b""`, `bytearray(b"")` |

**Everything else is truthy.** There is no other falsy value in the standard library unless a class implements one of the hooks below.

## Practical implications

```python
if items:           # True when items is a non-empty sequence
if not items:       # True when items is empty or None

if count:           # True when count is non-zero
if count is not None and count >= 0:  # the explicit version
```

The short form is usually preferable — unless the difference between "zero" and "missing" matters, in which case you need the explicit `is not None` check. See [Avoid common conditional mistakes](../recipes/avoid-common-conditional-mistakes.md) for the distinction.

## Customising truthiness for your own classes

Python calls `__bool__()` (if defined) or `__len__()` (if `__bool__` is absent) to decide whether an instance is truthy. If neither is defined, every instance is truthy by default.

### Using `__bool__`

```python
class TemperatureReading:
    def __init__(self, celsius, valid):
        self.celsius = celsius
        self.valid = valid

    def __bool__(self):
        return self.valid

r = TemperatureReading(18.5, valid=True)
if r:
    print(f"Got a reading of {r.celsius} °C")
```

### Using `__len__`

If your class represents a container, defining `__len__` makes it falsy when empty without needing a separate `__bool__`:

```python
class Queue:
    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

q = Queue()
if not q:           # True — __len__ returns 0
    print("queue is empty")
```

`bool(q)` calls `__len__` and returns `True` if the length is non-zero.

### The priority

If a class defines both `__bool__` and `__len__`, `__bool__` wins. If both are absent, instances are always truthy — including instances of classes like `object()`, which is why `bool(object()) is True`.

## Gotchas

- **NumPy arrays** override `__bool__` to raise `ValueError` for arrays with more than one element — use `.any()` or `.all()` instead.
- **Pandas `DataFrame` / `Series`** do the same. The fix is again `.any()`, `.all()`, or `.empty`.
- **Custom classes without `__len__`** are always truthy even if "empty" — don't rely on truthiness for types you haven't hooked into.

## Related pages

- [Why truthiness works the way it does](../concepts/why-truthiness-works-the-way-it-does.md) — the design rationale.
- [Comparison and boolean operators](comparison-and-boolean-operators.md) — the operators that use truthiness.
