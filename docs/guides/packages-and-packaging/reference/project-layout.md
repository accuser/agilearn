# Project layout

The canonical shapes a Python project takes on disk, and where the supporting files belong.

## The `src/` layout (recommended)

```text
my-package/
    pyproject.toml
    README.md
    LICENSE
    .gitignore
    src/
        my_package/
            __init__.py
            core.py
            cli.py
    tests/
        __init__.py
        test_core.py
        test_cli.py
    docs/
        index.md
```

This is the default for new projects. The package's importable code lives under `src/`, isolated from everything else.

### Why the extra directory?

Because `src/` is **not on `sys.path` by default**, you can't accidentally import the package without going through the installed copy. That sounds pedantic until you see what it prevents:

- **Stale tests.** Without `src/`, `pytest` can find the package at the project root before the install does its job — broken installs go unnoticed because the tests pass against the source tree. With `src/`, the only way `import my_package` works is if the install is set up correctly, so a broken install fails the tests immediately.
- **Path-leakage bugs.** Code that accidentally relies on relative file paths from the package root works in development but breaks once installed. The `src/` layout exposes these in test, not in production.

The cost is one extra directory and a small amount of friction running ad-hoc scripts (`python -m my_package.cli` instead of `python my_package/cli.py`). Nearly always worth it.

## The flat layout

```text
my-package/
    pyproject.toml
    README.md
    my_package/
        __init__.py
        core.py
        cli.py
    tests/
        test_core.py
```

The package directory sits at the project root. This is conventional for many older projects and is still acceptable for small, single-package repositories. It works; it just gives up the safety the `src/` layout provides.

If you do use it, make absolutely sure your tests run against the *installed* package, not the source tree — `pip install -e .` first, then `cd tests && pytest`.

## Where the supporting files go

### Tests

A sibling `tests/` directory at the project root, **not** inside `src/<package>/`. Tests inside the package directory get included in the wheel (users `pip install`ing your package would receive your test files), and they make `import my_package.tests.test_core` accidentally legal.

```text
my-package/
    src/my_package/...
    tests/
        test_core.py
```

A top-level `tests/__init__.py` is optional. Without it, each test file is its own module — fine for `pytest`. With it, the tests form a package — necessary for some tools.

### Documentation

A sibling `docs/` directory:

```text
my-package/
    src/my_package/...
    docs/
        index.md
        api.md
```

If you use Sphinx, MkDocs, or a similar tool, its config typically lives at the repository root (`mkdocs.yml`, `docs/conf.py`).

### Configuration files

Configuration belongs at the project root, not inside `src/`:

```text
my-package/
    .gitignore
    .gitattributes
    .editorconfig
    .pre-commit-config.yaml
    pyproject.toml
    README.md
    LICENSE
    CHANGELOG.md
```

Tool configuration (ruff, black, mypy, pytest) goes into `pyproject.toml` under `[tool.<name>]` whenever the tool supports it. A separate `pytest.ini` or `setup.cfg` is fine when it doesn't.

### Examples

A sibling `examples/` directory if you want runnable example scripts:

```text
my-package/
    src/my_package/...
    examples/
        basic.py
        advanced.py
```

These don't go inside the package — they shouldn't be imported as `my_package.examples`.

### Data files that ship with the package

Files the *installed* package needs at runtime live inside the package directory:

```text
src/my_package/
    __init__.py
    core.py
    data/
        defaults.json
        templates/
            email.html
```

Read them through `importlib.resources`, which works regardless of how the package is installed:

```python
from importlib import resources

defaults = resources.files("my_package.data") / "defaults.json"
text = defaults.read_text(encoding="utf-8")
```

For most build backends, files inside the package directory are included in the wheel automatically. Some backends (and some layouts) need explicit configuration — see the build backend's docs if a data file isn't being shipped.

## Multiple packages in one repository

Same shape, with several directories under `src/`:

```text
acme-toolkit/
    pyproject.toml
    src/
        acme_core/
            __init__.py
        acme_cli/
            __init__.py
    tests/
        test_acme_core.py
        test_acme_cli.py
```

A single `pyproject.toml` can declare multiple importable packages — most build backends auto-detect every directory under `src/` that has an `__init__.py`. Larger projects sometimes prefer one repository per package, or use a monorepo tool; both are valid choices, neither is forced by the layout.

## What goes in `.gitignore`

A reasonable starting point for any Python project:

```text
.venv/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.mypy_cache/
.ruff_cache/
build/
dist/
*.egg-info/
```

Treat your virtual environment, build artefacts, and tool caches as ephemeral. They reproduce from the committed `pyproject.toml`.

## Related

- [Authoring a package](../learn/05-authoring-a-package.ipynb) — the walkthrough that builds an example of this layout.
- [pyproject.toml field reference](pyproject-toml-field-reference.md) — the metadata file at the centre of all this.
- [Avoid common packaging mistakes](../recipes/avoid-common-packaging-mistakes.md) — the layout-related traps and how to avoid them.
