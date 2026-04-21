---
title: Why truthiness works the way it does
---

# Why truthiness works the way it does

Python lets you write `if items:` instead of `if len(items) > 0:`, and `if user:` instead of `if user is not None:`. That feels convenient at first, dangerous on closer inspection, and — once you've sat with it — deliberately chosen.

## The design choice

Python's designers made a specific decision: **every object should be able to answer the question "am I meaningful in this context?"** That question has different answers for different types, and the type knows best.

For a list, "meaningful" means "not empty". For a number, "non-zero". For a user-defined class, whatever the class author decides. Truthiness is the protocol that lets every type plug into conditional code without the code needing to know the type.

This is [duck typing](https://docs.python.org/3/glossary.html#term-duck-typing) applied to conditions. If an object quacks like something truthy, it is.

## The hooks

A class can define two methods to participate in truthiness:

- `__bool__(self)` returns `True` or `False` directly. Use this when the class has a natural notion of "valid" or "present" that isn't about length.
- `__len__(self)` returns an integer. If the class *is* a container, `len` doing double duty for truthiness is convenient — you only write one method.

If neither is defined, the default is "always truthy". This is why `bool(object()) is True` — a bare `object` instance has no notion of emptiness, so it can't be anything other than truthy.

## The trade-off

The idiomatic form is concise:

```python
if items:
    process(items)
```

The explicit form is precise:

```python
if items is not None and len(items) > 0:
    process(items)
```

Both are valid Python. The question is which one you want.

The idiomatic form reads better, matches how most Python is written, and works across any type that implements the truthiness protocol sensibly. The cost is that it collapses distinctions: `0` and `None`, `""` and `None`, `[]` and `None` all look the same to `if`.

If your code needs to distinguish those cases — and sometimes it does — then `is None` is the right check.

```python
def greet(name=None):
    if name is None:
        name = "friend"
    ...
```

Using `if not name:` there would treat `""` as "missing" too, which might be what you want, or might not. The explicit check forces you to decide.

## The counterargument

Some style guides (notably some corporate Python guides) push back on truthiness and prefer explicit comparisons everywhere. The argument: it's clearer to the reader, and it sidesteps the NumPy/Pandas truthiness trap (where arrays and dataframes refuse to answer `bool(...)` when they have more than one element).

That's a legitimate position. The counterargument is that idiomatic Python is what most Python *is*, and fighting the convention makes your code read less like Python, not more.

Where most working Python lands: use truthiness for "is this thing meaningful?" checks, use `is None` when the distinction between "missing" and "empty" matters, and know which of those two questions you're asking.

## Where it bites

The traps are concentrated in a small set of cases:

- **Numeric zero** is falsy. A function returning `0` will look "empty" to `if result:` even though the call succeeded.
- **NumPy and Pandas** refuse to coerce multi-element arrays to `bool` — they raise `ValueError: The truth value of an array ... is ambiguous`. Use `.any()`, `.all()`, or `.empty` instead.
- **Custom classes without `__len__`** are always truthy, which might not be what you want. Add `__bool__` if the notion of "valid" applies.

Each of these is well-known enough to avoid with a little care. None of them is a reason to abandon the convention; they're reasons to know when you're in one of the sharp corners.

## Further reading

- [Truthiness rules](../reference/truthiness-rules.md) — the canonical falsy list and how `__bool__`/`__len__` interact.
- [Avoid common conditional mistakes](../recipes/avoid-common-conditional-mistakes.md) — the sharp corners in practical form.
