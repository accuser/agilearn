# How to turn a script folder into a package

# I have a folder of `.py` files I keep `cd`-ing into to run. How do I turn it into a proper installable package?

This is the most common "I should probably package this" moment. The good news is that the migration is almost mechanical — five small steps, and it works.

## The starting point

Suppose you have something like this:

```text
report-tools/
    fetch.py
    transform.py
    plot.py
    cli.py
```

You've been running it as `python cli.py` from inside the folder, and it imports its siblings with `import fetch` and `import transform`. It works, but only from this directory.

## The five steps

### 1. Add a virtual environment

If you don't already have one for the project:

```bash
cd report-tools
python -m venv .venv
source .venv/bin/activate
```

### 2. Reshape the folder

Adopt the standard `src/` layout. Pick an import name (Python identifier, underscores allowed; here, `report_tools`):

```text
report-tools/
    pyproject.toml
    src/
        report_tools/
            __init__.py
            fetch.py
            transform.py
            plot.py
            cli.py
```

You can do this with a few `mv` commands:

```bash
mkdir -p src/report_tools
mv fetch.py transform.py plot.py cli.py src/report_tools/
touch src/report_tools/__init__.py
```

### 3. Fix the imports

Sibling imports change form. `import fetch` was working because `fetch.py` happened to be in the same directory you were running from. Once it's a module *inside* a package, the imports must say so.

```python
# old: cli.py used to say
import fetch
import transform

# new: cli.py now says
from report_tools import fetch, transform
```

Or, if you prefer relative imports inside the package:

```python
from . import fetch, transform
```

Either is fine. Pick one and use it consistently.

### 4. Write a minimal `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "report-tools"
version = "0.1.0"
description = "Internal tools for the weekly report."
requires-python = ">=3.10"
dependencies = [
    "requests",
    "pandas",
    "matplotlib",
]
```

List the third-party packages your code actually imports under `dependencies`. The standard library doesn't go there.

### 5. Editable-install

```bash
pip install -e .
```

Now `import report_tools` works from anywhere — inside the venv, from any directory. No more `cd` dance.

## Verifying

A quick smoke test from the project root:

```bash
python -c "from report_tools import fetch; print(fetch.__file__)"
```

The path printed should point inside `src/report_tools/`, not the editable-install link's location. If you can run that without a `ModuleNotFoundError`, the migration is good.

## Why it works

The `src/` layout's value isn't aesthetic — it's that **your tests can never accidentally import from the source tree directly**. Without `src/`, running `pytest` from the project root finds the package by walking the current directory before the install does its job, so even a broken `pip install` looks fine to your test suite. With `src/`, the only way for `import report_tools` to work is if the package is properly installed; tests fail loudly when something is wrong with the install rather than silently passing on stale code.

The `pyproject.toml` is a contract with `pip`. It declares the build backend, the package name, the dependencies, and (importantly) tells `pip` to look for `report_tools` under `src/`. Hatchling figures out the layout from that — you don't have to tell it.

Editable installs are what make the workflow ergonomic. Without `-e`, you'd have to `pip install .` after every change. With `-e`, your source tree *is* the install — every edit is immediately picked up.

## Trade-offs

A handful of things go differently in package shape, all of them ultimately for the better.

**You can't `python script_name.py` any more.** Inside a package, modules import from `report_tools.x`, which doesn't resolve when you run a single file directly. Use `python -m report_tools.cli` instead, and add a `[project.scripts]` entry point to give yourself a proper command (see [Add a console-script entry point](add-a-console-script-entry-point.md)).

**Tests need to be aware of the new layout.** If you've been testing by importing source files directly, those imports now have to go through the package. The fix is the same one users will see: install the package (editable mode is fine for development), then test.

**Data files take a bit more thought.** Files alongside `.py` files used to be findable with simple relative paths; once installed, the package may be inside a wheel. The cure is `importlib.resources`, which gives you a stable way to read package data files regardless of how the package is installed.

## Related

- [Authoring a package](../learn/05-authoring-a-package.ipynb) — the broader walkthrough this recipe is a focused slice of.
- [Add a console-script entry point](add-a-console-script-entry-point.md) — give your CLI a proper command.
- [Project layout](../reference/project-layout.md) — the canonical layouts side-by-side.
- [Resolve import errors](resolve-import-errors.md) — the most common things that go wrong when the imports are mid-migration.
