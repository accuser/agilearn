---
title: mypy cheatsheet
---

# `mypy` cheatsheet

`mypy` is the reference Python type-checker. Same role as `pyright` (from Microsoft) — they check the same annotations, differ in speed, defaults, and a few niche corners. This page covers the mypy workflow; pyright is broadly similar.

## Running it

```bash
pip install mypy

# Check a single file
mypy my_script.py

# Check a whole package
mypy src/

# Check the current directory, obeying mypy.ini / pyproject.toml
mypy .
```

First runs are slow; subsequent runs use a cache in `.mypy_cache/` and are much faster.

## Common flags

| Flag | Effect |
| --- | --- |
| `--strict` | Enable all the strict checks — a good default for new projects |
| `--disallow-untyped-defs` | Every function must be fully annotated |
| `--warn-unused-ignores` | Flag `# type: ignore` comments that are no longer needed |
| `--no-implicit-reexport` | `from foo import bar` in `foo/__init__.py` doesn't re-export `bar` unless explicit |
| `--python-version 3.10` | Check against a specific Python version's typing features |
| `--ignore-missing-imports` | Don't error on imports mypy can't find types for |

`--strict` is shorthand for a bundle including all the above. Start strict if you can; it's harder to retrofit.

## Config in `pyproject.toml`

```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_unused_ignores = true

# Per-module overrides for untyped third-party libs
[[tool.mypy.overrides]]
module = ["scipy.*", "matplotlib.*"]
ignore_missing_imports = true
```

Keeping config in `pyproject.toml` (or `mypy.ini`) means everyone on the team runs the same checks.

## Reading the errors

A typical error:

```
src/app.py:12: error: Argument 1 to "greet" has incompatible type "int"; expected "str"
```

The format is `file:line: error: <message>`. Errors usually point at the call site, not the definition — mypy is telling you where to fix the caller.

Warnings (`note:` lines) give extra context — "did you mean X?" or "this is where the conflicting type was declared".

## Silencing a specific error

Add `# type: ignore[error-code]` at the end of the offending line:

```python
result = some_untyped_library.do_thing()  # type: ignore[no-any-return]
```

The error code (like `no-any-return`) narrows the ignore to that specific problem — so if a different error appears on the same line later, you still see it.

**Never** add a bare `# type: ignore` without a code — it silences everything, forever.

## Finding the error codes

Run with `--show-error-codes` (on by default in mypy 0.920+) to see codes on every error. The common ones:

| Code | Meaning |
| --- | --- |
| `arg-type` | Argument has wrong type |
| `return-value` | Return doesn't match annotated type |
| `assignment` | Assigning wrong type to variable |
| `attr-defined` | Attribute doesn't exist on this type |
| `no-any-return` | Function returns `Any` implicitly |
| `no-untyped-def` | Function is missing annotations |
| `import-untyped` | Imported module has no type info |
| `name-defined` | Name isn't defined (also a runtime error usually) |

## Inspecting what mypy inferred

`reveal_type(expr)` inside your code makes mypy print the inferred type when it checks that line. Not a runtime call — remove before deploying.

```python
from typing import reveal_type

x = [1, 2, 3]
reveal_type(x)   # mypy will print: Revealed type is "builtins.list[builtins.int]"
```

Also `reveal_locals()` dumps the local variable types at that point. Useful when debugging why a check is failing.

## Narrowing tricks

Mypy narrows types on:

- `isinstance(x, T)` and `type(x) is T`
- `if x is None`, `if x is not None`
- `if x:` (narrows `Optional[X]` to `X` if X is never falsy by itself — not always true!)
- `assert isinstance(x, T)`, `assert x is not None`
- Walrus operator — `if (y := f()) is not None:`
- Structural match — `match x: case int(): ...`

If mypy isn't narrowing when you think it should, try an `assert` or a cast. Usually it means your code shape is slightly weird — worth understanding rather than silencing.

## Strict mode gradually

If an existing codebase can't pass `--strict` today, enable the checks one at a time:

```toml
[tool.mypy]
python_version = "3.10"
# Start weak, tighten over time:
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = false     # Turn on later
disallow_untyped_calls = false    # Turn on later
```

Fix the errors under each flag, then tighten the next one. It's slower than flipping `strict = true` and fixing everything at once, but realistic for large codebases.

## Third-party types

Many packages ship their own type stubs. If `mypy` complains `import-untyped`, try:

```bash
pip install types-<package>       # community-maintained stubs
```

For example, `types-requests`, `types-PyYAML`, `types-python-dateutil`. See [typeshed](https://github.com/python/typeshed) for the full catalogue.

If no stubs exist and you can't add them, use the `ignore_missing_imports` override — it's the right call for mature libraries you don't control.

## Fast feedback: `mypy --daemon`

`dmypy` runs mypy as a long-lived process, checking files in milliseconds instead of seconds. Huge for editor-driven workflows:

```bash
dmypy run -- src/
# subsequent calls are instant
dmypy run -- src/
```

Most editor integrations use `dmypy` under the hood already.
