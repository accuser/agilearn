# How to resolve import errors

# Why is my `import` failing, and what's the quickest way to find out?

`ModuleNotFoundError`, `ImportError`, and circular-import surprises share a single root question: *where is Python looking, and is what I want there?* This recipe is the diagnostic flow.

## The answer

Most import failures fall into one of these patterns:

| Symptom | Most common cause | First thing to check |
|---|---|---|
| `ModuleNotFoundError: No module named 'X'` | The module isn't installed, or the wrong Python is being used | `which python`, `pip show X` |
| `ModuleNotFoundError` for your *own* package | Wrong working directory, or `sys.path` doesn't include it | `python -c "import sys; print(sys.path)"` |
| `ImportError: cannot import name 'Y' from 'X'` | `X` exists but doesn't expose `Y` (typo, version mismatch, or circular import) | `dir(X)` from a Python REPL |
| `ImportError` with a circular reference in the traceback | Two modules import each other at the top level | Move one import inside a function |
| Works in REPL, fails in script (or vice versa) | Different `sys.path` between the two contexts | Compare `sys.path` in both |

The single most common root cause across all of these is the same: **the wrong Python interpreter is being used**.

## Step 1: Confirm which Python you're running

```bash
which python
python -c "import sys; print(sys.executable); print(sys.version)"
```

If the path printed isn't your venv's `python` (`.../.venv/bin/python`), nothing else matters until you fix that. Activate the venv, or invoke `python` by full path.

```bash
which pip
pip show requests   # or whichever package
```

If `pip` and `python` come from different directories, you're installing into one Python and importing from another. Always invoke pip via the active Python: `python -m pip install ...`.

## Step 2: Look at `sys.path`

```bash
python -c "import sys; print('\n'.join(sys.path))"
```

This is the list of directories Python searches for modules. The first entry is usually `''` — meaning *the current directory* — or the directory of the script you ran. The rest are the standard library and site-packages.

For a `ModuleNotFoundError` on a package you've authored: is the package's parent directory in this list? If not, that's the problem. The conventional fix isn't to mutate `sys.path`; it's to install your package (`pip install -e .`).

## Step 3: Distinguish "module doesn't exist" from "module exists but is broken"

A `ModuleNotFoundError` says *Python couldn't find a file*. An `ImportError` says *Python found the file, but something went wrong reading it*. Different problems, different fixes.

For `ImportError: cannot import name 'Y' from 'X'`:

```bash
python -c "import X; print(dir(X))"
```

Look for `Y` in the output. If it isn't there:

- **Typo on your end.** Easy fix.
- **Version mismatch.** `Y` exists in newer or older versions of `X` than the one you have installed. `pip show X` reveals the version; check the package's changelog.
- **Circular import.** See below.

## Step 4: Spot a circular import

A circular import looks like this in the traceback:

```text
ImportError: cannot import name 'Foo' from partially initialized module 'a' (most likely due to a circular import)
```

It happens when `a.py` imports from `b.py` at the top, and `b.py` imports from `a.py` at the top. The first import to run gets stuck partway through — the second module sees an unfinished version of the first.

Three ways out, in order of preference:

1. **Move the offending import inside the function** that uses it. Imports at function scope happen the first time the function runs, by which time both modules are fully loaded.
2. **Refactor the shared piece into a third module** that both can import without depending on each other.
3. **Use a `TYPE_CHECKING` guard** (from the [`typing`](../../type-hints/) module) for imports that exist only for type hints — those are never actually executed at runtime.

## Step 5: When the error happens *during* import

Sometimes the failure isn't your code — it's a top-level statement in someone else's package failing while `pip` has it half-imported. The traceback shows a path inside `site-packages/`. Two usual suspects:

- **Missing dependency.** A package imports something it expected to be installed, but isn't. `pip install` the missing one (or — better — re-install with the package's full dependency set: `pip install -e ".[test]"` if it's an extras issue).
- **Native library missing.** A wheel imports a `.so` or `.dll`; the platform doesn't have it. Common with packages that wrap C libraries; the package's installation docs usually describe the system prerequisite.

## Trade-offs

A couple of things people do when they hit an import error that they shouldn't.

**Don't `sys.path.insert(0, "/some/abs/path")`.** It papers over the problem and bakes a path into your code that won't work on anyone else's machine. The fix is almost always to install the package properly or to fix the working directory.

**Don't catch `ImportError` to silence it** unless you're explicitly providing optional functionality. Wrapping every import in `try/except ImportError: pass` lets the program limp on with missing functionality, often producing a confusing failure much later. If a dependency is genuinely optional, do the dance once at module load and set a sentinel:

```python
try:
    import optional_thing
    HAS_OPTIONAL_THING = True
except ImportError:
    HAS_OPTIONAL_THING = False
```

Then check the sentinel where the optional code-path is needed.

## Related

- [Modules and imports](../learn/01-modules-and-imports.ipynb) — `sys.modules`, `sys.path`, and what `import` actually does.
- [How Python's import system works](../concepts/how-pythons-import-system-works.md) — finders, loaders, and the gory detail.
- [Avoid common packaging mistakes](avoid-common-packaging-mistakes.md) — many of the traps it lists end up as import errors.
