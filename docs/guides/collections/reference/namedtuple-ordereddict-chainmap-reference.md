---
title: namedtuple, OrderedDict, and ChainMap reference
---

# `namedtuple`, `OrderedDict`, and `ChainMap` reference

```python
from collections import namedtuple, OrderedDict, ChainMap
```

## `namedtuple`

A factory that builds a tuple subclass with named fields.

### Defining and creating

| Form | Result |
| --- | --- |
| `namedtuple('Point', ['x', 'y'])` | a class with fields `x`, `y` |
| `namedtuple('Point', 'x y')` | same — space/comma-separated string |
| `namedtuple('P', 'x y', defaults=[0])` | `defaults` fill from the **right** (`y=0`) |
| `namedtuple('P', ['class'], rename=True)` | illegal names auto-renamed to `_0`, `_1`, … |

Field names must be valid identifiers, not keywords, not starting with a digit or underscore (unless `rename=True`).

### Access and methods

| Member | Does |
| --- | --- |
| `p.x` / `p[0]` | by name / by index (it's a tuple) |
| `x, y = p` | unpacks like a tuple |
| `p._replace(x=10)` | **returns a new** instance with fields changed |
| `p._asdict()` | a regular `dict` of the fields |
| `p._fields` | tuple of field names |
| `T._make(iterable)` | build an instance from a sequence (e.g. a CSV row) |
| `T._field_defaults` | dict of any defaults |

Instances are immutable, hashable, and compare/sort as plain tuples.

### `namedtuple` vs `dict` vs dataclass

| | `namedtuple` | `dict` | `@dataclass` |
| --- | --- | --- | --- |
| mutable | no | yes | yes (default) |
| access | `.field` and `[i]` | `['key']` | `.field` |
| is a tuple (unpacks, compares) | yes | no | no |
| methods / behaviour | minimal | none | full class |
| best for | small fixed records | dynamic key/value data | records with logic |

See the [classes guide](../../classes-and-objects/index.md) for the dataclass comparison in depth.

## `OrderedDict`

A `dict` subclass. Plain dicts keep insertion order since Python 3.7, so reach for `OrderedDict` only for these extras:

| Member | Does |
| --- | --- |
| `move_to_end(key, last=True)` | move an existing key to the back (or front with `last=False`) |
| `popitem(last=True)` | pop from the back; `last=False` pops from the **front** |
| order-sensitive `==` | two `OrderedDict`s are equal only if order matches too |

Everything else is identical to `dict`. Typical use: LRU caches, order-significant configs.

## `ChainMap`

Groups several mappings into one view, searched first to last.

| Member | Does |
| --- | --- |
| `ChainMap(m1, m2, ...)` | view over the maps; lookup returns the **first** match |
| `cm.maps` | the underlying list of maps (`maps[0]` is searched first) |
| `cm[key] = v` / `del cm[key]` | writes and deletes affect **only `maps[0]`** |
| `cm.new_child(m=None)` | new `ChainMap` with a fresh map prepended (for nested scopes) |
| `cm.parents` | a `ChainMap` of all but the first map |
| `dict(cm)` | flattened merge (first-wins) as a plain dict |

Typical use: layered configuration — `ChainMap(cli_args, env_vars, defaults)` resolves each setting from the highest-priority source that defines it, without copying.
