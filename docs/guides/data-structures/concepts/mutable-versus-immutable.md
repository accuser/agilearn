# Mutable versus immutable

Python distinguishes between objects that can be changed after creation (mutable) and objects that cannot (immutable). Understanding this distinction is fundamental to writing correct and predictable Python code.

## What mutability means

An object is **mutable** if its state can be modified after it is created. An object is **immutable** if its state cannot be changed — any operation that appears to modify it actually creates a new object.

## Mutable types

The following built-in data structures are mutable:

- **Lists** — you can add, remove, and change items
- **Dictionaries** — you can add, remove, and update key-value pairs
- **Sets** — you can add and remove elements

```python
# Lists are mutable
fruits = ["apple", "banana"]
fruits.append("cherry")  # Modifies the original list

# Dictionaries are mutable
person = {"name": "Alice"}
person["age"] = 30  # Modifies the original dictionary
```

## Immutable types

The following built-in types are immutable:

- **Tuples** — cannot add, remove, or change items
- **Strings** — cannot change individual characters
- **Frozensets** — cannot add or remove elements
- **Numbers** (integers, floats, booleans)

```python
# Tuples are immutable
coordinates = (51.5074, -0.1278)
# coordinates[0] = 52.0  # This would raise TypeError
```

## Why immutability matters

### Safety

Immutable objects cannot be changed accidentally. If you pass a tuple to a function, you know the function cannot modify it.

### Hashability

Immutable objects can be **hashed**, which means they can be used as dictionary keys and set members. This is because their hash value never changes.

```python
# Tuples can be dictionary keys
locations = {(51.5074, -0.1278): "London"}

# Lists cannot be dictionary keys
# {[1, 2]: "value"}  # This would raise TypeError
```

### Predictability

When an object is immutable, you can reason about its value with confidence. There is no risk of another part of your program changing it unexpectedly.

## Identity versus equality

Python distinguishes between **identity** (whether two variables point to the same object) and **equality** (whether two objects have the same value).

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)   # True — same value
print(a is b)   # False — different objects
```

This distinction becomes important with mutable objects because of aliasing.

## Aliasing and copying

### The aliasing problem

When you assign a mutable object to a new variable, both variables point to the **same object** in memory. Changes through one variable are visible through the other:

```python
original = [1, 2, 3]
alias = original  # Both point to the same list

alias.append(4)
print(original)  # [1, 2, 3, 4] — the original changed too
```

### Shallow copies

A shallow copy creates a new object but does not copy nested objects:

```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)

shallow[0].append(99)
print(original)  # [[1, 2, 99], [3, 4]] — nested list was shared
```

You can also use `list.copy()`, `dict.copy()`, or slice notation `[:]` for shallow copies.

### Deep copies

A deep copy creates a completely independent copy, including all nested objects:

```python
import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

deep[0].append(99)
print(original)  # [[1, 2], [3, 4]] — original is unchanged
```

## Common pitfalls

### Mutable default arguments

A common mistake is using a mutable object as a default argument. The default is created once and shared across all calls:

```python
# Problematic
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))  # ["a"]
print(add_item("b"))  # ["a", "b"] — not ["b"] as expected
```

The fix is to use `None` as the default and create a new list inside the function:

```python
# Correct
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Modifying a list while iterating

Changing a list while looping over it can lead to skipped items or infinite loops:

```python
# Problematic — skips items
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)
```

Instead, iterate over a copy or use a list comprehension:

```python
# Correct — use a comprehension
numbers = [1, 2, 3, 4, 5]
numbers = [n for n in numbers if n % 2 != 0]
```

## When to choose mutable versus immutable

Choose **mutable** (list, dict, set) when:

- The collection needs to grow, shrink, or change over time
- You are building up a result incrementally
- You need to modify items in place

Choose **immutable** (tuple, frozenset, string) when:

- The data should not change after creation
- You need to use the data as a dictionary key or set member
- You want to prevent accidental modification
- You are returning data that should be read-only

## Summary

Mutability is a core concept in Python that affects how you work with data structures. Mutable objects offer flexibility but require care to avoid unintended side effects. Immutable objects provide safety and predictability at the cost of requiring new objects for any changes. Understanding this trade-off helps you choose the right data structure for each situation.
