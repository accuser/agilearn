# Import statement forms

Every shape `import` and `from … import …` can take, with a one-line description and a worked example.

## Plain imports

### `import x`

Bind the module `x` to the local name `x`.

```python
import math
math.pi
```

### `import x.y`

Import a sub-module. Both `x` and `x.y` are loaded; `x` is bound, and `x.y` is reached through the dot.

```python
import os.path
os.path.join("a", "b")
```

### `import x as alias`

Bind the module `x` to a local name of your choice — useful for conventional shorter names.

```python
import numpy as np
np.array([1, 2, 3])
```

### `import x.y as alias`

Bind a sub-module to a local name without exposing the parent.

```python
import xml.etree.ElementTree as ET
ET.parse(path)
```

## `from` imports

### `from x import y`

Bind the name `y` from `x` into the local namespace. `y` can be a function, class, variable, or sub-module.

```python
from math import pi, sqrt
sqrt(pi)
```

### `from x import y as alias`

Bind `y` to a local name of your choice. Mix and match in a single statement:

```python
from math import pi, sqrt as square_root
```

### `from x import *`

Import every public name from `x`. *Avoid in non-interactive code* — it shadows local variables silently. If a module wants to be wildcard-importable, it sets `__all__`.

```python
from math import *   # don't do this in a real module
```

## Relative imports (inside packages only)

Relative imports use leading dots to mean "current package" and "parent package". They only work inside a package — modules run as scripts can't use them.

### `from . import y`

Import the sibling module `y` from the current package.

```python
# inside shapes/square.py
from . import polygons
```

### `from .y import z`

Import `z` from the sibling module `y`.

```python
# inside shapes/__init__.py
from .square import area
```

### `from .. import y`

Import `y` from the parent package.

```python
# inside shapes/polygons/triangle.py
from .. import square
```

### `from ..y import z`

Import `z` from a module in the parent package.

```python
# inside shapes/polygons/triangle.py
from ..square import area
```

## Conditional imports

Used to optionally import a module that may not be installed, or to defer imports inside a function (often to break a circular import).

```python
try:
    import orjson as _json
except ImportError:
    import json as _json
```

```python
def render():
    # Imported lazily — only when this function is actually called.
    from heavy_module import Thing
    return Thing()
```

## Type-only imports

For names imported only to use as type hints, the `TYPE_CHECKING` constant from `typing` lets you import without the runtime cost (and avoids circular imports caused purely by hints).

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .other import OtherClass

def f(x: "OtherClass") -> None:
    ...
```

The type checker sees `OtherClass`; at runtime the import never happens, so the string `"OtherClass"` (a forward reference) is what matters.

## What `import` actually binds

| Form | Bound name | Module also loaded? |
|---|---|---|
| `import x` | `x` | yes |
| `import x.y` | `x` (with `x.y` reachable through it) | both `x` and `x.y` |
| `import x.y as alias` | `alias` | both `x` and `x.y` |
| `from x import y` | `y` | `x` (and so `y` becomes accessible) |
| `from x import *` | every public name in `x` | `x` |
| `from . import y` | `y` | the current package, then `y` |

## Related

- [Modules and imports](../learn/01-modules-and-imports.ipynb) — the tutorial walkthrough.
- [How Python's import system works](../concepts/how-pythons-import-system-works.md) — what happens behind every import.
- [Resolve import errors](../recipes/resolve-import-errors.md) — when the import you wrote isn't doing what you expected.
