---
title: Avoid common class mistakes
---

# Avoid common class mistakes

A short list of the bugs that experienced Python programmers see in junior code most often. Each one comes with a fix.

## Mutable defaults as class attributes

The bug:

```python
class Basket:
    items = []     # SHARED across all instances

    def add(self, item):
        self.items.append(item)
```

Every `Basket()` shares the same `items` list. Adding to one adds to all. The same trap appears with mutable defaults to function parameters — see [Use default and keyword arguments](../../functions/recipes/use-default-and-keyword-arguments.ipynb) in the functions guide.

The fix — set the mutable attribute per-instance in `__init__`:

```python
class Basket:
    def __init__(self):
        self.items = []
```

Or, with a dataclass, use `field(default_factory=list)`:

```python
from dataclasses import dataclass, field

@dataclass
class Basket:
    items: list = field(default_factory=list)
```

## Inheriting from `list`, `dict`, or `set` to "extend" them

The bug:

```python
class Stack(list):
    def push(self, item):
        self.append(item)
```

`Stack` now has *every* list method — `insert`, `[i] = ...`, `extend`, `reverse`. Callers can break the stack invariants without the type system noticing. The same applies to subclassing `dict` to make a "case-insensitive dict": every `dict` method needs careful overriding, and you'll miss some.

The fix — composition. Hold a `list` (or `dict`) as an attribute and expose only the operations that preserve your invariants:

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def __len__(self):
        return len(self._items)
```

If you need actual list/dict/set behaviour with a couple of changes, consider `collections.UserList`, `UserDict`, or `UserString` — they're designed to be subclassed safely.

## Forgetting `super().__init__(...)`

The bug:

```python
class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

class Car(Vehicle):
    def __init__(self, make, model, num_doors):
        self.num_doors = num_doors    # forgot super().__init__!

c = Car("Honda", "Civic", num_doors=4)
print(c.make)    # AttributeError
```

The parent's `__init__` doesn't run automatically when the child defines its own. The fix is to call it explicitly:

```python
class Car(Vehicle):
    def __init__(self, make, model, num_doors):
        super().__init__(make, model)
        self.num_doors = num_doors
```

## Defining `__eq__` without `__hash__`

The bug:

```python
class Point:
    def __init__(self, x, y):
        self.x = x; self.y = y
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

p = Point(3, 4)
{p}    # TypeError: unhashable type: 'Point'
```

Defining `__eq__` removes the inherited `__hash__`. Python does this on purpose — equal objects must have equal hashes, and Python can't guarantee that automatically.

The fix depends on whether the class is mutable:

- **Immutable** (none of the equality-relevant fields ever change): add `__hash__` that hashes the same fields `__eq__` compares.
  ```python
  def __hash__(self):
      return hash((self.x, self.y))
  ```
  Better: use `@dataclass(frozen=True)`, which generates both for you.
- **Mutable**: leave it unhashable. If you make it hashable, an instance whose equality changes while it's in a set or dict will silently disappear from lookups. That's a very nasty bug class.

## Returning `False` (not `NotImplemented`) for unknown `__eq__` types

```python
class Point:
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y    # crashes for non-Points
```

Comparing a `Point` to a string raises `AttributeError` because the string doesn't have `.x`. You might be tempted to return `False` for unknown types, but the right answer is `NotImplemented`:

```python
def __eq__(self, other):
    if not isinstance(other, Point):
        return NotImplemented
    return self.x == other.x and self.y == other.y
```

`NotImplemented` (the built-in singleton, not the exception `NotImplementedError`) tells Python to try the *other* object's `__eq__` before giving up. If you return `False`, you've prevented that — and `Point(1, 2) == 1` will silently return `False` even if some hypothetical custom number type would have considered them equal.

## Using `@property` to wrap nothing

The bug:

```python
class Box:
    def __init__(self, width):
        self._width = width

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
```

That's just a public attribute with extra typing. `@property` earns its place when you're computing something, validating something, or hiding internal storage that's likely to change. If all the getter does is return the underscored version of the name, delete it and use a plain attribute. You can always add the property *later* — Python's attribute access is uniform, so callers won't notice.

## Deep inheritance hierarchies

The bug:

```
class Animal: ...
class Mammal(Animal): ...
class Carnivore(Mammal): ...
class Canine(Carnivore): ...
class Dog(Canine): ...
class Labrador(Dog): ...
```

Reading `Labrador` now means reading six classes to know what it does. Methods defined in the middle of the chain can be overridden anywhere below, and the MRO becomes load-bearing.

The fix is design rather than syntax: prefer composition. Most "is-a" relationships in real code are better modelled as "has-a" — give your `Dog` a `breed` attribute rather than making `Labrador` a subclass. If you need polymorphism, `typing.Protocol` (covered in the [type hints guide](../../type-hints/)) gives you it without the inheritance.

## `super().__init__()` with multiple inheritance

When you have multiple inheritance, `super()` doesn't necessarily call the class you'd expect — it follows the MRO, which depends on every subclass that uses the type. This is solvable, but it's also a sign you've reached for a tool that's bigger than the problem. If you find yourself debugging C3 linearisation to understand a six-line `__init__`, step back and consider composition or a flatter hierarchy.
