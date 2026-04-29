# How Python's import system works

The `import` statement looks simple — one line — but a lot happens between you typing it and your code being able to use whatever it imported. Knowing the steps Python takes is what turns mysterious `ModuleNotFoundError`s into ten-second diagnoses.

## What `import math` actually does

When the interpreter executes `import math`, it goes through roughly the following steps.

**1. Check the cache.** Python keeps every module it has already imported in a dictionary called `sys.modules`, keyed by name. If `"math"` is in there, the work is done — Python binds the existing module object to the local name and moves on. This is why importing a module ten times costs almost nothing after the first.

**2. Search for it.** If the module isn't cached, Python asks each entry in `sys.meta_path` — a list of *finders* — whether it can locate `math`. The default finders cover three cases, in order:

- *Built-in modules*, baked into the interpreter (`sys`, `_thread`, `gc`, and a handful of others).
- *Frozen modules*, built into the interpreter as bytecode for fast startup (most of the standard library, in modern Python).
- *Path-based modules*, found by walking `sys.path` looking for a matching `.py` file or package directory.

The first finder that says "yes, I can find this" returns a *spec* — metadata describing where the module is and how to load it. If no finder claims the name, Python raises `ModuleNotFoundError`.

**3. Load it.** With a spec in hand, Python invokes the corresponding *loader*. For a `.py` file, that means reading the file, compiling it to bytecode, and executing the bytecode top-to-bottom in a fresh namespace. For a built-in module, the loader is a no-op — the module's namespace is already initialised in C.

The result of execution *is* the module. Every `def` and `class` and assignment at the top level becomes an attribute on the module object.

**4. Cache and bind.** The new module is stored in `sys.modules` under its full name (`math`), and the local name `math` is bound to it. Sub-packages (`os.path`) are stored under their full dotted name, and any intermediate packages are loaded too — so `import os.path` puts both `os` and `os.path` in the cache.

The next `import math` anywhere in the program skips straight to step 4.

## `sys.path` — where Python looks for files

`sys.path` is a list of directory strings. At interpreter startup, it's populated from several sources, roughly in this order:

1. The directory of the script you ran (or `''` — the current directory — for an interactive session).
2. The `PYTHONPATH` environment variable, if set.
3. The standard library's installation directory.
4. Each `site-packages` directory the interpreter knows about.

A virtual environment changes the last one: activating a venv replaces the system `site-packages` with the venv's, so `pip install`s into the venv are visible and the system Python's packages aren't.

When `import requests` fails, the cure is almost always that `requests` isn't in any directory on `sys.path` — usually because you're running the wrong Python, or you forgot to `pip install` it into the active environment. The diagnostic, every time:

```python
import sys
print(sys.executable)
print('\n'.join(sys.path))
```

## The cache is forever (within a process)

`sys.modules` doesn't expire. Once a module is in there, subsequent imports return the same object — even if you've edited the file. This is *deliberate*: it makes module-level state like `_some_cache = {}` actually work, and it stops circular imports from re-running each module repeatedly.

It's also why editing a file and re-running `import` doesn't pick up your changes. The two solutions:

- **Restart the process.** The simplest answer, and what you should reach for first.
- **`importlib.reload(module)`** explicitly. This re-executes the module's code, but doesn't update names already imported elsewhere — `from x import y` bindings keep pointing at the old object. Reload is fiddly enough that most projects avoid it, except in interactive notebooks with their own autoreload extension.

## Packages are imported in pieces

For a package, the import process recurses. `import os.path` walks the dotted name from the left, importing each level:

1. `os` — find `os/__init__.py` (or its built-in equivalent), execute it, cache it.
2. `os.path` — within the now-imported `os`, find `path` as a sub-module, execute its file, cache it as `os.path`.

The package's `__init__.py` runs once, the first time *anything* in the package is imported. Imports between modules in the same package use this same machinery — `from .square import area` is equivalent to `from package.square import area`, with the leading dot resolved relative to the importing module's location.

## Where common errors come from

With the model above, the typical traceback patterns become readable.

**`ModuleNotFoundError: No module named 'X'`** means no finder claimed `X`. The directories in `sys.path` don't contain a matching file, the cache doesn't have it, and there's no built-in or frozen module with that name. Almost always: wrong Python, or missing install.

**`ImportError: cannot import name 'Y' from 'X'`** means the module `X` was found and loaded, but it doesn't have an attribute called `Y`. The loader executed `X.py` to completion; the resulting namespace simply doesn't include `Y`. Causes: typo, version mismatch, or a circular import that left `X` partially initialised.

**Circular imports** happen when `a.py` imports `b.py` at the top, and `b.py` imports `a.py` at the top. The cache helps and hurts at the same time: while `a.py` is still being executed, it's already in `sys.modules` (as a partially-initialised module), so the import of `a` from inside `b` doesn't restart it — it sees a half-finished version. The fix is usually to move the import inside a function, where it runs only when the function is called, by which time both modules have finished loading.

## Why this design

You could imagine a simpler import system — every `import` re-reads and re-executes the file. It would also be unusable: every `import os` would cost the same as the first one, and module-level state would reset constantly.

You could also imagine an entirely lazy system — modules aren't loaded until something inside them is referenced. Python's import system is *almost* that, but not quite: the *first* import of a module loads it eagerly, top-to-bottom, so that any side effects in the module body (registering with a framework, for example) happen at a predictable time. The cache is what makes subsequent uses cheap.

The result is a system that's both fast (subsequent imports are dictionary lookups) and predictable (a module's top-level code runs once, when it's first imported, in a known order). Almost every quirk you'll encounter — `__init__.py`, `if __name__ == "__main__":`, the rules of relative imports — is a downstream consequence of those two design goals.

## Related

- [Modules and imports](../learn/01-modules-and-imports.ipynb) — the practical first encounter.
- [Packages and namespaces](../learn/02-packages-and-namespaces.ipynb) — what changes for directories.
- [Resolve import errors](../recipes/resolve-import-errors.md) — the diagnostic flow that puts this knowledge to work.
- [Import statement forms](../reference/import-statement-forms.md) — every shape `import` can take.
