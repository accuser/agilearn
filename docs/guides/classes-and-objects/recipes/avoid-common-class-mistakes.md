# Avoid common class mistakes

**The question.** You're reviewing a class and something smells — a mutable default shared between instances, an `__eq__` without `__hash__`, a six-level inheritance chain. You want the short list of traps and the fix for each.

The short list is below, then each trap in detail.

## The answer

| Looks like… | Why it bites | Fix |
| --- | --- | --- |
| `items = []` as class attribute | Shared across all instances | Move to `__init__`, or `field(default_factory=list)` |
| `class Stack(list)` | Exposes every list method; invariants slip | Composition: `self._items = []`, expose only the methods you want |
| Child `__init__` without `super().__init__(...)` | Parent setup never runs | Call `super().__init__(...)` first |
| `__eq__` without `__hash__` | Instance becomes unhashable, breaks sets/dicts | `@dataclass(frozen=True)`, or add a matching `__hash__` — if the class is immutable |
| `return False` for unknown `__eq__` types | Blocks the other side's `__eq__` | `return NotImplemented` |
| `@property` that just returns `self._x` | Public attribute with extra typing | Delete the property, use a plain attribute |
| `Dog(Canine(Carnivore(Mammal(Animal))))` | Deep MRO, hard to reason about | Prefer composition; `typing.Protocol` for polymorphism |
| `super().__init__()` in multiple inheritance | MRO-dependent, surprises readers | Step back — flatter hierarchy or composition |

Each of these in turn below.

## Mutable defaults as class attributes

```python
class Basket:
    items = []     # SHARED across all instances

    def add(self, item):
        self.items.append(item)
```

Every `Basket()` shares the same `items` list. Adding to one adds to all. Same trap as the mutable-default-argument bug — the default is created once, when the class body runs, and then reused forever.

Fix: set mutable state in `__init__`, or use `field(default_factory=list)` on a dataclass.

```python
class Basket:
    def __init__(self):
        self.items = []

# or
from dataclasses import dataclass, field

@dataclass
class Basket:
    items: list = field(default_factory=list)
```

## Inheriting from `list`, `dict`, or `set` to "extend" them

```python
class Stack(list):
    def push(self, item):
        self.append(item)
```

`Stack` inherits *every* list method — `insert`, `extend`, slice assignment. Callers can break the LIFO invariant without the type system noticing. The same applies to subclassing `dict` for a case-insensitive dict: you'll miss an override somewhere.

Fix: composition. Hold a `list` as an attribute, expose only the operations that preserve your invariants. If you genuinely need near-list behaviour with tweaks, `collections.UserList`, `UserDict`, or `UserString` are built to be subclassed.

## Forgetting `super().__init__(...)`

```python
class Car(Vehicle):
    def __init__(self, make, model, num_doors):
        self.num_doors = num_doors      # forgot super().__init__!
```

The parent's `__init__` doesn't run automatically when the child defines its own. Attribute access to anything the parent would have set will raise `AttributeError`.

Fix: call `super().__init__(...)` first.

```python
class Car(Vehicle):
    def __init__(self, make, model, num_doors):
        super().__init__(make, model)
        self.num_doors = num_doors
```

## Defining `__eq__` without `__hash__`

```python
class Point:
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

{Point(3, 4)}      # TypeError: unhashable type: 'Point'
```

Defining `__eq__` removes the inherited `__hash__` on purpose: equal objects must have equal hashes, and Python can't guarantee that automatically. The fix depends on mutability:

- **Immutable** (the equality-relevant fields never change after construction): add `__hash__` that hashes the same fields `__eq__` compares. Better still, `@dataclass(frozen=True)` does both.
- **Mutable**: leave it unhashable. If you make it hashable and its equality changes while it's in a set or dict, lookups silently miss.

## Returning `False` (not `NotImplemented`) for unknown `__eq__` types

```python
def __eq__(self, other):
    if not isinstance(other, Point):
        return NotImplemented      # not False, not raise
    return (self.x, self.y) == (other.x, other.y)
```

`NotImplemented` (the singleton, not the exception) tells Python to try the other side's `__eq__` before giving up. Returning `False` would block that — `Point(1, 2) == some_custom_num` would return `False` even if the custom number type would have said they were equal.

## Using `@property` to wrap nothing

```python
@property
def width(self):
    return self._width

@width.setter
def width(self, value):
    self._width = value
```

That's a public attribute with extra typing. `@property` earns its place when you're computing, validating, or hiding internal storage that's likely to change. If the getter only returns the underscored version of the name, delete the property and use a plain attribute. You can add the property *later* without changing any call sites.

## Deep inheritance hierarchies

```
Animal → Mammal → Carnivore → Canine → Dog → Labrador
```

Reading `Labrador` now means reading six classes to know what it does. Methods defined in the middle of the chain can be overridden anywhere below, and the MRO becomes load-bearing. The fix is design: prefer composition. Give `Dog` a `breed` attribute rather than making `Labrador` a subclass. For polymorphism without inheritance, `typing.Protocol` is often what you actually want.

## `super().__init__()` with multiple inheritance

With multiple inheritance, `super()` follows the **MRO** (method-resolution order), which depends on every subclass that uses the type. This is solvable — cooperative `super()` calls are a real pattern — but it's also a sign you've reached for a tool bigger than the problem. If you find yourself reasoning about C3 linearisation to understand a six-line `__init__`, step back and consider composition or a flatter hierarchy.

## When the pattern is fine

Each of these is a *pattern*, not an absolute rule. Subclassing `UserDict` is fine when you need dict behaviour with two or three tweaks. A well-documented class attribute is fine when the attribute is genuinely shared (a class-level constant, say — `RETRY_LIMIT = 3`). Single-level inheritance is fine when the relationship really is "is-a" and the parent has real state or behaviour to share.

The traps bite when the shortcut is applied out of habit to a case where the defaults don't match the intent.

## Related reading

- [Choose between @dataclass, NamedTuple, and a plain class](choose-between-dataclass-namedtuple-class.md) — often the right fix is "don't write a class in the first place".
- [Validate attributes on assignment](validate-attributes-on-assignment.ipynb) — the `@property`-that-does-nothing antipattern in its own recipe.
- [Dataclass parameters](../reference/dataclass-parameters.md) — every `@dataclass` option in one place.
