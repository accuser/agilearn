---
title: "@dataclass parameters"
---

# `@dataclass` parameters

Quick reference for the decorator parameters on `@dataclass` and the arguments to `dataclasses.field()`. For the tutorial treatment see the [data classes notebook](../learn/03-data-classes.ipynb).

## Decorator parameters

```python
@dataclass(
    init=True,          # generate __init__
    repr=True,          # generate __repr__
    eq=True,            # generate __eq__
    order=False,        # generate __lt__, __le__, __gt__, __ge__
    unsafe_hash=False,  # generate __hash__ even when it would be risky
    frozen=False,       # make instances immutable
    match_args=True,    # (3.10+) expose __match_args__ for match/case
    kw_only=False,      # (3.10+) all fields are keyword-only
    slots=False,        # (3.10+) use __slots__
    weakref_slot=False, # (3.11+) add a __weakref__ slot
)
class Thing:
    ...
```

| Parameter | Default | Effect |
| --- | --- | --- |
| `init` | `True` | Generate `__init__`. Set `False` if you want to write your own. |
| `repr` | `True` | Generate `__repr__`. |
| `eq` | `True` | Generate `__eq__` that compares all fields in order. |
| `order` | `False` | Generate `__lt__`/`__le__`/`__gt__`/`__ge__`. Requires `eq=True`. |
| `unsafe_hash` | `False` | Force a generated `__hash__` even when the combination of `eq`/`frozen` would normally leave hashing off. Rarely needed. |
| `frozen` | `False` | Make instances immutable. Assigning to a field raises `FrozenInstanceError`. Frozen classes get `__hash__` automatically. |
| `match_args` | `True` | Generate `__match_args__` (Python 3.10+) so the class can be used in `match` patterns. |
| `kw_only` | `False` | Make every field keyword-only. Useful when you have a lot of fields and want callers to name them at call sites. |
| `slots` | `False` | Generate a `__slots__` class. Smaller instances, rejects undeclared attributes. Note: this replaces the class with a new one, so some metaclass or weakref tricks need extra care. |
| `weakref_slot` | `False` | With `slots=True`, reserve a slot for weak references. |

## `field()` — per-attribute options

```python
from dataclasses import dataclass, field

@dataclass
class Item:
    name: str
    tags: list[str] = field(default_factory=list)
    id_: int = field(default=0, repr=False)
    _cache: dict = field(default_factory=dict, compare=False, init=False)
```

| Argument | Purpose |
| --- | --- |
| `default=` | A simple default value (immutable only). |
| `default_factory=` | A zero-arg callable called fresh for each instance. Use for `list`, `dict`, `set`, or any mutable default. |
| `init=` | If `False`, the field is not a parameter to `__init__`. Usually combined with `default` or `default_factory`. |
| `repr=` | If `False`, the field is omitted from the generated `__repr__`. Useful for noisy or sensitive fields. |
| `compare=` | If `False`, the field is ignored by `__eq__` and the ordering methods. |
| `hash=` | If `False`, the field is omitted from `__hash__`. Usually you want `compare` and `hash` aligned. |
| `metadata=` | A read-only mapping for third-party tools. Dataclass itself doesn't consult it. |
| `kw_only=` | (3.10+) Per-field keyword-only control, overriding the class-level `kw_only`. |

## Related utilities

From the `dataclasses` module:

| Function | Purpose |
| --- | --- |
| `fields(cls_or_instance)` | Returns the tuple of `Field` objects. Iterable, introspectable. |
| `asdict(instance)` | Recursively converts to a dict (nested dataclasses too). |
| `astuple(instance)` | Recursively converts to a tuple. |
| `replace(instance, **changes)` | Returns a new instance with some fields changed. Essential for `frozen=True` classes. |
| `make_dataclass(name, fields, ...)` | Creates a dataclass dynamically. Rarely needed. |
| `is_dataclass(obj)` | Returns `True` if the argument is a dataclass (class or instance). |
